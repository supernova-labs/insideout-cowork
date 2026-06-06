"""
Gemini Video Generation Module (Veo)

Wrapper pra Claude Code chamar — gera UM vídeo curto via Veo, fazendo o polling
da operação long-running e salvando o `.mp4`. Espelha o `image_gen.py` (mesma
`.env`/`GEMINI_API_KEY`, mesma pasta `outputs/`). NÃO tem sessão multi-turn
(vídeo não é conversacional como o chat de imagem).

Vídeo é caro e lento (~1-3 min por clipe) — a skill `generate-video` confirma
custo/tempo com o usuário ANTES de chamar. Sem efeitos colaterais no import além
do `load_dotenv()` (igual `image_gen`).

API (google-genai 1.70.x): `client.models.generate_videos(model, prompt, image,
config) -> operation` long-running; poll `client.operations.get(op)` até
`op.done`; `op.response.generated_videos[0].video`; `client.files.download(file=
video)` + `video.save(path)`.
"""
import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types

# Configuration
OUTPUT_DIR = "outputs"
# Modelo Veo. Se a conta não tiver este id habilitado, a 1ª chamada estoura
# "model not found" — troque por uma alternativa (veo-3.0-fast-generate-001,
# veo-2.0-generate-001, ou um id de preview). Documentado no SKILL.md.
DEFAULT_VIDEO_MODEL = "veo-3.0-generate-001"
DEFAULT_ASPECT_RATIO = "9:16"      # stories/reels — uso mais comum da InsideOut
DEFAULT_RESOLUTION = "720p"        # 720p ou 1080p (1080p só 16:9 em alguns modelos)
DEFAULT_DURATION = 8               # segundos
DEFAULT_POLL_INTERVAL = 10         # s entre checagens da operação
DEFAULT_TIMEOUT = 360              # s no total esperando o vídeo concluir

_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".webp": "image/webp"}


def _get_client():
    """Initialize Gemini client (mesma chave da image-generation)."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment. Check your .env file.")
    return genai.Client(api_key=api_key)


def _ensure_output_dir():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)


def _next_output_path() -> str:
    _ensure_output_dir()
    ts = datetime.now().strftime("%H%M%S")
    n = 1
    while Path(f"{OUTPUT_DIR}/video_{n:03d}_{ts}.mp4").exists():
        n += 1
    return f"{OUTPUT_DIR}/video_{n:03d}_{ts}.mp4"


def _load_anchor_image(image_path: str):
    p = Path(image_path)
    if not p.is_file():
        raise FileNotFoundError(f"Imagem-âncora não encontrada: {image_path}")
    mime = _MIME.get(p.suffix.lower(), "image/png")
    return types.Image.from_file(location=str(p), mime_type=mime)


def generate_video(
    prompt: str,
    *,
    image: str | None = None,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    duration_seconds: int = DEFAULT_DURATION,
    negative_prompt: str | None = None,
    model: str = DEFAULT_VIDEO_MODEL,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    """Gera UM vídeo curto via Veo e salva o `.mp4` em `outputs/`. Devolve o caminho.

    Args:
        prompt: descrição do vídeo — enriqueça com movimento de câmera, ação,
                mood e atmosfera antes (regra herdada da `image-generation`).
        image:  caminho de uma imagem-âncora (image-to-video) pra dar consistência
                de cena/"ator" — opcional, mas recomendado (resolve a dor do
                ator que começa diferente do que termina).
        aspect_ratio: '9:16' (stories/reels, default) ou '16:9'.
        resolution: '720p' (default) ou '1080p'.
        duration_seconds: duração do clipe (default 8).
        negative_prompt: o que evitar (opcional).
        model: id do modelo Veo (ver DEFAULT_VIDEO_MODEL).

    Veo é long-running: dispara, faz polling até concluir, baixa e salva. Levanta
    em timeout, erro da operação, ou filtro de conteúdo (nenhum vídeo retornado).
    """
    client = _get_client()

    cfg_kwargs = dict(aspect_ratio=aspect_ratio, resolution=resolution,
                      duration_seconds=duration_seconds, number_of_videos=1)
    if negative_prompt:
        cfg_kwargs["negative_prompt"] = negative_prompt
    config = types.GenerateVideosConfig(**cfg_kwargs)

    kwargs = {"model": model, "prompt": prompt, "config": config}
    if image:
        kwargs["image"] = _load_anchor_image(image)

    print(f"Gerando vídeo (Veo {model}, {aspect_ratio}, {resolution}, "
          f"{duration_seconds}s)... leva ~1-3 min.")
    operation = client.models.generate_videos(**kwargs)

    waited = 0
    while not operation.done:
        if waited >= timeout:
            raise TimeoutError(
                f"Veo não concluiu em {timeout}s. A operação pode ainda estar "
                f"rodando no servidor — tente de novo ou aumente o timeout.")
        time.sleep(poll_interval)
        waited += poll_interval
        operation = client.operations.get(operation)
        print(f"  ...{waited}s")

    if operation.error:
        raise RuntimeError(f"Veo retornou erro: {operation.error}")

    resp = operation.response
    vids = getattr(resp, "generated_videos", None) or []
    if not vids:
        reasons = getattr(resp, "rai_media_filtered_reasons", None)
        raise RuntimeError(
            "Veo não retornou vídeo — provável filtro de conteúdo. "
            f"Motivos: {reasons or 'não informado'}. Ajuste o prompt.")

    video = vids[0].video
    client.files.download(file=video)
    out = _next_output_path()
    video.save(out)
    print(f"Vídeo salvo: {out}")
    return out


def gen_video(prompt, **kwargs):
    """Atalho pra generate_video()."""
    return generate_video(prompt, **kwargs)


if __name__ == "__main__":
    print("Video Generation Module (Veo) carregado.")
    print("Use: generate_video(prompt, image=<caminho opcional>, "
          "aspect_ratio='9:16'|'16:9')")
