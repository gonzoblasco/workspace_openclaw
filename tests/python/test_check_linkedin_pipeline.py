"""Tests for scripts/check-linkedin-pipeline.py (el gate de la cadena OSS -> LinkedIn).

El checker existe porque la skill `linkedin-merge-post` (workshop de MIND) exige en su paso 6
"clear both publish gates", y uno de los dos -el "anti-ai pass" de `skills/anti-ai`- **no
existe**: la skill fue eliminada el 2026-09-22 y para entonces ya era un placeholder. El paso 6
era inejecutable, y la cadena de posts (una de las tres acciones del ROADMAP 2.2) no tenia gate.

El script restituye el gate con las reglas ORIGINALES de ese `anti-ai`, recuperadas del historial
(commit c0182f17), no inventadas. Y agrega el gate de CIERRE, que es el que el diagnostico
mostro como el cuello de botella real: 5 drafts esperando OK y 2 merges elegibles sin post.

Propiedades criticas:
  1. El em dash y el en dash FALLAN (regla dura de Gonzo).
  2. Un post sin `Status` FALLA: sin el no se sabe si es borrador o publicado.
  3. Un post sin `Nicho` / `Niche` FALLA: sin el no se sabe a que pilar de branding pertenece.
  4. Un post que no cita el PR FALLA: sin el no es trazable al merge que lo origina.
  5. Las dos grafias del header (es/en) se aceptan: 4 posts usan `Nicho`, 3 usan `Niche`.
  6. Los patrones de estilo (muletillas, cierre generico) AVISAN pero NO bloquean: son señales,
     no hechos. Un gate que reprima al post canonico esta roto.
  7. La longitud fuera de la ventana AVISA, no falla.
  8. Un post en espanol FALLA: el contenido publicable va en ingles.
  9. La auditoria de cierre detecta drafts vencidos y merges elegibles sin post.
 10. La auditoria NO reporta como vencido un post recien modificado.

Cada test siembra el caso en un arbol falso; el ultimo exige que el gate DISTINGA el arbol
limpio del sucio.
"""
import importlib.util
import os
import sqlite3
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-linkedin-pipeline.py"


CLEAN_POST = """# LinkedIn Post - facebook/astryx #4605

**Status:** draft para revision de Gonzo
**Idioma:** ingles
**Nicho:** a11y
**Proyecto:** facebook/astryx
**PR:** #4605

---

## Post

Some fixes are invisible. This one is a single line of CSS that took three weeks to land - and
it is the kind of change that makes the web a little more usable for people who do not see color
the way most of us do.

A few weeks ago I opened an issue on **astryx** (Meta's open-source React component library):
the current page in the breadcrumb trail was distinguished from the links only by color. A link is
`--color-text-secondary`, the current page is `--color-text-primary`. If you cannot perceive that
color difference - color blindness, low vision, a high-contrast display - the breadcrumb silently
fails WCAG 2.1 SC 1.4.1 (Use of Color). You would have no idea where you are in the site.

The fix sounds trivial: add `font-weight: var(--font-weight-semibold)` to the current item's style,
on top of the `aria-current="page"` that was already there for screen readers. Now the current
page reads as current by weight, not just by color.

But the interesting part is what happened between the issue and the merge.

My first version of the PR was a mess. I had accidentally let unrelated commits from a
color-contrast branch leak into it. A reviewer would have been right to close it. So I rebased onto
`main`, cleaned the scope down to exactly one change, and re-verified everything: 25/25 tests, lint
clean, package boundaries clean.

Then something genuinely cool happened. astryx runs a nightly component auditor that found the same
bug I had filed - and explicitly deferred it to my PR, rather than landing a color-only patch
that would have conflicted with the proper fix. The audit literally cited my open PR as the right
way to solve it.

That is the part I love about open source: the system itself pointed at the correct fix. The
maintainer who reviewed it said that was the fix the Breadcrumbs audit pointed at.

Merged today. One line of CSS, three weeks of patience, and a breadcrumb that now tells you where
you are - even if you cannot see the difference between two grays.

If you build UI, go check your breadcrumbs. If the current item is only distinguished by color,
you have the same bug I had.

PR: https://github.com/facebook/astryx/pull/4605

#accessibility #a11y #openaccessibility #assistivetechnology #inclusivedesign #webdev #reactjs

---

## Notas para Gonzo

- **Longitud:** ~300 palabras.
"""


# Un post enteramente en espanol. Hay 2 vivos asi (base-ui-aria-orientation.md y
# moderno-refactor.md), asi que el defecto que el gate caza es real, no teorico. El fixture
# tiene que ser POST Entero en espanol: con un solo parrafo en espanol sobre 383 palabras la
# proporcion se diluye y el detector no dispara (medido).
SPANISH_POST = """# LinkedIn Post: aria-orientation en los role owners (base-ui)

**Status:** draft para revision de Gonzo
**Idioma:** espanol
**Nicho:** a11y
**Proyecto:** mui/base-ui
**PR:** #5551

---

## Post

El error de accesibilidad mas dificil de detectar no es el que rompe el screen reader, sino el que
lo confunde con informacion invalida.

Hace unos dias mergee un fix en MUI Base UI que ilustra perfectamente este punto: un
`aria-orientation` mal ubicado.

La idea era simple: el atributo tiene que estar en los elementos que son los "role owners" de
verdad, no en cualquier contenedor. Cuando vive en el elemento equivocado, el screen reader lo
anuncia como si fuera informacion de orientacion cuando en realidad no lo es, y la persona que
navega con teclado termina con una sensacion de desorientacion que no puede explicar.

El fix fue mover `aria-orientation` a los elementos que realmente son los "role owners" - los que
si soportan el atributo - y omitirlo en `grid` y `presentation`. Siete archivos, 69 lineas agregadas,
4 eliminadas, con tests de regresion para asegurar que la navegacion por teclado se preservara.

La parte interesante no fue el cambio en si, sino la revision: el maintainer pidio acotar el alcance
a los componentes que de verdad soportan el atributo, y el PR quedo tres veces mas chico que la
primera version. Menos diff, mismo efecto.

PR: https://github.com/mui/base-ui/pull/5551

#accessibility #a11y #openaccessibility #assistivetechnology #inclusivedesign

---

## Notas para Gonzo

- **Longitud:** ~250 palabras.
"""


def load():
    spec = importlib.util.spec_from_file_location("check_linkedin_pipeline", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def seed(root, post=CLEAN_POST, name="post-test.md", merged=(), status_lines=None):
    """Siembra un post y una DB de memoria. `merged` son (repo, pr) para el gate de cierre."""
    posts_dir = root / "docs" / "linkedin"
    posts_dir.mkdir(parents=True, exist_ok=True)
    (root / "memory").mkdir(parents=True, exist_ok=True)

    path = posts_dir / name
    path.write_text(post, encoding="utf-8")

    db = root / "memory" / "memory.db"
    con = sqlite3.connect(db)
    con.execute(
        "create table contributions (id integer primary key autoincrement, repo text not null, "
        "issue text, issue_url text, pr text, pr_url text, status text not null default 'open', "
        "detail text, context text, tier text, created_at text, updated_at text, "
        "tipo text not null default 'pr')"
    )
    for repo, pr in merged:
        con.execute(
            "insert into contributions (repo, pr, status, tipo) values (?, ?, 'merged', 'pr')",
            (repo, pr),
        )
    con.commit()
    con.close()
    return path


# --- el post: reglas innegociables ---

def test_clean_post_passes(tmp_path):
    mod = load()
    path = seed(tmp_path)
    problems, warnings = mod.check_post(path, 14)
    assert not problems, problems


def test_em_dash_fails(tmp_path):
    mod = load()
    path = seed(tmp_path, post=CLEAN_POST.replace("Some fixes are invisible.", "Some fixes are invisible - really.").replace(" - ", " — "))
    problems, _ = mod.check_post(path, 14)
    assert any("Guiones largos" in p for p in problems)


def test_en_dash_fails(tmp_path):
    mod = load()
    path = seed(tmp_path, post=CLEAN_POST.replace("only by color", "only by colour – really"))
    problems, _ = mod.check_post(path, 14)
    assert any("Guiones largos" in p for p in problems)


def test_invisible_glyphs_fail(tmp_path):
    # Medido el 2026-10-22: los 2 posts que escribio el subagente traian 10 y 9 guiones no
    # separables (U+2011) y 8 espacios angostos (U+202F). El gate de guiones largo
    # (`check_em_dash.py`) solo mira U+2014 y U+2013, asi que estos pasaban. Los 10 posts
    # canonicos tienen CERO de estos: son el mismo defecto que el em dash, uno que se ve bien
    # y no lo esta.
    mod = load()
    post = CLEAN_POST.replace("Some fixes are invisible.", "Some fixes are invisible\u2011really.")
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert any("invisibles" in p for p in problems), problems


def test_narrow_no_break_space_fails(tmp_path):
    mod = load()
    post = CLEAN_POST.replace("Some fixes are invisible.", "Some fixes are invisible\u202freally.")
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert any("invisibles" in p for p in problems), problems


def test_missing_status_fails(tmp_path):
    # Sin Status no se sabe si el post se publico o quedo en borrador: el archivo miente.
    mod = load()
    post = CLEAN_POST.replace("**Status:** draft para revision de Gonzo\n", "")
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert any("Status" in p for p in problems)


def test_missing_niche_fails(tmp_path):
    mod = load()
    post = CLEAN_POST.replace("**Nicho:** a11y\n", "")
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert any("Nicho" in p for p in problems)


def test_english_spelling_of_niche_is_accepted(tmp_path):
    # 3 de los 10 posts vivos usan "Niche" y "Project" en ingles. Aceptar las dos grafias.
    mod = load()
    post = CLEAN_POST.replace("**Nicho:** a11y", "**Niche:** a11y").replace(
        "**Proyecto:** facebook/astryx", "**Project:** facebook/astryx"
    )
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert not problems, problems


def test_missing_pr_link_fails(tmp_path):
    # Sin el link al PR el post no es trazable al merge que lo origina.
    mod = load()
    post = CLEAN_POST.replace("https://github.com/facebook/astryx/pull/4605", "")
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert any("PR" in p for p in problems)


def test_spanish_body_fails(tmp_path):
    # El post publicable va en ingles; el reporte a Gonzo, en espanol.
    # El caso real es un post ENTERO en espanol (hay 2 vivos asi: base-ui y moderno), no
    # una frase suelta: el detector es de proporcion, y el fixture tiene que reflejar el
    # defecto que el gate caza.
    mod = load()
    path = seed(tmp_path, post=SPANISH_POST)
    problems, _ = mod.check_post(path, 14)
    assert any("espanol" in p or "español" in p for p in problems), problems


# --- el post: lo que AVISA pero no bloquea ---

def test_style_patterns_warn_but_do_not_block(tmp_path):
    # Las 6 categorias del anti-ai original son senales, no hechos. Un gate que reprima al
    # post canonico esta roto: "realm" puede ser la palabra correcta.
    mod = load()
    post = CLEAN_POST.replace(
        "Some fixes are invisible.",
        "Some fixes are invisible. In conclusion, however, this is worth mentioning - a testament "
        "to the seamless landscape of accessibility tooling.",
    )
    path = seed(tmp_path, post=post)
    problems, warnings = mod.check_post(path, 14)
    assert not problems, problems
    assert any("Muletillas" in w or "Cierre generico" in w for w in warnings)


def test_length_outside_window_warns_but_does_not_block(tmp_path):
    mod = load()
    path = seed(tmp_path, post=CLEAN_POST + "\n\n" + ("extra words here to push it over " * 30))
    problems, warnings = mod.check_post(path, 14)
    assert not problems, problems
    assert any("Longitud" in w for w in warnings)


def test_draft_status_warns_without_blocking(tmp_path):
    mod = load()
    path = seed(tmp_path)
    problems, warnings = mod.check_post(path, 14)
    assert not problems
    assert any("draft" in w.lower() for w in warnings)


def test_spanish_post_that_is_already_published_only_warns(tmp_path):
    # Correccion de diseno (2026-10-22): la regla "el post va en ingles" es de PUBLICACION, no de
    # archivo. En un post ya publicado el idioma es un HECHO: el gate no puede cambiar lo que ya
    # salio. Lo detecto el gate contra 2 posts reales de la cadena, publicados en espanol.
    mod = load()
    post = SPANISH_POST.replace("**Status:** draft para revision de Gonzo", "**Status:** PUBLICADO 24/08/2026")
    path = seed(tmp_path, post=post)
    problems, warnings = mod.check_post(path, 14)
    assert not problems, problems
    assert any("espanol" in w or "español" in w for w in warnings)


def test_a11y_post_in_spanish_fails_when_draft(tmp_path):
    # Regla del 2026-10-22: el idioma del post lo decide la MATERIA. Todo lo que sea a11y va en
    # ingles; todo lo demas, en espanol. Un post a11y en espanol no es estilo: es la regla rota.
    mod = load()
    post = SPANISH_POST  # ya es del nicho a11y
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert any("a11y" in p and "ingles" in p for p in problems), problems


def test_non_a11y_post_in_spanish_is_expected(tmp_path):
    # Al reves: un post que NO es a11y, en espanol, es lo que la regla pide. No puede fallar.
    mod = load()
    post = SPANISH_POST.replace("**Nicho:** a11y", "**Nicho:** Agentic / AI-Native")
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    # El mensaje de la rama "no es a11y" menciona "a11y" al decir que NO lo es, asi que el
    # assert tiene que ser especifico: la regla rota es "es del nicho a11y y va en ingles".
    assert not any("es del nicho a11y y la regla dice" in p for p in problems), problems


def test_spanish_draft_still_fails(tmp_path):
    # En un borrador si se puede corregir: ahi FALLA.
    mod = load()
    path = seed(tmp_path, post=SPANISH_POST)
    problems, _ = mod.check_post(path, 14)
    assert any("espanol" in p or "español" in p for p in problems), problems


def test_pr_link_required_only_when_header_declares_a_pr(tmp_path):
    # Un post sobre material propio (un refactor de un proyecto) no tiene merge que citar, y
    # exigirle un link seria un falso positivo. El gate lo pidio a un post de proyecto propio.
    mod = load()
    post = CLEAN_POST.replace("**PR:** #4605\n", "").replace(
        "PR: https://github.com/facebook/astryx/pull/4605", ""
    )
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert not any("PR" in p for p in problems), problems


def test_pr_link_required_when_header_declares_a_pr(tmp_path):
    mod = load()
    post = CLEAN_POST.replace("PR: https://github.com/facebook/astryx/pull/4605", "")
    path = seed(tmp_path, post=post)
    problems, _ = mod.check_post(path, 14)
    assert any("PR" in p for p in problems), problems


# --- el gate de cierre ---

def test_audit_detects_stale_draft(tmp_path):
    mod = load()
    seed(tmp_path)
    # Envejecer el archivo 20 dias.
    posts = tmp_path / "docs" / "linkedin" / "post-test.md"
    old = time.time() - (20 * 86400)
    os.utime(posts, (old, old))
    problems = mod.audit_chain(14, tmp_path)
    assert any("Draft vencido" in p for p in problems)


def test_audit_ignores_fresh_draft(tmp_path):
    mod = load()
    seed(tmp_path)
    problems = mod.audit_chain(14, tmp_path)
    assert not any("Draft vencido" in p for p in problems)


def test_audit_detects_merged_pr_without_post(tmp_path):
    mod = load()
    seed(tmp_path, merged=[("adobe/react-spectrum", "#10503")])
    problems = mod.audit_chain(14, tmp_path)
    assert any("Merges elegibles sin post" in p for p in problems)
    assert any("10503" in p for p in problems)


def test_audit_ignores_merged_pr_with_post(tmp_path):
    mod = load()
    seed(tmp_path, merged=[("facebook/astryx", "#4605")])
    problems = mod.audit_chain(14, tmp_path)
    assert not any("Merges elegibles sin post" in p for p in problems)


def test_audit_of_clean_chain_passes(tmp_path):
    mod = load()
    seed(tmp_path, merged=[("facebook/astryx", "#4605")])
    problems = mod.audit_chain(14, tmp_path)
    assert not problems, problems


def test_audit_reports_contributions_with_attributable_outcome(tmp_path):
    # Regla de branding del 2026-10-22: un review o colaboracion ES material de post cuando
    # tiene cambio atribuible. El gate lo AVISA (no falla): la 3ra condicion -detalle con
    # criterio- es un juicio del dueno, no del script.
    mod = load()
    root = tmp_path
    (root / "docs" / "linkedin").mkdir(parents=True, exist_ok=True)
    (root / "memory").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "linkedin" / "post.md").write_text(CLEAN_POST, encoding="utf-8")

    db = root / "memory" / "memory.db"
    con = sqlite3.connect(db)
    con.execute(
        "create table contributions (id integer primary key autoincrement, repo text not null, "
        "issue text, issue_url text, pr text, pr_url text, status text not null default 'open', "
        "detail text, context text, tier text, created_at text, updated_at text, "
        "tipo text not null default 'pr')"
    )
    con.execute(
        "insert into contributions (repo, pr, status, detail, tipo) values (?, ?, ?, ?, 'pr')",
        ("carbon-design-system/ibm-products", "9869", "comment",
         "Review de PR ajeno: el autor incorporo nuestra pregunta 1 y el PR se MERGED."),
    )
    con.commit()
    con.close()

    avisos = mod.audit_contributions(root)
    assert avisos and "9869" in avisos[0], avisos


def test_audit_ignores_contribution_whose_fix_came_from_another_author(tmp_path):
    # El credito del fix que llega a main via PR de otro autor es material de ENTREVISTA
    # (evidencia de proceso), no de LinkedIn. No es candidato.
    mod = load()
    root = tmp_path
    (root / "docs" / "linkedin").mkdir(parents=True, exist_ok=True)
    (root / "memory").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "linkedin" / "post.md").write_text(CLEAN_POST, encoding="utf-8")

    db = root / "memory" / "memory.db"
    con = sqlite3.connect(db)
    con.execute(
        "create table contributions (id integer primary key autoincrement, repo text not null, "
        "issue text, issue_url text, pr text, pr_url text, status text not null default 'open', "
        "detail text, context text, tier text, created_at text, updated_at text, "
        "tipo text not null default 'pr')"
    )
    con.execute(
        "insert into contributions (repo, pr, status, detail, tipo) values (?, ?, ?, ?, 'pr')",
        ("facebook/astryx", "#5107", "collab",
         "El fix llego a main via PR de otro autor (merged)."),
    )
    con.commit()
    con.close()

    assert not mod.audit_contributions(root)


# --- el final: distinguir el arbol limpio del sucio ---

def test_dirty_tree_fails_and_clean_tree_passes(tmp_path):
    mod = load()
    clean_root = tmp_path / "clean"
    clean = seed(clean_root, merged=[("facebook/astryx", "#4605")])
    assert not mod.check_post(clean, 14)[0]
    assert not mod.audit_chain(14, clean_root)

    dirty_root = tmp_path / "dirty"
    dirty = seed(
        dirty_root,
        post=CLEAN_POST.replace("**Nicho:** a11y\n", "").replace(
            "Some fixes are invisible.", "Some fixes are invisible — really."
        ),
        merged=[("adobe/react-spectrum", "#10503")],
    )
    problems, _ = mod.check_post(dirty, 14)
    assert len(problems) >= 2, problems
