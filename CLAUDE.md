# InsideOut Cowork Plugin

Plugin do Claude Cowork para a InsideOut PR.

## Estrutura

- `.claude-plugin/plugin.json` — Manifesto do plugin
- `skills/insideout-pr/` — Conhecimento sobre a empresa, serviços e modelo de operação
- `skills/analyze-briefing/` — Framework de qualidade + fluxo de análise de briefings
- `agents/` — Sub-agentes por cliente (futuro)

## Uso

Para analisar um briefing, use a skill `analyze-briefing` e forneça o briefing (via Google Drive ou texto direto).
