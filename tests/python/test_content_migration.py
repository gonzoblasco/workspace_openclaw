"""Tests for scripts/content-parse.py y scripts/migrate-content.py.

Todo el contenido de memory.db es markdown en un campo de texto. Estos tests
cubren las tres extracciones y, sobre todo, la propiedad que las hace seguras:
los offsets de `sections` reconstruyen el body desde el texto del padre, sin
copiarlo (copiarlo duplicaba el 95% del contenido; ver ADR-059).
"""
import importlib.util
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cp():
    return load("content_parse", "scripts/content-parse.py")


# --- doc_kind ---

def test_doc_kind_harness():
    m = cp()
    assert m.doc_kind("# Session: 2026-08-05 14:22\n\n- **Session Key**: x") == "harness"


def test_doc_kind_daily():
    m = cp()
    assert m.doc_kind("# 2026-08-27\n\n## Algo") == "daily"
    assert m.doc_kind("## Session End - workspace\n**End:** x") == "daily"


def test_doc_kind_handles_leading_whitespace():
    m = cp()
    assert m.doc_kind("\n\n# Session: x") == "harness"


def test_doc_kind_empty_is_daily():
    """Un doc vacio no debe clasificar como harness."""
    m = cp()
    assert m.doc_kind("") == "daily"
    assert m.doc_kind("\n\n") == "daily"


# --- harness_fields ---

def test_harness_fields_extracted():
    m = cp()
    text = (
        "# Session: 2026-08-05 14:22:37 GMT-3\n\n"
        "- **Session Key**: agent:main:dashboard:abc\n"
        "- **Session ID**: 0cfe3c3d-bccd\n"
        "- **Source**: webchat\n"
    )
    hf = m.harness_fields(text)
    assert hf["session_key"] == "agent:main:dashboard:abc"
    assert hf["session_id"] == "0cfe3c3d-bccd"
    assert hf["source"] == "webchat"


def test_harness_fields_only_for_harness():
    """Un daily narrativo no debe inventar campos del harness."""
    m = cp()
    hf = m.harness_fields("# 2026-08-27\n\n- **Session Key**: falso\n")
    assert hf == {"session_key": None, "session_id": None, "source": None}


def test_harness_fields_missing_are_none():
    m = cp()
    hf = m.harness_fields("# Session: x\n\nsin campos")
    assert hf["session_key"] is None and hf["source"] is None


# --- split_sections: offsets ---

SAMPLE = """# 2026-09-22

## Cambio de config (01:41 - 01:46)

Aplicado el cambio.

- [ ] Verificar
- [x] Backup

### Detalle

Texto de detalle.
"""


def test_split_sections_count_and_titles():
    m = cp()
    secs = m.split_sections(SAMPLE)
    assert [s["title"] for s in secs] == ["Cambio de config", "Detalle"]


def test_split_sections_separates_time_range():
    """El rango horario sale del titulo y va a columnas propias."""
    m = cp()
    s = m.split_sections(SAMPLE)[0]
    assert s["title"] == "Cambio de config"
    assert s["time_start"] == "01:41" and s["time_end"] == "01:46"


def test_offsets_reconstruct_body():
    """La propiedad central: content[char_start:char_end] es el body."""
    m = cp()
    secs = m.split_sections(SAMPLE)
    assert "Aplicado el cambio" in SAMPLE[secs[0]["char_start"]:secs[0]["char_end"]]
    assert "Texto de detalle" in SAMPLE[secs[1]["char_start"]:secs[1]["char_end"]]


def test_offsets_are_ordered_and_bounded():
    m = cp()
    secs = m.split_sections(SAMPLE)
    for s in secs:
        assert 0 <= s["char_start"] <= s["char_end"] <= len(SAMPLE)
    assert secs[0]["char_end"] <= secs[1]["char_start"]


def test_offsets_survive_append():
    """Un doc solo crece por append: los char_start no se mueven.

    Al agregar un heading al final, la seccion nueva se SUMA a la lista: los
    originales quedan en los mismos indices. El char_end de la ultima seccion
    original si avanza (absorbe lo agregado antes del heading nuevo), asi que
    solo se compara byte a byte el char_end de las no-finales.
    """
    m = cp()
    before = m.split_sections(SAMPLE)
    grown = SAMPLE + "\n## Seccion nueva\n\nContenido nuevo.\n"
    after = m.split_sections(grown)

    assert len(after) == len(before) + 1, "la seccion nueva no se detecto"
    n = len(before)

    # Todas las originales conservan su char_start y su indice.
    for i in range(n):
        assert before[i]["char_start"] == after[i]["char_start"], "un char_start se movio"
        assert before[i]["title"] == after[i]["title"]

    # Todas menos la ultima: el body es byte a byte identico.
    for i in range(n - 1):
        b, a = before[i], after[i]
        assert SAMPLE[b["char_start"]:b["char_end"]] == grown[a["char_start"]:a["char_end"]]

    # La ultima original conserva su inicio, y su body viejo sigue adentro
    # (el char_end avanzo para absorber el texto agregado).
    last_b, last_a = before[-1], after[n - 1]
    assert last_b["char_start"] == last_a["char_start"]
    assert SAMPLE[last_b["char_start"]:last_b["char_end"]] in grown[last_a["char_start"]:last_a["char_end"]]
    assert last_a["char_end"] > last_b["char_end"], "el char_end final deberia avanzar"


def test_no_body_key_in_sections():
    """Las secciones NO deben cargar el body: seria duplicar el texto."""
    m = cp()
    for s in m.split_sections(SAMPLE):
        assert "body" not in s, "el body copiado es exactamente lo que se evita"


def test_empty_text_gives_no_sections():
    m = cp()
    assert m.split_sections("") == []
    assert m.split_sections("# solo un titulo") == []


def test_preamble_without_heading_body():
    """Un h1 solo, sin cuerpo, no genera seccion."""
    m = cp()
    secs = m.split_sections("# 2026-09-22\n\n## Uno\n\nx")
    assert len(secs) == 1 and secs[0]["title"] == "Uno"


def test_preamble_with_body_is_kepth():
    m = cp()
    secs = m.split_sections("# 2026-09-22\n\nPreambulo real.\n\n## Uno\n\nx")
    assert len(secs) == 2
    assert secs[0]["level"] == 1 and secs[0]["title"] == ""


# --- extract_checklist ---

def test_extract_checklist():
    m = cp()
    items = m.extract_checklist(SAMPLE)
    assert len(items) == 2
    assert items[0]["done"] == 0 and items[0]["text"] == "Verificar"
    assert items[1]["done"] == 1 and items[1]["text"] == "Backup"


def test_checklist_keeps_section():
    m = cp()
    items = m.extract_checklist(SAMPLE)
    assert items[0]["section"] == "Cambio de config"


def test_uppercase_X_counts_as_done():
    m = cp()
    items = m.extract_checklist("## S\n- [X] hecho\n")
    assert items[0]["done"] == 1


def test_no_checklist_gives_empty():
    m = cp()
    assert m.extract_checklist("## S\n\ntexto sin items\n") == []


# --- migrate-content sobre una DB que reproduce el problema ---

def make_db(tmp_path):
    db = tmp_path / "memory.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        """
        CREATE TABLE daily_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL, type TEXT DEFAULT 'daily',
            content TEXT NOT NULL, source_file TEXT, created_at TEXT
        );
        CREATE TABLE sessions_relacional (
            id INTEGER PRIMARY KEY, date TEXT NOT NULL, title TEXT NOT NULL,
            tags TEXT, complexity_score INTEGER DEFAULT 0,
            model_used TEXT DEFAULT 'unknown', thinking_level TEXT DEFAULT 'high',
            summary TEXT, session_duration INTEGER DEFAULT 0,
            content_bare TEXT NOT NULL, created_at TEXT NOT NULL
        );
        """
    )
    harness = (
        "# Session: 2026-08-05 14:22:37 GMT-3\n\n"
        "- **Session Key**: agent:main:main\n"
        "- **Session ID**: abc-123\n"
        "- **Source**: webchat\n\n"
        "## Conversation Summary\n\nResumen corto.\n"
    )
    # el dump del harness mal marcado como 'daily' (el defecto del id 39/96-100)
    conn.execute("INSERT INTO daily_notes (id,date,type,content,created_at) VALUES (1,'2026-08-05','daily',?, 'x')", (harness,))
    narr = "# 2026-08-27\n\n## Cambio de config (01:41 - 01:46)\n\n- [ ] pendiente\n- [x] hecho\n"
    conn.execute("INSERT INTO daily_notes (id,date,type,content,created_at) VALUES (2,'2026-08-27','daily',?, 'x')", (narr,))
    conn.execute(
        "INSERT INTO sessions_relacional (id,date,title,content_bare,created_at) VALUES (1,'2026-08-05','t',?, 'x')",
        (narr,),
    )
    conn.commit()
    conn.close()
    return db


def migrate_copy(tmp_path):
    db = make_db(tmp_path)
    mod = load("migrate_content", "scripts/migrate-content.py")
    mod.DB = db
    m = cp()
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, m, dry_run=False)
    return mod, m, conn


def test_type_corrected_from_content(tmp_path):
    """Un dump del harness marcado 'daily' debe quedar como 'session'."""
    _, _, conn = migrate_copy(tmp_path)
    row = conn.execute("SELECT type, doc_kind FROM daily_notes WHERE id=1").fetchone()
    conn.close()
    assert row == ("session", "harness")


def test_type_stays_daily_for_narrative(tmp_path):
    _, _, conn = migrate_copy(tmp_path)
    row = conn.execute("SELECT type, doc_kind FROM daily_notes WHERE id=2").fetchone()
    conn.close()
    assert row == ("daily", "daily")


def test_harness_metadata_stored(tmp_path):
    _, _, conn = migrate_copy(tmp_path)
    r = conn.execute("SELECT session_key, session_id, source FROM daily_notes WHERE id=1").fetchone()
    conn.close()
    assert r == ("agent:main:main", "abc-123", "webchat")


def test_sections_created_for_both_tables(tmp_path):
    _, _, conn = migrate_copy(tmp_path)
    n_daily = conn.execute("SELECT count(*) FROM sections WHERE doc_type='daily'").fetchone()[0]
    n_sess = conn.execute("SELECT count(*) FROM sections WHERE doc_type='session'").fetchone()[0]
    conn.close()
    assert n_daily > 0 and n_sess > 0


def test_sections_have_no_body_column(tmp_path):
    """La tabla no debe tener columna body: el texto se referencia."""
    _, _, conn = migrate_copy(tmp_path)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(sections)")]
    conn.close()
    assert "body" not in cols
    assert "char_start" in cols and "char_end" in cols


def test_offsets_resolve_against_parent(tmp_path):
    _, _, conn = migrate_copy(tmp_path)
    row = conn.execute(
        "SELECT doc_id, char_start, char_end FROM sections WHERE doc_type='daily' ORDER BY ordinal LIMIT 1"
    ).fetchone()
    did, cs, ce = row
    content = conn.execute("SELECT content FROM daily_notes WHERE id=?", (did,)).fetchone()[0]
    conn.close()
    assert content[cs:ce].strip(), "el offset no reconstruye contenido"


def test_checklist_extracted_and_linked(tmp_path):
    _, _, conn = migrate_copy(tmp_path)
    rows = conn.execute(
        "SELECT text, done, section FROM checklist_items ORDER BY ordinal"
    ).fetchall()
    conn.close()
    assert ("pendiente", 0, "Cambio de config") in rows
    assert ("hecho", 1, "Cambio de config") in rows


def test_migration_does_not_touch_content(tmp_path):
    """La migracion es aditiva: el markdown original queda intacto."""
    db = make_db(tmp_path)
    before = sqlite3.connect(db).execute("SELECT id, content FROM daily_notes ORDER BY id").fetchall()
    mod = load("migrate_content", "scripts/migrate-content.py")
    mod.DB = db
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, mod_cp := cp(), dry_run=False)
    after = conn.execute("SELECT id, content FROM daily_notes ORDER BY id").fetchall()
    conn.close()
    assert before == after


def test_idempotent(tmp_path):
    """Correr dos veces no debe duplicar filas."""
    db = make_db(tmp_path)
    mod = load("migrate_content", "scripts/migrate-content.py")
    mod.DB = db
    m = cp()
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, m, dry_run=False)
    s1 = conn.execute("SELECT count(*) FROM sections").fetchone()[0]
    c1 = conn.execute("SELECT count(*) FROM checklist_items").fetchone()[0]
    mod.migrate(conn, m, dry_run=False)
    s2 = conn.execute("SELECT count(*) FROM sections").fetchone()[0]
    c2 = conn.execute("SELECT count(*) FROM checklist_items").fetchone()[0]
    conn.close()
    assert s1 == s2 and c1 == c2


def test_dry_run_changes_nothing(tmp_path):
    db = make_db(tmp_path)
    mod = load("migrate_content", "scripts/migrate-content.py")
    mod.DB = db
    conn = sqlite3.connect(db)
    cols_before = [r[1] for r in conn.execute("PRAGMA table_info(daily_notes)")]
    mod.migrate(conn, cp(), dry_run=True)
    cols_after = [r[1] for r in conn.execute("PRAGMA table_info(daily_notes)")]
    conn.close()
    assert cols_before == cols_after


# --- clean_title: titulos legibles ---

def test_clean_title_strips_html_comment():
    """El comentario de proyecto se veia crudo en la UI de la ficha."""
    m = cp()
    assert m.clean_title("Engram - adopcion <!-- project: github.com/x/y -->") == "Engram - adopcion"


def test_clean_title_strips_time_range():
    m = cp()
    assert m.clean_title("Sesion (08:00 - 10:35)") == "Sesion"


def test_clean_title_strips_both():
    m = cp()
    assert m.clean_title("Tema (09:00-10:00) <!-- project: a/b -->") == "Tema"


def test_clean_title_keeps_normal():
    m = cp()
    assert m.clean_title("Technical Debt") == "Technical Debt"


def test_clean_title_handles_multiline_comment():
    """Un comentario puede ocupar varias lineas."""
    m = cp()
    out = m.clean_title("Titulo <!-- project:\nowner/repo -->")
    assert out == "Titulo"


def test_sections_have_no_html_comment():
    """Ningun titulo extraido debe conservar el comentario."""
    m = cp()
    sample = "# Doc\n\n## Real <!-- project: a/b -->\n\ncuerpo\n"
    secs = m.split_sections(sample)
    for sec in secs:
        assert "<!--" not in sec["title"], f"comentario crudo en {sec['title']!r}"
