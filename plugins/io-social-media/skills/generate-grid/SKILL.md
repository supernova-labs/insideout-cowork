---
name: generate-grid
description: 'Grid editorial mensal por marca da InsideOut — criar grid do mês, ingerir planilha histórica (2026), mover/trocar/editar posts e abrir o grid HTML. Use para "cria o grid de maio da Clinique", "ingere essa planilha", "move o post do dia 6 pro dia 8", "troca os posts do dia 3 e 5", "abre o grid", "edita o post do dia 10".'
allowed-tools: Bash, Read, Write
argument-hint: '[criar grid | ingerir planilha | mover/trocar post | editar post | abrir grid]'
disable-model-invocation: false
---

# Generate Grid — grid editorial mensal por marca InsideOut

Terceiro pilar da geração de social media. A `style-gallery` diz **"como a
peça parece"**; o `product-catalog` diz **"o que é o produto e como a marca
fala"**; aqui mora **"o que postar e quando"**: um grid = 1 marca × 1 mês,
colapsando num único artefato canônico as duas planilhas Excel que a Estela
(social media Clinique/EL/TF) mantém hoje à mão.

> **Escopo desta versão (Fase 1):** esqueleto canônico + ingestão do histórico
> **2026** + edição conversacional de posts + grid HTML navegável. **Ainda
> não** gera grid a partir do briefing (Fase 2) nem mockup por post (Fase 3).
> As **regras da Estela** (`rules/<marca>.md`) e o **calendário comemorativo**
> (`calendar/<ano>.md`) já são materializados aqui pra Estela/Carol curarem
> cedo — são consumidos na geração da Fase 2.

## Onde rodar (crítico)

O diretório do plugin (`${CLAUDE_PLUGIN_ROOT}`) é **read-only e efêmero por
sessão** no Cowork. O grid **vivo** do cliente vive na **pasta de trabalho**,
não no plugin. Nunca faça `cd` para o `core/`; importe via `sys.path` com
cwd = pasta de trabalho.

Padrão de invocação (use em tudo abaixo):
```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
import grid_library as gl
# ... chamada ...
"
```
Dependências (se faltar import): `pip install -r "$CORE/requirements.txt"`
(a ingestão de planilha precisa de `openpyxl`).

## Onde fica o grid

`gl.find_library_dir()` resolve nesta ordem:
1. variável de ambiente `GRIDS_DIR`, se setada;
2. busca **pra cima** a partir do cwd por uma pasta `grids/` existente
   (para na raiz do git/filesystem) — rodar de uma subpasta não duplica;
3. se nada: cria `<pasta de trabalho>/grids/`.

Estrutura: `grids/<marca>/<AAAA-MM>.json` (1 arquivo por grid marca-mês),
`grids/rules/<marca>.md` (regras editáveis da marca), `grids/calendar/<ano>.md`
(calendário comemorativo compartilhado), `grids/mockups/` (Fase 3),
`grids/grids.html` (gerado), `grids/.trash/`. Sem grid no workspace, leitura
cai no **seed embarcado** (1 grid Clinique exemplo) — funciona com zero config.

Se for um repositório git, garanta no `.gitignore` da pasta de trabalho:
ignorar `grids/grids.html` e `grids/.trash/`; **versionar**
`grids/<marca>/*.json`, `grids/rules/*.md`, `grids/calendar/*.md` e
`grids/mockups/` (é o ativo editorial do cliente).

## Operações

**Primeiro uso é automático** — não chame `bootstrap` manualmente. Qualquer
operação que exibe/cria/muta já faz **lazy-ensure**: materializa o seed
(grid exemplo + `rules/<marca>.md` + `calendar/<ano>.md`) no workspace,
idempotente, nunca sobrescrevendo o que existe.

**Listar / ver:**
```python
for g in gl.list_grids():            print(g['brand'], g['month'], g['posts'])
for g in gl.list_grids('clinique'):  print(g['month'])
print(gl.get_grid('clinique', '2026-05'))     # grid completo
```

**Criar grid vazio do mês** (esqueleto semanal domingo→sábado, só os dias do
mês; preenche depois conversando):
```python
gl.new_grid("clinique", "2026-05",
            focus_products=["almost-lipstick-black-honey"])
# ou: gl.new_grid("clinique", "maio", year=2026)
```

**Ingerir planilha histórica (só 2026 — Fase 1):**
```python
gl.xlsx_sheets("/caminho/PLANILHA.xlsx")          # lista as abas
gl.ingest_xlsx("/caminho/ESTRATEGIA.xlsx",
               sheet="CL_MAIO", brand="clinique", month="05", year=2026)
gl.ingest_xlsx("/caminho/BRIEFING DESIGN.xlsx",
               sheet="CLINIQUE - MAIO 2026", brand="clinique", month="05")
```
`sheet`, `brand` e `month` são **explícitos**, mas **não confiados**: a aba
tem que **provar** ser {mês}/2026 ou é recusada (nunca regravada com ano/mês
errado). A prova é determinística: ano no nome da aba quando existe (Briefing
Design) + âncora de calendário (coluna do dia-1 e nº de dias do mês). Nome e
célula-título da aba **mentem** (vimos `CL JANEIRO` com título `NOVEMBRO`, e
`CL MAIO` que é maio/2025); o layout dos dias não mente. Detecta o tipo
sozinho: linha `ABORDAGEM` → Estratégia Mensal; `STORY` → Briefing Design.

⚠️ **Rode a ingestão SEMPRE in-process** (este bloco Python único), **nunca**
por `python -c` cujo stdout é capturado: o console Windows (cp1252) corrompe
acento e grava `�` silencioso. Há guard que recusa U+FFFD, mas a regra é não
expor a ingestão ao round-trip de console.

**Editar posts (reescreve o JSON canônico atomicamente — NUNCA o HTML):**
```python
gl.move_post("clinique", "2026-05", "2026-05-10", "2026-05-11")  # puxa pra outro dia
gl.swap_posts("clinique", "2026-05", "2026-05-03", "2026-05-05") # troca dois dias
gl.set_post("clinique", "2026-05", "2026-05-06",
            product="almost-lipstick-black-honey", approach="PRODUTO",
            subject="Black Honey", channel="feed",
            ref={"kind": "style", "id": 3},
            lettering={"topo": "O tom que vira a sua cor"},
            rationale="Por que essa escolha — vira log de aprendizado")
gl.clear_post("clinique", "2026-05", "2026-05-06")               # esvazia o slot
```
Campos editáveis de um post: `channel, approach, product, subject, ref,
lettering, mockup, rationale, notes` (data e dia-da-semana são imutáveis).
`approach` segue a taxonomia da planilha: `LANÇAMENTO`, `FARMA`,
`EDUCACIONAL`, `DATA OPORTUNIDADE`, `PRODUTO`, `TREND`. `product` é o slug do
`product-catalog` quando há produto; `null` em data-oportunidade (use
`subject`). `ref` = `{"kind":"style","id":N}` (estilo curado da
`style-gallery`, caminho preferido) ou `{"kind":"url","url":"..."}`.

**Regras e calendário (curadoria humana — arquivos Markdown):**
- `grids/rules/<marca>.md` — as regras da Estela pra montar o grid daquela
  marca, em linguagem humana. Materializado do seed; **a Estela/Carol editam
  direto** (é a fonte do julgamento da Fase 2, não código).
- `grids/calendar/<ano>.md` — datas comemorativas, compartilhado entre marcas.
  Tabela Markdown editável.

  Quando o usuário pedir pra "ajustar as regras" / "adicionar uma data
  comemorativa": leia o arquivo, mostre, edite com `Write`/`Edit` e confirme.
  Não embuta regra/data em código.

**Abrir o grid:**
```python
print(gl.open_grids())   # regenera e devolve o caminho do grids.html
```
Informe o caminho ao usuário e diga para abrir no navegador. Filtro por
marca/mês no topo; cada dia mostra abordagem (cor), subject/produto, canal,
lettering e mockup (quando houver).

## Relação com as outras skills

- **`analyze-briefing`** alimenta a Fase 2 (gerar grid do briefing) — ainda
  não implementada; por ora o grid é criado vazio (`new_grid`) ou ingerido.
- **`product-catalog`** é a fonte do campo `product` (slug). Cadastre o
  produto lá antes de referenciá-lo no grid.
- **`style-gallery`** é a biblioteca de refs: `ref.kind="style"` aponta pra um
  estilo curado lá. (A geração do mockup por post — juntar grid × produto ×
  estilo via `compose_generation_brief` — é Fase 3.)
- **`image-generation`** fará o mockup do post na Fase 3.

## Lógica de decisão

- "cria/monta o grid de <mês> da <marca>" → `new_grid` (esqueleto vazio do
  mês; Fase 1 não gera do briefing — diga isso e ofereça preencher post a
  post ou ingerir uma planilha).
- "ingere/importa essa planilha", "puxa o histórico" → `xlsx_sheets` pra
  achar a aba, confirme marca/mês, `ingest_xlsx` (só 2026).
- "move/puxa o post do dia X pro dia Y" → `move_post`.
- "troca os posts do dia X e Y" → `swap_posts`.
- "muda/edita o post do dia X" (produto, abordagem, legenda, canal…) →
  `set_post`.
- "tira/esvazia o post do dia X" → `clear_post` (confirme).
- "apaga o grid de <mês>" → **confirme explicitamente**; `delete_grid`
  (reversível via `.trash/`).
- "que grids eu tenho", "abre o grid" → `list_grids` / `open_grids`.
- "ajusta as regras / adiciona data comemorativa" → editar
  `grids/rules/<marca>.md` ou `grids/calendar/<ano>.md` com Read+Edit.
- "gera o mockup do post", "gera o grid a partir do briefing" → **ainda não**
  (Fase 3 / Fase 2): explique o escopo atual e o que dá pra fazer agora.

## Regras importantes

- Confirme antes de deletar/esvaziar; nunca delete em lote.
- Nunca edite `grids.html` nem os `*.json` na mão — use as funções (escrita
  atômica + regen do grid). A planilha apodrecia exatamente por edição manual.
- `core/` é read-only: nunca grave lá; toda escrita vai pra pasta de trabalho.
- Ao editar um post, preencha o `rationale` (1 linha do porquê) quando o
  usuário der a razão — é o log de aprendizado pedido pelo Lucas.
- Sempre reporte o caminho do `grids.html` ao abrir/atualizar.
- Não exponha caminhos de arquivo a menos que o usuário peça — fale em
  "marca/mês" e datas.

## Tratamento de erros

- **`GridNotFound`**: confira com `list_grids()`; o seed é materializado no 1º
  uso (lazy-ensure) e é editável como qualquer registro.
- **`InvalidGrid`**: mês fora de `AAAA-MM`, grid sem brand/month, ou campo de
  post não editável — corrija conforme a mensagem.
- **`GridError` "Ingestão limitada a 2026"** / **"tem ano … no nome"** /
  **"corresponde a [outros anos]"** / **"vai até o dia N, mas … tem M dias"**:
  a aba **não provou** ser {mês}/2026 (é 2025, ano no nome, ou mês trocado).
  Recusa proposital — não é bug. Escolha a aba 2026 certa (`xlsx_sheets()`);
  na Estratégia o redo 2026 costuma ser a variante com underscore (`CL_MAIO`).
- **`GridError` "contém U+FFFD (mojibake)"**: a ingestão foi conduzida por
  console/`python -c` capturado (cp1252 corrompeu acento). Rode in-process.
- **`GridError` "openpyxl ausente"**: `pip install -r "$CORE/requirements.txt"`.
- **`GridError` "plugin mal empacotado"**: `grids.seed.json` /
  `rules-seed` / `calendar-seed` ausentes ou inacessíveis no `core/`
  instalado — reinstalar/atualizar o plugin. (Falha **alto** de propósito:
  mesma disciplina do bug UWP 0.3.7.)
- **Import falha**: `pip install -r "$CORE/requirements.txt"`.
