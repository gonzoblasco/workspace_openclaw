#!/bin/bash
# Utilidades para la base de datos de memoria (memory/memory.db)
# Uso:
#   ./scripts/memory-db.sh export-daily [fecha]   - exporta un daily note a markdown
#   ./scripts/memory-db.sh export-all             - exporta todos los daily notes a memory/export/
#   ./scripts/memory-db.sh export-oss              - regenera docs/OSS-TRACKER.md desde la DB
#   ./scripts/memory-db.sh stats                   - muestra estadísticas de la DB
#   ./scripts/memory-db.sh todos                   - lista todos pendientes
#   ./scripts/memory-db.sh inbox                   - lista inbox
#   ./scripts/memory-db.sh contributions [estado]  - lista contribuciones OSS (opcional filtro por estado)
#   ./scripts/memory-db.sh add-todo "texto" [proyecto] - agrega un todo
#   ./scripts/memory-db.sh add-inbox "idea"       - agrega una idea al inbox
#   ./scripts/memory-db.sh learnings [categoria]  - lista lecciones (opcional filtro por categoria)
#   ./scripts/memory-db.sh add-learning <cat> "<titulo>" "<contenido>" [tags] - agrega una leccion
#   ./scripts/memory-db.sh export-learnings       - regenera docs/learnings/ desde la DB

DB="memory/memory.db"

case "$1" in
  export-daily)
    date="${2:-$(date +%F)}"
    sqlite3 "$DB" "SELECT content FROM daily_notes WHERE date='$date' AND type='daily' ORDER BY id DESC LIMIT 1;"
    ;;
  export-all)
    mkdir -p memory/export
    sqlite3 "$DB" "SELECT date, content FROM daily_notes WHERE type='daily' ORDER BY date;" | while IFS='|' read -r d c; do
      echo "$c" > "memory/export/$d.md"
    done
    echo "Exportados a memory/export/"
    ;;
  export-oss)
    # Regenera docs/OSS-TRACKER.md desde la DB
    {
      echo "# OSS-TRACKER.md - Open Source Contributions Tracker"
      echo ""
      echo "> Generado desde memory/memory.db (tabla contributions). Fuente de verdad: la DB."
      echo "> Regenerar con: ./scripts/memory-db.sh export-oss"
      echo ""
      echo "## Estado actual"
      echo ""
      echo "| Métrica | Valor |"
      echo "|---------|-------|"
      echo "| PRs abiertos | $(sqlite3 "$DB" "SELECT count(*) FROM contributions WHERE status IN ('open','waiting_review');") |"
      echo "| PRs mergeados | $(sqlite3 "$DB" "SELECT count(*) FROM contributions WHERE status='merged';") |"
      echo "| PRs cerrados sin merge | $(sqlite3 "$DB" "SELECT count(*) FROM contributions WHERE status='closed';") |"
      echo "| Repos con PRs | $(sqlite3 "$DB" "SELECT count(DISTINCT repo) FROM contributions;") |"
      echo ""
      echo "## PR Registry"
      echo ""
      sqlite3 "$DB" "SELECT repo FROM contributions GROUP BY repo ORDER BY repo;" | while read -r repo; do
        echo "### $repo"
        echo ""
        echo "| Eslabón | Link | Detalle |"
        echo "|---------|------|---------|"
        sqlite3 "$DB" "SELECT issue, issue_url, pr, pr_url, status, detail, context FROM contributions WHERE repo='$repo' ORDER BY id;" | while IFS='|' read -r issue iurl pr purl status detail context; do
          if [ -n "$issue" ]; then
            echo "| **Issue** | [$issue]($iurl) | $detail |"
          else
            echo "| **Issue** | - | $detail |"
          fi
          echo "| **Nuestro PR** | [$pr]($purl) | **$status** |"
          if [ -n "$context" ]; then
            echo "| **Contexto** | - | $context |"
          fi
          echo ""
        done
      done
    } > docs/OSS-TRACKER.md
    echo "OSS-TRACKER.md regenerado desde la DB."
    ;;
  export-todos)
    # Regenera memory/todos.md desde la DB (tabla todos)
    {
      echo "# TODO.md - Backlog de Tareas"
      echo ""
      echo "> Generado desde memory/memory.db (tabla todos). Fuente de verdad: la DB."
      echo "> Regenerar con: ./scripts/memory-db.sh export-todos"
      echo ""
      echo "## Abiertos"
      echo ""
      sqlite3 "$DB" "SELECT id, priority, project, text FROM todos WHERE status='open' ORDER BY priority DESC, id;" | while IFS='|' read -r id prio proj txt; do
        echo "- [ ] **[$proj]** ($prio) $txt"
      done
      echo ""
      echo "## Completados"
      echo ""
      sqlite3 "$DB" "SELECT id, project, text FROM todos WHERE status='done' ORDER BY id DESC;" | while IFS='|' read -r id proj txt; do
        echo "- [x] **[$proj]** $txt"
      done
      echo ""
    } > memory/todos.md
    echo "memory/todos.md regenerado desde la DB."
    ;;
  export-inbox)
    # Regenera memory/inbox.md desde la DB (tabla inbox)
    {
      echo "# INBOX.md - Ideas y Referencias"
      echo ""
      echo "> Generado desde memory/memory.db (tabla inbox). Fuente de verdad: la DB."
      echo "> Regenerar con: ./scripts/memory-db.sh export-inbox"
      echo ""
      echo "## Abiertas"
      echo ""
      sqlite3 "$DB" "SELECT id, idea FROM inbox WHERE status='open' ORDER BY id;" | while IFS='|' read -r id idea; do
        echo "- **#$id** $idea"
      done
      echo ""
    } > memory/inbox.md
    echo "memory/inbox.md regenerado desde la DB."
    ;;
  stats)
    echo "=== Daily notes ==="
    sqlite3 "$DB" "SELECT type, count(*) FROM daily_notes GROUP BY type;"
    echo "=== Todos ==="
    sqlite3 "$DB" "SELECT status, count(*) FROM todos GROUP BY status;"
    echo "=== Inbox ==="
    sqlite3 "$DB" "SELECT status, count(*) FROM inbox GROUP BY status;"
    echo "=== Contribuciones ==="
    sqlite3 "$DB" "SELECT status, count(*) FROM contributions GROUP BY status;"
    echo "=== Learnings ==="
    sqlite3 "$DB" "SELECT category, count(*) FROM learnings GROUP BY category;"
    ;;
  todos)
    sqlite3 -header -column "$DB" "SELECT id, status, priority, project, text FROM todos ORDER BY status, priority DESC;"
    ;;
  inbox)
    sqlite3 -header -column "$DB" "SELECT id, status, substr(idea,1,60) AS idea FROM inbox ORDER BY id DESC;"
    ;;
  contributions)
    filter="${2:-%}"
    sqlite3 -header -column "$DB" "SELECT repo, pr, status, substr(detail,1,50) AS detail FROM contributions WHERE status LIKE '$filter' ORDER BY repo;"
    ;;
  add-todo)
    text="$2"; project="${3:-}"
    sqlite3 "$DB" "INSERT INTO todos (text, project) VALUES ('$text', '$project');"
    echo "Todo agregado."
    ;;
  add-inbox)
    idea="$2"
    sqlite3 "$DB" "INSERT INTO inbox (idea) VALUES ('$idea');"
    echo "Idea agregada al inbox."
    ;;
  learnings)
    cat_filter="${2:-%}"
    sqlite3 -header -column "$DB" "SELECT id, category, substr(title,1,60) AS title, substr(tags,1,40) AS tags FROM learnings WHERE category LIKE '$cat_filter' ORDER BY category, id;"
    ;;
  add-learning)
    cat="$2"; title="$3"; content="$4"; tags="${5:-}"
    sqlite3 "$DB" "INSERT INTO learnings (category, title, content, tags) VALUES ('$cat', '$title', '$content', '$tags');"
    echo "Leccion agregada (categoria: $cat)."
    ;;
  export-learnings)
    # Regenera docs/learnings/ desde la DB (tabla learnings)
    mkdir -p docs/learnings
    # README indice
    {
      echo "# Learnings por categoria"
      echo ""
      echo "> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB."
      echo "> Regenerar con: ./scripts/memory-db.sh export-learnings"
      echo ""
      echo "## Como consultar"
      echo ""
      echo "Segun el tipo de tarea, abrir el archivo de esa categoria. Consulta rapida desde la DB:"
      echo ""
      echo "\`\`\`bash"
      echo "./scripts/memory-db.sh learnings <categoria>"
      echo "\`\`\`"
      echo ""
      echo "## Categorias"
      echo ""
      sqlite3 "$DB" "SELECT category, count(*) FROM learnings GROUP BY category ORDER BY category;" | while IFS='|' read -r cat n; do
        echo "- **[$cat](docs/learnings/$cat.md)** - $n lecciones"
      done
      echo ""
      echo "## Total"
      echo ""
      echo "$(sqlite3 "$DB" "SELECT count(*) FROM learnings;") lecciones en total."
    } > docs/learnings/README.md
    # Un archivo por categoria. Iterar por id para manejar contenido multilinea
    # sin romper el parseo (cada campo se lee por separado).
    sqlite3 "$DB" "SELECT DISTINCT category FROM learnings ORDER BY category;" | while read -r cat; do
      out="docs/learnings/$cat.md"
      {
        echo "# Learnings - $cat"
        echo ""
        echo "> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB."
        echo ""
      } > "$out"
      sqlite3 "$DB" "SELECT id FROM learnings WHERE category='$cat' ORDER BY id;" | while read -r id; do
        title=$(sqlite3 "$DB" "SELECT title FROM learnings WHERE id=$id;")
        content=$(sqlite3 "$DB" "SELECT content FROM learnings WHERE id=$id;")
        tags=$(sqlite3 "$DB" "SELECT tags FROM learnings WHERE id=$id;")
        {
          echo "## $title"
          echo ""
          echo "$content"
          echo ""
          if [ -n "$tags" ]; then
            echo "**Tags:** $tags"
            echo ""
          fi
          echo "---"
          echo ""
        } >> "$out"
      done
    done
    echo "docs/learnings/ regenerado desde la DB."
    ;;
  *)
    echo "Uso: $0 {export-daily|export-all|export-oss|export-todos|export-inbox|stats|todos|inbox|contributions|add-todo|add-inbox|learnings|add-learning|export-learnings}"
    ;;
esac
