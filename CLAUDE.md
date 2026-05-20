# InsideOut Marketplace

Marketplace de plugins do Claude Cowork da InsideOut PR.

Doc humana/mantenedor (skills, install, release): ver [`README.md`](README.md). Este arquivo é a referência do agente trabalhando no repo.

## Estrutura

- `.claude-plugin/marketplace.json` — Manifesto do marketplace (`insideout-marketplace`)
- `agent-smith-index.json` — Mapa de componentes (mode: marketplace)
- `plugins/io-social-media/` — Plugin de análise de briefings e gestão de social media
  - `.claude-plugin/plugin.json` — Manifesto do plugin
  - `core/` — Motor Python compartilhado (read-only/efêmero no Cowork): `_libcommon.py` (primitivos + disciplina UWP-safe, único ponto de verdade), `style_library.py` (contrato único de estilos), `product_library.py` (contrato único de produtos/marcas), `grid_library.py` (contrato único de grids editoriais), `image_gen.py`, `style_extract.py`, `get_style.py`/`get_product.py`/`get_grid.py` (shims), `gallery-template.html`/`product-catalog-template.html`/`grid-template.html`, `styles.seed.json`/`products.seed.json`/`grids.seed.json` (+ `product-seed-photos/`, `rules-seed/`, `calendar-seed/`)
  - `skills/about-insideout/` — Conhecimento sobre a empresa, serviços e modelo de operação
  - `skills/analyze-briefing/SKILL.md` — Skill de análise de briefings (framework + fluxo em 3 passos); Passo 4 opcional popula/atualiza marca no catálogo via `product_library.brand_from_briefing` (idempotente por slug, não inventa campos ausentes)
  - `skills/image-generation/` — Geração de imagens com IA (Gemini 3 Pro) para social media; consome estilos da galeria e junta produto do catálogo × estilo (`product_library.compose_generation_brief`, modos recriar/preservar). Roda da pasta de trabalho; `GEMINI_API_KEY` via `.env` na pasta de trabalho (o agente cria e gerencia). userConfig do plugin é alternativa quando o bug do Cowork #39455/#39827 for resolvido
  - `skills/style-gallery/` — Biblioteca de estilos visuais reutilizáveis do cliente ("como a peça parece"; CRUD conversacional + galeria HTML); dados em `<pasta de trabalho>/style-gallery/styles/*.json`
  - `skills/product-catalog/` — Catálogo de produtos por marca ("o que é o produto e como a marca fala": voz, mensagens-chave, público, fotos; CRUD + catálogo HTML); dados em `<pasta de trabalho>/product-catalog/{brands,products}/*.json` + `photos/`
  - `skills/generate-grid/` — Grid editorial mensal por marca ("o que postar e quando": **geração do andaime a partir do briefing** via boundary dict com `analyze-briefing` Passo 5, loop de julgamento guiado por `rules/<marca>.md`, ingestão de planilha histórica 2026, edição conversacional de posts, regras/calendário editáveis + grid HTML); dados em `<pasta de trabalho>/grids/<marca>/<AAAA-MM>.json` + `rules/`, `calendar/`. Fase 2 entregue; mockup por post fica pra Fase 3
  - `skills/generate-copy/SKILL.md` — Copy de post + lettering de imagem ("o que o texto diz"): legenda (Hook→Valor→CTA, por plataforma) e bloco de lettering injetável pela `image-generation`/`generate-grid`, alinhados à voz da marca (`product_library` via `get_product.py`, read-only). **Skill de processo: geração efêmera, sem store/seed/HTML, nenhum dado na pasta de trabalho**; frameworks em `references/copy-frameworks.md`

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
