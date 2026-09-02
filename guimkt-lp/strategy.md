# Estratégia GUIMKT — Claude Code Export

## Premissas autorizadas

- Público: desenvolvedores que usam Claude Code e precisam retomar trabalho entre sessões.
- Conversão: clone do repositório no GitHub.
- Canal: tráfego orgânico.
- Prova social, cases, concorrentes e métricas: não fornecidos; não declarar na LP.

## ICP operacional

O visitante ideal já conhece Claude Code, lida com arquivos JSONL e percebe a perda de contexto como atrito de trabalho. Busca uma forma local, legível e filtrável de levar uma sessão a outro editor ou agente. As objeções centrais são segurança do conteúdo exportado, esforço de instalação e utilidade real dos arquivos gerados.

## Espectro da proposta de valor

1. Empresa: projeto open source, sem promessa proprietária não verificável.
2. Persona: desenvolvedor que não quer reexplicar decisões a cada sessão.
3. Produto: lê sessões locais e gera índice, conversas em Markdown e handoff.
4. Aquisição: a página entrega em poucos segundos o comando de clone e explica o resultado.

## Wireframe-Tabela resumido

| Seção | Framework Q.U.E.S.T. | Conteúdo | Decisão de design |
|---|---|---|---|
| Hero | Qualify | "Seu contexto não acabou" + CTA GitHub | Glass escuro com terminal visual estático |
| Dor | Understand | Sessão longa não é memória reutilizável | Contraste antes/depois, sem números inventados |
| Solução | Educate | Ler, filtrar, exportar, continuar | Demonstração de arquivos resultantes |
| Diferencial | Stimulate | Local, modo seguro, recortes por projeto/termo/data | Faixa de benefícios verificáveis |
| Conversão | Transition | Clone + comando copiável | CTA único e FAQ de objeções |

## Escolha de framework

Q.U.E.S.T. atende um visitante técnico, orientado a avaliar mecanismo e resultado antes de instalar. AIDA foi descartado por pressupor produto conhecido; PAS exageraria uma dor sem dados de urgência; FAB seria útil, mas menos adequado para educar sobre o fluxo completo.

## Gate LPO

- Motivação: headline conecta a retomada de contexto ao uso de Claude Code.
- Valor: explica artefatos concretos e recortes suportados.
- Incentivo: CTA entrega o clone imediatamente.
- Fricção: sem cadastro, formulário ou promessa de integração inexistente.
- Incerteza: FAQ esclarece processamento local e modo seguro sem alegações além do README.
