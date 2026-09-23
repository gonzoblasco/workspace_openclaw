"""Tests for scripts/migrate-entries.py y scripts/interpret-entries.py.

Cubre las dos etapas del refactor de fichas (2026-09-23):

  1. Desaplanar: una ficha es un DIA con varias unidades de nivel 2 adentro.
     Medido: 521 unidades en 51 fichas, hoy invisibles dentro de un texto.
  2. Interpretar: el LLM PROPONE campos, no los escribe. Nada llega a la DB sin
     verificacion, y las propuestas viven en su propia tabla.

La propiedad central es la misma que en ADR-059: los offsets reconstruyen el
texto, no lo copian.
"""
import importlib.util
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def me():
    return load("migrate_entries", "scripts/migrate-entries.py")


def ie():
    return load("interpret_entries", "scripts/interpret-entries.py")


# --- split_level2: la unidad que estaba aplanada ---

SAMPLE = """# 2026-08-25

## Fusion de skills de estudio (09:00 - 10:30)

Se fusionaron tres skills en una.

### Contexto

Tres skills solapadas.

## Configuracion OpenClaw VPS

Migracion a la nube.

### Problema

El modelo saltaba a uno caro.

## Self-reflection (guardar sesion)

Notas del cierre.
"""


def test_split_counts_level2_units():
    m = me()
    entries = m.split_level2(SAMPLE)
    assert len(entries) == 3
    # El parentesis que NO es un rango horario se conserva: aporta contexto
    # ("guardar sesion") y sacarlo perderia informacion.
    assert [e["title"] for e in entries] == [
        "Fusion de skills de estudio",
        "Configuracion OpenClaw VPS",
        "Self-reflection (guardar sesion)",
    ]


def test_split_separates_time_range():
    m = me()
    e = m.split_level2(SAMPLE)[0]
    assert e["time_start"] == "09:00" and e["time_end"] == "10:30"
    assert e["title"] == "Fusion de skills de estudio"


def test_kind_classifies_boilerplate():
    """'Self-reflection' es estructura del proceso, no un tema de trabajo."""
    m = me()
    entries = m.split_level2(SAMPLE)
    assert entries[0]["kind"] == "tema"
    assert entries[1]["kind"] == "tema"
    assert entries[2]["kind"] == "boilerplate"


def test_boilerplate_patterns():
    m = me()
    for t in ("Session End - workspace", "Cierre de sesion", "Conversation Summary"):
        assert m.BOILERPLATE.match(t), t


def test_kind_keeps_non_time_parenthetical():
    """Solo se saca el parentesis si es un rango horario."""
    m = me()
    e = m.split_level2("## Tema (con detalle)\n\ncuerpo\n")[0]
    assert e["title"] == "Tema (con detalle)"
    e2 = m.split_level2("## Tema (08:00 - 09:30)\n\ncuerpo\n")[0]
    assert e2["title"] == "Tema"
    assert e2["time_start"] == "08:00"


def test_offsets_reconstruct_entry():
    m = me()
    entries = m.split_level2(SAMPLE)
    body0 = SAMPLE[entries[0]["char_start"]:entries[0]["char_end"]]
    assert "Se fusionaron tres skills" in body0
    assert "Tres skills solapadas" in body0  # incluye las subsecciones ###
    body1 = SAMPLE[entries[1]["char_start"]:entries[1]["char_end"]]
    assert "Migracion a la nube" in body1
    assert "Fusion de skills" not in body1


def test_offsets_ordered_and_bounded():
    m = me()
    entries = m.split_level2(SAMPLE)
    for e in entries:
        assert 0 <= e["char_start"] <= e["char_end"] <= len(SAMPLE)
    for a, b in zip(entries, entries[1:]):
        assert a["char_end"] <= b["char_start"]


def test_offsets_survive_append():
    """Los offsets no se invalidan: el doc solo crece por append."""
    m = me()
    before = m.split_level2(SAMPLE)
    grown = SAMPLE + "\n## Unidad nueva\n\nContenido nuevo.\n"
    after = m.split_level2(grown)
    assert len(after) == len(before) + 1
    for i in range(len(before) - 1):
        assert before[i]["char_start"] == after[i]["char_start"]
        assert SAMPLE[before[i]["char_start"]:before[i]["char_end"]] == grown[
            after[i]["char_start"]:after[i]["char_end"]
        ]


def test_empty_text_gives_no_entries():
    m = me()
    assert m.split_level2("") == []
    assert m.split_level2("# solo un h1\n") == []


# --- la migracion sobre una DB ---

def make_db(tmp_path):
    db = tmp_path / "memory.db"
    conn = sqlite3.connect(db)
    conn.executescript(
        """
        CREATE TABLE daily_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL, type TEXT DEFAULT 'daily', content TEXT NOT NULL
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
    conn.execute("INSERT INTO daily_notes (id,date,content) VALUES (10,'2026-08-25','texto del daily')")
    conn.execute(
        "INSERT INTO sessions_relacional (id,date,title,content_bare,created_at) VALUES (10,'2026-08-25','2026-08-25',?, 'x')",
        (SAMPLE,),
    )
    # una ficha sin correspondencia en daily_notes
    conn.execute(
        "INSERT INTO sessions_relacional (id,date,title,content_bare,created_at) VALUES (99,'2026-01-01','sola',?, 'x')",
        ("# 2026-01-01\n\n## Algo\n\ncuerpo\n",),
    )
    conn.commit()
    conn.close()
    return db


def migrate_copy(tmp_path):
    db = make_db(tmp_path)
    mod = me()
    mod.DB = db
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, dry_run=False)
    return mod, conn


def test_migration_creates_entries(tmp_path):
    _, conn = migrate_copy(tmp_path)
    n = conn.execute("SELECT count(*) FROM session_entries WHERE session_id=10").fetchone()[0]
    conn.close()
    assert n == 3


def test_migration_adds_columns(tmp_path):
    _, conn = migrate_copy(tmp_path)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(sessions_relacional)")]
    conn.close()
    assert "project" in cols and "daily_id" in cols


def test_daily_id_links_when_date_matches(tmp_path):
    _, conn = migrate_copy(tmp_path)
    r = conn.execute("SELECT daily_id FROM sessions_relacional WHERE id=10").fetchone()
    conn.close()
    assert r[0] == "10"


def test_daily_id_null_when_no_match(tmp_path):
    """Sin correspondencia verificable, NULL. No se inventa el vinculo."""
    _, conn = migrate_copy(tmp_path)
    r = conn.execute("SELECT daily_id FROM sessions_relacional WHERE id=99").fetchone()
    conn.close()
    assert r[0] is None


def test_entries_kinds_stored(tmp_path):
    _, conn = migrate_copy(tmp_path)
    r = conn.execute(
        "SELECT kind, count(*) FROM session_entries WHERE session_id=10 GROUP BY kind"
    ).fetchall()
    conn.close()
    assert dict(r) == {"tema": 2, "boilerplate": 1}


def test_entries_offsets_resolve(tmp_path):
    _, conn = migrate_copy(tmp_path)
    row = conn.execute(
        "SELECT char_start, char_end FROM session_entries WHERE session_id=10 AND ordinal=0"
    ).fetchone()
    cb = conn.execute("SELECT content_bare FROM sessions_relacional WHERE id=10").fetchone()[0]
    conn.close()
    assert "Se fusionaron tres skills" in cb[row[0]:row[1]]


def test_migration_does_not_touch_content(tmp_path):
    db = make_db(tmp_path)
    before = sqlite3.connect(db).execute(
        "SELECT id, content_bare FROM sessions_relacional ORDER BY id"
    ).fetchall()
    mod = me()
    mod.DB = db
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, dry_run=False)
    after = conn.execute("SELECT id, content_bare FROM sessions_relacional ORDER BY id").fetchall()
    conn.close()
    assert before == after


def test_migration_idempotent(tmp_path):
    db = make_db(tmp_path)
    mod = me()
    mod.DB = db
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, dry_run=False)
    n1 = conn.execute("SELECT count(*) FROM session_entries").fetchone()[0]
    mod.migrate(conn, dry_run=False)
    n2 = conn.execute("SELECT count(*) FROM session_entries").fetchone()[0]
    conn.close()
    assert n1 == n2


# --- interpretacion: el modelo propone, la validacion decide ---

def test_parse_json_extracts_object():
    m = ie()
    assert m.parse_json('```json\n{"project":"kanam-os"}\n```') == {"project": "kanam-os"}
    assert m.parse_json('bla {"a":1} bla') == {"a": 1}


def test_parse_json_rejects_garbage():
    m = ie()
    assert m.parse_json("no hay json") is None
    assert m.parse_json("") is None
    assert m.parse_json(None) is None
    assert m.parse_json("[1,2,3]") is None  # no es objeto


def test_validate_rejects_invented_project():
    """El proyecto debe existir en disco. 'ninguno' y basura se descartan."""
    m = ie()
    projects = ["kanam-os", "soporteml"]
    ok = m.validate(None, 1, {"project": "proyecto-inventado"}, projects)
    assert "project" not in ok
    ok = m.validate(None, 1, {"project": "ninguno"}, projects)
    assert "project" not in ok
    ok = m.validate(None, 1, {"project": "soporteml"}, projects)
    assert ok["project"] == "soporteml"


def test_validate_project_is_case_insensitive():
    m = ie()
    ok = m.validate(None, 1, {"project": "KANAM-OS"}, ["kanam-os"])
    assert ok["project"] == "kanam-os"


def test_validate_rejects_bad_kind():
    m = ie()
    assert "activity" not in m.validate(None, 1, {"kind": "inventado"}, [])
    assert m.validate(None, 1, {"kind": "estudio"}, [])["activity"] == "estudio"


def test_validate_rejects_too_short():
    """Un topic o summary demasiado cortos no aportan."""
    m = ie()
    assert "topic" not in m.validate(None, 1, {"topic": "ab"}, [])
    assert "summary" not in m.validate(None, 1, {"summary": "corto"}, [])


def test_validate_truncates_long_values():
    """Un valor largo se trunca, no se descarta: el contenido sirve igual."""
    m = ie()
    ok = m.validate(None, 1, {"summary": "x" * 500}, [])
    assert len(ok["summary"]) == 300
    ok = m.validate(None, 1, {"topic": "y" * 200}, [])
    assert len(ok["topic"]) == 80


def test_validate_empty_response_gives_nothing():
    m = ie()
    assert m.validate(None, 1, {}, []) == {}


def test_real_projects_reads_disk():
    m = ie()
    projects = m.real_projects()
    assert isinstance(projects, list)
    # En el workspace real hay proyectos; en un tmp vacio no. Solo se verifica
    # que no explota y que devuelve nombres, no rutas.
    for p in projects:
        assert "/" not in p


# --- la tabla de propuestas es separada de las columnas de la ficha ---

def test_proposals_live_in_their_own_table(tmp_path):
    """Una propuesta erronea no debe contaminar la ficha."""
    m = ie()
    db = make_db(tmp_path)
    mod = me()
    mod.DB = db
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, dry_run=False)
    conn.executescript(m.SCHEMA)
    conn.commit()
    eid = conn.execute("SELECT id FROM session_entries LIMIT 1").fetchone()[0]
    conn.execute(
        "INSERT INTO proposed_fields (entry_id, field, value, status) VALUES (?,?,?, 'pending')",
        (eid, "topic", "algo propuesto"),
    )
    conn.commit()
    # la ficha sigue sin columnas de campo semantico
    cols = [r[1] for r in conn.execute("PRAGMA table_info(sessions_relacional)")]
    props = conn.execute("SELECT count(*) FROM proposed_fields WHERE status='pending'").fetchone()[0]
    conn.close()
    assert props == 1
    assert "topic" not in cols


# --- aplicar: el ciclo revisar -> aprobar -> escribir ---

def test_central_project_in_title_accepted():
    """El proyecto es central si esta en el TITULO."""
    m = ie()
    assert m.is_central("texto sin el proyecto", "Sesion: soporteml-v4 - tags", "soporteml")


def test_central_project_repeated_accepted():
    """O si aparece 2+ veces en el cuerpo."""
    m = ie()
    body = "arreglamos soporteml y despues soporteml otra vez"
    assert m.is_central(body, "Sin mencion", "soporteml")


def test_incidental_mention_rejected():
    """El falso positivo real: 1 mencion de paso en un cuerpo ajeno.

    'libros OpenClaw + sync workspace + post LinkedIn' recibio project=soporteml
    porque decia una vez 'seccion SoporteML del remote' al resolver un conflicto.
    """
    m = ie()
    body = "resolviendo el conflicto preservando la seccion SoporteML del remote"
    assert not m.is_central(body, "Sesion: libros OpenClaw para el puesto", "soporteml")


def test_validate_needs_title_and_body_for_project():
    """Sin titulo/cuerpo no se puede evaluar centralidad, asi que se confia en la lista."""
    m = ie()
    ok = m.validate(None, 1, {"project": "soporteml"}, ["soporteml"])
    assert ok["project"] == "soporteml"


def test_validate_rejects_incidental_project():
    m = ie()
    body = "una mencion suelta de kanam-os aca"
    ok = m.validate(None, 1, {"project": "kanam-os"}, ["kanam-os"], title="Otra cosa", body=body)
    assert "project" not in ok


def make_conn(tmp_path):
    db = make_db(tmp_path)
    mod = me()
    mod.DB = db
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, dry_run=False)
    conn.executescript(ie().SCHEMA)
    conn.commit()
    return conn


def make_conn_fresh(tmp_path):
    """Igual, pero sin correr migrate: para probar do_apply con FK activas."""
    db = make_db(tmp_path)
    mod = me()
    mod.DB = db
    conn = sqlite3.connect(db)
    conn.executescript(mod.SCHEMA)
    conn.commit()
    mod.migrate(conn, dry_run=False)
    conn.executescript(ie().SCHEMA)
    conn.commit()
    return conn


def test_apply_only_touches_approved(tmp_path):
    """Una propuesta PENDIENTE no se aplica. Solo las aprobadas."""
    m = ie()
    conn = make_conn(tmp_path)
    eid = conn.execute("SELECT id FROM session_entries WHERE session_id=10 LIMIT 1").fetchone()[0]
    conn.execute(
        "INSERT INTO proposed_fields (entry_id, field, value, status) VALUES (?,?,?, 'pending')",
        (eid, "topic", "pendiente sin aprobar"),
    )
    conn.commit()
    n = m.do_apply(conn, None)
    val = conn.execute("SELECT topic FROM session_entries WHERE id=?", (eid,)).fetchone()[0]
    conn.close()
    assert n == 0
    assert val is None


def test_apply_writes_entry_fields(tmp_path):
    m = ie()
    conn = make_conn(tmp_path)
    eid = conn.execute("SELECT id FROM session_entries WHERE session_id=10 LIMIT 1").fetchone()[0]
    conn.execute(
        """INSERT INTO proposed_fields (entry_id, field, value, status)
           VALUES (?,?,?, 'approved')""",
        (eid, "topic", "un topic aprobado"),
    )
    conn.commit()
    m.do_apply(conn, None)
    val = conn.execute("SELECT topic FROM session_entries WHERE id=?", (eid,)).fetchone()[0]
    conn.close()
    assert val == "un topic aprobado"


def test_apply_writes_project_to_ficha(tmp_path):
    m = ie()
    conn = make_conn(tmp_path)
    eid = conn.execute("SELECT id FROM session_entries WHERE session_id=10 LIMIT 1").fetchone()[0]
    conn.execute(
        "INSERT INTO proposed_fields (entry_id, field, value, status) VALUES (?,?,?, 'approved')",
        (eid, "project", "kanam-os"),
    )
    conn.commit()
    m.do_apply(conn, None)
    val = conn.execute("SELECT project FROM sessions_relacional WHERE id=10").fetchone()[0]
    conn.close()
    assert val == "kanam-os"


def test_apply_marks_as_applied(tmp_path):
    """Una vez aplicada, la propuesta deja de estar aprobada: ya es dato."""
    m = ie()
    conn = make_conn(tmp_path)
    eid = conn.execute("SELECT id FROM session_entries WHERE session_id=10 LIMIT 1").fetchone()[0]
    conn.execute(
        "INSERT INTO proposed_fields (entry_id, field, value, status) VALUES (?,?,?, 'approved')",
        (eid, "topic", "x" * 12),
    )
    conn.commit()
    m.do_apply(conn, None)
    st = conn.execute("SELECT status FROM proposed_fields WHERE entry_id=?", (eid,)).fetchone()[0]
    conn.close()
    assert st == "applied"


def test_apply_is_idempotent(tmp_path):
    m = ie()
    conn = make_conn(tmp_path)
    eid = conn.execute("SELECT id FROM session_entries WHERE session_id=10 LIMIT 1").fetchone()[0]
    conn.execute(
        "INSERT INTO proposed_fields (entry_id, field, value, status) VALUES (?,?,?, 'approved')",
        (eid, "topic", "un topic"),
    )
    conn.commit()
    m.do_apply(conn, None)
    n2 = m.do_apply(conn, None)  # segunda vez: ya no hay aprobadas
    conn.close()
    assert n2 == 0


def test_apply_dry_run_changes_nothing(tmp_path):
    m = ie()
    conn = make_conn(tmp_path)
    eid = conn.execute("SELECT id FROM session_entries WHERE session_id=10 LIMIT 1").fetchone()[0]
    conn.execute(
        "INSERT INTO proposed_fields (entry_id, field, value, status) VALUES (?,?,?, 'approved')",
        (eid, "topic", "no deberia escribirse"),
    )
    conn.commit()
    m.do_apply(conn, None, dry_run=True)
    val = conn.execute("SELECT topic FROM session_entries WHERE id=?", (eid,)).fetchone()[0]
    st = conn.execute("SELECT status FROM proposed_fields WHERE entry_id=?", (eid,)).fetchone()[0]
    conn.close()
    assert val is None
    assert st == "approved"


def test_set_status_approve_and_reject(tmp_path):
    m = ie()
    conn = make_conn(tmp_path)
    rows = conn.execute("SELECT id FROM session_entries WHERE session_id=10").fetchall()
    for i, (eid,) in enumerate(rows):
        conn.execute(
            "INSERT INTO proposed_fields (entry_id, field, value) VALUES (?,?,?)",
            (eid, "topic", f"t{i}" * 3),
        )
    conn.commit()
    m.set_status(conn, 10, "approved")
    n = conn.execute("SELECT count(*) FROM proposed_fields WHERE status='approved'").fetchone()[0]
    conn.close()
    assert n == len(rows)


def test_project_is_per_ficha_not_per_entry(tmp_path):
    """Si dos unidades del mismo dia proponen proyectos distintos, se toma uno."""
    m = ie()
    conn = make_conn(tmp_path)
    rows = conn.execute(
        "SELECT id FROM session_entries WHERE session_id=10 ORDER BY ordinal LIMIT 2"
    ).fetchall()
    for eid, val in zip(rows, ("kanam-os", "soporteml")):
        conn.execute(
            "INSERT INTO proposed_fields (entry_id, field, value, status) VALUES (?,?,?, 'approved')",
            (eid[0], "project", val),
        )
    conn.commit()
    m.do_apply(conn, None)
    val = conn.execute("SELECT project FROM sessions_relacional WHERE id=10").fetchone()[0]
    conn.close()
    assert val == "kanam-os"


# --- los dos ejes NO se mezclan ---

def test_activity_does_not_overwrite_kind():
    """El bug real: 'kind' mezclaba el eje determinista y el interpretado.

    Las 8 unidades interpretadas pisaron su clasificacion determinista (408
    'tema' pasaron a 400). Mismo defecto que `contributions.tier`, que mezcla
    numero con categoria.
    """
    m = ie()
    ok = m.validate(None, 1, {"kind": "trabajo"}, [])
    # Se guarda como `activity`, nunca como `kind`.
    assert "activity" in ok and ok["activity"] == "trabajo"
    assert "kind" not in ok


def test_entry_columns_map_to_distinct_columns():
    """kind no debe aparecer como destino: es el eje determinista."""
    m = ie()
    assert "kind" not in m.ENTRY_COLUMNS.values()
    assert m.ENTRY_COLUMNS["activity"] == "activity"


def test_kind_and_activity_coexist(tmp_path):
    """Las dos columnas existen y son independientes."""
    conn = make_conn(tmp_path)
    cols = {r[1] for r in conn.execute("PRAGMA table_info(session_entries)")}
    conn.close()
    assert "kind" in cols and "activity" in cols


def test_deterministic_kind_survives_activity_apply(tmp_path):
    """Aplicar una actividad no debe tocar el kind de la fila."""
    m = ie()
    conn = make_conn(tmp_path)
    eid, kind0 = conn.execute(
        "SELECT id, kind FROM session_entries WHERE session_id=10 LIMIT 1"
    ).fetchone()
    conn.execute(
        "INSERT INTO proposed_fields (entry_id, field, value, status) VALUES (?,?,?, 'approved')",
        (eid, "activity", "estudio"),
    )
    conn.commit()
    m.do_apply(conn, None)
    kind1, act = conn.execute(
        "SELECT kind, activity FROM session_entries WHERE id=?", (eid,)
    ).fetchone()
    conn.close()
    assert kind1 == kind0, "el eje determinista se perdio"
    assert act == "estudio"
