---
name: generate-video
description: 'Geração de vídeo curto com IA (Veo) para social media da InsideOut — stories, reels, teasers. Use para "gera um vídeo pro story", "cria um reels de X", "transforma essa imagem em vídeo", "faz um vídeo de 8 segundos de Y", "anima essa peça". Vídeo é caro e lento — confirme antes de gerar.'
allowed-tools: Bash, Read, Write
argument-hint: '[descrição do vídeo | "anima esta imagem" | story/reels]'
disable-model-invocation: false
---

# Generate Video — vídeo curto InsideOut (Veo)

Gera clipes curtos (stories, reels, teasers) com o Veo, a partir de um prompt de
texto e — de preferência — de uma **imagem-âncora** pra dar consistência de cena.
Os stories da InsideOut têm muito vídeo; esta skill cobre esse pedaço.

> **Tom com o usuário (sempre):** quem opera não é técnico. Leia e aplique `${CLAUDE_PLUGIN_ROOT}/skills/voz-usuario.md` — fale de vídeo, story, reels, cena; **nunca** de implementação (API, polling, caminho, encoding). Resolva erros nos bastidores e relate só o essencial.

> **⚠️ Vídeo é caro e lento.** Cada clipe leva ~1-3 min e consome bem mais que uma
> imagem. **Confirme com o usuário antes de gerar** (descrição + formato + que é
> ~1 clipe curto). Nunca gere em lote sem confirmar.

## Princípio central: enriqueça o prompt (igual imagem) + ancore numa imagem

1. **Enriqueça** o prompt do usuário antes de gerar — **movimento de câmera**
   (travelling, zoom-in lento, estático), **ação/movimento na cena**, ritmo,
   iluminação, mood, atmosfera. Mostre o prompt enriquecido antes de gerar.
2. **Ancore numa imagem** sempre que possível (`image=<caminho>`): o Veo parte
   dela (image-to-video), o que mantém a cena/"ator" consistente. É o jeito de
   evitar a dor clássica — o personagem que começa não é o que termina. Use uma
   imagem boa (gerada na `image-generation`, foto do produto, frame de marca).

## Onde rodar (crítico)

O diretório do plugin (`${CLAUDE_PLUGIN_ROOT}`) é **read-only e efêmero por
sessão** no Cowork. Rode da **pasta de trabalho**; importe o motor via `sys.path`
(nunca `cd` para o `core/`). Os `.mp4` saem em `outputs/` na pasta de trabalho.

```bash
CORE="${CLAUDE_PLUGIN_ROOT}/core"
python -c "
import sys; sys.path.insert(0, r'$CORE')
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
import video_gen as vg
caminho = vg.generate_video(
    'PROMPT ENRIQUECIDO AQUI — movimento de câmera, ação, mood',
    image='outputs/anchor.png',      # opcional, mas recomendado (image-to-video)
    aspect_ratio='9:16',             # 9:16 stories/reels (default) | 16:9 horizontal
    resolution='720p',               # 720p (default) | 1080p
    duration_seconds=8)
print('VÍDEO:', caminho)
"
```
Dependências (se faltar import): `pip install -r "$CORE/requirements.txt"`
(usa `google-genai`, o mesmo da geração de imagem).

## Chave de API

Precisa de `GEMINI_API_KEY` no `.env` da **pasta de trabalho** — a **mesma** chave
da `image-generation` (o agente cria/gerencia; o usuário não toca no plugin).
Sem chave, a chamada estoura `ValueError "GEMINI_API_KEY not found"`.

## Formatos

| Destino | aspect_ratio |
|---|---|
| Stories / Reels / TikTok | `9:16` (default) |
| Horizontal (YouTube, capa) | `16:9` |

Resolução: `720p` (default, mais rápido/barato) ou `1080p`. Duração: ~8s por clipe
(modelos abertos não geram clipes longos — pra vídeo maior, gere 2-3 clipes e
costure na edição).

## Costura com as outras skills

- **`image-generation`** — gere primeiro a **imagem-âncora** lá (capa/cena do
  vídeo) e passe o caminho em `image=` aqui. É o caminho recomendado pra
  consistência.
- **`generate-grid`** — o grid hoje guarda **mockup de imagem** por post. Vídeo
  ainda **não** é anexado ao grid (fast-follow); por ora entregue o `.mp4` e diga
  ao usuário onde ele está.

## Lógica de decisão

- "gera um vídeo de X" / "vídeo pro story" → confirme descrição + formato +
  custo/tempo, enriqueça o prompt, **mostre antes**, gere com `generate_video`.
- "transforma essa imagem em vídeo" / "anima essa peça" → `image=<caminho da
  imagem>` + prompt de movimento; é o caminho image-to-video.
- "um vídeo mais longo" → explique que sai em clipes de ~8s; gere âncoras e
  costure (ou gere 2-3 e ofereça juntar).

## Regras importantes

- **Confirme custo/tempo antes de gerar** — vídeo é caro e demora; nunca gere em
  lote sem o OK do usuário.
- **Enriqueça o prompt** (movimento/câmera/mood) e **mostre antes** de gerar.
- **Ancore numa imagem** quando possível — consistência de cena.
- `core/` é read-only: o `.mp4` vai pra `outputs/` na pasta de trabalho.
- Reporte só o caminho do vídeo e o que ele mostra, em linguagem de negócio.

## Tratamento de erros

- **`ValueError "GEMINI_API_KEY not found"`** — crie o `.env` na pasta de trabalho
  com a chave (https://aistudio.google.com/apikey), igual à `image-generation`.
- **"model not found" / modelo indisponível** — a conta pode não ter o `veo-3.0-
  generate-001` habilitado. Tente `model='veo-3.0-fast-generate-001'`,
  `model='veo-2.0-generate-001'`, ou um id de preview vigente.
- **Filtro de conteúdo (nenhum vídeo retornado)** — ajuste o prompt (pessoas,
  marcas, conteúdo sensível). A mensagem traz os motivos quando disponíveis.
- **`TimeoutError`** — o vídeo demorou mais que o timeout; tente de novo ou
  aumente `timeout=` (a geração pode seguir no servidor).
- **Import falha** — `pip install -r "$CORE/requirements.txt"`.
