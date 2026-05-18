---
name: generate-copy
description: 'Cria copy de post e lettering de imagem para social media/PR da InsideOut, alinhado à voz da marca. Use para "escreve a legenda desse post", "cria a copy pra esse feed", "qual o lettering dessa arte", "headline pra essa imagem", "texto pro story", "escreve a copy do [produto] da [marca]", "preciso de hooks pra esse post".'
allowed-tools: Bash, Read, Write
argument-hint: '[copy do post | lettering da imagem | ambos | hooks alternativos]'
disable-model-invocation: false
---

# Generate Copy — copy de post + lettering de imagem InsideOut

Quarto pilar da produção de social media. A `style-gallery` diz **"como a peça
parece"**; o `product-catalog` diz **"o que é o produto e como a marca fala"**;
a `generate-grid` diz **"o que postar e quando"**; aqui mora **"o que o texto
diz"** — a **copy do post** (legenda) e o **lettering** (texto dentro da arte).

Existe um buraco deliberado no resto do plugin: a geração de imagem **não
escreve texto na peça** ("o brief da marca só molda tom, paleta e composição").
Esta skill preenche esse buraco — e gera também a legenda que acompanha o post.

**Geração efêmera por peça.** Esta skill **não** é uma biblioteca: não há
CRUD, seed, HTML nem dados na pasta de trabalho. A voz da marca já persiste no
`product-catalog` (`brand.json`); o texto da peça é por-peça. O output é
**apresentado no chat**; só salve em arquivo se o usuário pedir (`Write` simples
na pasta de trabalho, sem estrutura de biblioteca).

## O que esta skill produz

- **A. Copy do post (legenda)** — Hook (1ª linha, sem emoji) · corpo/valor ·
  CTA específico em linha isolada · hashtags · no sweet-spot da plataforma.
  Sempre ofereça **2–3 hooks alternativos**.
- **B. Lettering (texto na imagem)** — bloco **estruturado** (headline 3–7
  palavras · apoio opcional ≤ 12 palavras · total ≤ 15–20 · nota de hierarquia
  e contraste), formatado pra ser **injetável** pela `image-generation` ou pra
  preencher o campo `lettering` de um post na `generate-grid`.

Peça pode ser uma só, a outra, ou ambas — pergunte se não estiver claro.

## Leia os frameworks antes de escrever (obrigatório)

A pesquisa do que **funciona e não funciona** (estrutura Hook→Valor→CTA, regras
de hook/CTA, limites por plataforma, regras de lettering, anti-padrões, checklist)
vive em [`references/copy-frameworks.md`](./references/copy-frameworks.md).
**Leia esse arquivo antes de gerar qualquer copy/lettering** — é o critério de
qualidade, não decoração. Não escreva de intuição: rode o output contra o
checklist do reference antes de entregar.

## Onde rodar (crítico)

O diretório do plugin (`${CLAUDE_PLUGIN_ROOT}`) é **read-only e efêmero por
sessão** no Cowork. Esta skill não grava nada no plugin nem materializa
biblioteca. Ela só **lê** a voz da marca do catálogo, importando o motor via
`sys.path` com cwd = pasta de trabalho (nunca `cd` para o `core/`).

Puxe o brief da marca (voz/mensagens/público/paleta/guardrails) pelo shim já
existente do `product-catalog`:
```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python "$CORE/get_product.py" --list                 # marcas + produtos
python "$CORE/get_product.py" <id|slug|nome>         # produto + brief da marca
```
Saída traz `-- Brief da marca --` (Voz, Mensagens-chave, Público, Paleta,
Guardrails) — é a **verdade de voz** quando há marca no catálogo.
Dependências (se faltar import): `pip install -r "$CORE/requirements.txt"`.

## Insumos que a skill reúne (não inventa)

1. **Voz da marca** (verdade quando há marca): `get_product.py` → brief da
   marca. `voice`/`guardrails` são **restrição rígida**; `keyMessages` orientam
   o ângulo, mas **só viram texto-na-imagem se o usuário pedir explicitamente**
   (mesma regra do `compose_generation_brief`).
2. **Tom da agência**: skill `about-insideout` — premium, sofisticado, orgânico,
   "histórias e vínculos, não canais", conexão natural sem hype.
3. **Contexto da peça** (pergunte o que faltar, não presuma): objetivo
   (awareness · engajamento · conversão · educativo), **plataforma**
   (Instagram feed/Reels/Stories · LinkedIn · genérico), formato pedido
   (copy · lettering · ambos), e **se o texto vai NA imagem**.
4. Opcional: saída da `analyze-briefing` (objetivo/público/mensagens) como
   insumo de contexto.

**Não inventar (regra dura):** sem marca/voz disponível, **não fabrique**
posicionamento, claim ou tom. Sinalize o gap, ofereça puxar do briefing
(`analyze-briefing` → `brand_from_briefing` via `product-catalog`) ou pergunte.
Nunca trate dedução como fato — mesma disciplina do "não presuma" da
`analyze-briefing`.

## Output A — copy do post (formato de entrega)

Entregue no chat assim (adapte ao sweet-spot da plataforma — ver tabela no
reference):

```
Hooks (escolha 1):
1. <hook A — sem emoji, cabe no corte visível>
2. <hook B>
3. <hook C>

Legenda:
<hook escolhido sugerido>

<corpo: valor/história, frases curtas, quebras pro mobile>

<CTA específico — linha isolada>

<hashtags relevantes, se a marca usa>
```
Reporte a contagem aproximada de caracteres e em que sweet-spot caiu
(ex.: "≈ 320 chars — médio Instagram, hook em 110 chars cabe antes do corte").

## Output B — lettering (formato injetável)

```
LETTERING
- headline: "<3–7 palavras>"
- apoio: "<≤ 12 palavras, opcional>"
- hierarquia: headline primário (maior/mais peso) · apoio secundário
- nota visual: ≤ 2 fontes · contraste mínimo 3:1 (grande)/4.5:1 (corpo) ·
  testar legibilidade no mobile · reservar espaço seguro na composição
- total: <n> palavras (teto 15–20)
```
Esse bloco é o boundary object: ele pode ser passado **direto** como a
instrução explícita de texto no prompt da `image-generation`, ou colado no
campo `lettering` de um post da `generate-grid`.

## Costura com as outras skills

- **`image-generation`** — quando o usuário quer **texto na imagem**, a
  `image-generation` chama esta skill primeiro e injeta o bloco `LETTERING`
  como a instrução explícita de copy do prompt (o `compose_generation_brief`
  continua sem escrever copy; o lettering entra **por cima**, como já previsto).
- **`generate-grid`** — o campo `lettering` de um post (e a copy da legenda)
  vêm daqui. "Escreve o lettering do post do dia 6" → gere o bloco e ofereça
  gravar via `generate-grid` `set_post(..., lettering={...})`.
- **`product-catalog`** — fonte da voz. "A marca não está cadastrada" →
  encaminhe pra lá (ou `analyze-briefing` se houver briefing).
- **`about-insideout`** — tom-base da agência quando não há marca específica.

## Lógica de decisão

- "escreve a legenda / copy desse post", "copy do [produto] da [marca]" →
  puxe o brief (`get_product.py`), confirme plataforma e objetivo, leia o
  reference, entregue **Output A** com 2–3 hooks.
- "qual o lettering / headline dessa arte", "texto pra essa imagem" →
  **Output B** (bloco injetável).
- "copy e arte", "texto completo do post" → ambos (A + B), coerentes entre si
  (a imagem leva o gancho, a legenda expande — não repita).
- "gera a imagem com esse texto / com copy na arte" → é da `image-generation`;
  gere o **Output B** e encaminhe o bloco pra lá.
- "lettering pro post do dia X do grid" → **Output B** + ofereça gravar via
  `generate-grid`.
- "só me dá uns hooks" → 3–5 hooks alternativos seguindo as regras de hook.
- marca não cadastrada / sem voz → **não invente**: sinalize e ofereça o
  caminho briefing/catálogo.

## Regras importantes

- **Leia `references/copy-frameworks.md` antes de gerar** e rode o output
  contra o checklist de lá. Carregar a regra não é aplicá-la.
- Voz da marca (`voice`/`guardrails`) é restrição rígida; `keyMessages` só
  vira texto-na-arte sob pedido explícito.
- **Não inventar** marca/claim/posicionamento — sinalize gaps, não os preencha.
- Sem emoji no hook; CTA específico em linha isolada; nada de ALL-CAPS/buzzword.
- Lettering: headline ≤ 7 palavras, total ≤ 20, ≤ 2 fontes, hierarquia clara.
- Output **efêmero** no chat. Só grave arquivo se o usuário pedir — `Write`
  simples na pasta de trabalho, **sem** criar estrutura de biblioteca.
- `core/` é read-only: esta skill só **lê** dele (via `get_product.py`).
- Respeite o sweet-spot/corte visível da plataforma, não o limite máximo.

## Tratamento de erros

- **`ProductNotFound` / `BrandNotFound`** ao puxar a voz: confira com
  `python "$CORE/get_product.py" --list`; a marca pode não estar cadastrada —
  encaminhe pra `product-catalog`/`analyze-briefing`, **não** invente a voz.
- **`ProductCatalogError` "plugin mal empacotado"**: `products.seed.json`
  ausente/inacessível no `core/` — reinstalar/atualizar o plugin.
- **Import falha**: `pip install -r "$CORE/requirements.txt"`.
- **Sem marca e sem briefing**: gere no tom-base `about-insideout` e **avise
  explicitamente** que a peça está em voz genérica de agência, não da marca.
