#!/usr/bin/env python3
"""
check-agent-skill-boundary.py - Verifica que la frontera entre el arbol del CORE y
los arboles de rol se respeta.

POR QUE EXISTE (2026-09-29). El CORE escribio codigo de produccion de un proyecto
durante toda una sesion: migraciones SQL, el cliente de datos, una pantalla de
revision completa y un e2e de Playwright. Eso es el dominio de kanam-dev. La regla
estaba escrita (SKILLS-INDEX.md seccion 2.4, ADR-073, ADR-074) y NADIE la verificaba:
`scripts/dispatch-validation.sh` existe, es lo que los docs citan como "lo verifica",
y es un chequeo VOLUNTARIO - hay que pasarle el nombre de la skill, asi que si el
CORE no lo corre no pasa nada. Peor: no mira lo que ocurrio, solo responde "¿esta
skill existe en otro agente?".

La causa mecanica fue esta: las 9 skills del ciclo de desarrollo (Hermes SDD) vivian
en `skills/`, el arbol que ve el CORE. `hermes-builder` dice, textualmente,
"implementation. Writes the change's code". El CORE tenia el playbook de ingenieria
en su catalogo y lo ejecuto.

Que revisa:
  1. CICLO SDD EN EL ARBOL DEL CORE - una skill del ciclo de desarrollo en `skills/`.
     Es la causa raiz; este es el check que la caza.
  2. SKILL EN DOS ARBOLES  - un duplicado anula la separacion: si la skill tambien
     esta en `skills/`, el CORE la ve y la puede ejecutar.
  3. CICLO SDD INCOMPLETO   - el ciclo tiene que estar completo en su arbol de rol.
     Un movimiento a medias pierde etapas sin que nada lo diga.

Las rutas son inyectables (`root` como parametro) para que los tests construyan
arboles falsos en un directorio temporal, y para que el defecto se siembre en un
corpus descartable y no en el workspace real.

Uso:
    check-agent-skill-boundary.py
Salida: exit 0 si la frontera se respeta, 1 si hay violaciones.
"""

import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent

# El ciclo de desarrollo, explicito y no derivado. Deliberado: la regla es "estas
# skills pertenecen al rol de ingenieria", y una lista explicita sigue valiendo
# aunque alguien las borre de su arbol de rol y las reponga en el del CORE.
# Derivar de `agents/kanam-dev/skills/` debilitaria el check justo en el caso que
# existe para prevenir.
SDD_CYCLE: Tuple[str, ...] = (
    "hermes-discovery",
    "hermes-openspec",
    "hermes-architect",
    "hermes-planner",
    "hermes-builder",
    "hermes-reviewer",
    "hermes-pr-reviewer",
    "hermes-qa",
    "hermes-release",
)

# El rol dueno del ciclo de desarrollo.
SDD_ROLE = "kanam-dev"

CORE_TREE = "skills"


def role_trees(root: Path) -> List[Path]:
    """Los arboles de skills de cada rol, por convencion `agents/<rol>/skills/`."""
    agents = root / "agents"
    if not agents.is_dir():
        return []
    return sorted(
        p for p in agents.glob("*/skills") if p.is_dir()
    )


def skill_names(tree: Path) -> List[str]:
    """Los slugs de skill dentro de un arbol: directorios con un SKILL.md."""
    if not tree.is_dir():
        return []
    return sorted(
        d.name for d in tree.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()
    )


def find_violations(root: Path) -> List[str]:
    """Devuelve las violaciones de la frontera, como textos listos para imprimir."""
    violations: List[str] = []
    core = root / CORE_TREE
    core_skills = skill_names(core)

    # 1) El ciclo de desarrollo no vive en el arbol del CORE.
    for name in SDD_CYCLE:
        if name in core_skills:
            violations.append(
                "SDD skill in the Core tree: %s/%s/ - this skill belongs to the %s "
                "role. While the Core can see it, the Core can execute it." % (CORE_TREE, name, SDD_ROLE)
            )

    # 2) Ninguna skill vive en dos arboles: un duplicado anula la separacion.
    role_membership = {}  # type: dict
    for tree in role_trees(root):
        role = tree.parent.name
        for name in skill_names(tree):
            role_membership.setdefault(name, []).append(role)

    for name, roles in sorted(role_membership.items()):
        if name in core_skills:
            violations.append(
                "skill in two trees: %s is in %s/ (Core) and in %s. A shared skill "
                "is visible to the Core again, which is what the split exists to "
                "prevent." % (name, CORE_TREE, ", ".join(roles))
            )
        if len(roles) > 1:
            violations.append(
                "skill in two role trees: %s is in %s. One owner per skill."
                % (name, ", ".join(roles))
            )

    # 3) El ciclo de desarrollo esta completo en su arbol de rol.
    sdd_tree = root / "agents" / SDD_ROLE / "skills"
    if sdd_tree.is_dir():
        owned = set(skill_names(sdd_tree))
        for name in SDD_CYCLE:
            if name not in owned:
                violations.append(
                    "SDD cycle incomplete: %s is not in agents/%s/skills/ - the cycle "
                    "lost a stage." % (name, SDD_ROLE)
                )

    return violations


def main(argv: List[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else ROOT
    if not (root / 'skills').is_dir() and not (root / 'agents').is_dir():
        print("ERROR no hay skills/ ni agents/ bajo %s; no se pudo correr (exit 3)"
              % root, file=sys.stderr)
        return 3

    violations = find_violations(root)

    if violations:
        print("FRONTERA DE SKILLS VIOLADA (%d):" % len(violations))
        for v in violations:
            print("  - " + v)
        print()
        print(
            "El CORE no ejecuta el ciclo de desarrollo. Las skills de un rol viven en "
            "su arbol (agents/<rol>/skills/), nunca en skills/."
        )
        return 1

    print(
        "OK: frontera de skills respetada (%d skills del ciclo SDD en agents/%s/skills/, "
        "0 en %s/, 0 duplicados)." % (len(SDD_CYCLE), SDD_ROLE, CORE_TREE)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
