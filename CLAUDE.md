# InsideOut Marketplace

Marketplace de plugins do Claude Cowork da InsideOut PR.

Doc humana/mantenedor (skills, install, release): ver [`README.md`](README.md). Este arquivo é a referência do agente trabalhando no repo.

## Estrutura

- `.claude-plugin/marketplace.json` — Manifesto do marketplace (`insideout-marketplace`)
- `agent-smith-index.json` — Mapa de componentes (mode: marketplace)
- `plugins/io-social-media/` — Plugin de análise de briefings e gestão de social media
  - `.claude-plugin/plugin.json` — Manifesto do plugin
  - `core/` — Motor Python compartilhado (read-only/efêmero no Cowork): `_libcommon.py` (primitivos + disciplina UWP-safe, único ponto de verdade), `style_library.py` (contrato único de estilos), `product_library.py` (contrato único de produtos/marcas), `grid_library.py` (contrato único de grids editoriais), `dashboard.py` (orquestra os três num **painel único** — `insideout-painel.html` na raiz da pasta de trabalho, abas Estilos/Produtos/Grid + seletor de marca global; substitui os três HTMLs antigos), `image_gen.py`, `video_gen.py` (wrapper Veo p/ a skill `generate-video`), `style_extract.py`, `get_style.py`/`get_product.py`/`get_grid.py` (shims), `dashboard-template.html`, `styles.seed.json`/`products.seed.json`/`grids.seed.json` (+ `product-seed-photos/`, `rules-seed/`, `calendar-seed/`)
  - `skills/about-insideout/` — Conhecimento sobre a empresa, serviços e modelo de operação
  - `skills/analyze-briefing/SKILL.md` — Skill de análise de briefings (framework + fluxo em 3 passos); **valida o briefing contra o escopo contratado** do cliente (`skills/analyze-briefing/scopes/<marca>.md`, ex.: `clinique.md`) levantando red flag fora de escopo (Passo 3); Passo 4 opcional popula/atualiza marca no catálogo via `product_library.brand_from_briefing` (idempotente por slug, não inventa campos ausentes)
  - `skills/image-generation/` — Geração de imagens com IA (Gemini 3 Pro) para social media; consome estilos da galeria e junta produto do catálogo × estilo (`product_library.compose_generation_brief`, modos recriar/preservar). Roda da pasta de trabalho; `GEMINI_API_KEY` via `.env` na pasta de trabalho (o agente cria e gerencia). userConfig do plugin é alternativa quando o bug do Cowork #39455/#39827 for resolvido
  - `skills/style-gallery/` — Biblioteca de estilos visuais reutilizáveis do cliente ("como a peça parece"; CRUD conversacional + aba Estilos do painel único); dados em `<pasta de trabalho>/style-gallery/styles/*.json`
  - `skills/product-catalog/` — Catálogo de produtos por marca ("o que é o produto e como a marca fala": voz, mensagens-chave, público, **posicionamento**, **brandGuide** (identidade visual: paleta/fontes/princípios), paleta, guardrails, fotos; CRUD + aba Produtos do painel único). `positioning` e `brandGuide` entram no prompt via `compose_generation_brief`; dados em `<pasta de trabalho>/product-catalog/{brands,products}/*.json` + `photos/`
  - `skills/generate-grid/` — Grid editorial mensal por marca ("o que postar e quando": **geração do andaime a partir do briefing** via boundary dict com `analyze-briefing` Passo 5 + loop de julgamento guiado por `rules/<marca>.md` + **mockup por post via Gemini 3 Pro Image** orquestrando `image_gen` em 3 modos (ref+product / product_only / ref_only) com sidecar JSON de auditoria e batch sequencial, ingestão de planilha histórica 2026, edição conversacional de posts, regras/calendário editáveis + aba Grid do painel único); dados em `<pasta de trabalho>/grids/<marca>/<AAAA-MM>.json` + `rules/`, `calendar/`, `mockups/<AAAA-MM>/<dia>.{png,json}`. Fase 3 fechada — ciclo completo briefing→andaime→julgamento→mockup→approval visual. Post tem campo `copy` (legenda, renderizado no rodapé do card); `attach_mockup(marca,mês,dia,imagem)` anexa imagem ad-hoc ao caminho canônico (`dashboard` resolve o mockup pro arquivo real, sem o bug de caminho relativo/`grids/grids`). O gatilho briefing→grid preenche o primeiro-take (não para no andaime vazio). **Vídeo no grid**: campo `video` no post (mp4 em `mockups/<AAAA-MM>/<dia>.mp4`), `video_for_post` (gera+anexa via Veo, frame-âncora = mockup do dia) e `attach_video` (anexa vídeo ad-hoc); o card mostra o vídeo como pôster + ▶. **Clicar em qualquer dia abre o modal de detalhe** (conteúdo completo, sem corte: legenda e lettering integrais, mídia grande, vídeo tocável inline). Inserção confiável = caminho grid-nativo (`mockup_for_post`/`video_for_post` gera-e-anexa) ou `attach_*` obrigatório quando a mídia vem da skill standalone.
  - `skills/generate-copy/SKILL.md` — Copy de post + lettering de imagem ("o que o texto diz"): legenda (Hook→Valor→CTA, por plataforma) e bloco de lettering injetável pela `image-generation`/`generate-grid`, alinhados à voz da marca (`product_library` via `get_product.py`, read-only). **Skill de processo: geração efêmera, sem store/seed/HTML, nenhum dado na pasta de trabalho**; frameworks em `references/copy-frameworks.md`. Legenda de um post do grid vai no campo `copy` via `generate-grid` `set_post(copy=...)`
  - `skills/generate-video/SKILL.md` — Geração de vídeo curto com IA (Veo) para stories/reels ("o vídeo da peça"): prompt enriquecido + **imagem-âncora (image-to-video)** p/ consistência de cena, via `video_gen.py` (mesma `GEMINI_API_KEY`/.env da `image-generation`). **Skill de processo: efêmera, `.mp4` em `outputs/`, sem dados na pasta de trabalho**; vídeo é caro/lento (confirmar antes). Ainda não anexa ao grid (fast-follow)
  - `skills/voz-usuario.md` — Referência compartilhada de tom: o usuário não é técnico; todas as skills a leem e aplicam (falar de marca/post/data, nunca de implementação)

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
