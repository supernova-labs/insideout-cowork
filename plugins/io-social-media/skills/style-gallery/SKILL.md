---
name: style-gallery
description: 'Biblioteca de estilos visuais reutilizáveis da InsideOut — criar, listar, editar, remover estilos e abrir a galeria HTML. Use para "salvar este visual como estilo", "mostra a galeria de estilos", "renomeia/edita/apaga o estilo X", "que estilos eu tenho".'
allowed-tools: Bash, Read, Write
argument-hint: '[listar | abrir galeria | salvar estilo | editar | remover]'
disable-model-invocation: false
---

# Style Gallery — biblioteca de estilos InsideOut

Cria e mantém a biblioteca de estilos visuais reutilizáveis do cliente. Cada estilo é um prompt de imagem nomeado, com categoria, tags e thumbnail. A skill `image-generation` consome esta biblioteca ("gere usando o estilo #N").

> **Tom com o usuário (sempre):** quem opera não é técnico. Leia e aplique `${CLAUDE_PLUGIN_ROOT}/skills/voz-usuario.md` — fale de estilo, visual e referência; **nunca** de implementação (HTML, JSON, caminho, "renderizar", encoding). Resolva erros nos bastidores e relate só o essencial.

## Onde rodar (crítico)

O diretório do plugin (`${CLAUDE_PLUGIN_ROOT}`) é **read-only e efêmero por sessão** no Cowork. A biblioteca **viva** do cliente vive na **pasta de trabalho**, não no plugin. Nunca faça `cd` para o `core/`; importe via `sys.path` com cwd = pasta de trabalho.

Padrão de invocação (use em tudo abaixo):
```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
import style_library as sl
# ... chamada ...
"
```
Dependências (se faltar import): `pip install -r "$CORE/requirements.txt"`.

## Onde fica a biblioteca

`sl.find_library_dir()` resolve nesta ordem:
1. variável de ambiente `STYLE_GALLERY_DIR`, se setada;
2. busca **pra cima** a partir do cwd por uma pasta `style-gallery/` existente (para na raiz do git/filesystem) — assim rodar de uma subpasta não cria biblioteca duplicada;
3. se nada: cria `<pasta de trabalho>/style-gallery/`.

Estrutura: `style-gallery/styles/<slug>.json` (1 arquivo por estilo — fonte da verdade), `thumbnails/`, `.trash/`. Sem biblioteca no workspace, leitura cai no **seed embarcado** (5 exemplos) — funciona com zero config. A visualização HTML é o **painel unificado** (`insideout-painel.html`, gerado na raiz da pasta de trabalho, aba Estilos) — ver "Abrir a galeria".

Se for um repositório git, garanta no `.gitignore` da pasta de trabalho: ignorar `insideout-painel.html` (derivado) e `style-gallery/.trash/`; **versionar** `style-gallery/styles/` e `style-gallery/thumbnails/` (é o ativo de marca do cliente).

## Operações

**Primeiro uso é automático** — não chame `bootstrap` manualmente. Qualquer operação que exibe/cura/muta (`render_gallery`, `open_gallery`, `add_style`, `update_style`, `delete_style`) já faz **lazy-ensure**: na primeira vez materializa os 5 exemplos + thumbnails no workspace (idempotente, nunca sobrescreve estilo existente). O usuário simplesmente pede o que quer; a biblioteca se prepara sozinha.

Ação avançada opcional — **restaurar exemplos** (se o usuário apagou os exemplos e quer de volta): mover/limpar `styles/` e rodar `sl.bootstrap(sl.find_library_dir())`. Não é pré-requisito de nada.

**Listar / ver:**
```python
for s in sl.list_styles(): print(s['id'], s['slug'], '-', s['name'], s['category'], s['tags'])
print(sl.get_style(3))            # por id
print(sl.get_style('product-launch-gradient'))  # por slug
```

**Criar** (valida categoria/tags; slug único; id monotônico; escrita atômica):
```python
sl.add_style("Tom Institucional Azul", "<prompt completo>",
             category="Campanha", tags=["sazonal","key-visual"],
             example_use="posts institucionais",
             thumbnail="caminho/opcional/para/imagem.png")
```

**Editar** (slug e id são estáveis; revalida categoria/tags):
```python
sl.update_style(6, exampleUse="...", category="Editorial", tags=["moodboard"])
```

**Remover** (soft-delete reversível — move pra `.trash/`, **não** apaga a imagem; **não existe** "apagar tudo"):
```python
sl.delete_style(6)
```

A galeria HTML é regenerada automaticamente após todo `add/update/delete`.

## Adicionar a partir de uma imagem de referência

Quando o usuário disser "gostei desse visual, salva como estilo" e fornecer uma imagem:
```python
import style_library as sl
from style_extract import extract_style
prompt = extract_style("caminho/da/referencia.jpg")     # análise de visão do Gemini
sl.add_style("<nome do estilo>", prompt, category="<categoria>",
             tags=[...], thumbnail="caminho/da/referencia.jpg")
```
A própria imagem de referência vira o thumbnail (sem custo de geração extra). Requer `GEMINI_API_KEY` (ver skill `image-generation` para o fluxo de chave via `.env` na pasta de trabalho).

## Abrir a galeria

```python
print(sl.open_gallery())   # regenera o painel unificado e devolve o caminho (abre na aba Estilos)
```
A galeria virou a **aba Estilos** do painel único da InsideOut (`insideout-painel.html`, na raiz da pasta de trabalho, junto das pastas `style-gallery/`/`product-catalog/`/`grids/`). Informe o caminho ao usuário e diga para abrir no navegador — o painel abre direto na aba Estilos (deep-link `#styles`). Os thumbnails carregam via caminho relativo; estilo sem thumbnail mostra placeholder limpo ("sem preview") automaticamente.

## Categorias e tags canônicas

Use **somente** estas (espelham a galeria; `add/update` rejeitam fora disso):

- **Categorias**: Produto, Campanha, Pessoas, Editorial, Evento, Imprensa
- **Tags por categoria** (ex.): Produto → `packshot, flat-lay, still-life, em-cenario, macro-textura, lancamento`; Campanha → `sazonal, data-comemorativa, key-visual, teaser, oferta, feito-a-mao`; Editorial → `moodboard, colagem, color-story, capa-editorial, serie`; Pessoas → `beauty, retrato, lifestyle, close-pele, kol-influencer, diversidade`. Lista completa: `python -c "import sys;sys.path.insert(0,r'$CORE');import style_library as sl;print(sl.CANONICAL_TAGS)"`.

Para peça da InsideOut, alinhe à marca via skill `about-insideout` antes de definir nome/categoria.

## Lógica de decisão

- "salva este visual como estilo" / "guarda esse" → `add_style` (confirme nome e categoria com o usuário antes; se veio de imagem de referência, extraia o prompt com `extract_style` e use a imagem como thumbnail).
- "mostra/abre a galeria", "que estilos eu tenho" → `list_styles` / `open_gallery`.
- "renomeia/edita/muda o estilo X" → `update_style` (nome/exampleUse/prompt/category/tags; slug e id não mudam).
- "apaga/remove o estilo X" → **confirme explicitamente** antes; `delete_style` (é reversível via `.trash/`).
- "gera uma imagem com o estilo X" → **não é aqui**: encaminhe para a skill `image-generation`.

## Regras importantes

- Confirme antes de deletar; nunca delete em lote nem ofereça "limpar tudo".
- Após criar, resuma ao usuário: nome, categoria, tags, id (referência "estilo #id").
- Não exponha `slug`/caminhos de arquivo a menos que o usuário peça — fale em nome e "#id".
- Sempre reporte o caminho do painel (`insideout-painel.html`) ao abrir/atualizar a galeria.
- `core/` é read-only: nunca tente gravar lá; toda escrita vai para a pasta de trabalho via o módulo.
- Não edite `styles/*.json` na mão — use as funções (escrita atômica + regen da galeria).

## Tratamento de erros

- **`InvalidCategory` / `InvalidTag`**: a mensagem traz as opções válidas — escolha uma delas e repita.
- **`StyleNotFound`**: confira com `list_styles()`; os 5 exemplos são materializados no 1º uso (lazy-ensure) e são editáveis como qualquer estilo.
- **`StyleLibraryError` "plugin mal empacotado"**: `styles.seed.json`/`thumbnails` ausentes no `core/` instalado — reinstalar/atualizar o plugin.
- **Import falha**: `pip install -r "$CORE/requirements.txt"`.
- **`extract_style` falha**: confirme `GEMINI_API_KEY` (fluxo `.env` na pasta de trabalho — ver `image-generation`) e que o caminho da imagem existe.
