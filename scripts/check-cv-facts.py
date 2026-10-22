#!/usr/bin/env python3
"""
check-cv-facts.py - Los CVs no inventan hechos. Los citan.

POR QUE EXISTE (2026-10-20). Gonzo: "por cada postulacion tenemos un cv con una
verdad distinta y eso no es creible siendo yo uno solo... los unicos casos son
los de distinto perfil, pero para perfiles similares debe ser siempre el mismo".

Medido ese dia sobre 5 CVs vivos, con el perfil documentado como referencia:

  1. Anos totales: 10+, 10+, 10+, 10 anos... y 9+ en el CV de a11y. Dos verdades.
  2. Anos de a11y: el perfil documenta ~5 (Super7 ~1 + EY ~3.7); el CV de a11y
     declara "6+ years in enterprise digital accessibility". Dos verdades.
  3. Idioma: la regla dura es B2, y el CV de fullstack dice "Advanced written,
     intermediate spoken". "Advanced" se lee como C1: contradice la regla.
  4. Certificacion: el CV de a11y dice "Completed Deque University accessibility
     certification" sobre un ROL de 2020-2021, cuando el programa es de 2021, y
     "certification" insinua una credencial IAAP que no tiene.

Un CV con un numero distinto por postulacion es el mismo defecto que un ADR con
dos verdades: se puede citar el conveniente. Este gate lo vuelve imposible.

Que verifica:
  1. ANOS: el headline de cada CV coincide con `total_years`.
  2. A11Y: todo "N+ years" pegado a accessibility coincide con `a11y_years`.
  3. IDIOMA: ningun CV declara un nivel superior al `english` del bloque.
  4. CONTACTO: telefono, email, LinkedIn y GitHub coinciden.
  5. FECHAS DE ROL: los periodos coinciden con los declarados.
  6. CERTIFICACION: no se declara una credencial IAAP que no existe.
  7. PENDIENTES: un hecho marcado `pending` en el dueno FRENA el commit. Una
     contradiccion sin decidir no se commitea "para arreglarla despues".
  8. CLAIMS SIN RESPALDO (2026-10-21): un bullet de experiencia que el dueno
     no registra se AVISA. No frena: el dueno puede estar incompleto, y el
     aviso es la señal de que hay que扩充 el dueno o sacar el claim.

Por que 8 (medido el 2026-10-21, no es teorico): los bullets de A/B testing
("Ran A/B experiments in production using Adobe Target", "Implemented A/B
testing infrastructure") estaban en 4 CVs y NO en el dueno. El gate pasaba en
verde: no compara contra el dueno lo que el dueno NO tiene. Un hecho puede
entrar a un CV por una puerta que no pasa por el corpus, y ahi no hay control.
Este control cierra esa puerta: avisa, y con eso la decision (ampliar el dueno
o sacar el claim) es de Gonzo, no del gate.

Uso:
    check-cv-facts.py [root]
Salida: 0 si todo coincide, 1 si hay contradiccion o decision pendiente.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FACTS_FILE = "memory/career-facts.md"
FACTS_BLOCK = re.compile(r"```facts\n(.*?)```", re.DOTALL)
CV_DIR = "docs/entrevistas"

# Nivel CEFR ordenado. Un CV nunca declara por encima del nivel del dueno.
LEVELS = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
# Frases que se leen como un nivel CEFR aunque no lo nombren.
LEVEL_WORDS = {
    "fluent": 5,
    "bilingual": 6,
    "native": 6,
    "advanced": 5,
    "upper intermediate": 4,
    "intermediate": 3,
}

YEARS_RE = re.compile(r"(\d+)\s*\+?\s*(?:years?|años?|anos?)", re.IGNORECASE)
# "N years <frase>" - la frase que sigue dice DE QUE son los anos. Sin ella no
# se puede saber si el numero contradice al dueno: "9+ years in frontend" y
# "3+ years across SDLC phases" son hechos distintos en la misma linea.
# OJO: la frase NO puede contener digitos. Con `0-9` en la clase, el match de
# "10+ years in frontend engineering and 6+ years in enterprise..." se comia el
# "and 6" dentro de la frase del primero, y el segundo claim desaparecia: el
# gate reportaba OK sobre la linea que mas lo necesita. Cazado 2026-10-20
# mirando los matches, no el exit code.
#
# El numero puede ser DECIMAL (2026-10-22): "1.5 years building AI-native
# products" es un hecho valido y no contradice al dueno (ai_years: 1, que es
# la calibracion interna de "desde 05/2025"). Antes el patron `(\d+)` cortaba
# en el punto y leia "5 years building AI-native products": una violacion
# FALSA en los tres CVs de AI-native (2026-10-22). Con decimal, la
# comparacion se hace contra el dueno con tolerancia: un decimal cerca del
# entero del dueno es el mismo hecho redondeado ("1.5" ~ 1), no una
# contradiccion. Un decimal lejos (por ejemplo "3.5" contra ai_years: 1) si
# se reporta.
YEARS_CLAIM = re.compile(
    r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|años?|anos?)\s+(?:of\s+|in\s+|as\s+|building\s+|working\s+|with\s+)?([a-z ,/'-]{0,60})",
    re.IGNORECASE,
)

# Categoria documentada -> como se la reconoce en el texto del CV.
# El orden importa: la primera que matchea gana.
# Una frase que HABLA de accesibilidad sin ser una categoria comparable.
A11Y_HINT = re.compile(r"accessibility|accesibilidad|a11y", re.IGNORECASE)

YEAR_CATEGORIES = [
    # El orden es la prioridad. "10+ years building and shipping production web
    # applications, working AI-first since 2025" declara el TOTAL y solo nombra
    # a11y/IA de paso: si ai_years fuera primero, el headline de cada CV se
    # reportaria como si declarara anios de IA. La mas especifica gana.
    ("sdlc_years", re.compile(r"sdlc|concurrent|matrixed|cross-regional", re.IGNORECASE)),
    ("total_years", re.compile(r"frontend|front-end|full stack|fullstack|software|production|building", re.IGNORECASE)),
    ("ai_years", re.compile(r"ai-first|ai-assisted|ai engineering|\bai\b", re.IGNORECASE)),
]

# Accesibilidad NO se declara con numero (decision de Gonzo, 2026-10-20). La
# aritmetica de las fechas canonicas da 4.42 anios de funcion central y 5.83
# contando todo el freelance: cualquier numero redondo obliga a elegir entre
# quedar corto o inflar, y el reclutador puede hacer la misma suma. Se cuenta
# nombrando los roles.
#
# Por eso `a11y` NO esta en YEAR_CATEGORIES como categoria comparable: se
# detecta despues, y solo cuando la frase del claim no cayo en otra categoria.
# "10+ years building production software, leading accessibility at Super7UI"
# declara el TOTAL y solo nombra a11y de paso; marcarlo seria un falso positivo
# en el headline de cada CV.

ENGLISH_LINE = re.compile(r"english|ingl[eé]s", re.IGNORECASE)

# --- Claims de experiencia sin respaldo (control 8) ---
#
# Hechos que el dueno tiene que registrar para que un CV pueda declararlos.
# Si un CV afirma uno de estos y el dueno no lo contiene, se AVISA.
#
# NO frena. El dueno puede estar incompleto (y a veces esta): lo que hace el
# gate es poner el claim en la mesa, para que la decision de ampliar el dueno
# o de sacar el claim sea explicita. Un gate que frena obligaria a elegir entre
# perder informacion real o agregar al dueno sin pensar.
#
# El criterio de "esta en el dueno" es la presencia del termino en el archivo
# del corpus, no una coincidencia exacta: el dueno cuenta la historia con sus
# palabras y la del CV es otra redaccion del mismo hecho.
UNBACKED_CLAIMS = {
    "a/b testing": ("experimentacion", "a/b testing", "adobe target", "a/b experiments"),
    "analytics": ("analytics", "instrumentacion de analytics", "engagement metrics"),
    "feature flags": ("feature flag",),
    "funnel": ("funnel", "analisis de funnel"),
    "conversion": ("conversion", "optimizacion de conversion", "activacion, retencion"),
    "observability": ("observability", "datadog", "new relic", "sentry"),
    # "java" tiene que ser la palabra completa: "JavaScript" matchea "java" y
    # disparaba el aviso en cada CV que lista JavaScript. Verificado 2026-10-21.
    "java/kotlin": (r"\bjava\b", r"\bkotlin\b"),
}

# Terminos que aparecen en la seccion de requisitos del propio CV, no en un
# claim de experiencia. "A/B testing" en la linea de "Requirements" no es una
# afirmacion sobre lo que Gonzo hizo.
SKIP_SECTIONS = ("requirement", "nice to have", "requirement:", "qualifications", "about the role")

# Secciones del CV que NO son un claim de experiencia (2026-10-22).
#
# "## Notes / gaps" lista los requisitos del JD que NO se pueden cubrir, y
# "## Keyword map" mapea requisito -> seccion. En las dos, la palabra
# "feature flags" o "5+ years" aparece como REQUERIDO DEL PUESTO o como
# DECLARACION DE VACIO, no como afirmacion sobre lo que Gonzo hizo. El gate
# las leia como claims y reportaba contradicciones falsas: en el CV de Mural
# marcaba "5+ years building production software" (que en realidad era una
# fila del keyword map que resumia el headline) y los gaps honestos
# declarados como si fueran fraude.
#
# El control 8 (claims sin respaldo) se saltea estas secciones por la misma
# razon: no hay claim que respaldar, hay un gap declarado.
GAP_SECTIONS = re.compile(
    r"^\s*#{1,6}\s*(?:notes|gaps|notes\s*/\s*gaps|keyword\s*map|keywords?\s*map|"
    r"coverage|pendientes?|to\s*confirm)\b",
    re.IGNORECASE,
)

# Encabezado de un rol. Los CVs usan `### Empresa - Titulo`; el bloque de fechas
# viene en la linea siguiente. Solo aca se declaran periodos.
ROLE_HEADING = re.compile(r"^\s*(###|\*\*)", re.IGNORECASE)
# Un extremo de periodo: MM/YYYY o solo YYYY. "Present"/"Presente" no es fecha.
ROLE_DATE = re.compile(r"(?:\d{2}/)?\d{4}")


def _years_agree(got: float, want: float) -> bool:
    """Dos decimales de años son el MISMO hecho que el entero del dueño.

    El dueño guarda `ai_years: 1` como calibración interna de "desde 05/2025"
    (que en la práctica son ~1,5 años, y así lo dice §6.3 del corpus). Un CV
    que declara "1.5 years building AI-native products" NO contradice al
    dueño: es el mismo hecho con más precisión. Lo que sí contradice es un
    decimal lejos del entero (por ejemplo "3.5" contra `ai_years: 1`), y eso
    se reporta.

    La tolerancia es 0.75: suficiente para absorber el redondeo entre "~1 año
    de calibración interna" y "1,5 años reales", y lo bastante ajustada para
    que "3.5" o "2" no pasen como el mismo hecho que "1".
    """
    return abs(got - want) <= 0.75


def parse_facts(root: Path):
    path = root / FACTS_FILE
    if not path.exists():
        return None
    m = FACTS_BLOCK.search(path.read_text(encoding="utf-8"))
    if not m:
        return None
    facts = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        facts[key.strip()] = value.strip().strip('"')
    return facts


def cvs(root: Path):
    base = root / CV_DIR
    if not base.exists():
        return []
    # Los CVs no usan un unico nombre: conviven "cv-frontend-code-evaluator-...md"
    # y "eit-cv-gonzalo-blasco-a11y.md". Un glob que solo ancle al principio se
    # pierde los que llevan el prefijo adelante: el CV de EIT/HTC tiene el
    # bullet de A/B testing y ningun control lo miraba. Verificado 2026-10-21.
    # Se toma cualquier .md cuyo nombre contenga el token "cv" como parte de
    # una palabra, separado por guiones o al inicio.
    out = []
    for p in base.rglob("*.md"):
        parts = re.split(r"[-_]", p.stem.lower())
        if "cv" in parts:
            out.append(p)
    return sorted(out)


def declared_level(line: str):
    """Nivel CEFR implicito en una linea de idioma, o None."""
    upper = line.lower()
    best = None
    for cefr, rank in LEVELS.items():
        if re.search(rf"\b{cefr.lower()}\b", upper):
            best = max(best or 0, rank)
    for word, rank in LEVEL_WORDS.items():
        if word in upper:
            best = max(best or 0, rank)
    return best


def _in_gap_section(lines, n) -> bool:
    """¿La linea n esta dentro de una seccion de gaps / keyword map?

    Esas secciones citan los REQUISITOS DEL PUESTO (que no son hechos de
    Gonzo) y declaran los vacios. Juzgarlas con las reglas de los claims
    produce contradicciones falsas. Ver GAP_SECTIONS.
    """
    for i in range(n - 1, -1, -1):
        line = lines[i]
        if line.startswith("#"):
            return bool(GAP_SECTIONS.match(line))
    return False


def check_cv(path: Path, facts: dict):
    """(violaciones, pendientes) de un CV."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    name = path.name
    violations = []

    # 1-2) Anos: cada "N years <frase>" se compara contra la categoria que
    # describe la frase. Un numero suelto sin categoria no se juzga: no hay
    # contra que compararlo.
    #
    # Accesibilidad es la excepcion: no lleva numero NUNCA. Se evalua solo
    # cuando la frase no cayo en otra categoria, para no marcar el headline del
    # total por mencionar a11y de paso.
    for n, line in enumerate(lines, 1):
        if _in_gap_section(lines, n):
            continue
        for m in YEARS_CLAIM.finditer(line):
            got = float(m.group(1))
            phrase = m.group(2)
            matched = None
            for key, pattern in YEAR_CATEGORIES:
                if pattern.search(phrase):
                    matched = key
                    break
            if matched:
                want = facts.get(matched)
                if want and not _years_agree(got, float(want)):
                    violations.append(
                        (
                            name,
                            n,
                            f"declara {got:g} anios de {matched}, el dueno dice {want}",
                            line.strip()[:110],
                        )
                    )
            elif A11Y_HINT.search(phrase):
                violations.append(
                    (
                        name,
                        n,
                        "declara un numero de anios de accesibilidad (no se declara numero)",
                        line.strip()[:110],
                    )
                )

    # 3) Idioma: nunca por encima del nivel del dueno.
    owner = facts.get("english")
    if owner and owner in LEVELS:
        ceiling = LEVELS[owner]
        for n, line in enumerate(lines, 1):
            if not ENGLISH_LINE.search(line):
                continue
            got = declared_level(line)
            if got and got > ceiling:
                violations.append(
                    (name, n, f"declara nivel {got} (> {owner}) en ingles", line.strip()[:110])
                )

    # 4) Contacto.
    for key, label in (
        ("contact_phone", "telefono"),
        ("contact_email", "email"),
        ("contact_linkedin", "LinkedIn"),
        ("contact_github", "GitHub"),
    ):
        want = facts.get(key)
        if not want:
            continue
        # Cada dato presente debe COINCIDIR; no se exige que este en todos.
        found = []
        if key == "contact_phone":
            found = re.findall(r"\+54[\s0-9]{8,}", text)
        elif key == "contact_email":
            found = re.findall(r"[\w.+-]+@[\w.-]+\.\w+", text)
        elif key == "contact_linkedin":
            found = re.findall(r"linkedin\.com/in/[\w-]+", text)
        else:
            found = re.findall(r"github\.com/[\w-]+", text)
            # Los repos citados (github.com/adobe/...) no son el perfil.
            found = [f for f in found if f.count("/") == 2]
        for f in set(found):
            if f.strip() != want.strip():
                violations.append((name, 0, f"{label} '{f}' no coincide con '{want}'", ""))

    # 5) Fechas de rol: se comparan los ANOS, no el formato. Un CV puede
    # escribir "2021 - 2025" y otro "09/2021 - 05/2025": es el mismo hecho con
    # distinto detalle, y exigir el formato convierte una decision de estilo en
    # una violacion falsa.
    periods = {
        "role_freelance": "Freelancer",
        "role_ey": "EY",
        "role_super7": "Super7",
        "role_minutentag": "Minutentag",
    }
    for key, label in periods.items():
        want = facts.get(key)
        if not want:
            continue
        if label.lower() not in text.lower():
            continue
        want_endpoints = ROLE_DATE.findall(want)
        # Solo un ENCABEZADO de rol declara fechas. Un "Azure (Super7UI, EY)" en
        # una linea de skills nombra la empresa sin afirmar un periodo: buscar
        # ahi produce un falso positivo en cada CV con skills agrupadas.
        for n, line in enumerate(lines, 1):
            if not ROLE_HEADING.match(line):
                continue
            if label.lower() not in line.lower():
                continue
            block = " ".join(lines[n - 1 : n + 3])
            got = ROLE_DATE.findall(block)
            # Precision declarada: si el CV escribe MM/YYYY, el mes importa;
            # si escribe solo YYYY, el ano es todo lo que afirma. Comparar un
            # CV no-tecnico ("2021 - 2025") contra un dueno con mes era marcar
            # como contradiccion una decision de formato.
            got_has_month = any("/" in g for g in got)
            for want_ep in want_endpoints:
                want_year = want_ep.split("/")[-1]
                if got_has_month and "/" in want_ep:
                    ok = want_ep in got
                else:
                    ok = any(g.endswith(want_year) or g == want_year for g in got)
                if not ok:
                    violations.append(
                        (name, n, f"fechas de {label}: falta {want_ep}", line.strip()[:110])
                    )
            break

    # 6) Certificacion: no declarar una credencial que no existe.
    # OJO: "IAAP Certification Quick Guide" es el NOMBRE de un curso de Deque,
    # no una afirmacion de estar certificado. Por eso se busca "certified" /
    # "credential" / "holder" y no la palabra "certification": la primera
    # version marcaba el indice de cursos y habria obligado a borrar evidencia
    # real de formacion.
    for n, line in enumerate(lines, 1):
        low = line.lower()
        if "deque" in low and "certification" in low and "program" not in low:
            violations.append(
                (name, n, "Deque como 'certification': es un programa, no una credencial", line.strip()[:110])
            )
        if re.search(r"\bIAAP\b", line) and re.search(r"\bcertified\b|\bcredential\b|\bholder\b", low):
            violations.append((name, n, "insinua credencial IAAP que no tiene", line.strip()[:110]))

    return violations


def unbacked_claims(root: Path, facts: dict):
    """Claims de experiencia en CVs que el dueno no registra. (avisos)"""
    corpus_path = root / FACTS_FILE
    if not corpus_path.exists():
        return []
    raw = corpus_path.read_text(encoding="utf-8")
    corpus = raw.lower()
    # Una mencion en la seccion "Falta relevar" NO es un hecho registrado: es
    # un hecho declarado desconocido. Si el dueno dice "A/B testing: PENDIENTE
    # DE RESOLVER", el claim sigue sin respaldo y el aviso tiene que seguir
    # apareciendo. Sin esto, anotar la duda en el dueno la hacia invisible
    # para el control: el pendiente se confundia con el hecho.
    unresolved = set()
    m = re.search(r"##\s*11\.\s*Falta relevar(.*?)(?=\n##\s|\Z)", raw, re.DOTALL)
    if m:
        section = m.group(1).lower()
        for claim, needles in UNBACKED_CLAIMS.items():
            if any(re.search(n, section) for n in needles):
                unresolved.add(claim)
    out = []
    for cv in cvs(root):
        text = cv.read_text(encoding="utf-8")
        lines = text.splitlines()
        for n, line in enumerate(lines, 1):
            low = line.lower()
            if not low.strip().startswith("-"):
                continue
            if any(marker in low for marker in SKIP_SECTIONS):
                continue
            # Las secciones de gaps y keyword map citan requisitos del JD, no
            # claims de Gonzo. Sin este salto, un gap honesto ("feature flags
            # - not part of my experience") se reportaba como claim sin
            # respaldo: el gate marcaba la honestidad como fraude.
            if _in_gap_section(lines, n):
                continue
            for claim, needles in UNBACKED_CLAIMS.items():
                if not any(re.search(n, low) for n in needles):
                    continue
                # ¿El dueno registra este hecho?
                if claim in unresolved:
                    # esta en "Falta relevar": el dueno lo declara desconocido.
                    out.append((cv.name, n, claim, line.strip()[:110]))
                    break
                if any(re.search(n, corpus) for n in needles):
                    continue
                out.append((cv.name, n, claim, line.strip()[:110]))
                break
    return out


def pending_facts(facts: dict):
    """Hechos marcados como decision pendiente."""
    out = []
    count = int(facts.get("pending", "0") or 0)
    for i in range(1, count + 1):
        key = "pending_note" if i == 1 else f"pending_note_{i}"
        note = facts.get(key)
        if note:
            out.append(note)
    return out


def main(argv=None):
    root = ROOT if argv is None else Path(argv[0])
    facts = parse_facts(root)
    if facts is None:
        print(f"FALTA: {FACTS_FILE} sin bloque ```facts. Es el dueno de los hechos.")
        return 1

    violations = []
    for cv in cvs(root):
        violations.extend(check_cv(cv, facts))

    pending = pending_facts(facts)
    warnings = unbacked_claims(root, facts)

    if not violations and not pending and not warnings:
        print(f"OK: {len(cvs(root))} CVs coinciden con {FACTS_FILE}.")
        return 0

    if violations:
        print(f"CONTRADICCIONES ({len(violations)}):\n")
        for name, n, msg, line in violations:
            where = f"{name}:{n}" if n else name
            print(f"  {where}  {msg}")
            if line:
                print(f"      {line}")
        print("\nEl CV no define hechos: los cita desde el dueno.\n")

    if pending:
        print(f"FRENO - DECISIONES PENDIENTES ({len(pending)}):\n")
        for note in pending:
            print(f"  - {note}")
        print(
            "\nUna contradiccion sin decidir no se commitea 'para arreglarla despues':\n"
            "se decide ahora, se corrige el dueno y se propaga. (AGENTS.md, seccion 0)"
        )

    if warnings:
        print(f"AVISOS - CLAIMS SIN RESPALDO EN EL DUENO ({len(warnings)}):\n")
        for name, n, claim, line in warnings:
            print(f"  {name}:{n}  '{claim}' no esta en {FACTS_FILE}")
            print(f"      {line}")
        print(
            "\nEstos bullets no frenan el commit, pero el dueno tiene que registrar el\n"
            "hecho o el CV tiene que sacarlo. Si el hecho es real, va al dueno PRIMERO\n"
            "(ADR-101: el corpus es la verdad, el perfil es un filtro).\n"
        )

    return 1 if (violations or pending) else 0


if __name__ == "__main__":
    sys.exit(main())
