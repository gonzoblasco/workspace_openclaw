#!/usr/bin/env python3
"""Migra docs/LEARNINGS.md a la tabla learnings de memory/memory.db.

Clasifica cada seccion (##) en una categoria. Las sub-secciones (###) de la
consolidacion del 2026-08-23 se tratan como lecciones individuales.

Uso: python3 scripts/migrate-learnings.py
"""
import re
import sqlite3
import sys

DB = "memory/memory.db"
SRC = "docs/LEARNINGS.md"

# Mapeo explicito: fragmento del titulo -> categoria
# Orden importa: se evalua en orden, primera coincidencia gana.
CATEGORY_RULES = [
    # a11y / accesibilidad
    ("role=\"presentation\"", "a11y"),
    ("aria-orientation", "a11y"),
    ("Portfolio de accesibilidad", "a11y"),
    ("Colaboración OSS: astryx #4914 + radix #4109", "a11y"),
    ("radix-ui: cuando alguien implementa tu análisis", "a11y"),
    ("Reviews de bots pueden detectar regresiones", "a11y"),
    # pipeline de agentes / IA
    ("Cross-review multi-ronda", "pipeline-agentes"),
    ("El cross-review puede INTRODUCIR bugs", "pipeline-agentes"),
    ("Delegar a Qwen Code", "pipeline-agentes"),
    ("modelo cloud de IA en loops", "pipeline-agentes"),
    # infraestructura / setup
    ("Service worker cache", "infraestructura"),
    ("Template literals", "infraestructura"),
    ("Double-click is not double-tap", "infraestructura"),
    ("Build is the real quality gate", "infraestructura"),
    ("Orphaned submodule", "infraestructura"),
    ("Refactorización del setup", "infraestructura"),
    ("Compatibilidad en cascada", "infraestructura"),
    ("Tailwind 4 utilities", "infraestructura"),
    ("Dockerizar un stack cloud", "infraestructura"),
    ("Sync de workspace", "infraestructura"),
    ("OpenClaw no mostraba los modelos", "infraestructura"),
    ("memory-wiki como capa analítica", "infraestructura"),
    # proyectos
    ("SoporteML v3: estructura de doble git", "proyectos"),
    ("soporteml-v3: modelo cloud", "proyectos"),
    ("Estructura de estudio gamificada", "proyectos"),
    ("Tormenta de ideas", "proyectos"),
    ("Skill consolidation", "proyectos"),
    ("Consolidación no-dev", "proyectos"),
    ("Narrativa del pipeline", "proyectos"),
    # metodologia
    ("Documentation at milestone end", "metodologia"),
    ("Patrón por inercia", "metodologia"),
    ("Reflexión del curso", "metodologia"),
    ("Godot: aprender juntos", "metodologia"),
    ("Skill Workshop stale", "metodologia"),
    ("MCP server", "metodologia"),
    ("Export templates de Godot", "metodologia"),
    ("Sport Cars", "metodologia"),
    ("Feature flags portable", "metodologia"),
    ("No commitear mockups", "metodologia"),
    ("npm 404", "metodologia"),
    ("npm login", "metodologia"),
    ("AI Engineering Bootcamp", "metodologia"),
    # oss (default para lo que mencione PRs/OSS)
    ("OSS", "oss"),
    ("astryx", "oss"),
    ("radix", "oss"),
    ("zod", "oss"),
    ("PRs", "oss"),
    ("Em dash", "oss"),
    ("Triage de PRs", "oss"),
    ("Buscar oportunidades OSS", "oss"),
    ("Serializers de hash", "oss"),
    ("Verificar el estado real de los PRs", "oss"),
]

# Categorias por defecto para las sub-secciones de la consolidacion 2026-08-23
SUBSECTION_DEFAULT = {
    "Godot: aprender juntos": "metodologia",
    "Skill Workshop stale": "metodologia",
    "MCP server": "metodologia",
    "Export templates de Godot": "metodologia",
    "Sport Cars": "metodologia",
    "Feature flags portable": "metodologia",
    "No commitear mockups": "metodologia",
    "npm 404": "metodologia",
    "npm login": "metodologia",
    "AI Engineering Bootcamp": "metodologia",
    "Patrón por inercia": "metodologia",
    "Reflexión del curso": "metodologia",
}


def classify(title):
    for frag, cat in CATEGORY_RULES:
        if frag.lower() in title.lower():
            return cat
    return "metodologia"  # fallback


def parse_sections(text):
    """Devuelve lista de (titulo, contenido) para cada seccion ## y ###.

    Las sub-secciones ### se tratan como lecciones individuales (cada una
    con su categoria), en lugar de agruparse bajo la seccion ## padre.
    """
    lines = text.split("\n")
    sections = []
    current = None
    for line in lines:
        if line.startswith("## ") or line.startswith("### "):
            if current:
                sections.append(current)
            # quitar el prefijo de nivel y quedarse con el titulo
            title = line.lstrip("# ").strip()
            current = [title, []]
        elif current is not None:
            current[1].append(line)
    if current:
        sections.append(current)
    return sections


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()

    # Quitar el encabezado (hasta el primer ##)
    idx = text.find("## ")
    if idx == -1:
        print("No se encontraron secciones")
        sys.exit(1)
    body = text[idx:]

    sections = parse_sections(body)

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Limpiar tabla si ya tiene datos (migracion idempotente)
    cur.execute("DELETE FROM learnings")

    count = 0
    for title, content_lines in sections:
        content = "\n".join(content_lines).strip()
        if not content:
            continue
        # Saltar la seccion contenedora de la consolidacion (solo intro, sin leccion propia)
        if title.startswith("2026-08-23 - Consolidación de lecciones"):
            continue
        cat = classify(title)
        # tags simples derivados del titulo
        tags = title.split(" - ")[-1] if " - " in title else title
        cur.execute(
            "INSERT INTO learnings (category, title, content, tags) VALUES (?, ?, ?, ?)",
            (cat, title, content, tags),
        )
        count += 1

    conn.commit()
    conn.close()
    print(f"Migradas {count} lecciones a la tabla learnings.")


if __name__ == "__main__":
    main()
