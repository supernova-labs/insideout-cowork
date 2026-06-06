# InsideOut Marketplace

Marketplace de plugins do Claude Cowork da **InsideOut PR**, mantido pela Supernova Labs.

> Doc para mantenedores/guilda. O cliente não-técnico interage pela UI do Cowork — as descrições das skills aparecem lá automaticamente (frontmatter de cada `SKILL.md`). `CLAUDE.md` é a referência para o agente que trabalha neste repo.

## O que é

Um marketplace (`insideout-marketplace`) com um plugin: **`io-social-media`** — análise de briefings e produção de social media/PR. Cada skill é invocável por `/io-social-media:<skill>` ou disparada automaticamente pela descrição.

## Skills

Fonte canônica de cada skill é o próprio `SKILL.md` (e o inventário em `agent-smith-index.json`). Resumo:

| Skill | Comando | O que faz |
|---|---|---|
| [`about-insideout`](plugins/io-social-media/skills/about-insideout/SKILL.md) | `/io-social-media:about-insideout` | Base de conhecimento da agência (empresa, serviços, clientes, tendências). Consumida pelas demais. |
| [`analyze-briefing`](plugins/io-social-media/skills/analyze-briefing/SKILL.md) | `/io-social-media:analyze-briefing` | Analisa um briefing de cliente pelo framework InsideOut (fluxo em 3 passos); **valida o briefing contra o escopo contratado do cliente** (`scopes/<marca>.md`) com red flags; opcionalmente popula/atualiza a marca no catálogo a partir do briefing (ponte `brand_from_briefing`, sem inventar). |
| [`image-generation`](plugins/io-social-media/skills/image-generation/SKILL.md) | `/io-social-media:image-generation` | Gera imagens (Gemini 3 Pro) para social media; enriquece prompt, consome estilos da galeria, extrai estilo de referência, **junta produto do catálogo × estilo** (modos recriar/preservar). |
| [`style-gallery`](plugins/io-social-media/skills/style-gallery/SKILL.md) | `/io-social-media:style-gallery` | Biblioteca de estilos reutilizáveis do cliente ("como a peça parece"): criar/listar/editar/remover + aba Estilos do painel. |
| [`product-catalog`](plugins/io-social-media/skills/product-catalog/SKILL.md) | `/io-social-media:product-catalog` | Catálogo de produtos por marca ("o que é o produto e como a marca fala"): marcas (voz/mensagens/público/**posicionamento**/**brandGuide** de identidade visual/paleta/guardrails), produtos, fotos + aba Produtos do painel. `positioning` e `brandGuide` alimentam a geração. |
| [`generate-grid`](plugins/io-social-media/skills/generate-grid/SKILL.md) | `/io-social-media:generate-grid` | Grid editorial mensal por marca ("o que postar e quando"): **geração do andaime a partir do briefing** (boundary com `analyze-briefing`: andaime mecânico + loop de julgamento guiado por `rules/<marca>.md`) + **mockup por post via Gemini 3 Pro Image** (3 modos: `ref+product` / `product_only` / `ref_only`, sidecar JSON de auditoria; batch sequencial com confirmação de custo), **vídeo por post via Veo** (`video_for_post`/`attach_video`, frame-âncora = mockup do dia; card mostra pôster + ▶ → lightbox), ingestão de planilha histórica (2026), edição conversacional de posts, regras/calendário editáveis + aba Grid do painel. |
| [`generate-copy`](plugins/io-social-media/skills/generate-copy/SKILL.md) | `/io-social-media:generate-copy` | Copy de post e lettering de imagem ("o que o texto diz"): legenda (Hook→Valor→CTA, hooks alternativos, por plataforma) e bloco de lettering injetável, alinhados à voz da marca. Skill de processo (geração efêmera, sem dados na pasta de trabalho). A legenda de um post do grid vai no campo `copy`. |
| [`generate-video`](plugins/io-social-media/skills/generate-video/SKILL.md) | `/io-social-media:generate-video` | Geração de vídeo curto com IA (Veo) para stories/reels: prompt enriquecido + **imagem-âncora** (image-to-video) para consistência de cena. Mesma `GEMINI_API_KEY`/`.env` da `image-generation`; `.mp4` em `outputs/`. Vídeo é caro/lento — confirma antes. |

`core/` é o motor Python compartilhado (read-only): `_libcommon.py` centraliza os primitivos e a disciplina UWP-safe; `style_library.py` é o contrato único de estilos, `product_library.py` o de produtos/marcas e `grid_library.py` o de grids editoriais; `dashboard.py` orquestra os três num **painel único** (`insideout-painel.html` na raiz da pasta de trabalho) renderizado de `dashboard-template.html` (abas Estilos/Produtos/Grid + seletor de marca global); `image_gen.py`, `video_gen.py` (wrapper Veo da skill `generate-video`), `style_extract.py`, `get_style.py`/`get_product.py`/`get_grid.py` (shims), `styles.seed.json`/`products.seed.json`/`grids.seed.json` (+ `product-seed-photos/`, `rules-seed/`, `calendar-seed/`).

## Instalar / atualizar

```bash
claude marketplace add ./            # ou o repo GitHub
claude plugin install io-social-media
```

Atualizar para uma versão nova: atualizar o **marketplace** primeiro, depois o **plugin**. Há um lag de propagação (GitHub/CDN + cache do Cowork, ~5 min) — se o marketplace disser "já atualizado" logo após um release, aguarde e repita.

### Chave de API (skill image-generation)

Precisa de `GEMINI_API_KEY`. O fluxo confiável é via `.env` na **pasta de trabalho** da sessão — o agente cria e gerencia (o usuário nunca toca no diretório do plugin, que é read-only/efêmero no Cowork). `userConfig` do plugin é a alternativa quando o bug do Cowork #39455/#39827 for resolvido. Detalhes no `SKILL.md` da `image-generation`.

## Processo de release

Repo **co-acessado com o cliente** → fechar por branch + PR, nunca push direto na `main`.

1. Branch (`feat/…`, `fix/…`), commit conventional, push, `gh pr create`.
2. Merge do PR (`gh pr merge --squash --delete-branch`), `git checkout main && git pull`.
3. Bump de versão **sincronizado** em `plugins/io-social-media/.claude-plugin/plugin.json` **e** `.claude-plugin/marketplace.json` (têm que concordar — `claude plugin tag` valida) e em `agent-smith-index.json`.
4. Tag de release: do diretório do plugin, `claude plugin tag --push` → cria `io-social-media--v{versão}`. A resolução de versão do Cowork ancora nessa tag; sem ela o update não enxerga a versão nova.

Mudança só de docs não precisa de bump nem tag.

## Adicionar um plugin ou skill

- **Novo plugin**: criar `plugins/<novo>/.claude-plugin/plugin.json`, adicionar a entrada em `.claude-plugin/marketplace.json` (`plugins[]`), atualizar `agent-smith-index.json`.
- **Nova skill / manutenção do skill layer**: usar a skill `agent-smith` (cria/revê/audita skills e mantém o `agent-smith-index.json`).

## Dev / teste local

`core/` é importado via `sys.path` com cwd na pasta de trabalho (nunca `cd` pro plugin). Dados mutáveis (chave, `outputs/`, `style-gallery/`) vivem na pasta de trabalho — ver `CLAUDE.md` e os `SKILL.md`. `pip install -r plugins/io-social-media/core/requirements.txt` para rodar o motor.
