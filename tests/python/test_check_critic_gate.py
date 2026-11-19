"""Tests de scripts/check-critic-gate.py (T5.2, 2026-11-19).

El gate tiene cuatro salidas y cada una es una decision distinta: 0 pasa, 3 VETO,
4 no hay veredicto, 2 no se pudo evaluar. Un test que solo mire stdout deja pasar
el bug caro (exit 0 por un reporte ausente), asi que cada caso afirma el exit code
y la linea de motivo.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts' / 'check-critic-gate.py'

spec = importlib.util.spec_from_file_location('ccg', SCRIPT)
ccg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ccg)


def _cites(n, report_dir):
    """n citas `archivo:linea` cuyos archivos existen de verdad junto al reporte."""
    lines = []
    for i in range(n):
        name = f'fuente{i}.py'
        (report_dir / name).write_text('x = 1\n', encoding='utf-8')
        lines.append(f'Evidencia: {name}:1')
    return '\n'.join(lines)


def make_fixture(tmp_path, rows, slug='art-x', citations=5, report=True, verdict='Aprobado'):
    reviews = tmp_path / 'reviews'
    reviews.mkdir(exist_ok=True)
    ledger = tmp_path / 'verdicts.jsonl'
    ledger.write_text('\n'.join(json.dumps(r) for r in rows) + '\n', encoding='utf-8')
    if report:
        body = f'# Reporte {slug}\n\n## Sharpness\n\n' + _cites(citations, reviews)
        (reviews / f'2026-11-19-{slug}.md').write_text(body, encoding='utf-8')
    return ledger, reviews


def row(slug, verdict='Aprobado', total=None, **extra):
    rec = {'artifact': slug, 'verdict': verdict,
           'scores': {'S': 4, 'H': 4, 'A': 4, 'R': 4, 'P': 4},
           'total': total if total is not None else 20,
           'timestamp': '2026-11-19T12:00:00Z'}
    rec.update(extra)
    return rec


def run(monkeypatch, argv, ledger, reviews, capsys):
    monkeypatch.setattr(ccg, 'ROOT', ledger.parent)
    code = ccg.main(argv + ['--ledger', str(ledger), '--reviews', str(reviews)])
    return code, capsys.readouterr().out


# --- 1. fila aprobada con reporte y citas => 0 -------------------------------

def test_aprobado_con_reporte_y_citas_pasa(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('art-x')])
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 0
    assert 'CRITIC-GATE: PASS  (art-x)' in out
    assert 'citas: 5 con archivo existente' in out


# --- 2. VETO vigente => 3 ----------------------------------------------------

def test_veto_vigente_da_exit_3(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('art-x', verdict='VETO', total=15, notes='Asymmetry')],
                                   verdict='VETO')
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 3
    assert 'VETO vigente: Asymmetry' in out
    assert 'CRITIC-GATE: VETO  (art-x)' in out


# --- 3. sin fila => 4 --------------------------------------------------------

def test_sin_fila_da_exit_4(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('otro-art')])
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 4
    assert 'no hay ninguna fila' in out
    assert 'CRITIC-GATE: MISSING  (art-x)' in out


# --- 4. fila invalidada => usa la anterior; si no hay, 4 ---------------------

def test_fila_invalidada_usa_la_anterior(tmp_path, monkeypatch, capsys):
    rows = [
        row('art-x', verdict='VETO', total=12),
        row('art-x', verdict='Aprobado', total=20),
        row('art-x', status='invalidated', invalidation_reason='sin reporte'),
    ]
    ledger, reviews = make_fixture(tmp_path, rows)
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 0, out
    assert '1 fila(s) invalidada(s) descartada(s)' in out


def test_todas_las_filas_invalidadas_da_exit_4(tmp_path, monkeypatch, capsys):
    rows = [row('art-x', status='invalidated', invalidation_reason='VETO mal etiquetado')]
    ledger, reviews = make_fixture(tmp_path, rows)
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 4
    assert "todas las filas de 'art-x' estan invalidadas" in out
    assert 'CRITIC-GATE: MISSING  (art-x)' in out


# --- 5. reporte ausente => rojo ----------------------------------------------

def test_reporte_ausente_es_rojo(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('art-x')], report=False)
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 4
    assert 'ROJO  reporte:' in out


def test_reporte_declarado_que_no_existe_es_rojo(tmp_path, monkeypatch, capsys):
    rec = row('art-x', report='docs/reviews/2026-11-19-art-x.md')
    ledger, reviews = make_fixture(tmp_path, [rec])
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 4
    assert 'ese archivo no existe' in out


# --- 6. reporte con <5 citas => rojo ----------------------------------------

def test_reporte_con_pocas_citas_es_rojo(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('art-x')], citations=4)
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 4
    assert 'solo 4 cita(s) ruta:linea' in out


def test_citas_a_archivos_inexistentes_no_cuentan(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('art-x')])
    (reviews / '2026-11-19-art-x.md').write_text(
        'Sharpness\n' + '\n'.join(f'fantasma{i}.py:1' for i in range(6)), encoding='utf-8')
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 4
    assert 'solo 0 cita(s)' in out


# --- 7. ledger ilegible => 2 -------------------------------------------------

def test_ledger_ilegible_da_exit_2(tmp_path, monkeypatch, capsys):
    reviews = tmp_path / 'reviews'
    reviews.mkdir()
    ledger = tmp_path / 'verdicts.jsonl'
    ledger.write_text('{"artifact": "art-x"}\nno es json\n', encoding='utf-8')
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 2
    assert 'ledger ilegible' in out
    assert 'CRITIC-GATE: ERROR  (art-x)' in out


def test_ledger_inexistente_da_exit_2(tmp_path, monkeypatch, capsys):
    reviews = tmp_path / 'reviews'
    reviews.mkdir()
    code, out = run(monkeypatch, ['art-x'], tmp_path / 'nope.jsonl', reviews, capsys)
    assert code == 2
    assert 'ledger inexistente' in out


def test_sin_argumentos_da_exit_2(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('art-x')])
    code, out = run(monkeypatch, [], ledger, reviews, capsys)
    assert code == 2
    assert 'exactamente uno' in out


def test_verdict_desconocido_da_exit_2(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('art-x', verdict='Aprobadoish')])
    code, out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert code == 2
    assert 'no es un veredicto conocido' in out


# --- 8. --all recorre todos --------------------------------------------------

def test_all_recorre_todos_los_artefactos(tmp_path, monkeypatch, capsys):
    rows = [
        row('art-bueno', verdict='Aprobado', total=20),
        row('art-vetado', verdict='VETO', total=15),
        row('sample_artifact', verdict='Aprobado', total=20),
    ]
    ledger, reviews = make_fixture(tmp_path, rows, slug='art-bueno')
    (reviews / '2026-11-19-art-vetado.md').write_text('# VETO\n', encoding='utf-8')
    code, out = run(monkeypatch, ['--all'], ledger, reviews, capsys)
    assert code == 0, out
    assert 'OK    art-bueno  Aprobado 20' in out
    assert 'VETO  art-vetado  VETO 15' in out
    assert 'SKIP  sample_artifact' in out
    assert 'heads=2 aprobados=1 vetados=1' in out
    assert out.strip().endswith('CRITIC-GATE: PASS  (--all, heads=2 aprobados=1 vetados=1 fuera_de_alcance=1)')


def test_all_no_pasa_si_un_head_no_tiene_reporte(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [row('art-bueno'), row('art-huerfano')], slug='art-bueno')
    code, out = run(monkeypatch, ['--all'], ledger, reviews, capsys)
    assert code == 4
    assert 'ROJO  art-huerfano' in out
    assert 'CRITIC-GATE: MISSING  (--all' in out


def test_all_vacio_da_exit_4(tmp_path, monkeypatch, capsys):
    ledger, reviews = make_fixture(tmp_path, [], report=False)
    code, out = run(monkeypatch, ['--all'], ledger, reviews, capsys)
    assert code == 4
    assert 'no hay ningun artefacto evaluable' in out


# --- 9. caso real: VETO en el slug base y aprobado en la revision ------------

def test_revision_r2_no_hereda_el_veto_del_slug_base(tmp_path, monkeypatch, capsys):
    """El caso del 2026-11-19: T4.1 VETO 18/25 y T4.1-r2 Aprobado 20/25 en el mismo ledger."""
    rows = [
        row('art-x', verdict='VETO', total=18),
        row('art-x-r2', verdict='Aprobado', total=20),
    ]
    ledger, reviews = make_fixture(tmp_path, rows, slug='art-x')
    (reviews / '2026-11-19-art-x-r2.md').write_text(
        'Sharpness\n' + _cites(5, reviews), encoding='utf-8')

    base_code, base_out = run(monkeypatch, ['art-x'], ledger, reviews, capsys)
    assert base_code == 3, base_out
    assert 'NOTA  existe revision posterior: art-x-r2=Aprobado' in base_out
    r2_code, r2_out = run(monkeypatch, ['art-x-r2'], ledger, reviews, capsys)
    assert r2_code == 0, r2_out
    assert 'CRITIC-GATE: PASS  (art-x-r2)' in r2_out

    all_code, all_out = run(monkeypatch, ['--all'], ledger, reviews, capsys)
    assert all_code == 0, all_out
    assert 'SKIP  art-x  historia: superado por art-x-r2' in all_out
