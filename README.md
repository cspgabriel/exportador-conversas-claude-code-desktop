# Exportador Conversas Claude Code Desktop

Skill para Codex exportar conversas do Claude Code Desktop salvas em:

```text
~/.claude/projects/*/*.jsonl
```

Ela transforma os JSONL em um pacote legivel para continuar conversas no Codex:

- `index.md`
- `index.json`
- `CONTINUAR-NO-CODEX.md`
- `conversations/*.md`

## Uso Rapido

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --limit 10
```

Exporta para:

```text
./claude-code-conversation-export/YYYYMMDD-HHMMSS/
```

## Exemplos

Exportar 25 conversas recentes:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --limit 25
```

Filtrar por projeto:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --project agenciar-site --limit 20
```

Buscar termo dentro das conversas:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --query "deploy vercel" --limit 10
```

Exportar desde uma data:

```powershell
python "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop\scripts\export_claude_code_conversations.py" --since 2026-07-01 --limit 50
```

## Instalacao

Clone direto na pasta de skills do Codex:

```powershell
git clone https://github.com/cspgabriel/exportador-conversas-claude-code-desktop.git "$env:USERPROFILE\.codex\skills\exportador-conversas-claude-code-desktop"
```

Depois peça ao Codex:

```text
Use a skill exportador-conversas-claude-code-desktop para exportar as conversas recentes do Claude Code Desktop.
```

## Seguranca

Por padrao, o exportador:

- redige padroes comuns de tokens, senhas, API keys e Authorization headers;
- omite conteudo volumoso de `tool_result`;
- preserva caminho do JSONL original para auditoria local.

Use `--include-tool-content` somente quando precisar depurar uma conversa especifica.

## Licenca

MIT.
