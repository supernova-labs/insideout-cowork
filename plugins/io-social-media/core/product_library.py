"""
product_library — catálogo de produtos por marca (InsideOut).

Segunda fonte de referência da geração de imagens (a primeira é
`style_library`): "o que é o produto e como a marca fala". Contrato único
consumido pela skill `product-catalog` (CRUD) e, na Fase B, pela
`image-generation` (junção estilo×produto).

Princípios (mesmos do `style_library`, ver plano swift-prancing-gosling):
- Dados na PASTA DE TRABALHO do usuário — 1 JSON por marca e 1 JSON por
  produto (`<workspace>/product-catalog/{brands,products}/<slug>.json`);
  fotos em `product-catalog/photos/<marca>/<produto>/`. Nunca no plugin dir.
- O catálogo HTML é SEMPRE derivado (gerado do JSON) — nunca fonte de dado.
- Escrita atômica; delete é soft (.trash/); nada de "apagar tudo".
- Sem workspace, cai no seed embarcado (read-only) — zero-config funciona.

A disciplina UWP-safe (nunca `.resolve()` em `__file__` de plugin; desconfiar
de todo stat do plugin dir) vive em `_libcommon`, compartilhada com
`style_library`. Sem efeitos colaterais no import.
"""
from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import _libcommon as lc

SCHEMA_VERSION = 1
LIB_DIRNAME = "product-catalog"
ENV_OVERRIDE = "PRODUCT_CATALOG_DIR"

_CORE_DIR = lc.CORE_DIR
_SEED_FILE = _CORE_DIR / "products.seed.json"
_SEED_PHOTOS_DIR = _CORE_DIR / "product-seed-photos"


class ProductCatalogError(lc.LibCommonError):
    """Erro base do catálogo."""


class BrandNotFound(ProductCatalogError):
    pass


class ProductNotFound(ProductCatalogError):
    pass


class InvalidBrand(ProductCatalogError):
    pass


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def slugify(name: str) -> str:
    return lc.slugify(name, fallback="item")


def _subdirs(lib_dir: Path):
    return (lib_dir / "brands", lib_dir / "products", lib_dir / "photos",
            lib_dir / ".trash", lib_dir / f"{LIB_DIRNAME}.html")


def _ensure_dirs(lib_dir: Path) -> Path:
    brands, products, photos, trash, _ = _subdirs(lib_dir)
    lc.ensure_dirs(lib_dir, brands, products, photos, trash)
    return lib_dir


def find_library_dir(start: Path | None = None, create: bool = True) -> Path | None:
    """
    Resolve o diretório do catálogo. Ordem:
      1. $PRODUCT_CATALOG_DIR (se setado).
      2. Busca pra cima a partir de `start` (default cwd) por um
         `product-catalog/` existente; para na raiz do git ou do filesystem.
      3. Se nada e create=True: cria `<cwd>/product-catalog/`.
         Se create=False: retorna None.
    """
    d = lc.find_library_dir(LIB_DIRNAME, ENV_OVERRIDE, start, create)
    if d is not None and create:
        return _ensure_dirs(d)
    return d


def _seed() -> dict:
    """Lê products.seed.json DE FATO. Estrutura: {brands:[...], products:[...]}."""
    data = lc.read_json_strict(_SEED_FILE)
    if not isinstance(data, dict):
        raise ProductCatalogError(
            f"products.seed.json malformado em {_SEED_FILE} — esperado objeto "
            f"com 'brands' e 'products'.")
    data.setdefault("brands", [])
    data.setdefault("products", [])
    return data


# --------------------------------------------------------------------------- #
# bootstrap / lazy-ensure
# --------------------------------------------------------------------------- #
def _copy_seed_photos(lib_dir: Path) -> dict:
    """
    Copia as fotos do seed (plugin dir) pro workspace, produto a produto.
    Disciplina anti-stat-mentiroso do `_libcommon`, agregada.

    Dirige-se pela lista `photos` DECLARADA em cada produto do seed:
    - produto sem fotos declaradas → ignora (não é erro);
    - produto COM fotos declaradas cujo subdir não pode ser lido (bloqueado
      em UWP ou ausente por packaging quebrado) → `copy_seed_assets` FALHA
      ALTO (nunca produzir catálogo mudo "sem foto" em silêncio);
    - todos listáveis mas nada copiou/existia → falha alto agregado.
    """
    _, _, photos_dir, _, _ = _subdirs(lib_dir)
    seed = _seed()
    grand_copied = grand_existed = grand_total = 0
    all_errors: list[str] = []
    for prod in seed.get("products", []):
        if not prod.get("photos"):
            continue  # seed não declara fotos pra esse produto: ok
        b = prod.get("brand", "")
        p = prod.get("slug", "")
        src = _SEED_PHOTOS_DIR / b / p
        # raise_on_empty=False: o zero-cópia é decidido agregado abaixo; mas
        # copy_seed_assets AINDA levanta se o os.listdir(src) falhar (subdir
        # bloqueado/ausente com fotos declaradas) — esse é o loud que importa.
        res = lc.copy_seed_assets(src, photos_dir / b / p, exts=lc.IMG_EXT,
                                  error_cls=ProductCatalogError,
                                  label=f"product-seed-photos/{b}/{p}",
                                  raise_on_empty=False)
        grand_copied += res["copied"]
        grand_existed += res["existed"]
        grand_total += res["total"]
        all_errors += res["errors"]
    if grand_total and grand_copied == 0 and grand_existed == 0:
        raise ProductCatalogError(
            f"Nenhuma das {grand_total} fotos do seed chegou ao workspace "
            f"({_SEED_PHOTOS_DIR} -> {photos_dir}). Erros: "
            f"{all_errors or '[sem exceção; provável bloqueio silencioso de '
            f'acesso ao diretório do plugin]'}.")
    return {"copied": grand_copied, "existed": grand_existed,
            "total": grand_total, "errors": all_errors}


def bootstrap(lib_dir: Path, _render: bool = True) -> dict:
    """
    Se `brands/` está vazio, semeia marcas+produtos a partir de
    products.seed.json (1 arquivo por entidade) e copia as fotos do seed.
    Idempotente: nunca sobrescreve arquivo já existente. As fotos são
    copiadas SEMPRE (mesmo com entidades já presentes) — responsabilidade
    distinta, como os thumbnails no style_library.
    Retorna {brands, products, photos:{copied,existed,total,errors}}.
    """
    lib_dir = _ensure_dirs(Path(lib_dir))
    brands_dir, products_dir, _, _, _ = _subdirs(lib_dir)

    # Validar seed lendo DE FATO (não .exists()).
    try:
        _seed()
    except (OSError, ValueError) as e:
        raise ProductCatalogError(
            f"products.seed.json ilegível em {_CORE_DIR} ({e!r}) — plugin mal "
            f"empacotado ou ambiente bloqueando acesso a arquivo.") from e

    photos_res = _copy_seed_photos(lib_dir)

    # Guard de idempotência: entidades só são semeadas uma vez.
    if any(brands_dir.glob("*.json")):
        if _render:
            render_catalog(lib_dir)
        return {"brands": 0, "products": 0, "photos": photos_res}

    seed = _seed()
    nb = np = 0
    for b in seed.get("brands", []):
        dest = brands_dir / f"{b['slug']}.json"
        if dest.exists():
            continue
        lc.atomic_write(dest, json.dumps(b, ensure_ascii=False, indent=2) + "\n")
        nb += 1
    for p in seed.get("products", []):
        dest = products_dir / f"{p['slug']}.json"
        if dest.exists():
            continue
        lc.atomic_write(dest, json.dumps(p, ensure_ascii=False, indent=2) + "\n")
        np += 1
    if _render:
        render_catalog(lib_dir)
    return {"brands": nb, "products": np, "photos": photos_res}


def _ensure_ready(lib_dir: Path | None = None) -> Path:
    """Lazy-ensure: resolve a pasta (criando se preciso) e roda bootstrap
    (idempotente, sem render). Workspace vira fonte única ANTES de
    exibir/curar/mutar — elimina o fallback-fantasma de seed."""
    lib_dir = _ensure_dirs(find_library_dir() if lib_dir is None else Path(lib_dir))
    bootstrap(lib_dir, _render=False)
    return lib_dir


# --------------------------------------------------------------------------- #
# leitura (pura: zero-config, sem efeito colateral — cai no seed)
# --------------------------------------------------------------------------- #
def _read_brands(lib_dir: Path) -> list[dict]:
    brands_dir, *_ = _subdirs(lib_dir)
    return lc.read_workspace_json(brands_dir)


def _read_products(lib_dir: Path) -> list[dict]:
    _, products_dir, *_ = _subdirs(lib_dir)
    return lc.read_workspace_json(products_dir)


def _resolve(lib_dir, kind: str):
    """kind: 'brands' | 'products'. Retorna (lista, origem)."""
    if lib_dir is None:
        lib_dir = find_library_dir(create=False)
    if lib_dir is not None:
        items = (_read_brands(Path(lib_dir)) if kind == "brands"
                 else _read_products(Path(lib_dir)))
        if items:
            return items, "workspace"
    return _seed().get(kind, []), "seed"


def list_brands(lib_dir: Path | None = None) -> list[dict]:
    items, _ = _resolve(lib_dir, "brands")
    return sorted(items, key=lambda b: b.get("id", 0))


def get_brand(ref, lib_dir: Path | None = None) -> dict:
    items, _ = _resolve(lib_dir, "brands")
    s = str(ref).strip()
    if s.isdigit():
        for b in items:
            if b.get("id") == int(s):
                return b
    for b in items:
        if b.get("slug") == s or b.get("name") == ref:
            return b
    raise BrandNotFound(
        f"Marca '{ref}' não encontrada (use list_brands / --list).")


def list_products(brand=None, lib_dir: Path | None = None) -> list[dict]:
    items, _ = _resolve(lib_dir, "products")
    if brand is not None:
        bslug = _brand_slug(brand, lib_dir)
        items = [p for p in items if p.get("brand") == bslug]
    return sorted(items, key=lambda p: p.get("id", 0))


def _brand_slug(brand, lib_dir) -> str:
    """Aceita slug, nome ou id de marca; devolve o slug canônico."""
    try:
        return get_brand(brand, lib_dir)["slug"]
    except BrandNotFound:
        return str(brand).strip()


def get_product(ref, brand=None, lib_dir: Path | None = None) -> dict:
    items, _ = _resolve(lib_dir, "products")
    if brand is not None:
        bslug = _brand_slug(brand, lib_dir)
        items = [p for p in items if p.get("brand") == bslug]
    s = str(ref).strip()
    if s.isdigit():
        for p in items:
            if p.get("id") == int(s):
                return p
    for p in items:
        if p.get("slug") == s or p.get("name") == ref:
            return p
    raise ProductNotFound(
        f"Produto '{ref}' não encontrado"
        f"{f' na marca {brand}' if brand else ''} (use list_products / --list).")


def _photo_abs(rel: str, lib_dir) -> str:
    """Resolve o caminho absoluto de uma foto. Prefere o workspace; cai no
    seed do plugin se ainda não materializado (leitura é segura no plugin
    dir; o bug UWP era de stat na CÓPIA, não de read)."""
    if lib_dir is not None:
        cand = Path(lib_dir) / rel
        if cand.is_file():
            return str(cand)
    # "photos/<marca>/<produto>/<arquivo>" -> seed em product-seed-photos/
    parts = Path(rel).parts
    if parts and parts[0] == "photos":
        seed_cand = _SEED_PHOTOS_DIR.joinpath(*parts[1:])
        return str(seed_cand)
    return rel


def get_product_resolved(ref, brand=None, lib_dir: Path | None = None) -> dict:
    """Produto + brief da marca + caminhos de foto absolutos, numa chamada.
    Usado pelo shim `get_product.py` e (Fase B) pela `image-generation`."""
    if lib_dir is None:
        lib_dir = find_library_dir(create=False)
    prod = get_product(ref, brand, lib_dir)
    try:
        brand_brief = get_brand(prod.get("brand", ""), lib_dir)
    except BrandNotFound:
        brand_brief = None
    return {
        **prod,
        "_brand_brief": brand_brief,
        "_photos_abs": [_photo_abs(r, lib_dir) for r in prod.get("photos", [])],
    }


# --------------------------------------------------------------------------- #
# ponte briefing → marca (Fase C) — consumida pela skill analyze-briefing
# --------------------------------------------------------------------------- #
# Campos de marca que o briefing PODE alimentar. Mapeamento explícito
# briefing -> brand.json. NÃO inventa nada: o que não veio fica vazio e é
# reportado em 'missing' pra um humano preencher (regra do analyze-briefing:
# "Não presuma informações" + fricção de inferência de briefing ruidoso).
_BRIEFING_MAP = {
    "voice": "voice",
    "key_messages": "keyMessages",
    "audience": "audience",
    "palette_hints": "paletteHints",
    "guardrails": "guardrails",
    "positioning": "positioning",
}
# brandGuide NÃO entra no briefing mensal — vem do brand-guidelines (set via
# update_brand). positioning pode vir do contexto do cliente OU do briefing.
_BRAND_OPTIONAL = ("voice", "keyMessages", "audience",
                   "paletteHints", "guardrails", "positioning", "brandGuide")


def _norm_messages(v) -> list[str]:
    """keyMessages pode vir como lista ou string solta do briefing."""
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [str(x).strip() for x in v if str(x).strip()]
    parts = re.split(r"[;\n]+", str(v))
    return [p.strip(" -•\t") for p in parts if p.strip(" -•\t")]


def brand_from_briefing(briefing: dict, *, lib_dir: Path | None = None,
                        overwrite: bool = False) -> dict:
    """
    Ponte analyze-briefing -> brand.json. Determinística e idempotente.

    NÃO INVENTA: mapeia só os campos que o briefing trouxe; o que faltar
    fica vazio e volta em 'missing' pra um humano preencher (a skill
    confirma com o usuário antes de chamar isto — não é auto-executado).

    `briefing` aceita: name (obrigatório), voice, key_messages (list|str),
    audience, palette_hints, guardrails.

    Idempotente por slug: marca nova -> add_brand; marca existente ->
    update_brand, e por padrão só sobrescreve um campo se o novo valor não
    for vazio (não apaga o que já estava). overwrite=True força o briefing
    a mandar mesmo com valor vazio.

    Retorna {"brand": <dict>, "action": "created"|"updated",
             "missing": [campos brand.json ainda vazios]}.
    """
    name = (briefing.get("name") or "").strip()
    if not name:
        raise ProductCatalogError(
            "briefing sem 'name' — a marca precisa de um nome "
            "(o analyze-briefing extrai 'Cliente/Marca' no Passo 1).")

    mapped: dict = {}
    for src, dst in _BRIEFING_MAP.items():
        if src not in briefing:
            continue
        val = (_norm_messages(briefing[src]) if dst == "keyMessages"
               else (str(briefing[src]).strip() if briefing[src] is not None
                     else ""))
        mapped[dst] = val

    lib_dir = _ensure_ready(lib_dir)
    slug = lc.slugify(name, fallback="item")
    existing = next((b for b in _read_brands(lib_dir)
                     if b.get("slug") == slug), None)

    if existing is None:
        brand = add_brand(
            name,
            voice=mapped.get("voice", ""),
            key_messages=mapped.get("keyMessages", []),
            audience=mapped.get("audience", ""),
            palette_hints=mapped.get("paletteHints", ""),
            guardrails=mapped.get("guardrails", ""),
            positioning=mapped.get("positioning", ""),
            lib_dir=lib_dir)
        action = "created"
    else:
        changes = {}
        for dst, val in mapped.items():
            if overwrite or val not in ("", [], None):
                changes[dst] = val
        brand = (update_brand(slug, lib_dir=lib_dir, **changes)
                 if changes else existing)
        action = "updated"

    missing = [f for f in _BRAND_OPTIONAL if not brand.get(f)]
    return {"brand": brand, "action": action, "missing": missing}


# --------------------------------------------------------------------------- #
# junção estilo × produto (Fase B) — consumida pela skill image-generation
# --------------------------------------------------------------------------- #
GENERATION_MODES = ("recriar", "preservar")

_MODE_INSTRUCTION = {
    "recriar": (
        "Recrie o produto fotorrealisticamente GUIADO pelas fotos de "
        "referência fornecidas (vários ângulos/composições). Mantenha "
        "proporções, cor, material e rótulo fiéis à marca; o produto pode "
        "ser reposicionado e reiluminado conforme o estilo pede."),
    "preservar": (
        "Use a foto de referência principal do produto como elemento "
        "INTOCÁVEL: NÃO redesenhe nem reinterprete o produto. Componha "
        "apenas o cenário, o fundo e o tratamento do estilo ao redor dele, "
        "integrando luz e sombra de forma coerente com a foto original."),
}


def compose_generation_brief(style: dict, product: dict,
                             brand: dict | None = None,
                             mode: str = "recriar", *,
                             lib_dir: Path | None = None) -> dict:
    """
    Junta as DUAS fontes de referência num briefing único pra geração:
    estilo (tratamento — "como a peça parece") + produto (subject + fotos
    como `reference_images`) + brief da marca (tom/composição/guardrails —
    NUNCA copy automática). Determinístico e testável; o agente ainda faz o
    enriquecimento final (skill image-generation) antes de chamar generate().

    `style`   : dict de style_library.get_style (usa prompt/name).
    `product` : dict de get_product / get_product_resolved.
    `brand`   : dict da marca; se None, usa product['_brand_brief'].
    `mode`    : 'recriar' (fotos guiam, modelo recria o produto) ou
                'preservar' (foto real intocável, só o entorno muda).

    Retorna {prompt, mode, reference_images, style, product, brand}.
    `reference_images`: recriar → todas as fotos; preservar → a 1ª (principal).
    """
    if mode not in GENERATION_MODES:
        raise ProductCatalogError(
            f"Modo '{mode}' inválido. Use um de: {', '.join(GENERATION_MODES)}.")

    if brand is None:
        brand = product.get("_brand_brief")
    brand = brand or {}

    photos_abs = product.get("_photos_abs")
    if photos_abs is None:
        photos_abs = [_photo_abs(r, lib_dir) for r in product.get("photos", [])]
    refs = photos_abs if mode == "recriar" else photos_abs[:1]

    claims = ", ".join(product.get("claims", [])) or "—"
    tags = ", ".join(product.get("tags", [])) or "—"
    msgs = "; ".join(brand.get("keyMessages", [])) or "—"
    bname = brand.get("name") or product.get("brand", "a marca")

    prompt = (
        f"**Tarefa:** Gerar uma peça de social media para "
        f"\"{product.get('name', '')}\" da marca \"{bname}\", aplicando o "
        f"estilo \"{style.get('name', '')}\".\n\n"

        f"**Estilo (tratamento visual — como a peça deve parecer):**\n"
        f"{style.get('prompt', '').strip()}\n\n"

        f"**Produto (assunto — o que aparece na peça):**\n"
        f"- {product.get('name', '')}: {product.get('description', '').strip()}\n"
        f"- Claims/atributos a respeitar: {claims}\n"
        f"- Tags do produto: {tags}\n"
        f"- Substitua qualquer \"produto-herói\" / \"[subject]\" / "
        f"\"[produto]\" do estilo por ESTE produto, com rótulo e embalagem "
        f"fiéis.\n\n"

        f"**Marca (tom e restrições — NÃO inventar copy):**\n"
        f"- Tom de voz: {brand.get('voice', '—')}\n"
        f"- Público-alvo: {brand.get('audience', '—')}\n"
        f"- Posicionamento (porquê/ancoragem da marca — orienta mood e "
        f"intenção, não vira texto): {brand.get('positioning') or '—'}\n"
        f"- Paleta/luz: {brand.get('paletteHints', '—')}\n"
        f"- Guia de identidade visual (paleta, fontes, princípios de composição "
        f"— RESPEITAR como diretriz visual): {brand.get('brandGuide') or '—'}\n"
        f"- Mensagens-chave (só para orientar mood/composição; NÃO escrever "
        f"como texto na imagem salvo pedido explícito): {msgs}\n"
        f"- Guardrails (restrições rígidas): "
        f"{brand.get('guardrails', '—')}\n\n"

        f"**Modo: {mode}**\n{_MODE_INSTRUCTION[mode]}\n\n"

        f"**Restrições:**\n"
        f"- Qualquer texto/UI da peça em português do Brasil.\n"
        f"- SEM copy/headline/claim escrito na imagem a menos que solicitado "
        f"explicitamente.\n"
        f"- Respeitar os guardrails da marca como limites rígidos.\n"
        f"- Coerência de luz/sombra entre o produto e o cenário."
    )

    return {
        "prompt": prompt,
        "mode": mode,
        "reference_images": refs,
        "style": style.get("id"),
        "product": product.get("slug"),
        "brand": brand.get("slug") or product.get("brand"),
    }


# --------------------------------------------------------------------------- #
# escrita — marcas
# --------------------------------------------------------------------------- #
def add_brand(name: str, *, voice: str = "", key_messages: list[str] | None = None,
              audience: str = "", palette_hints: str = "", guardrails: str = "",
              positioning: str = "", brand_guide: str = "",
              lib_dir: Path | None = None) -> dict:
    """Cria uma marca. Slug único, id monotônico, escrita atômica.

    `positioning` (contexto do cliente — por que a marca existe, ancoragem) e
    `brand_guide` (identidade visual: paleta, fontes, princípios, tom) alimentam
    a geração via compose_generation_brief."""
    lib_dir = _ensure_ready(lib_dir)
    brands_dir, *_ = _subdirs(lib_dir)
    slug = lc.unique_slug(brands_dir, slugify(name))
    ts = lc.now()
    brand = {
        "schemaVersion": SCHEMA_VERSION,
        "id": lc.next_id(_read_brands(lib_dir)),
        "slug": slug,
        "name": name,
        "voice": voice,
        "keyMessages": list(key_messages or []),
        "audience": audience,
        "paletteHints": palette_hints,
        "guardrails": guardrails,
        "positioning": positioning,
        "brandGuide": brand_guide,
        "createdAt": ts,
        "updatedAt": ts,
    }
    lc.atomic_write(brands_dir / f"{slug}.json",
                    json.dumps(brand, ensure_ascii=False, indent=2) + "\n")
    render_catalog(lib_dir)
    return brand


def update_brand(ref, *, lib_dir: Path | None = None, **fields) -> dict:
    """Atualiza campos de uma marca. slug e id são estáveis."""
    lib_dir = _ensure_ready(lib_dir)
    brands_dir, *_ = _subdirs(lib_dir)
    fp = lc.find_workspace_file(
        brands_dir, ref, error_cls=BrandNotFound,
        not_found_msg=f"Marca '{ref}' não encontrada na biblioteca.")
    brand = json.loads(fp.read_text(encoding="utf-8"))
    for k in ("schemaVersion", "id", "slug", "createdAt"):
        fields.pop(k, None)
    brand.update(fields)
    brand["updatedAt"] = lc.now()
    lc.atomic_write(fp, json.dumps(brand, ensure_ascii=False, indent=2) + "\n")
    render_catalog(lib_dir)
    return brand


def delete_brand(ref, *, lib_dir: Path | None = None) -> dict:
    """Soft-delete da marca (vai pra .trash/). NÃO cascateia: avisa quantos
    produtos ficam órfãos — quem chama (skill) decide o que fazer."""
    lib_dir = _ensure_ready(lib_dir)
    brands_dir, _, _, trash_dir, _ = _subdirs(lib_dir)
    fp = lc.find_workspace_file(
        brands_dir, ref, error_cls=BrandNotFound,
        not_found_msg=f"Marca '{ref}' não encontrada na biblioteca.")
    brand = json.loads(fp.read_text(encoding="utf-8"))
    attached = [p for p in _read_products(lib_dir)
                if p.get("brand") == brand.get("slug")]
    trash_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = trash_dir / f"brand.{fp.stem}.{stamp}.json"
    os.replace(fp, dest)
    render_catalog(lib_dir)
    return {"deleted": fp.name, "trash": str(dest),
            "orphanProducts": [p.get("slug") for p in attached]}


# --------------------------------------------------------------------------- #
# escrita — produtos
# --------------------------------------------------------------------------- #
def _ingest_photos(photos_root: Path, brand_slug: str, product_slug: str,
                   paths: list[str], start_idx: int = 1) -> list[str]:
    """Copia fotos pro workspace (`photos/<marca>/<produto>/`). Devolve os
    caminhos relativos (pra gravar no JSON do produto)."""
    tgt_dir = photos_root / brand_slug / product_slug
    tgt_dir.mkdir(parents=True, exist_ok=True)
    rels: list[str] = []
    i = start_idx
    for src in paths or []:
        sp = Path(src)
        if not sp.is_file():
            continue
        ext = sp.suffix.lower() or ".jpg"
        name = f"{i:02d}{ext}"
        while (tgt_dir / name).exists():
            i += 1
            name = f"{i:02d}{ext}"
        shutil.copy2(sp, tgt_dir / name)
        rels.append(f"photos/{brand_slug}/{product_slug}/{name}")
        i += 1
    return rels


def add_product(name: str, *, brand, description: str = "",
                claims: list[str] | None = None, tags: list[str] | None = None,
                photos: list[str] | None = None,
                lib_dir: Path | None = None) -> dict:
    """Cria um produto numa marca existente. A marca tem que existir."""
    lib_dir = _ensure_ready(lib_dir)
    brands_dir, products_dir, photos_root, _, _ = _subdirs(lib_dir)
    try:
        b = get_brand(brand, lib_dir)
    except BrandNotFound:
        raise InvalidBrand(
            f"Marca '{brand}' não existe. Crie a marca antes "
            f"(add_brand) ou use um slug/nome/id válido.")
    bslug = b["slug"]
    slug = lc.unique_slug(products_dir, slugify(name))
    rel_photos = _ingest_photos(photos_root, bslug, slug, photos or [])
    ts = lc.now()
    product = {
        "schemaVersion": SCHEMA_VERSION,
        "id": lc.next_id(_read_products(lib_dir)),
        "slug": slug,
        "brand": bslug,
        "name": name,
        "description": description,
        "claims": list(claims or []),
        "tags": list(tags or []),
        "photos": rel_photos,
        "createdAt": ts,
        "updatedAt": ts,
    }
    lc.atomic_write(products_dir / f"{slug}.json",
                    json.dumps(product, ensure_ascii=False, indent=2) + "\n")
    render_catalog(lib_dir)
    return product


def _find_product_file(lib_dir: Path, ref):
    _, products_dir, *_ = _subdirs(lib_dir)
    return lc.find_workspace_file(
        products_dir, ref, error_cls=ProductNotFound,
        not_found_msg=f"Produto '{ref}' não encontrado na biblioteca.")


def update_product(ref, *, lib_dir: Path | None = None, **fields) -> dict:
    """Atualiza campos de um produto. slug, id e brand são estáveis."""
    lib_dir = _ensure_ready(lib_dir)
    fp = _find_product_file(Path(lib_dir), ref)
    product = json.loads(fp.read_text(encoding="utf-8"))
    for k in ("schemaVersion", "id", "slug", "brand", "createdAt", "photos"):
        fields.pop(k, None)  # photos muda só via add_photos/remove_photo
    product.update(fields)
    product["updatedAt"] = lc.now()
    lc.atomic_write(fp, json.dumps(product, ensure_ascii=False, indent=2) + "\n")
    render_catalog(lib_dir)
    return product


def delete_product(ref, *, lib_dir: Path | None = None) -> dict:
    """Soft-delete: move o JSON pra .trash/ (recuperável). Não apaga fotos."""
    lib_dir = _ensure_ready(lib_dir)
    _, _, _, trash_dir, _ = _subdirs(lib_dir)
    fp = _find_product_file(lib_dir, ref)
    trash_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = trash_dir / f"product.{fp.stem}.{stamp}.json"
    os.replace(fp, dest)
    render_catalog(lib_dir)
    return {"deleted": fp.name, "trash": str(dest)}


def add_photos(product_ref, paths: list[str], *,
               lib_dir: Path | None = None) -> dict:
    """Adiciona fotos a um produto existente."""
    lib_dir = _ensure_ready(lib_dir)
    _, _, photos_root, _, _ = _subdirs(lib_dir)
    fp = _find_product_file(lib_dir, product_ref)
    product = json.loads(fp.read_text(encoding="utf-8"))
    existing = product.get("photos", [])
    rels = _ingest_photos(photos_root, product["brand"], product["slug"],
                          paths, start_idx=len(existing) + 1)
    product["photos"] = existing + rels
    product["updatedAt"] = lc.now()
    lc.atomic_write(fp, json.dumps(product, ensure_ascii=False, indent=2) + "\n")
    render_catalog(lib_dir)
    return {"product": product["slug"], "added": rels,
            "total": len(product["photos"])}


def remove_photo(product_ref, photo: str, *,
                 lib_dir: Path | None = None) -> dict:
    """Remove uma foto do produto (tira da lista + move o arquivo pra .trash/).
    `photo` aceita o caminho relativo completo ou só o nome do arquivo."""
    lib_dir = _ensure_ready(lib_dir)
    _, _, _, trash_dir, _ = _subdirs(lib_dir)
    fp = _find_product_file(lib_dir, product_ref)
    product = json.loads(fp.read_text(encoding="utf-8"))
    photos = product.get("photos", [])
    match = next((r for r in photos
                  if r == photo or Path(r).name == photo), None)
    if match is None:
        raise ProductNotFound(
            f"Foto '{photo}' não está no produto '{product['slug']}'.")
    src = Path(lib_dir) / match
    if src.is_file():
        trash_photos = trash_dir / "photos"
        trash_photos.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        os.replace(src, trash_photos / f"{product['slug']}.{stamp}.{src.name}")
    product["photos"] = [r for r in photos if r != match]
    product["updatedAt"] = lc.now()
    lc.atomic_write(fp, json.dumps(product, ensure_ascii=False, indent=2) + "\n")
    render_catalog(lib_dir)
    return {"product": product["slug"], "removed": match,
            "total": len(product["photos"])}


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def render_catalog(lib_dir: Path | None = None) -> Path:
    """Regenera o painel unificado da InsideOut (`insideout-painel.html`) com a
    aba Produtos. O catálogo virou uma aba do painel único; este wrapper preserva
    o nome histórico que o CRUD chama. As fotos são reescritas relativas ao painel
    (`product-catalog/photos/...`) pelo orquestrador. Sempre derivado."""
    lib_dir = _ensure_ready(lib_dir)
    import dashboard  # import tardio: quebra o ciclo dashboard <-> libs
    return dashboard.render_dashboard(active_tab="products", product_dir=lib_dir)


def open_catalog(lib_dir: Path | None = None) -> Path:
    """Regenera e devolve o caminho do painel (a skill instrui a abrir na aba
    Produtos via `#products`)."""
    return render_catalog(lib_dir)
