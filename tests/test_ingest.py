import pathlib
import sqlite3

from src.agent.ingest import ingest_file
from src.agent.db import get_chunks, init_db


def test_ingest_demo(tmp_path: pathlib.Path):
    # Create a temporary DB file
    db_file = tmp_path / "test.db"
    # Ingest each demo document
    demo_dir = pathlib.Path(__file__).parents[1] / "data" / "demo"
    for doc in demo_dir.iterdir():
        ingest_file(doc, db_file)

    # Verify that documents and chunks were stored
    conn = init_db(db_file)
    # There should be 3 documents
    docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    assert docs == 3
    # At least one chunk per document
    total_chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    assert total_chunks >= 3

    # Verify FTS works – search for a known term from contract1
    rows = get_chunks(conn, "Desarrollo")
    assert any("Desarrollo" in r[1] for r in rows)

    # Verify vector column stored (as JSON string from mock)
    vec = conn.execute("SELECT embedding FROM chunks LIMIT 1").fetchone()[0]
    # Simple check that it's JSON parsable
    import json
    parsed = json.loads(vec)
    assert isinstance(parsed, list) and len(parsed) == 3

    conn.close()

