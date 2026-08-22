"""
Audio Upload Security Module
-----------------------------
 validate uploaded audio files so only real, safe audio
gets through to the deepfake detection model — and nothing crashes the app.

Usage in your main Streamlit app:

    from audio_upload_security import validate_audio_upload
    import streamlit as st

    uploaded_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "ogg"])

    if uploaded_file is not None:
        is_valid, message, safe_path = validate_audio_upload(uploaded_file)
        if is_valid:
            st.success(message)
            # pass safe_path to Riddhi's DB layer / the AI model
        else:
            st.error(message)
"""

import os
import uuid
import wave
import contextlib

try:
    import magic  # python-magic — reads real file signature, not just extension
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False

# ---- CONFIG: matches app.py's st.file_uploader(type=["wav","mp3","flac","mpeg"]) ----
ALLOWED_EXTENSIONS = {"mp3", "wav", "flac", "mpeg", "mpga"}
ALLOWED_MIME_TYPES = {
    "audio/mpeg",       # mp3 AND mpeg audio (WhatsApp voice notes often use this)
    "audio/wav",
    "audio/x-wav",
    "audio/vnd.wave",
    "audio/flac",
    "audio/x-flac",
}
MAX_FILE_SIZE_MB = 25
UPLOAD_DIR = "safe_uploads"  # where sanitized files get saved


def _get_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def _check_extension(filename: str) -> tuple[bool, str]:
    ext = _get_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"File type '.{ext}' is not allowed. Use: {', '.join(ALLOWED_EXTENSIONS)}"
    return True, ""


def _check_size(uploaded_file) -> tuple[bool, str]:
    # uploaded_file.size is available directly on Streamlit's UploadedFile
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File is {size_mb:.1f} MB, which exceeds the {MAX_FILE_SIZE_MB} MB limit."
    if uploaded_file.size == 0:
        return False, "File is empty."
    return True, ""


def _check_magic_bytes(file_bytes: bytes) -> tuple[bool, str]:
    """Confirm the file's actual content is audio, not a renamed file of another type."""
    if not HAS_MAGIC:
        # Fallback: skip silently if libmagic isn't available in the environment,
        # but log so the team knows this check is degraded.
        return True, "(magic-byte check skipped — python-magic not installed)"

    detected_type = magic.from_buffer(file_bytes, mime=True)
    if detected_type not in ALLOWED_MIME_TYPES:
        return False, f"File content looks like '{detected_type}', not a supported audio format."
    return True, ""


def _sanitize_and_save(uploaded_file, file_bytes: bytes) -> str:
    """Generate a safe random filename and save to a controlled directory."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = _get_extension(uploaded_file.name)
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    safe_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(safe_path, "wb") as f:
        f.write(file_bytes)

    return safe_path


def _sanity_check_wav(path: str) -> tuple[bool, str]:
    """
    Extra check for WAV files: confirm it actually opens and has a real duration.
    (For mp3/m4a/ogg, a deeper check would use a library like pydub/librosa —
    ask Yash/the AI teammate if they want that check done in their pipeline instead,
    since it requires ffmpeg and heavier dependencies.)
    """
    if not path.lower().endswith(".wav"):
        return True, ""
    try:
        with contextlib.closing(wave.open(path, "rb")) as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate) if rate else 0
            if duration <= 0:
                return False, "WAV file has zero duration — likely corrupted."
    except wave.Error:
        return False, "WAV file is corrupted or not a valid WAV structure."
    except Exception as e:
        return False, f"Could not read WAV file: {e}"
    return True, ""


def validate_audio_upload(uploaded_file) -> tuple[bool, str, str | None]:
    """
    Main entry point. Runs all checks in order, fails fast, never raises.

    Returns:
        (is_valid, message, safe_path_or_None)
    """
    if uploaded_file is None:
        return False, "No file provided.", None

    try:
        # 1. Extension check
        ok, msg = _check_extension(uploaded_file.name)
        if not ok:
            return False, msg, None

        # 2. Size check
        ok, msg = _check_size(uploaded_file)
        if not ok:
            return False, msg, None

        # 3. Read bytes once, reuse everywhere (avoid re-reading stream issues)
        file_bytes = uploaded_file.getvalue()

        # 4. Magic byte / real content check
        ok, msg = _check_magic_bytes(file_bytes)
        if not ok:
            return False, msg, None

        # 5. Sanitize filename + save to controlled location
        safe_path = _sanitize_and_save(uploaded_file, file_bytes)

        # 6. Deeper sanity check (corrupted/empty audio)
        ok, msg = _sanity_check_wav(safe_path)
        if not ok:
            os.remove(safe_path)  # clean up bad file
            return False, msg, None

        return True, "File passed all security checks.", safe_path

    except Exception as e:
        # Catch-all: NEVER let a bad file crash the app.
        # Log this properly in production (e.g. logging.error(e))
        return False, f"Unexpected error while validating file: {e}", None