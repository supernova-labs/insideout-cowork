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
| [`analyze-briefing`](plugins/io-social-media/skills/analyze-briefing/SKILL.md) | `/io-social-media:analyze-briefing` | Analisa um briefing de cliente pelo framework InsideOut (fluxo em 3 passos). |
| [`image-generation`](plugins/io-social-media/skills/image-generation/SKILL.md) | `/io-social-media:image-generation` | Gera imagens (Gemini 3 Pro) para social media; enriquece prompt, consome estilos da galeria, extrai estilo de referência. |
| [`style-gallery`](plugins/io-social-media/skills/style-gallery/SKILL.md) | `/io-social-media:style-gallery` | Biblioteca de estilos reutilizáveis do cliente: criar/listar/editar/remover + galeria HTML. |

`core/` é o motor Python compartilhado (read-only): `style_library.py` é o contrato único de estilos; `image_gen.py`, `style_extract.py`, `get_style.py` (shim), `gallery-template.html`, `styles.seed.json`.

## Instalar / atualizar

```bash
claude marketplace add ./            # ou o repo GitHub
claude plugin install io-social-media
```

Atualizar para uma versão nova: atualizar o **marketplace** primeiro, depois o **plugin**. Há um lag de propagação (GitHub/CDN + cache do Cowork, ~5 min) — se o marketplace disser "já atualizado" logo após um release, aguarde e repita.

### Chave de API (skill image-generation)

Precisa de `GEMINI_API_KEY`. Fluxo: `.env` na **pasta de trabalho** da sessão, carregado com `load_dotenv(override=True)` — o agente cria e gerencia (o usuário nunca toca no diretório do plugin, read-only/efêmero no Cowork). O `userConfig` foi **removido na 0.3.1**: o bug do Cowork #39455/#39827 injeta a `GEMINI_API_KEY` **truncada** no ambiente, e sem `override` o `.env` correto era ignorado (chave recusada como "inválida"). Não reintroduzir userConfig nem `load_dotenv()` sem override enquanto o bug existir. Detalhes no `SKILL.md` da `image-generation`.

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
