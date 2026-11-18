import shutil
import sqlite3
from pathlib import Path

import pytest

from memori.oral.transcribe import transcribe_to_db
from memori.oral.db import get_segmentos


@pytest.mark.skipif(
    not shutil.which("whisper-cli"), reason="whisper-cli not installed"
)
def test_demo_transcription(tmp_path: Path) -> None:
    """Run the real whisper transcription on the demo audio.

    The test creates a temporary SQLite db, runs ``transcribe_to_db`` against
    the bundled demo WAV and asserts that at least one segment was stored with
    non‑empty text and that the end timestamp is greater than the start.
    """
    audio = Path(__file__).parents[2] / "data" / "demo" / "entrevista-demo.wav"
    model = Path(__file__).parents[2] / "models" / "ggml-large-v3-turbo-q5_0.bin"
    db_file = tmp_path / "test.db"

    transcribe_to_db(
        audio_path=audio,
        db_path=db_file,
        model_path=model,
        titulo="Demo transcripción",
        persona="Demo Persona",
    )

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    # Retrieve the interview id (the first one inserted)
    cur = conn.cursor()
    cur.execute("SELECT id FROM entrevistas LIMIT 1")
    entrevista_id = cur.fetchone()["id"]
    segmentos = get_segmentos(conn, entrevista_id)
    conn.close()

    assert segmentos, "No segments were inserted"
    first = segmentos[0]
    assert first["texto"].strip(), "Segment text is empty"
    assert first["fin_ms"] > first["inicio_ms"], "fin_ms must be greater than inicio_ms"

