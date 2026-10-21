"""Tests for scripts/check-cv-facts.py (los CVs citan hechos, no los inventan).

El checker existe porque el 2026-10-20 los 5 CVs vivos declaraban tres verdades
distintas sobre la misma persona: 9+ vs 10+ anios, un 6+ de a11y que no cierra
contra ninguna aritmetica, y "Advanced written" contra una regla dura de B2.

Propiedades criticas:
  1. Un headline de anos distinto del dueno se caza.
  2. NO se caza un numero suelto sin categoria ("3+ years across SDLC").
  3. El nivel de idioma por encima del dueno se caza; B2 no.
  4. "IAAP Certification Quick Guide" (nombre de curso) NO es credencial falsa.
     "IAAP certified" SI.
  5. Un hecho `pending` FRENA aunque no haya contradicciones: es la regla de
     freno de Gonzo - no se acumula una contradiccion sin decidir.
  6. Contacto distinto se caza.

Cada test siembra el caso en un arbol falso; el ultimo exige que el gate
DISTINGA el arbol limpio del sucio.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-cv-facts.py"

FACTS = """# Hechos

```facts
total_years: 10
a11y_years_internal: 5
a11y_claim: roles
ai_years: 5
sdlc_years: 3
english: B2
contact_phone: +54 11 4937 4656
contact_email: gonzoblasco@icloud.com
contact_linkedin: linkedin.com/in/gonzalo-blasco
contact_github: github.com/gonzoblasco
role_ey: 09/2021 - 05/2025
pending: 0
```
"""

CLEAN_CV = """# GONZALO BLASCO

gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## PROFILE

Engineer with 10+ years building production software, leading accessibility at Super7UI and EY.

### EY (Ernst & Young) - Senior Frontend Engineer
09/2021 - 05/2025 | Hybrid

## LANGUAGES

- **English** - B2.
"""


def load():
    spec = importlib.util.spec_from_file_location("check_cv_facts", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def seed(root, facts=FACTS, cv=CLEAN_CV, name="cv-test.md"):
    (root / "memory").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "entrevistas" / "proceso").mkdir(parents=True, exist_ok=True)
    (root / "memory" / "career-facts.md").write_text(facts, encoding="utf-8")
    path = root / "docs" / "entrevistas" / "proceso" / name
    path.write_text(cv, encoding="utf-8")
    return path


# --- anos ---

def test_total_years_mismatch_is_caught(tmp_path):
    mod = load()
    seed(tmp_path, cv=CLEAN_CV.replace("10+ years", "9+ years"))
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("total_years" in x[2] for x in v)


def test_a11y_number_is_always_rejected(tmp_path):
    # Decision de Gonzo (2026-10-20): accesibilidad no se declara con numero.
    # La aritmetica da 4.42 anios de funcion central y 5.83 contando el
    # freelance: cualquier redondo obliga a quedar corto o inflar.
    mod = load()
    seed(tmp_path, cv=CLEAN_CV.replace("leading accessibility at Super7UI and EY", "6+ years in accessibility"))
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("accesibilidad" in x[2] for x in v)


def test_a11y_roles_phrasing_is_accepted(tmp_path):
    # Contarlo por roles es la forma correcta: hechos, no un redondo.
    mod = load()
    seed(tmp_path)
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert not any("accesibilidad" in x[2] for x in v)


def test_two_claims_on_one_line_are_both_read(tmp_path):
    # El bug real: con digitos en la clase de la frase, el primer match se comia
    # el segundo claim y la linea mas importante del CV pasaba limpia.
    mod = load()
    seed(
        tmp_path,
        cv=CLEAN_CV.replace(
            "10+ years building production software, leading accessibility at Super7UI and EY",
            "10+ years in frontend engineering and 6+ years in enterprise accessibility",
        ),
    )
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("accesibilidad" in x[2] for x in v), "el segundo claim de la linea debe leerse"


def test_uncategorized_number_is_not_judged(tmp_path):
    # Un numero sin categoria documentada no se juzga: no hay contra que
    # compararlo. ("across SDLC" SI es una categoria: ese caso es otro test.)
    mod = load()
    seed(tmp_path, cv=CLEAN_CV.replace("leading accessibility at", "8+ years of mentoring, leading accessibility at"))
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert not any("years" in x[2] for x in v)


def test_sdlc_years_is_a_real_category(tmp_path):
    # "3+ years across SDLC phases" declara el hecho sdlc_years del dueno.
    mod = load()
    seed(tmp_path, cv=CLEAN_CV.replace("leading accessibility at", "8+ years across SDLC phases, leading accessibility at"))
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("sdlc_years" in x[2] for x in v)


# --- idioma ---

def test_level_above_owner_is_caught(tmp_path):
    mod = load()
    seed(tmp_path, cv=CLEAN_CV.replace("**English** - B2.", "**English** - Advanced written."))
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("ingles" in x[2] or "nivel" in x[2] for x in v)


def test_b2_is_accepted(tmp_path):
    mod = load()
    seed(tmp_path)
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert not any("nivel" in x[2] for x in v)


# --- certificaciones ---

def test_course_name_is_not_a_credential(tmp_path):
    # "IAAP Certification Quick Guide" es un curso de Deque, no una credencial.
    mod = load()
    seed(tmp_path, cv=CLEAN_CV + "\n- IAAP Certification Quick Guide (04/2021)\n")
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert not any("IAAP" in x[2] for x in v)


def test_iaap_credential_claim_is_caught(tmp_path):
    mod = load()
    seed(tmp_path, cv=CLEAN_CV + "\n- IAAP certified professional.\n")
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("IAAP" in x[2] for x in v)


def test_deque_as_certification_is_caught(tmp_path):
    mod = load()
    seed(tmp_path, cv=CLEAN_CV + "\n- Completed Deque University accessibility certification.\n")
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("Deque" in x[2] for x in v)


# --- contacto y fechas ---

def test_wrong_email_is_caught(tmp_path):
    mod = load()
    seed(tmp_path, cv=CLEAN_CV.replace("gonzoblasco@icloud.com", "gonzo@other.com"))
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("email" in x[2] for x in v)


def test_role_dates_must_match(tmp_path):
    mod = load()
    seed(tmp_path, cv=CLEAN_CV.replace("09/2021 - 05/2025", "09/2021 - 03/2025"))
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert any("EY" in x[2] for x in v)


def test_company_in_skills_line_is_not_a_role(tmp_path):
    # "Azure (Super7UI, EY)" nombra la empresa sin afirmar un periodo.
    mod = load()
    seed(tmp_path, cv=CLEAN_CV + "\n- **Cloud:** Azure (Super7UI, EY), Docker.\n")
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/cv-test.md", mod.parse_facts(tmp_path))
    assert not any("Super7" in x[2] for x in v)


# --- la regla de freno ---

def test_pending_decision_blocks_even_when_clean(tmp_path):
    mod = load()
    facts = FACTS.replace("pending: 0", 'pending: 1\npending_note: "falta decidir X"')
    seed(tmp_path, facts=facts)
    assert mod.main([str(tmp_path)]) == 1


def test_clean_tree_passes(tmp_path):
    mod = load()
    seed(tmp_path)
    assert mod.main([str(tmp_path)]) == 0


def test_gate_distinguishes_clean_from_dirty(tmp_path):
    mod = load()
    seed(tmp_path)
    assert mod.main([str(tmp_path)]) == 0
    seed(tmp_path, cv=CLEAN_CV.replace("10+ years", "9+ years"))
    assert mod.main([str(tmp_path)]) == 1


# --- claims sin respaldo (control 8, 2026-10-21) ---
#
# El caso que motivó el control: los bullets de A/B testing estaban en 4 CVs y
# NO en el dueno. El gate pasaba en verde porque compara contra el dueno lo
# que el dueno TIENE, no lo que el dueno NO tiene. Un hecho puede entrar a un
# CV por una puerta que no pasa por el corpus, y ahi no habia control.

def test_unbacked_ab_testing_claim_is_flagged(tmp_path):
    mod = load()
    seed(tmp_path, cv=CLEAN_CV + "\n- Ran A/B experiments in production using Adobe Target.\n")
    w = mod.unbacked_claims(tmp_path, mod.parse_facts(tmp_path))
    assert any("a/b testing" in x[2] for x in w)


def test_claim_backed_by_corpus_is_not_flagged(tmp_path):
    mod = load()
    facts = FACTS + "\nEn Minutentag corrio experimentos A/B testing con Adobe Target.\n"
    seed(tmp_path, facts=facts, cv=CLEAN_CV + "\n- Ran A/B experiments in production using Adobe Target.\n")
    w = mod.unbacked_claims(tmp_path, mod.parse_facts(tmp_path))
    assert not any("a/b testing" in x[2] for x in w)


def test_claim_mentioned_only_in_falta_revelar_is_still_flagged(tmp_path):
    # Anotar la duda en el dueno NO convierte el pendiente en hecho. Sin esto,
    # "A/B testing: PENDIENTE DE RESOLVER" en la seccion 11 hacia invisible
    # el aviso y el control：一个 hecho desconocido se confundia con uno
    # registrado.
    mod = load()
    facts = FACTS + "\n## 11. Falta relevar\n\n2. **A/B testing:** PENDIENTE DE RESOLVER.\n"
    seed(tmp_path, facts=facts, cv=CLEAN_CV + "\n- Ran A/B experiments in production using Adobe Target.\n")
    w = mod.unbacked_claims(tmp_path, mod.parse_facts(tmp_path))
    assert any("a/b testing" in x[2] for x in w)


def test_unbacked_claim_warns_but_does_not_block(tmp_path):
    # El aviso no frena: el dueno puede estar incompleto y la decision de
    # ampliarlo o sacar el claim es de Gonzo.
    mod = load()
    seed(tmp_path, cv=CLEAN_CV + "\n- Ran A/B experiments in production using Adobe Target.\n")
    assert mod.main([str(tmp_path)]) == 0


def test_cv_with_prefix_in_middle_is_covered(tmp_path):
    # "eit-cv-gonzalo-blasco-a11y.md": el glob `cv-*.md` no lo veia, y tenia
    # los dos errores que el gate existe para cazar (9+ anios, y un numero de
    # anios de accesibilidad). Verificado 2026-10-21.
    mod = load()
    seed(tmp_path, cv=CLEAN_CV.replace("10+ years", "9+ years"), name="eit-cv-gonzalo-blasco.md")
    v = mod.check_cv(tmp_path / "docs/entrevistas/proceso/eit-cv-gonzalo-blasco.md", mod.parse_facts(tmp_path))
    assert any("total_years" in x[2] for x in v)
