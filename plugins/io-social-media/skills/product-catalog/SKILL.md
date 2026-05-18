---
name: product-catalog
description: 'Catálogo de produtos por marca da InsideOut — cadastrar/listar/editar/remover marcas e produtos, gerenciar fotos e abrir o catálogo HTML. Use para "cadastra a marca X", "adiciona o produto Y", "que produtos tem a marca Z", "abre o catálogo", "atualiza o tom de voz da marca", "adiciona/remove foto do produto".'
allowed-tools: Bash, Read, Write
argument-hint: '[cadastrar marca | cadastrar produto | listar | abrir catálogo | editar | remover | fotos]'
disable-model-invocation: false
---

# Product Catalog — catálogo de produtos por marca InsideOut

Segunda fonte de referência da geração de imagens (a primeira é a
`style-gallery`): enquanto o estilo diz **"como a imagem deve parecer"**, o
catálogo diz **"o que é o produto e como a marca fala"**. Cada **marca** tem
tom de voz, mensagens-chave, público-alvo, paleta e guardrails; cada **produto**
tem descrição, claims, tags e várias **fotos** em ângulos/composições. A skill
`image-generation` consome este catálogo para compor uma peça (estilo × produto).

## Onde rodar (crítico)

O diretório do plugin (`${CLAUDE_PLUGIN_ROOT}`) é **read-only e efêmero por
sessão** no Cowork. O catálogo **vivo** do cliente vive na **pasta de
trabalho**, não no plugin. Nunca faça `cd` para o `core/`; importe via
`sys.path` com cwd = pasta de trabalho.

Padrão de invocação (use em tudo abaixo):
```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
import product_library as pc
# ... chamada ...
"
```
Dependências (se faltar import): `pip install -r "$CORE/requirements.txt"`.

## Onde fica o catálogo

`pc.find_library_dir()` resolve nesta ordem:
1. variável de ambiente `PRODUCT_CATALOG_DIR`, se setada;
2. busca **pra cima** a partir do cwd por uma pasta `product-catalog/`
   existente (para na raiz do git/filesystem) — rodar de uma subpasta não
   cria catálogo duplicado;
3. se nada: cria `<pasta de trabalho>/product-catalog/`.

Estrutura: `product-catalog/brands/<slug>.json` (1 arquivo por marca),
`products/<slug>.json` (1 por produto, com FK `brand`), `photos/<marca>/<produto>/`,
`product-catalog.html` (gerado), `.trash/`. Sem catálogo no workspace, leitura
cai no **seed embarcado** (1 marca exemplo + 2 produtos) — funciona com zero
config.

Se for um repositório git, garanta no `.gitignore` da pasta de trabalho:
ignorar `product-catalog/product-catalog.html` e `product-catalog/.trash/`;
**versionar** `product-catalog/brands/`, `product-catalog/products/` e
`product-catalog/photos/` (é o ativo de marca do cliente).

## Operações

**Primeiro uso é automático** — não chame `bootstrap` manualmente. Qualquer
operação que exibe/cura/muta (`render_catalog`, `open_catalog`, `add_brand`,
`add_product`, `update_*`, `delete_*`, `add_photos`, `remove_photo`) já faz
**lazy-ensure**: na primeira vez materializa o seed (marca/produtos/fotos
exemplo) no workspace (idempotente, nunca sobrescreve o que existe).

**Listar / ver:**
```python
for b in pc.list_brands(): print(b['id'], b['slug'], '-', b['name'])
for p in pc.list_products('marca-exemplo'): print(p['id'], p['name'], p['tags'])
print(pc.get_product(2))                       # por id
print(pc.get_product('serum-exemplo'))         # por slug
print(pc.get_product_resolved(2))              # + brief da marca + fotos abs
```

**Cadastrar marca** (slug único, id monotônico, escrita atômica):
```python
pc.add_brand("Nome da Marca",
             voice="tom de voz da marca, em 1-3 frases",
             key_messages=["mensagem-chave 1", "mensagem-chave 2"],
             audience="quem é o público-alvo",
             palette_hints="cores/luz típicas (opcional)",
             guardrails="o que NUNCA fazer com a marca (opcional)")
```

**Cadastrar produto** (a marca tem que existir; copia as fotos pro workspace):
```python
pc.add_product("Nome do Produto", brand="slug-ou-nome-da-marca",
               description="o que é o produto, embalagem, tamanho",
               claims=["claim 1", "claim 2"],
               tags=["packshot", "em-cenario"],
               photos=["/caminho/foto1.jpg", "/caminho/foto2.jpg"])
```

**Editar** (slug, id e brand são estáveis; `photos` muda só via add/remove):
```python
pc.update_brand("slug-marca", voice="novo tom", audience="novo público")
pc.update_product(3, description="...", tags=["still-life"])
```

**Fotos de um produto:**
```python
pc.add_photos(3, ["/caminho/nova-foto.jpg"])      # adiciona
pc.remove_photo(3, "02.jpg")                       # tira (vai pra .trash/)
```

**Remover** (soft-delete reversível — vai pra `.trash/`, **não existe**
"apagar tudo"; `delete_brand` **não** cascateia, só avisa produtos órfãos):
```python
pc.delete_product(3)
pc.delete_brand("slug-marca")   # retorna orphanProducts: [...]
```

O catálogo HTML é regenerado automaticamente após todo add/update/delete.

## Abrir o catálogo

```python
print(pc.open_catalog())   # regenera e devolve o caminho do product-catalog.html
```
Informe ao usuário o caminho e diga para abrir no navegador. Ele vive ao lado
de `photos/`, então os previews carregam; produto sem foto mostra placeholder
limpo ("sem fotos") automaticamente.

## Relação com a geração de imagens

Esta skill é **curadoria** do ativo de marca. **Gerar uma peça** combinando um
produto deste catálogo com um estilo da `style-gallery` é trabalho da skill
**`image-generation`** — encaminhe para lá quando o usuário pedir "gera um post
do produto X da marca Y no estilo #N". Para alinhar nome/tom de uma marca à
identidade da InsideOut, consulte a skill `about-insideout` antes de cadastrar.

## Lógica de decisão

- "cadastra/cria a marca X", "registra a marca" → confirme voz, mensagens-chave
  e público com o usuário antes; `add_brand`.
- "popula/atualiza a marca a partir do briefing", "salva a marca desse briefing"
  → `brand_from_briefing(briefing_dict)` — ponte idempotente por slug (cria ou
  atualiza só campos não-vazios). **Não inventa**: o que o briefing não trouxe
  volta em `missing`; reporte ao usuário o que falta preencher. O fluxo natural
  vem da skill `analyze-briefing` (Passo 4 opcional) — aqui você fecha o que
  ficou faltando depois.
- "adiciona o produto Y na marca X", "cadastra esse produto" → a marca tem que
  existir (senão crie antes); peça as fotos; `add_product`.
- "que marcas/produtos eu tenho", "abre o catálogo" → `list_brands` /
  `list_products` / `open_catalog`.
- "atualiza o tom de voz / público / descrição" → `update_brand` /
  `update_product` (slug e id não mudam).
- "adiciona/remove foto do produto" → `add_photos` / `remove_photo`.
- "apaga/remove a marca/produto X" → **confirme explicitamente** antes;
  `delete_*` (reversível via `.trash/`). Ao apagar marca, avise os produtos
  órfãos e pergunte o que fazer com eles (não cascateia sozinho).
- "gera uma imagem com o produto X" → **não é aqui**: encaminhe para
  `image-generation`.

## Regras importantes

- Confirme antes de deletar; nunca delete em lote nem ofereça "limpar tudo".
- Ao apagar uma marca, **não** apague os produtos junto — reporte os órfãos.
- Após cadastrar, resuma ao usuário: nome, e (produto) marca, tags, nº de
  fotos, id ("produto #id").
- Não exponha `slug`/caminhos de arquivo a menos que o usuário peça — fale em
  nome e "#id".
- Sempre reporte o caminho do `product-catalog.html` ao abrir/atualizar.
- `core/` é read-only: nunca grave lá; toda escrita vai para a pasta de
  trabalho via o módulo.
- Não edite `brands/*.json` / `products/*.json` na mão — use as funções
  (escrita atômica + regen do catálogo).

## Tratamento de erros

- **`InvalidBrand`**: o produto referencia uma marca inexistente — crie a marca
  (`add_brand`) ou corrija o slug/nome/id.
- **`BrandNotFound` / `ProductNotFound`**: confira com `list_brands()` /
  `list_products()`; o seed é materializado no 1º uso (lazy-ensure) e é
  editável como qualquer registro.
- **`ProductCatalogError` "plugin mal empacotado"**: `products.seed.json` /
  `product-seed-photos` ausentes ou inacessíveis no `core/` instalado —
  reinstalar/atualizar o plugin. (Falha **alto** de propósito: nunca produzir
  catálogo mudo "sem foto" em silêncio — mesma disciplina do bug UWP 0.3.7.)
- **Import falha**: `pip install -r "$CORE/requirements.txt"`.
