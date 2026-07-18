---
name: exportador-conversas-claude-code-desktop
description: Export Claude Code Desktop conversation JSONL files from ~/.claude/projects/*/*.jsonl into Markdown and JSON summaries so Codex can recover, inspect, and continue prior Claude Code app conversations. Use when the user asks to export Claude Code Desktop chats, continue conversations from the Claude Code app, inspect .claude/projects JSONL sessions, or create handoff context from Claude Desktop/Ccode history.
---

# Exportador Conversas Claude Code Desktop

## Quick Start

Run the bundled script first:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --limit 10
```

Default behavior:

- Read `~/.claude/projects/*/*.jsonl`.
- Export newest sessions to `./claude-code-conversation-export/YYYYMMDD-HHMMSS/`.
- Create `index.md`, `index.json`, one Markdown file per conversation, and `CONTINUAR-NO-CODEX.md`.
- Redact common token/key/password patterns.
- Summarize tool calls and skip bulky tool output unless explicitly requested.

## Common Commands

Export the latest 25 conversations:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --limit 25
```

Filter by project folder name:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --project agenciar-site --limit 20
```

Search conversations containing a term:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --query "calculadora" --limit 10
```

Export since a date:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --since 2026-07-01 --limit 50
```

Include tool outputs only when the user explicitly needs raw debugging evidence:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --include-tool-content --limit 3
```

## Handoff Workflow

1. Run the exporter with a tight filter first (`--project`, `--query`, `--since`, or small `--limit`).
2. Open `CONTINUAR-NO-CODEX.md` and use it as the compact handoff note.
3. Open the matching file under `conversations/` only if exact turns are needed.
4. Never paste raw secrets from JSONL into chat, commits, logs, or docs.

## Notes

- Claude Code JSONL schemas vary. The script tolerates `message.content` as strings, arrays, nested dicts, tool calls, attachments, and queue/system records.
- File order is based on `LastWriteTime`, then parsed timestamps.
- If output gets too large, rerun with lower `--max-chars-per-message` or a narrower filter.
