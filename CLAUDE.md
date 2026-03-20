# InsideOut Cowork Plugin

Plugin do Claude Cowork para a InsideOut PR.

## Estrutura

- `.claude-plugin/plugin.json` — Manifesto do plugin
- `skills/about-insideout/` — Conhecimento sobre a empresa, serviços e modelo de operação
- `skills/analyze-briefing.md` — Skill de análise de briefings (framework + fluxo em 3 passos)
- `agents/` — Sub-agentes por cliente (futuro)

## Uso

Para analisar um briefing, use o comando `/analyze-briefing` e forneça o briefing (via Google Drive ou texto direto).
