"""Tests for scripts/check-learnings-integrity.py.

El gate existe porque un DELETE mio borro 9 lecciones REALES de la tabla
`learnings` (2026-10-27): asumi que el cuerpo de la leccion vivia en la
columna `content`, cuando la tabla lo guarda en `title` (y en `tags` en otras
filas). El export a docs/learnings/*.md lee el cuerpo de `content`, asi que
esas lecciones se veian como seccion vacia.

Un chequeo que solo corre contra un arbol limpio NO esta probado. Cada test
SIEMBRA el defecto en una DB falsa en tmp_path, y el ultimo exige que el
check DISTINGA el caso limpio del sucio.

Lo que el gate tiene que distinguir (calibrado: separa PERDIDA de RUIDO):
  - PERDIDA (bloquea): el cuerpo de la leccion NO esta en `content`.
  - RUIDO (avisa): prosa en `tags`, titulo largo, cuerpo corto.

Un guard que reporta todo no se lee y no se respeta: la primera version
reportaba 169 filas y por eso fue calibrada.
"""
import importlib.util
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-learnings-integrity.py"

sys.path.insert(0, str(ROOT / "scripts"))


def load():
    spec = importlib.util.spec_from_file_location("check_learnings_integrity", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CUERPO = (
    "Un cuerpo de leccion con suficiente largo para superar el minimo de "
    "caracteres que el gate exige, para que el unico defecto sea donde vive."
)


def make_db(path, rows, junction_rows=()):
    """Crea una DB `learnings` minima con las filas dadas.

    Cada fila: (id, category, title, content, tags).
    `junction_rows`: pares (learning_id, tag) que se insertan en
    `learning_tags` + `tags`. Una fila sana tiene sus tags en la COLUMNA y en
    la JUNCTION: el export lee solo la junction, asi que tags en la columna
    sin junction es exactamente el defecto C4.
    """
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE learnings (
          id INTEGER PRIMARY KEY,
          category TEXT NOT NULL,
          title TEXT NOT NULL,
          content TEXT NOT NULL,
          tags TEXT,
          created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE tags (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE learning_tags (
          learning_id INTEGER NOT NULL,
          tag_id INTEGER NOT NULL,
          PRIMARY KEY (learning_id, tag_id)
        );
        """
    )
    for r in rows:
        conn.execute(
            "INSERT INTO learnings (id, category, title, content, tags) VALUES (?,?,?,?,?)",
            r,
        )
    for lid, tag in junction_rows:
        conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
        conn.execute(
            "INSERT OR IGNORE INTO learning_tags (learning_id, tag_id) "
            "SELECT ?, id FROM tags WHERE name = ?",
            (lid, tag),
        )
    conn.commit()
    conn.close()
    return path


def findings(mod, db_path):
    conn = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True)
    try:
        problemas, avisos = mod.collect(conn)
    finally:
        conn.close()
    return problemas, avisos


def codes(filas):
    out = set()
    for _lid, _cat, _title, found in filas:
        for code, _msg in found:
            out.add(code)
    return out


def test_tabla_sana_no_reporta_nada(tmp_path):
    """Una fila bien puesta (cuerpo en content, tags en la junction) no genera hallazgos."""
    mod = load()
    db = make_db(
        tmp_path / "ok.db",
        [(1, "debugging", "Un titulo corto y normal", CUERPO, "memoria,db")],
        junction_rows=[(1, "memoria"), (1, "db")],
    )
    problemas, avisos = findings(mod, db)
    assert problemas == [], "una fila sana no debe generar perdidas"
    assert avisos == [], "una fila sana no debe generar avisos"


def test_cuerpo_en_tags_bloquea(tmp_path):
    """C1: el cuerpo en la columna `tags` es perdida y tiene que bloquear."""
    mod = load()
    db = make_db(
        tmp_path / "c1.db",
        [(1, "debugging", "Titulo", "", CUERPO)],
    )
    problemas, _avisos = findings(mod, db)
    assert "C1_cuerpo_en_tags" in codes(problemas)


def test_cuerpo_en_title_bloquea(tmp_path):
    """C2: el cuerpo en la columna `title` es perdida y tiene que bloquear."""
    mod = load()
    db = make_db(
        tmp_path / "c2.db",
        [(1, "debugging", CUERPO, "", "")],
    )
    problemas, _avisos = findings(mod, db)
    assert "C2_cuerpo_en_title" in codes(problemas)


def test_tags_sin_junction_bloquea(tmp_path):
    """C4: tags reales en la columna pero sin junction = invisibles al export."""
    mod = load()
    db = make_db(
        tmp_path / "c4.db",
        [(1, "debugging", "Titulo", CUERPO, "memoria,db")],
    )
    problemas, _avisos = findings(mod, db)
    assert "C4_tags_invisibles" in codes(problemas)


def test_contenido_truncado_bloquea(tmp_path):
    """C5: el cuerpo cortado al tope del catalogo (500 chars) es perdida."""
    mod = load()
    db = make_db(
        tmp_path / "c5.db",
        [(1, "debugging", "Titulo", "x" * 500, "")],
    )
    problemas, _avisos = findings(mod, db)
    assert "C5_contenido_truncado" in codes(problemas)


def test_prosa_en_tags_solo_avisa(tmp_path):
    """C3: la prosa en `tags` (el fragmento del titulo) es ruido, no perdida."""
    mod = load()
    db = make_db(
        tmp_path / "c3.db",
        [(1, "debugging", "Titulo", CUERPO, "Un fragmento de prosa que no es un tag valido")],
    )
    problemas, avisos = findings(mod, db)
    assert problemas == [], "la prosa en tags no debe bloquear"
    assert "C3_prosa_en_tags" in codes(avisos)


def test_titulo_largo_solo_avisa(tmp_path):
    """Un titulo descriptivo y largo con cuerpo correcto es ruido, no perdida."""
    mod = load()
    db = make_db(
        tmp_path / "largo.db",
        [(1, "debugging", "Un titulo bastante largo " * 20, CUERPO, "")],
    )
    problemas, avisos = findings(mod, db)
    assert problemas == [], "un titulo largo con cuerpo correcto no debe bloquear"
    assert "C2_titulo_desproporcionado" in codes(avisos)


def test_el_gate_distingue_limpio_de_sucio(tmp_path):
    """El test final: la tabla sana y la tabla rota dan veredictos distintos."""
    mod = load()
    sana = make_db(tmp_path / "limpia.db", [(1, "debugging", "Titulo", CUERPO, "")])
    rota = make_db(tmp_path / "rota.db", [(1, "debugging", "Titulo", "", CUERPO)])

    p_limpia, _ = findings(mod, sana)
    p_rota, _ = findings(mod, rota)

    assert p_limpia == []
    assert len(p_rota) == 1
    assert p_rota[0][0] == 1
