---
name: image-generation
description: 'Geração de imagens com IA (Gemini 3 Pro) para social media e PR da InsideOut. Use para gerar, criar ou modificar imagens de posts, stories, reels e capas; extrair estilo de imagem de referência; ou usar estilos numerados (ex.: "estilo #42").'
allowed-tools: Bash, Read, Write
argument-hint: '[descrição da imagem, formato social ou "estilo #N"]'
disable-model-invocation: false
---

# Image Generation — InsideOut Social

Gera imagens de alta qualidade com Gemini 3 Pro para peças de social media e PR, com enriquecimento de prompt e alinhamento à marca do cliente.

## Princípio central: sempre enriqueça o prompt

**OBRIGATÓRIO**: enriqueça todo prompt do usuário antes de gerar. Adicione detalhes de:
- **Iluminação**: direção (frontal/lateral/contraluz), qualidade (suave/dura/difusa), temperatura de cor, sombras
- **Mood**: atmosfera emocional, tom, energia — alinhado ao posicionamento da marca
- **Texturas e materiais**: qualidades de superfície, propriedades específicas
- **Atmosfera**: condições do ambiente, ar, ambiance
- **Composição**: ângulo de câmera, enquadramento, regra dos terços, ponto focal, profundidade — **com espaço seguro para texto/logo quando a peça for receber copy**

**Sempre mostre o prompt enriquecido ao usuário antes de gerar.**

## Alinhamento de marca (InsideOut)

Antes de gerar uma peça para um cliente específico, use a skill `about-insideout` como base de conhecimento da agência e, se houver briefing ativo, puxe o contexto da marca (essência, tom, paleta, mensagens-chave). A InsideOut trabalha "de dentro para fora" — a imagem precisa ressoar com a essência da marca, não ser genérica.

Se o usuário não informou marca/campanha, pergunte rapidamente antes de enriquecer o prompt (ou siga genérico se ele pedir explicitamente).

## Presets de formato social

Mapeie o destino da peça para o `aspect_ratio` suportado pelo motor (`1:1`, `3:4`, `4:3`, `16:9`, `9:16`):

| Destino | aspect_ratio | Observação |
|---|---|---|
| Feed quadrado (Instagram/LinkedIn) | `1:1` | Padrão seguro |
| Feed retrato (Instagram 4:5) | `3:4` | 4:5 não é nativo — gere `3:4` e recorte, ou use `1:1` |
| Stories / Reels / TikTok | `9:16` | Tela cheia vertical |
| Capa horizontal (YouTube, link LinkedIn) | `16:9` | — |
| Carrossel | `1:1` ou `3:4` | Mantenha o mesmo ratio em todos os cards |

Resolução: `1K` (~US$0,10), `2K` (~US$0,20), `4K` (~US$0,40). Default `1K`; suba para `2K` em peça final/hero.

## Onde rodar (crítico)

O diretório do plugin (`${CLAUDE_PLUGIN_ROOT}`) é **read-only e efêmero por sessão** no Cowork — não dá pra editar nem persistir nada lá. Portanto:

- **Nunca** faça `cd` para o `core/` nem grave nada dentro dele.
- Rode tudo a partir da **pasta de trabalho da sessão** (o diretório que o usuário tem aberto no Cowork). É lá que ficam — e devem ficar — a chave (`.env`), as imagens (`outputs/`), a sessão (`.image_session.json`) e a biblioteca de estilos (`style-gallery/`): visíveis e persistentes pro usuário.
- Aponte o Python para o motor via `sys.path`, sem mudar o cwd. Caminho (só leitura): `${CLAUDE_PLUGIN_ROOT}/core`

Padrão de invocação (use em todos os comandos abaixo):
```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
from dotenv import load_dotenv; load_dotenv()   # carrega .env do cwd = pasta de trabalho
from image_gen import generate
print(generate('...'))
"
```
Dependências (se faltar import): `pip install -r "$CORE/requirements.txt"`.

### Chave de API — fluxo gerenciado por você (agente)

O usuário **não** deve navegar até o diretório do plugin. Você cuida disso antes da primeira geração:

1. Se `GEMINI_API_KEY` não estiver no ambiente **e** não houver `.env` com a chave preenchida na pasta de trabalho:
   - Crie `.env` **na pasta de trabalho** (cwd) com o conteúdo `GEMINI_API_KEY=` (use o `${CLAUDE_PLUGIN_ROOT}/core/.env.example` como modelo de texto).
   - Garanta que `.env`, `outputs/` e `.image_session.json` estejam no `.gitignore` da pasta de trabalho **se for um repositório git** — a chave não pode vazar.
   - Peça ao usuário para abrir esse `.env` (que está na pasta dele, não no AppData), colar a chave do Gemini depois do `=`, salvar e mandar continuar. Chave em https://aistudio.google.com/apikey
2. Com a chave no `.env` da pasta de trabalho, `load_dotenv()` a carrega automaticamente (cwd = pasta de trabalho).

`userConfig` do plugin (Cowork pede a chave na instalação) seria o ideal, mas há um bug conhecido na UI do Cowork (issues **#39455** e **#39827**) que impede a injeção — por isso o fluxo via `.env` na pasta de trabalho é o caminho atual. O script tenta `os.environ` primeiro, então quando o bug for corrigido o userConfig também funciona sem `.env`.

## Scripts disponíveis

### 1. image_gen.py — motor de geração

`generate(prompt, reference_images=None, aspect_ratio="1:1", resolution="1K", model="gemini-3-pro-image-preview")` → retorna o caminho da imagem (`outputs/output_XXX_HHMMSS.png`).
`new_session()` zera o histórico · `session_info()` mostra a sessão · `revert(turns=1)` desfaz N iterações.

Cada `generate()` continua a conversa anterior automaticamente (sessão em `.image_session.json`). Só chame `new_session()` ao começar uma peça nova e não relacionada.

```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
from dotenv import load_dotenv; load_dotenv()
from image_gen import generate
result = generate('prompt enriquecido aqui...', aspect_ratio='9:16', resolution='1K')
print(f'Gerada: {result}')
"
```
(Rodado da pasta de trabalho — `outputs/` e `.image_session.json` caem lá.)

### 2. style_extract.py — análise de estilo

Use quando o usuário fornecer uma **imagem custom** de referência ("use esta imagem", "aplique o visual desta foto"). **Obrigatório extrair antes de gerar** — a análise de visão do Gemini é muito superior a descrição manual.

```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
from dotenv import load_dotenv; load_dotenv()
from style_extract import extract_style
print(extract_style('caminho/para/referencia.jpg'))
"
```
Para um elemento específico (ex.: só a paleta, só a tipografia da peça de referência), passe `custom_prompt='...'` focado nesse elemento.

### 3. get_style.py — consumir um estilo da biblioteca

Use quando o usuário citar "estilo #3" / "usa o estilo product-launch-gradient". **Não** extraia — já está pronto.
```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python "$CORE/get_style.py" 3        # por id; aceita também o slug
python "$CORE/get_style.py" --list  # ver os disponíveis
```
Retorna `id`, `name`, `prompt` (substitua `[subject]` pelo assunto), `category`, `exampleUse`.

Os estilos vêm da **biblioteca do cliente** em `<pasta de trabalho>/style-gallery/styles/*.json`; sem biblioteca no workspace, cai automaticamente no **seed embarcado** (5 exemplos social/PR) — "estilo #N" funciona com zero config. Criar, editar, remover estilos e abrir a galeria visual é trabalho da skill **`style-gallery`** — encaminhe para lá quando o usuário quiser gerenciar.

### 4. get_product.py + compose_generation_brief — junção produto × estilo

Quando o usuário pedir uma peça de um **produto de marca** do catálogo ("gera um post do [produto] da [marca] no estilo #N"), junte as **duas fontes**: o estilo diz *como a peça parece*; o produto+marca diz *o que é o produto e como a marca fala*. O motor `image_gen.generate` **já aceita `reference_images`** — as fotos reais do produto entram como âncora; não há mudança de motor.

Fluxo:
```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python "$CORE/get_product.py" --list                 # marcas + produtos
python "$CORE/get_product.py" <id|slug|nome>         # produto + brief + fotos abs
python "$CORE/get_product.py" --brand <marca>        # produtos de uma marca
```
Depois componha o briefing (estilo + produto + brief da marca + modo) e gere:
```bash
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
from dotenv import load_dotenv; load_dotenv()
import style_library as sl, product_library as pc
from image_gen import generate
style = sl.get_style(3)
prod  = pc.get_product_resolved('serum-exemplo')      # já traz brief + fotos abs
brief = pc.compose_generation_brief(style, prod, mode='recriar')  # ou 'preservar'
# enriqueça brief['prompt'] (iluminação/mood/atmosfera/composição) e MOSTRE ao usuário
print(generate(brief['prompt'], reference_images=brief['reference_images'],
               aspect_ratio='3:4', resolution='1K'))
"
```

**Modos** (o usuário escolhe; default `recriar`):
- **`recriar`** — todas as fotos do produto entram como referência; o modelo recria o produto fielmente dentro do cenário/estilo. Mais liberdade de pose/ângulo; fidelidade de rótulo aproximada.
- **`preservar`** — só a foto principal entra; o produto é **intocável**, o estilo compõe apenas o cenário ao redor. Fidelidade máxima do produto; menos liberdade.

O `compose_generation_brief` **não escreve copy/headline na imagem** — o brief da marca só molda tom, paleta e composição. Só inclua texto na peça se o usuário pedir explicitamente. Quando ele pedir, **não escreva o lettering de improviso**: chame a skill **`generate-copy`** (Output B — bloco `LETTERING` estruturado, alinhado à voz da marca e às regras de tipografia/contraste) e injete esse bloco como a instrução explícita de copy do prompt, **fora** do compose. O enriquecimento obrigatório (iluminação/mood/atmosfera/composição) continua valendo **por cima** do `brief['prompt']`, e mostre o prompt final antes de gerar. Gerenciar marcas/produtos/fotos é da skill **`product-catalog`** — encaminhe para lá.

### Salvar como estilo (só sob pedido)

**Apenas quando o usuário pedir explicitamente** ("salva esse visual como estilo", "guarda isso na galeria") — nunca ofereça proativamente. Confirme nome e categoria, então grave via o módulo compartilhado (`add_style` já prepara a biblioteca sozinho — lazy-ensure; não rode bootstrap manual):
```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
import style_library as sl
sl.add_style('<nome>', '<prompt enriquecido que você acabou de usar>',
             category='<categoria canônica>', tags=[...],
             example_use='<quando usar>', thumbnail='<caminho do output gerado>')
"
```
A imagem recém-gerada vira o thumbnail. Categorias/tags canônicas e demais operações: ver skill `style-gallery`.

## Lógica de decisão

- **"Gere [algo] para [formato]"** → escolha o preset de aspect_ratio, alinhe à marca (about-insideout), enriqueça, mostre o prompt, gere com `image_gen.py` (continua a sessão).
- **"Use o estilo #42"** (id ou slug) → `get_style.py 42`, troque `[subject]`, enriqueça, mostre, gere.
- **"Gera [produto] da [marca] no estilo #N"** (produto do catálogo) → `get_product.py`/`get_product_resolved` + `get_style` + `compose_generation_brief(style, prod, mode=...)`; **pergunte o modo** (recriar vs preservar) se o usuário não disser; enriqueça por cima, mostre, gere com `reference_images=brief['reference_images']`. Ver seção "4. ... junção produto × estilo".
- **"Gera com esse texto / com copy/headline na arte"** (texto na imagem) → chame a skill **`generate-copy`** (Output B — bloco `LETTERING`), injete o bloco como instrução explícita de copy **por cima** do prompt (fora do compose), mostre o prompt final, gere. Escrever a legenda do post também é da `generate-copy`.
- **"Salva esse visual como estilo"** (só se pedido explícito) → ver seção "Salvar como estilo (só sob pedido)". Gerenciar a galeria (listar/editar/remover/abrir) → skill `style-gallery`.
- **"Use esta_imagem.jpg de referência"** → **extraia primeiro** com `style_extract.py`, incorpore a descrição ao prompt, gere com `reference_images=['esta_imagem.jpg']`.
- **"Deixe mais escuro / mais quente / adicione X"** → **não** chame `new_session()`; enriqueça o ajuste e gere (a sessão continua a partir da última imagem).
- **"Recomeçar / nova peça"** → `new_session()` e siga.

## Regras importantes

- **O `core/` é read-only** (`image_gen.py`, `style_extract.py`, `get_style.py`/`get_product.py`, `style_library.py`/`product_library.py`, `_libcommon.py`, `gallery-template.html`/`product-catalog-template.html`): não tente editar nem gravar nada lá. Lógica custom e dados rodam/vivem na pasta de trabalho importando o motor via `sys.path`.
- **`.env`, `outputs/`, `.image_session.json` e `style-gallery/` vivem na pasta de trabalho.** Se ela for um repositório git, garanta no `.gitignore`: ignorar `.env`, `outputs/`, `.image_session.json`, `style-gallery/style-gallery.html`, `style-gallery/.trash/`; versionar `style-gallery/styles/` e `style-gallery/thumbnails/`.
- Sempre retorne ao usuário o caminho da imagem gerada.
- Dependências: `pip install -r "$CORE/requirements.txt"` (google-genai, python-dotenv, pillow) caso a geração falhe por import.

## Tratamento de erros

**Geração falha**: verifique `GEMINI_API_KEY` (env ou `.env` na pasta de trabalho); confirme que está rodando da pasta de trabalho com o `core/` no `sys.path` (não fez `cd` pro plugin); tente `new_session()` (sessão corrompida); cheque os paths das imagens de referência; instale deps via `pip install -r "$CORE/requirements.txt"`.
**Extração falha**: confirme que o caminho da imagem existe e é legível; valide a chave.
**get_style falha**: confirme número/slug com `python "$CORE/get_style.py" --list`; a biblioteca resolve da pasta de trabalho (`style-gallery/`) ou cai no seed embarcado.

## Checklist por geração

- [ ] Marca/contexto alinhado (about-insideout / briefing) ou genérico assumido a pedido
- [ ] Preset de formato → aspect_ratio correto
- [ ] Prompt enriquecido (iluminação, mood, textura, atmosfera, composição, espaço para copy)
- [ ] Prompt mostrado ao usuário antes de gerar
- [ ] Estilo #N: recuperado com `get_style.py` · Imagem custom: extraída com `style_extract.py` · Produto do catálogo: `get_product` + `compose_generation_brief` (modo recriar/preservar confirmado)
- [ ] Sessão: continuar vs. nova decidido
- [ ] Caminho da imagem devolvido ao usuário

**Lembre**: o que separa resultado excepcional de genérico é o enriquecimento detalhado do prompt + alinhamento à marca. Nunca passe o prompt cru do usuário direto para a API.
