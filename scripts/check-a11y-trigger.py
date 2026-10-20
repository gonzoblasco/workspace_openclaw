#!/usr/bin/env python3
"""
check-a11y-trigger.py - Dispara la validacion manual de accesibilidad antes del commit.

Por que existe: la skill `a11y-at-validation` define cuando la validacion manual
con AT (VoiceOver/NVDA) es OBLIGATORIA, no opcional - cuando el cambio afecta lo
que el screen reader ANUNCIA, y eso no lo puede verificar un test unitario. El
caso testigo (radix #4109) tenia los atributos correctos en el DOM y 51 tests
verdes, y aun asi el primer option no anunciaba nada por una carrera de timing.

Ese disparador vivia solo en la skill, que el agente puede no leer. La regla del
guion comun SI tiene un gate que la hace cumplir; esto le da el mismo respaldo al
boundary de a11y. No intenta validar el anuncio (ningun script puede): lo que
hace es no dejar pasar EN SILENCIO un cambio que lo afecta.

Dos niveles, porque un grep no distingue "toca el anuncio" de "toca ARIA":
  - BLOQUEA: el patron por si solo cambia lo que se anuncia o cuando (posinset,
    setsize, live regions, activedescendant). Son los del caso testigo.
  - AVISA: toca ARIA o roles pero el juicio queda para quien escribe (label,
    rol, tabindex). Ruidoso bloquear aca: un aria-label estatico no cambia nada.

Uso:
    check-a11y-trigger.py               # el diff staged completo (lo que usa el hook)
    check-a11y-trigger.py <archivo>...  # archivos puntuales contra disco
    check-a11y-trigger.py --range A..B  # un rango de commits (segunda barrera en CI)

El rango existe porque el pre-commit se puede saltear con `--no-verify`. En CI no
hay diff staged: hay un rango (base..HEAD del PR, o HEAD~1..HEAD en un push a
main). Con `--range` el mismo juicio corre en la superficie publica.

Override: A11Y_VALIDATED=1 cuando la validacion manual se hizo y se documenta.
Exit 0 = nada que disparar, o disparo reconcido. Exit 1 = bloqueado.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# BLOQUEA: cambiar cualquiera de estos altera el anuncio o su timing, que es
# exactamente lo que ningun test cubre. Evidencia en a11y-at-validation
# ("Boundary: unit test vs manual") y en los casos radix #4109 / astryx #5344.
BLOCK = [
    (re.compile(r"aria-posinset|aria-setsize"),
     "posinset/setsize: el total que VoiceOver+Chrome cuenta en un listbox"),
    (re.compile(r"aria-(live|atomic|relevant)"),
     "live region: cuando y si se anuncia el cambio, no que dice"),
    (re.compile(r"aria-activedescendant"),
     "activedescendant: el anuncio del item activo sin mover el foco real"),
    (re.compile(r'role="(listbox|combobox|grid|menu|tree|treegrid)"'),
     "rol de widget: define el contrato de navegacion y anuncio"),
]

# AVISA: toca la superficie de ARIA, pero el efecto en el anuncio depende del
# caso. Se imprime el checklist y se sigue: bloquear aca seria castigar codigo
# correcto (un aria-label estatico es valido y no cambia ningun anuncio).
WARN = [
    (re.compile(r"aria-(label|labelledby|describedby)\b"),
     "label de accesibilidad"),
    (re.compile(r"\brole=|roleName"),
     "rol ARIA"),
    (re.compile(r"tabIndex|tabindex"),
     "orden de foco / roving focus"),
    (re.compile(r"VisuallyHidden|sr-only|srOnly"),
     "texto solo para el lector de pantalla"),
]

CHECKLIST = """La skill `a11y-at-validation` marca esta clase de cambio:

  [ ] Validation manual con AT hecha (VoiceOver: Cmd + F5, con captions)
  [ ] Casos limite probados: SIN valor preseleccionado, con valor,
      con grupos, opcion de limpiar/placeholder
  [ ] Las captions confirman la frase anunciada
  [ ] Si hubo hallazgo: verifique si es intencional antes de tocar el componente
  [ ] Evidencia documentada en el PR (que anuncio cada caso)

Tests en verde NO alcanzan: verifican atributos en el DOM, no el anuncio.
Para reconocer el disparo: A11Y_VALIDATED=1 (y documentar la evidencia)."""

HUNK = re.compile(r"^\+\+\+ b/(.+)$")
LINE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")

# Los tests no se embarcan: no pueden cambiar lo que anuncia el screen reader de
# ningun usuario. Su contenido ademas es data de prueba (los patrones aparecen
# como strings literales en las aserciones), asi que marcarlos seria un disparo
# permanente sobre algo que no es un cambio de UI. El gate encontro esto solo:
# al commitear su propio test, se bloqueo a si mismo. El mismo problema lo tuvo
# con su PROPIO script: los patrones de arriba son literales en el fuente.
#
# De ahi la regla de fondo: solo el codigo que RENDERIZA puede cambiar lo que se
# anuncia. Un script que imprime strings, un doc o un JSON no pueden. Filtrar
# por extension es lo que separa "toca ARIA" de "menciona ARIA".
#
# El segmento `tests` se busca en CUALQUIER nivel, no solo como prefijo raiz:
# los arboles de rol viven en `agents/<rol>/skills/<skill>/tests/`, y ahi el
# filtro por prefijo no llegaba. El gate bloqueaba sobre `tests/fixtures/*.html`
# de las skills de auditoria (2026-10-07) - fixtures que no se embarcan y que
# contienen los patrones ARIA como data de prueba. El propio gate ya declara
# que solo lo que RENDERIZA puede cambiar un anuncio; esto cierra la brecha
# entre esa intencion y el filtro.
# El segmento `docs` tambien se excluye, y por la MISMA razon que `tests`: un
# documento no se renderiza como UI de producto. `docs/` guarda CVs, informes y
# assets de prueba; el `.html` de un CV se abre en un navegador, pero nadie lo
# navega con un lector de pantalla esperando un contrato de widget. Sin esta
# exclusion, decir "aria-posinset" en un CV bloqueaba el commit y, peor, el CI
# del push: la linea 87 del CV de Staffy cuenta un PR sobre posinset real y el
# gate la leyo como un cambio de componente (2026-10-20).
#
# La regla de fondo no cambia: solo el codigo que RENDERIZA puede cambiar lo que
# se anuncia. Un CV renderiza texto, no una interfaz.
SKIP_PATH_PARTS = ("tests", "docs")
UI_EXTENSIONS = (".tsx", ".jsx", ".ts", ".js", ".mjs", ".cjs",
                 ".vue", ".svelte", ".astro", ".html")


def is_skipped_path(path: str) -> bool:
    """Un camino fuera de la superficie de UI no puede afectar un anuncio."""
    if any(part in SKIP_PATH_PARTS for part in path.split("/")):
        return True
    return not path.endswith(UI_EXTENSIONS)


def added_lines_from_diff(diff_text):
    """Devuelve [(archivo, numero_de_linea_nueva, texto)] de las lineas agregadas.

    Solo `+`: una linea que ya estaba no es un cambio de esta tarea, y marcarla
    haria que el gate disparara para siempre sobre el mismo codigo viejo.
    """
    out = []
    current = None
    new_no = 0
    for raw in diff_text.splitlines():
        m = HUNK.match(raw)
        if m:
            current = m.group(1)
            continue
        m = LINE.match(raw)
        if m:
            new_no = int(m.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+++"):
            continue
        if raw.startswith("+"):
            out.append((current, new_no, raw[1:]))
            new_no += 1
        elif raw.startswith("-"):
            continue
        elif raw.startswith(" "):
            new_no += 1
    return out


def classify(lines):
    """Separa los hallazgos en bloqueantes y avisos, sin duplicar por linea."""
    blocking, warnings = [], []
    for path, no, text in lines:
        for pattern, why in BLOCK:
            if pattern.search(text):
                blocking.append((path, no, why, text.strip()))
                break
        else:
            for pattern, why in WARN:
                if pattern.search(text):
                    warnings.append((path, no, why, text.strip()))
                    break
    return blocking, warnings


def staged_diff(args):
    files = [a for a in args if a != "-"]
    cmd = ["git", "diff", "--cached", "-U0", "--diff-filter=ACMR"]
    if files:
        cmd += ["--"] + files
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    except OSError:
        return ""
    return r.stdout if r.returncode == 0 else ""


def working_tree_diff(files):
    cmd = ["git", "diff", "-U0", "--"] + files
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    except OSError:
        return ""
    return r.stdout if r.returncode == 0 else ""


def range_diff(rev_range):
    """El diff de un rango de commits, para la barrera de CI (sin staging)."""
    cmd = ["git", "diff", "-U0", "--diff-filter=ACMR", f"{rev_range}"]
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    except OSError as exc:
        print(f"no pude resolver el rango '{rev_range}': {exc}")
        return None
    if r.returncode != 0:
        print(f"no pude resolver el rango '{rev_range}': {r.stderr.strip()}")
        return None
    return r.stdout


def parse_range(args):
    """Extrae el valor de `--range A..B`, o None si no vino."""
    for i, a in enumerate(args):
        if a == "--range":
            return args[i + 1] if i + 1 < len(args) else ""
        if a.startswith("--range="):
            return a.split("=", 1)[1]
    return None


def main(argv):
    args = [a for a in argv if not a.startswith("A11Y_")]

    rev_range = parse_range(args)
    if rev_range is not None:
        if not rev_range:
            print("--range necesita un valor, ej. --range origin/main..HEAD")
            return 2
        diff = range_diff(rev_range)
        if diff is None:
            # Un rango irresoluble no debe pasar en silencio: en CI seria una
            # barrera que no corre y no lo dice (el patron de pudricion que este
            # workspace ya registro dos veces).
            return 1
    else:
        files = [a for a in args if not a.startswith("--") and a != "-"]
        diff = staged_diff(files)
        if not diff and files:
            # Archivos explicitos: comparar contra HEAD (util sin nada staged).
            diff = working_tree_diff(files)

    blocking, warnings = classify(
        [line for line in added_lines_from_diff(diff) if not is_skipped_path(line[0])]
    )

    if warnings:
        print(f"a11y: {len(warnings)} linea(s) tocan la superficie de ARIA.")
        for path, no, why, text in warnings[:10]:
            print(f"    {path}:{no}  ({why})  {text[:70]}")
        if len(warnings) > 10:
            print(f"    ... y {len(warnings) - 10} mas")
        print("    Revisar el checklist abajo si el cambio afecta un anuncio.")

    if not blocking:
        return 0

    print()
    print(f"BLOQUEA: {len(blocking)} cambio(s) que afectan lo que ANUNCIA el screen reader.")
    for path, no, why, text in blocking:
        print(f"    {path}:{no}  {why}")
        print(f"        {text[:90]}")

    if os.environ.get("A11Y_VALIDATED") == "1":
        print()
        print("A11Y_VALIDATED=1: disparo reconocido. Documentar la evidencia en el PR.")
        return 0

    print()
    print(CHECKLIST)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
