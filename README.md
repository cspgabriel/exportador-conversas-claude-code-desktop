# Exportador Conversas Claude Code Desktop

Ferramenta open source para exportar conversas do Claude Code Desktop salvas em:

```text
~/.claude/projects/*/*.jsonl
```

Ela transforma os JSONL em um pacote legivel para continuar conversas em qualquer agente, editor ou fluxo de auditoria:

- `index.md`
- `index.json`
- `CONTINUAR-NO-CODEX.md`
- `conversations/*.md`

O repo tambem inclui `SKILL.md` para quem quiser instalar como skill do Codex, mas o exportador funciona sozinho como script Python.

## Uso Rapido

Clone o repo:

```powershell
git clone https://github.com/cspgabriel/exportador-conversas-claude-code-desktop.git
cd exportador-conversas-claude-code-desktop
```

Rode:

```powershell
python .\scripts\export_claude_code_conversations.py --limit 10
```

Exporta para:

```text
./claude-code-conversation-export/YYYYMMDD-HHMMSS/
```

## Exemplos

Exportar 25 conversas recentes:

```powershell
python .\scripts\export_claude_code_conversations.py --limit 25
```

Filtrar por projeto:

```powershell
python .\scripts\export_claude_code_conversations.py --project agenciar-site --limit 20
```

Buscar termo dentro das conversas:

```powershell
python .\scripts\export_claude_code_conversations.py --query "deploy vercel" --limit 10
```

Exportar desde uma data:

```powershell
python .\scripts\export_claude_code_conversations.py --since 2026-07-01 --limit 50
```

## Opcoes Uteis

Definir pasta de saida:

```powershell
python .\scripts\export_claude_code_conversations.py --output .\exports\ultimas --limit 10
```

Incluir conteudo de tool results:

```powershell
python .\scripts\export_claude_code_conversations.py --include-tool-content --limit 3
```

Desativar redacao automatica:

```powershell
python .\scripts\export_claude_code_conversations.py --no-redact --limit 1
```

## Uso Como Skill Codex

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
