#!/usr/bin/env python3
"""Export Claude Code Desktop JSONL conversations to Markdown/JSON."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|pwd|authorization|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-./+=]{12,})"),
    re.compile(r"\b(gh[pousr]_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\b(sk-[A-Za-z0-9_\-]{20,})\b"),
    re.compile(r"\b(xox[baprs]-[A-Za-z0-9\-]{20,})\b"),
]


@dataclass
class Turn:
    timestamp: str = ""
    role: str = "event"
    kind: str = ""
    text: str = ""


@dataclass
class Conversation:
    source_file: Path
    project_key: str
    session_id: str = ""
    cwd: str = ""
    first_timestamp: str = ""
    last_timestamp: str = ""
    turns: list[Turn] = field(default_factory=list)
    events: int = 0

    @property
    def title(self) -> str:
        for turn in self.turns:
            if turn.role == "user" and turn.text.strip():
                return one_line(turn.text, 90)
        return self.source_file.stem


def parse_args() -> argparse.Namespace:
    home = Path.home()
    default_input = home / ".claude" / "projects"
    default_output = Path.cwd() / "claude-code-conversation-export" / datetime.now().strftime("%Y%m%d-%H%M%S")
    parser = argparse.ArgumentParser(description="Export Claude Code Desktop JSONL conversations.")
    parser.add_argument("--config", default="", help="Optional JSON config file. CLI args override config values.")
    parser.add_argument("--preset", choices=["safe", "full"], default="", help="safe: redact/omit/trim. full: no redact/include tool content/no trim.")
    parser.add_argument("--all", action="store_true", help="Shortcut for --preset full.")
    parser.add_argument("--input", default=str(default_input), help="Claude projects directory. Default: ~/.claude/projects")
    parser.add_argument("--output", default=str(default_output), help="Output directory.")
    parser.add_argument("--limit", type=int, default=10, help="Max conversations to export after filtering.")
    parser.add_argument("--project", default="", help="Filter by project folder/path substring.")
    parser.add_argument("--query", default="", help="Filter by text contained in exported turns.")
    parser.add_argument("--since", default="", help="Filter files modified on/after YYYY-MM-DD.")
    parser.add_argument("--max-chars-per-message", type=int, default=6000, help="Trim each message to this size. Use 0 for no trim.")
    parser.add_argument("--include-tool-content", action="store_true", help="Include tool_result/tool content instead of summaries.")
    parser.add_argument("--no-redact", action="store_true", help="Disable secret redaction.")
    args = parser.parse_args()
    return apply_config(args, parser)


def apply_config(args: argparse.Namespace, parser: argparse.ArgumentParser) -> argparse.Namespace:
    defaults = parser.parse_args([])
    config: dict[str, Any] = {}
    if args.config:
        config_path = Path(os.path.expandvars(os.path.expanduser(args.config)))
        with config_path.open("r", encoding="utf-8") as handle:
            config = json.load(handle)

    for key, value in config.items():
        attr = key.replace("-", "_")
        if not hasattr(args, attr):
            continue
        if getattr(args, attr) == getattr(defaults, attr):
            setattr(args, attr, value)

    if args.all:
        args.preset = "full"
    if args.preset == "full":
        args.include_tool_content = True
        args.no_redact = True
        args.max_chars_per_message = 0
    elif args.preset == "safe":
        args.include_tool_content = False
        args.no_redact = False
        if args.max_chars_per_message == 0:
            args.max_chars_per_message = 6000
    return args


def redact(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(lambda m: m.group(0).replace(m.group(2) if len(m.groups()) > 1 else m.group(1), "[REDACTED]"), redacted)
    return redacted


def one_line(text: str, limit: int) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 3)].rstrip() + "..."


def safe_slug(value: str, limit: int = 80) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    return (slug or "conversation")[:limit]


def parse_timestamp(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def format_content(content: Any, include_tool_content: bool) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            item_text = format_content(item, include_tool_content)
            if item_text:
                parts.append(item_text)
        return "\n\n".join(parts)
    if isinstance(content, dict):
        ctype = str(content.get("type", ""))
        if ctype == "text":
            return str(content.get("text", ""))
        if ctype == "tool_use":
            name = content.get("name", "tool")
            tool_id = content.get("id", "")
            tool_input = content.get("input", {})
            compact_input = one_line(json.dumps(tool_input, ensure_ascii=False, default=str), 500)
            return f"[tool_use:{name} id={tool_id}] {compact_input}"
        if ctype == "tool_result":
            tool_id = content.get("tool_use_id", "")
            if not include_tool_content:
                raw = content.get("content", "")
                size = len(json.dumps(raw, ensure_ascii=False, default=str))
                return f"[tool_result id={tool_id} omitted; approx_chars={size}]"
            return f"[tool_result id={tool_id}]\n{format_content(content.get('content'), include_tool_content)}"
        if "text" in content:
            return str(content.get("text", ""))
        if "content" in content:
            return format_content(content.get("content"), include_tool_content)
        return one_line(json.dumps(content, ensure_ascii=False, default=str), 1000)
    return str(content)


def event_to_turn(obj: dict[str, Any], include_tool_content: bool) -> Turn | None:
    timestamp = str(obj.get("timestamp", ""))
    kind = str(obj.get("type", "event"))
    message = obj.get("message")

    if isinstance(message, dict):
        role = str(message.get("role") or obj.get("type") or "event")
        text = format_content(message.get("content"), include_tool_content)
        return Turn(timestamp=timestamp, role=role, kind=kind, text=text)

    if kind in {"user", "assistant"}:
        text = format_content(obj.get("content"), include_tool_content)
        return Turn(timestamp=timestamp, role=kind, kind=kind, text=text)

    if kind in {"summary", "system"}:
        text = format_content(obj.get("content") or obj.get("summary"), include_tool_content)
        return Turn(timestamp=timestamp, role=kind, kind=kind, text=text)

    return None


def load_conversation(path: Path, include_tool_content: bool, max_chars: int, should_redact: bool) -> Conversation:
    conv = Conversation(source_file=path, project_key=path.parent.name)
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            conv.events += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            conv.session_id = conv.session_id or str(obj.get("sessionId", ""))
            conv.cwd = conv.cwd or str(obj.get("cwd", ""))
            ts = str(obj.get("timestamp", ""))
            if ts:
                conv.first_timestamp = conv.first_timestamp or ts
                conv.last_timestamp = ts
            turn = event_to_turn(obj, include_tool_content)
            if not turn or not turn.text.strip():
                continue
            text = turn.text
            if should_redact:
                text = redact(text)
            if max_chars > 0 and len(text) > max_chars:
                text = text[:max_chars].rstrip() + "\n[TRUNCATED]"
            turn.text = text
            conv.turns.append(turn)
    return conv


def discover_files(root: Path, since: str) -> list[Path]:
    files = list(root.glob("*/*.jsonl"))
    if since:
        since_dt = datetime.fromisoformat(since).replace(tzinfo=timezone.utc)
        filtered = []
        for path in files:
            modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            if modified >= since_dt:
                filtered.append(path)
        files = filtered
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def matches(conv: Conversation, project: str, query: str) -> bool:
    if project:
        haystack = f"{conv.project_key} {conv.cwd} {conv.source_file}".lower()
        if project.lower() not in haystack:
            return False
    if query:
        text = "\n".join(t.text for t in conv.turns).lower()
        if query.lower() not in text:
            return False
    return True


def write_markdown(conv: Conversation, output_dir: Path, index: int) -> str:
    ts = parse_timestamp(conv.first_timestamp)
    date_prefix = ts.strftime("%Y%m%d-%H%M%S") if ts else f"{index:03d}"
    filename = f"{date_prefix}-{safe_slug(conv.session_id or conv.source_file.stem, 36)}.md"
    path = output_dir / "conversations" / filename
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {conv.title}",
        "",
        f"- Source: `{conv.source_file}`",
        f"- Project: `{conv.project_key}`",
        f"- Session: `{conv.session_id}`",
        f"- CWD: `{conv.cwd}`",
        f"- Time: `{conv.first_timestamp}` -> `{conv.last_timestamp}`",
        f"- Events: `{conv.events}`",
        "",
        "## Transcript",
        "",
    ]
    for turn in conv.turns:
        heading = f"### {turn.role}"
        if turn.timestamp:
            heading += f" - {turn.timestamp}"
        lines.extend([heading, "", turn.text.strip(), ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path.relative_to(output_dir))


def write_indexes(output_dir: Path, records: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.json").write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# Claude Code Desktop Conversation Export", ""]
    for idx, record in enumerate(records, 1):
        lines.extend([
            f"## {idx}. {record['title']}",
            "",
            f"- File: `{record['markdown']}`",
            f"- Project: `{record['project_key']}`",
            f"- Session: `{record['session_id']}`",
            f"- Time: `{record['first_timestamp']}` -> `{record['last_timestamp']}`",
            f"- CWD: `{record['cwd']}`",
            "",
        ])
    (output_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")

    handoff = [
        "# CONTINUAR NO CODEX",
        "",
        "Use este pacote como contexto compacto das conversas exportadas do Claude Code Desktop.",
        "",
        "1. Leia `index.md` para escolher a conversa.",
        "2. Abra o Markdown correspondente em `conversations/`.",
        "3. Continue a partir dos ultimos pedidos, decisoes, comandos e arquivos citados.",
        "4. Se precisar de evidencia bruta, volte ao JSONL original listado no topo da conversa.",
        "",
        "Conversas exportadas:",
        "",
    ]
    for record in records:
        handoff.append(f"- `{record['markdown']}` - {record['title']}")
    (output_dir / "CONTINUAR-NO-CODEX.md").write_text("\n".join(handoff) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = Path(os.path.expandvars(os.path.expanduser(args.input)))
    output_dir = Path(os.path.expandvars(os.path.expanduser(args.output)))
    if not root.exists():
        raise SystemExit(f"Input directory not found: {root}")

    records: list[dict[str, Any]] = []
    for path in discover_files(root, args.since):
        conv = load_conversation(path, args.include_tool_content, args.max_chars_per_message, not args.no_redact)
        if not conv.turns or not matches(conv, args.project, args.query):
            continue
        markdown = write_markdown(conv, output_dir, len(records) + 1)
        records.append({
            "title": conv.title,
            "markdown": markdown,
            "source_file": str(conv.source_file),
            "project_key": conv.project_key,
            "session_id": conv.session_id,
            "cwd": conv.cwd,
            "first_timestamp": conv.first_timestamp,
            "last_timestamp": conv.last_timestamp,
            "events": conv.events,
            "turns": len(conv.turns),
        })
        if len(records) >= args.limit:
            break

    write_indexes(output_dir, records)
    print(f"Exported {len(records)} conversations to {output_dir}")
    if records:
        print(f"Handoff: {output_dir / 'CONTINUAR-NO-CODEX.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
