# InsideOut Marketplace

Marketplace de plugins do Claude Cowork da InsideOut PR.

## Estrutura

- `.claude-plugin/marketplace.json` — Manifesto do marketplace (`insideout-marketplace`)
- `agent-smith-index.json` — Mapa de componentes (mode: marketplace)
- `plugins/io-social-media/` — Plugin de análise de briefings e gestão de social media
  - `.claude-plugin/plugin.json` — Manifesto do plugin
  - `skills/about-insideout/` — Conhecimento sobre a empresa, serviços e modelo de operação
  - `skills/analyze-briefing/SKILL.md` — Skill de análise de briefings (framework + fluxo em 3 passos)
  - `skills/image-generation/` — Geração de imagens com IA (Gemini 3 Pro) para social media; toolkit Python embarcado. Requer `GEMINI_API_KEY` via userConfig do plugin

## Uso

Registrar o marketplace e instalar o plugin:

```bash
claude marketplace add ./
claude plugin install io-social-media
```

Para analisar um briefing, use `/io-social-media:analyze-briefing` e forneça o briefing (via Google Drive ou texto direto).

## Adicionar um novo plugin

1. Criar `plugins/<novo-plugin>/.claude-plugin/plugin.json`
2. Adicionar a entrada em `.claude-plugin/marketplace.json` (`plugins[]`)
3. Atualizar `agent-smith-index.json`
