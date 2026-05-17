"""
Gemini Image Generation Module
Pre-built module for Claude Code to call - handles session management,
multi-turn conversations, and output saving.
"""
import os
import json
import base64
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types

# Configuration — env-overridable. No Cowork desktop o filesystem da pasta
# de trabalho (mount Windows→Linux) pode ser hostil: trunca leitura, barra
# criação de arquivo em subdir e barra unlink. Use IMAGE_GEN_OUTPUT_DIR /
# IMAGE_GEN_SESSION_FILE para apontar pra área nativa do sandbox.
SESSION_FILE = os.environ.get("IMAGE_GEN_SESSION_FILE", ".image_session.json")
OUTPUT_DIR = os.environ.get("IMAGE_GEN_OUTPUT_DIR", "outputs")
DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_ASPECT_RATIO = "1:1"
DEFAULT_RESOLUTION = "1K"


def _get_client():
    """Initialize Gemini client. Valida a chave antes de chamar a API —
    no Cowork desktop o mount trunca a leitura do .env e a chave chega
    cortada (~20 chars), gerando um API_KEY_INVALID críptico. Falhamos
    rápido com mensagem acionável."""
    api_key = (os.environ.get('GEMINI_API_KEY') or '').strip()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY ausente. Passe a chave inline no comando: "
            "GEMINI_API_KEY=<chave> python3 ... (não dependa de .env na "
            "pasta de trabalho montada — o Cowork desktop trunca a leitura).")
    if len(api_key) < 30 or not api_key.startswith("AIza"):
        raise ValueError(
            f"GEMINI_API_KEY parece truncada/inválida (len={len(api_key)}, "
            f"esperado ~39 e começar com 'AIza'). Causa provável: o mount da "
            f"pasta de trabalho no Cowork desktop trunca a leitura do .env. "
            f"Workaround: passe a chave inline — GEMINI_API_KEY=<chave completa> "
            f"python3 -c \"...\" — em vez de gravá-la num .env na pasta montada.")
    return genai.Client(api_key=api_key)


def _ensure_output_dir():
    """Garante um diretório de saída GRAVÁVEL. Se OUTPUT_DIR não aceitar
    escrita (mount hostil do Cowork), cai pra área nativa do sandbox e
    avisa onde os arquivos realmente foram parar."""
    global OUTPUT_DIR
    try:
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        probe = Path(OUTPUT_DIR) / ".write_probe"
        probe.write_bytes(b"ok")
        probe.unlink()
        return OUTPUT_DIR
    except (OSError, PermissionError):
        import tempfile
        fallback = os.path.join(tempfile.gettempdir(), "image-gen-outputs")
        Path(fallback).mkdir(parents=True, exist_ok=True)
        print(f"[image_gen] AVISO: '{OUTPUT_DIR}' não é gravável (mount "
              f"hostil do Cowork?). Usando fallback nativo: {fallback}. "
              f"Copie os arquivos pra pasta de trabalho com 'cp' depois.")
        OUTPUT_DIR = fallback
        return OUTPUT_DIR


def _load_session():
    """Load existing session or return empty session"""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"history": [], "outputs": [], "turn": 0}
    return {"history": [], "outputs": [], "turn": 0}


def _reconstruct_history(raw_history):
    """
    Convert raw history dicts back to types.Content objects.
    This is needed to preserve thought signatures for multi-turn.
    """
    reconstructed = []
    for item in raw_history:
        parts = []
        for part_data in item.get("parts", []):
            if "text" in part_data:
                # Text part
                part_kwargs = {"text": part_data["text"]}
                if "thought_signature" in part_data:
                    part_kwargs["thought_signature"] = base64.b64decode(part_data["thought_signature"])
                parts.append(types.Part(**part_kwargs))
            elif "inline_data" in part_data:
                # Image part
                blob = types.Blob(
                    mime_type=part_data["inline_data"]["mime_type"],
                    data=base64.b64decode(part_data["inline_data"]["data"])
                )
                part_kwargs = {"inline_data": blob}
                if "thought_signature" in part_data:
                    part_kwargs["thought_signature"] = base64.b64decode(part_data["thought_signature"])
                parts.append(types.Part(**part_kwargs))

        reconstructed.append(types.Content(
            role=item.get("role"),
            parts=parts
        ))
    return reconstructed


def _save_session(session):
    """Save session to file. Mount hostil do Cowork pode barrar a escrita —
    degrada com aviso em vez de derrubar uma geração bem-sucedida."""
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(session, f)
    except (OSError, PermissionError) as e:
        print(f"[image_gen] AVISO: não consegui salvar a sessão "
              f"({SESSION_FILE}: {e}). Geração ok; histórico multi-turn "
              f"pode não persistir. Defina IMAGE_GEN_SESSION_FILE para um "
              f"caminho gravável (área nativa do sandbox).")


def _get_next_output_path(session):
    """Generate next output filename"""
    _ensure_output_dir()
    turn = session.get("turn", 0) + 1
    timestamp = datetime.now().strftime("%H%M%S")
    return f"{OUTPUT_DIR}/output_{turn:03d}_{timestamp}.png"


def new_session():
    """Clear the current session and start fresh. Mount hostil do Cowork
    barra unlink (PermissionError) — nesse caso sobrescreve com sessão
    vazia em vez de deletar."""
    empty = {"history": [], "outputs": [], "turn": 0}
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except (PermissionError, OSError):
            try:
                with open(SESSION_FILE, 'w') as f:
                    json.dump(empty, f)
            except (PermissionError, OSError) as e:
                print(f"[image_gen] AVISO: não consegui limpar a sessão "
                      f"({e}). Use IMAGE_GEN_SESSION_FILE num caminho gravável.")
    print("Session cleared. Ready for new image generation.")
    return empty


def session_info():
    """Display current session status"""
    session = _load_session()
    turn_count = session.get("turn", 0)
    outputs = session.get("outputs", [])

    if turn_count == 0:
        print("No active session. Start generating to create one.")
        return None

    print(f"Current session: {turn_count} turn(s)")
    print(f"Outputs generated:")
    for i, output in enumerate(outputs, 1):
        print(f"  {i}. {output}")

    return session


def revert(turns: int = 1):
    """
    Undo the last N turns from the current session.

    Args:
        turns: Number of turns to revert (default: 1)

    Returns:
        The updated session, or None if nothing to revert
    """
    session = _load_session()
    turn_count = session.get("turn", 0)

    if turn_count == 0:
        print("No active session to revert.")
        return None

    if turns > turn_count:
        print(f"Can only revert {turn_count} turn(s). Reverting all.")
        turns = turn_count

    # Each turn = 2 history items (user message + model response)
    items_to_remove = turns * 2
    session["history"] = session["history"][:-items_to_remove]

    # Remove outputs
    session["outputs"] = session["outputs"][:-turns]

    # Update turn count
    session["turn"] = turn_count - turns

    _save_session(session)

    if session["turn"] == 0:
        print(f"Reverted {turns} turn(s). Session is now empty.")
    else:
        print(f"Reverted {turns} turn(s). Now at turn {session['turn']}.")
        print(f"Last output: {session['outputs'][-1] if session['outputs'] else 'None'}")

    return session


def generate(
    prompt: str,
    reference_images: list = None,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    model: str = DEFAULT_MODEL
) -> str:
    """
    Generate or refine an image. Automatically continues existing session.

    Args:
        prompt: Text description of what to generate/change
        reference_images: Optional list of image paths to use as references
        aspect_ratio: "1:1", "3:4", "16:9", etc.
        resolution: "1K", "2K", or "4K"
        model: "gemini-2.5-flash-image" or "gemini-3-pro-image-preview"

    Returns:
        Path to the generated image
    """
    client = _get_client()
    session = _load_session()

    # Build the content for this turn
    content_parts = [prompt]

    # Add reference images if provided
    if reference_images:
        from PIL import Image
        for img_path in reference_images:
            if os.path.exists(img_path):
                content_parts.append(Image.open(img_path))
            else:
                print(f"Warning: Reference image not found: {img_path}")

    # Build config
    config = types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspectRatio=aspect_ratio
        )
    )

    # Check if we're continuing an existing session
    if session["history"]:
        # Continuing multi-turn: use chat
        print(f"Continuing session (turn {session['turn'] + 1})...")

        # Reconstruct history with proper types (including thought signatures)
        reconstructed_history = _reconstruct_history(session["history"])

        # Reconstruct chat from history
        chat = client.chats.create(
            model=model,
            config=config,
            history=reconstructed_history
        )

        response = chat.send_message(content_parts)

        # Update history with new exchange
        session["history"].append({"role": "user", "parts": [{"text": prompt}]})

    else:
        # New session: create fresh chat
        print("Starting new session...")

        chat = client.chats.create(
            model=model,
            config=config
        )

        response = chat.send_message(content_parts)

        # Start history
        session["history"].append({"role": "user", "parts": [{"text": prompt}]})

    # Process response
    output_path = None
    response_parts = []

    for part in response.parts:
        if part.text is not None:
            print(f"Model: {part.text}")
            part_data = {"text": part.text}
            # Preserve thought signature if present
            if hasattr(part, 'thought_signature') and part.thought_signature:
                part_data["thought_signature"] = base64.b64encode(part.thought_signature).decode('utf-8')
            response_parts.append(part_data)
        elif part.inline_data is not None:
            # Save the image
            output_path = _get_next_output_path(session)
            image = part.as_image()
            image.save(output_path)
            print(f"Saved: {output_path}")

            # Store image data in history for continuation
            # Note: This makes the session file large but preserves full context
            part_data = {
                "inline_data": {
                    "mime_type": part.inline_data.mime_type,
                    "data": base64.b64encode(part.inline_data.data).decode('utf-8')
                }
            }
            # Preserve thought signature if present (critical for multi-turn with Gemini 3 Pro)
            if hasattr(part, 'thought_signature') and part.thought_signature:
                part_data["thought_signature"] = base64.b64encode(part.thought_signature).decode('utf-8')
            response_parts.append(part_data)

    # Update session
    session["history"].append({"role": "model", "parts": response_parts})
    session["turn"] = session.get("turn", 0) + 1
    if output_path:
        session["outputs"].append(output_path)

    _save_session(session)

    return output_path


# Convenience aliases
def gen(prompt, **kwargs):
    """Shorthand for generate()"""
    return generate(prompt, **kwargs)


if __name__ == "__main__":
    # Quick test
    print("Image Generation Module loaded.")
    print("Use: generate(prompt), new_session(), session_info(), revert()")
    print("")
    print("Functions:")
    print("  generate(prompt)     - Generate/refine an image")
    print("  new_session()        - Clear session, start fresh")
    print("  session_info()       - Show current session status")
    print("  revert(turns=1)      - Undo last N turns")
