#!/usr/bin/env python3
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Configuración
BASE_DIR = Path("/Users/gonzoblasco/.openclaw/workspace/.knowledge/entities")
CATEGORIES = ["people", "companies", "projects"]

def record_entity(name, category, fact, source="session"):
    if category not in CATEGORIES:
        print(f"Error: Categoría inválida. Use: {CATEGORIES}")
        sys.exit(1)

    entity_dir = BASE_DIR / category
    entity_dir.mkdir(parents=True, exist_ok=True)
    
    # Normalizar nombre para archivos
    safe_name = name.lower().replace(" ", "_")
    jsonl_path = entity_dir / f"{safe_name}.jsonl"
    md_path = entity_dir / f"{safe_name}.md"

    # 1. Escribir en JSONL (Append-only)
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "fact": fact,
        "source": source
    }
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 2. Manejar el Markdown Summary
    if not md_path.exists():
        # Crear summary inicial
        content = f"# {name}\n\n**Categoría:** {category}\n\n## Resumen\n{fact}\n\n## Hechos Recientes\n- {fact} (desde {source})\n"
        md_path.write_text(content, encoding="utf-8")
        print(f"✅ Entidad nueva creada: {name}")
    else:
        # Agregar al summary si es relevante (simplificado: agregar a la lista de hechos)
        with open(md_path, "a", encoding="utf-8") as f:
            f.write(f"\n- {fact} (desde {source})")
        print(f"✅ Hecho agregado a {name}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python3 record_entity.py <nombre> <categoría> <hecho> [fuente]")
        sys.exit(1)
    
    name = sys.argv[1]
    cat = sys.argv[2]
    fct = sys.argv[3]
    src = sys.argv[4] if len(sys.argv) > 4 else "session"
    
    record_entity(name, cat, fct, src)
