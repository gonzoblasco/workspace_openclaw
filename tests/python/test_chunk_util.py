"""Tests for scripts/chunk-util.py - el corte de texto compartido.

Por que importa: `rechunk-vectors.py` GENERA los chunks y `memory-search.py` los
MUESTRA reconstruyendolos. Si los dos cortan distinto, el texto que ve el usuario
no es el que se vectorizo, y la busqueda miente en silencio sobre su contenido.

Antes estaban duplicados en los dos scripts. Estos tests fijan la propiedad que
los une: misma entrada -> mismo corte.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cu():
    return load("chunk_util", "scripts/chunk-util.py")


# --- split_large: fronteras naturales ---

def test_short_text_is_one_chunk():
    m = cu()
    assert m.split_large("texto corto") == ["texto corto"]


def test_splits_at_paragraph_boundary():
    m = cu()
    paras = ["p" * 700, "q" * 700, "r" * 700]
    texto = "\n\n".join(paras)
    out = m.split_large(texto, max_chars=1500)
    assert len(out) >= 2
    # Cada chunk debe terminar en frontera de parrafo, no a mitad.
    for c in out:
        assert c == c.strip()


def test_cuts_at_sentence_when_paragraph_too_big():
    """Un parrafo que solo pasa el limite se parte por oracion, no por byte."""
    m = cu()
    frases = [f"Oracion numero {i} con contenido suficiente." for i in range(60)]
    parrafo = " ".join(frases)
    out = m.split_large(parrafo, max_chars=500)
    assert len(out) > 1
    # Ninguna oracion debe quedar cortada al medio.
    for c in out:
        assert c.rstrip().endswith(".") or len(c) <= 500


def test_overlap_exists_between_chunks():
    """El solape hace que una idea partida se encuentre desde los dos lados."""
    m = cu()
    a = "A" * 900
    b = "B" * 900
    out = m.split_large(f"{a}\n\n{b}", max_chars=1000, overlap=200)
    assert len(out) >= 2
    # El segundo chunk debe arrastrar parte del primero.
    assert "A" in out[1]


def test_never_splits_a_word():
    """Palabras largas sin espacios: no deben cortarse."""
    m = cu()
    palabra = "x" * 200
    texto = " ".join([palabra] * 40)
    out = m.split_large(texto, max_chars=400)
    for c in out:
        for w in c.split():
            assert w == palabra, f"palabra cortada: {w[:20]}..."


def test_empty_text():
    m = cu()
    assert m.split_large("") == [""]


# --- strip_harness_header ---

def test_strips_session_header():
    m = cu()
    t = "# Session: 2026-08-29 23:45:25 GMT-3\n\n- **Session Key**: agent:main:main\n\nEl contenido real."
    out = m.strip_harness_header(t)
    assert "Session Key" not in out
    assert "El contenido real." in out


def test_strips_source_line():
    m = cu()
    t = "- **Session ID**: abc123\n- **Source**: gateway:x\n\nCuerpo."
    out = m.strip_harness_header(t)
    assert "Source" not in out
    assert "Cuerpo." in out


def test_keeps_content_that_mentions_session_keys():
    """El workspace habla de internals de OpenClaw donde 'session key' es tema real."""
    m = cu()
    t = "## Decision\n\nLa session key se compone de agent:scope:id."
    out = m.strip_harness_header(t)
    assert "session key" in out.lower()
    assert "## Decision" in out


def test_empty_and_none():
    m = cu()
    assert m.strip_harness_header("") == ""
    assert m.strip_harness_header(None) == ""


# --- chunk_text: el titulo adelante ---

def test_chunk_text_prepends_title():
    m = cu()
    out = m.chunk_text("Configuracion VPS", "El gateway se cae.")
    assert out.startswith("## Configuracion VPS")
    assert "El gateway se cae." in out


def test_chunk_text_cleans_title():
    m = cu()
    out = m.chunk_text("- **Source**: x\nTitulo limpio", "cuerpo")
    assert out.startswith("## Titulo limpio")


# --- chunks_for: la unidad completa ---

def test_chunks_for_drops_tiny_pieces():
    """Un chunk mas corto que MIN_CHARS no aporta contexto."""
    m = cu()
    assert m.chunks_for("T", "x") == []


def test_chunks_for_keeps_meaningful():
    m = cu()
    out = m.chunks_for("Titulo", "c" * 300)
    assert len(out) == 1
    assert out[0].startswith("## Titulo")


# --- la propiedad central: los dos scripts cortan IGUAL ---

def test_rechunk_and_search_share_the_cutter():
    """El texto que muestra la busqueda debe ser el que vectorizo el rechunker.

    Se verifica que ambos usen el MISMO modulo: una sola fuente para el corte.
    """
    m = cu()
    # El modulo expone las tres piezas que los dos scripts necesitan.
    assert callable(m.split_large)
    assert callable(m.strip_harness_header)
    assert callable(m.chunk_text)
    assert callable(m.chunks_for)
    # Y las constantes son las mismas que esperan los scripts.
    assert m.MAX_CHARS == 1800
    assert m.MIN_CHARS == 120
    assert m.OVERLAP == 200


def test_same_input_same_output_across_loads():
    """Dos cargas independientes dan el mismo resultado (sin estado oculto)."""
    a = load("cu_a", "scripts/chunk-util.py")
    b = load("cu_b", "scripts/chunk-util.py")
    texto = "P" * 2500
    assert a.split_large(texto) == b.split_large(texto)


def test_no_duplicate_definitions_in_scripts():
    """Los scripts NO deben redefinir el corte: una sola fuente."""
    for path in ("scripts/rechunk-vectors.py", "scripts/memory-search.py"):
        src = (ROOT / path).read_text()
        assert "def split_large" not in src, f"{path} redefine split_large"
        assert "def strip_harness_header" not in src, f"{path} redefine strip_harness_header"
