# InsideOut Marketplace

Marketplace de plugins do Claude Cowork da InsideOut PR.

Doc humana/mantenedor (skills, install, release): ver [`README.md`](README.md). Este arquivo é a referência do agente trabalhando no repo.

## Estrutura

- `.claude-plugin/marketplace.json` — Manifesto do marketplace (`insideout-marketplace`)
- `agent-smith-index.json` — Mapa de componentes (mode: marketplace)
- `plugins/io-social-media/` — Plugin de análise de briefings e gestão de social media
  - `.claude-plugin/plugin.json` — Manifesto do plugin
  - `core/` — Motor Python compartilhado (read-only/efêmero no Cowork): `style_library.py` (lógica única de estilos), `image_gen.py`, `style_extract.py`, `get_style.py` (shim), `gallery-template.html`, `styles.seed.json`
  - `skills/about-insideout/` — Conhecimento sobre a empresa, serviços e modelo de operação
  - `skills/analyze-briefing/SKILL.md` — Skill de análise de briefings (framework + fluxo em 3 passos)
  - `skills/image-generation/` — Geração de imagens com IA (Gemini 3 Pro) para social media; consome estilos da galeria. Roda da pasta de trabalho; `GEMINI_API_KEY` via `.env` na pasta de trabalho (o agente cria e gerencia). userConfig do plugin é alternativa quando o bug do Cowork #39455/#39827 for resolvido
  - `skills/style-gallery/` — Biblioteca de estilos visuais reutilizáveis do cliente (CRUD conversacional + galeria HTML); dados em `<pasta de trabalho>/style-gallery/styles/*.json`

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

## Release (repo co-acessado com cliente)

Nunca push direto na `main` — branch + PR, e quem trabalha aqui mergeia o próprio PR. Bump de versão **sincronizado** em `plugin.json` + `marketplace.json` (+ `agent-smith-index.json`); depois `claude plugin tag --push` do diretório do plugin → tag `io-social-media--v{versão}` (a resolução de versão do Cowork ancora nela). Docs-only não precisa de bump/tag. Detalhe completo no [`README.md`](README.md).
