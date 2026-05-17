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

## Localização do toolkit

Scripts em: `${CLAUDE_PLUGIN_ROOT}/skills/image-generation/toolkit/`

Antes de qualquer comando Python, entre no diretório do toolkit:
```bash
cd "${CLAUDE_PLUGIN_ROOT}/skills/image-generation/toolkit"
```
(Em desenvolvimento local, se `${CLAUDE_PLUGIN_ROOT}` não estiver setado, use o caminho do plugin no repo: `.../insideout-cowork/plugins/io-social-media/skills/image-generation/toolkit`.)

### Chave de API

O motor lê `GEMINI_API_KEY` do ambiente. Configure por uma destas formas (nunca commite a chave):

1. **Arquivo `.env` (método confiável hoje)**: no diretório do toolkit existe um `.env.example`. Copie-o para `.env` na mesma pasta e preencha a chave:
   ```bash
   cd "${CLAUDE_PLUGIN_ROOT}/skills/image-generation/toolkit"
   cp .env.example .env   # depois edite .env e cole a chave em GEMINI_API_KEY=
   ```
   O `.env` é gitignored — a chave nunca vai para o repositório. Chave em https://aistudio.google.com/apikey
2. **userConfig do plugin**: ao instalar, o Cowork pede `GEMINI_API_KEY` e injeta como variável de ambiente. ⚠️ Há um bug conhecido na UI do Cowork (issues #39455 e #39827) que pode impedir a injeção — por isso o método 1 (`.env`) é o recomendado até o bug ser resolvido. Quando funcionar, o userConfig dispensa o `.env`.

O script tenta `os.environ` e depois `load_dotenv()`, então qualquer um dos dois caminhos funciona (e o `.env` tem precedência prática quando o userConfig falha).

## Scripts disponíveis

### 1. image_gen.py — motor de geração

`generate(prompt, reference_images=None, aspect_ratio="1:1", resolution="1K", model="gemini-3-pro-image-preview")` → retorna o caminho da imagem (`outputs/output_XXX_HHMMSS.png`).
`new_session()` zera o histórico · `session_info()` mostra a sessão · `revert(turns=1)` desfaz N iterações.

Cada `generate()` continua a conversa anterior automaticamente (sessão em `.image_session.json`). Só chame `new_session()` ao começar uma peça nova e não relacionada.

```bash
cd "${CLAUDE_PLUGIN_ROOT}/skills/image-generation/toolkit"
python -c "
from dotenv import load_dotenv; load_dotenv()
from image_gen import generate
result = generate('prompt enriquecido aqui...', aspect_ratio='9:16', resolution='1K')
print(f'Gerada: {result}')
"
```

### 2. style_extract.py — análise de estilo

Use quando o usuário fornecer uma **imagem custom** de referência ("use esta imagem", "aplique o visual desta foto"). **Obrigatório extrair antes de gerar** — a análise de visão do Gemini é muito superior a descrição manual.

```bash
cd "${CLAUDE_PLUGIN_ROOT}/skills/image-generation/toolkit"
python -c "
from dotenv import load_dotenv; load_dotenv()
from style_extract import extract_style
print(extract_style('caminho/para/referencia.jpg'))
"
```
Para um elemento específico (ex.: só a paleta, só a tipografia da peça de referência), passe `custom_prompt='...'` focado nesse elemento.

### 3. get_style.py — biblioteca de estilos numerados

Use quando o usuário citar "estilo #125" / "usa o estilo 42". **Não** extraia — esses estilos já estão prontos.
```bash
cd "${CLAUDE_PLUGIN_ROOT}/skills/image-generation/toolkit"
python get_style.py 125
```
Retorna `id`, `name`, `prompt` (substitua `[subject]` pelo assunto), `category`, `exampleUse`.

Catálogo navegável: abra `toolkit/style-library.html` no navegador. **Nota**: o catálogo nasce com **5 estilos de exemplo** (social/PR) — a Inside.out monta as próprias referências de marca adicionando objetos ao array `const styles` no `style-library.html` (campos: `id`, `name`, `category`, `tags`, `prompt`, `exampleUse`, `thumbnail`). Estilo sem thumbnail gerado ainda exibe um placeholder limpo ("sem preview") automaticamente — segue 100% utilizável via `get_style.py` / "estilo #N".

## Lógica de decisão

- **"Gere [algo] para [formato]"** → escolha o preset de aspect_ratio, alinhe à marca (about-insideout), enriqueça, mostre o prompt, gere com `image_gen.py` (continua a sessão).
- **"Use o estilo #42"** → `get_style.py 42`, troque `[subject]`, enriqueça, mostre, gere.
- **"Use esta_imagem.jpg de referência"** → **extraia primeiro** com `style_extract.py`, incorpore a descrição ao prompt, gere com `reference_images=['esta_imagem.jpg']`.
- **"Deixe mais escuro / mais quente / adicione X"** → **não** chame `new_session()`; enriqueça o ajuste e gere (a sessão continua a partir da última imagem).
- **"Recomeçar / nova peça"** → `new_session()` e siga.

## Regras importantes

- **Nunca modifique os scripts do toolkit** (`image_gen.py`, `style_extract.py`, `get_style.py`, `style-library.html`, `.env`). Se precisar de lógica custom, crie um arquivo temporário que importe do toolkit.
- **Nunca commite `.env`, `outputs/` nem `.image_session.json`** (já cobertos pelo `.gitignore`).
- Sempre retorne ao usuário o caminho da imagem gerada.
- Dependências: `pip install -r requirements.txt` (google-genai, python-dotenv, pillow) caso a geração falhe por import.

## Tratamento de erros

**Geração falha**: verifique `GEMINI_API_KEY` no ambiente/`.env`; confirme o diretório do toolkit; tente `new_session()` (sessão corrompida); cheque os paths das imagens de referência; instale deps via `requirements.txt`.
**Extração falha**: confirme que o caminho da imagem existe e é legível; valide a chave.
**get_style falha**: confirme que o número existe no catálogo e que `style-library.html` está presente.

## Checklist por geração

- [ ] Marca/contexto alinhado (about-insideout / briefing) ou genérico assumido a pedido
- [ ] Preset de formato → aspect_ratio correto
- [ ] Prompt enriquecido (iluminação, mood, textura, atmosfera, composição, espaço para copy)
- [ ] Prompt mostrado ao usuário antes de gerar
- [ ] Estilo #N: recuperado com `get_style.py` · Imagem custom: extraída com `style_extract.py`
- [ ] Sessão: continuar vs. nova decidido
- [ ] Caminho da imagem devolvido ao usuário

**Lembre**: o que separa resultado excepcional de genérico é o enriquecimento detalhado do prompt + alinhamento à marca. Nunca passe o prompt cru do usuário direto para a API.
