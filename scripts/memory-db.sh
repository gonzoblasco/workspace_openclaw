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
#   ./scripts/memory-db.sh add-contribution <repo> <pr> <pr_url> <status> "<detail>" [context] [issue] [issue_url] [tier] [tipo]
#     - registra una contribucion OSS en la DB (tipo default 'pr'; 'collab' para no-codigo)
#   ./scripts/memory-db.sh add-todo "texto" [proyecto] - agrega un todo
#   ./scripts/memory-db.sh edit-todo <id> "texto"    - reescribe el texto de un todo
#   ./scripts/memory-db.sh done-todo <id>            - marca un todo como hecho
#   ./scripts/memory-db.sh reopen-todo <id>          - reabre un todo
#   ./scripts/memory-db.sh set-todo-priority <id> <high|medium|low> - cambia la prioridad
#   ./scripts/memory-db.sh add-inbox "idea"       - agrega una idea al inbox
#   ./scripts/memory-db.sh learnings [categoria]  - lista lecciones (opcional filtro por categoria)
#   ./scripts/memory-db.sh add-learning <cat> "<titulo>" "<contenido>" [tags] - agrega una leccion
#     El contenido puede ser: texto directo, @archivo (lee el archivo), o - (lee de stdin)
#     para contenidos multilinea largos sin problemas de quoting del shell.
#   ./scripts/memory-db.sh export-learnings       - regenera docs/learnings/ desde la DB
#   ./scripts/memory-db.sh catalog                - cataloga memoria en DB relacional + embeddings (memory-catalog-v2.py)
#   ./scripts/memory-db.sh search "<query>" [n]  - busqueda semantica sobre la memoria (memory-search.py)
#   ./scripts/memory-db.sh topics                - lista topics con frecuencia
#   ./scripts/memory-db.sh recent [n]             - lista sesiones recientes

# Permite apuntar a otra DB (para probar sobre una copia sin tocar la real).
# Los scripts de Python ya respetan MEMORY_DB; esto los alinea.
DB="${MEMORY_DB:-memory/memory.db}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Escape comillas simples para interpolacion SQL segura (evita SQL injection / broken quoting)
sql_escape() {
  printf '%s' "$1" | sed "s/'/''/g"
}

# CLI de sqlite3 con las FOREIGN KEYS ACTIVAS.
#
# `PRAGMA foreign_keys` es por conexion y viene APAGADA por defecto: declarar la
# FK en el schema no alcanza. Medido el 2026-09-23: la DB tenia 6 FK declaradas y
# 0 activas, y por eso se acumularon huerfanos que hubo que limpiar a mano.
# Toda escritura pasa por aca para que la integridad se aplique siempre.
# (Los SELECT tambien lo llevan: activarlo en lectura no rompe nada y mantiene un
# unico camino de acceso.)
db() {
  sqlite3 -cmd "PRAGMA foreign_keys = ON" "$DB" "$@"
}

case "$1" in
  catalog)
    # Cataloga memoria en DB relacional + embeddings
    python3 "$SCRIPT_DIR/memory-catalog-v2.py"
    ;;
  search)
    # Busqueda semantica sobre la memoria
    query="${2:-}"
    if [ -z "$query" ]; then
      echo "Uso: $0 search \"<query>\" [top_n]" >&2
      exit 1
    fi
    top_n="${3:-5}"
    python3 "$SCRIPT_DIR/memory-search.py" "$query" --top "$top_n"
    ;;
  topics)
    python3 "$SCRIPT_DIR/memory-search.py" --topics
    ;;
  topics-cluster)
    # Descubre topics emergentes via K-means clustering
    python3 "$SCRIPT_DIR/memory-topics.py" --refresh
    ;;
  topics-list)
    python3 "$SCRIPT_DIR/memory-topics.py" --list
    ;;
  recent)
    n="${2:-10}"
    python3 "$SCRIPT_DIR/memory-search.py" --recent "$n"
    ;;
  export-daily)
    date="${2:-$(date +%F)}"
    sqlite3 "$DB" "SELECT content FROM daily_notes WHERE date='$date' AND type='daily' ORDER BY id DESC LIMIT 1;"
    ;;
    export-all)
    # Nueva ubicación: archivado de sesiones en docs/archives/sesiones/
    mkdir -p docs/archives/sesiones
    # Robust: una consulta por fecha (el contenido markdown es multilinea).
    dates=$(sqlite3 "$DB" "SELECT DISTINCT date FROM daily_notes WHERE type='daily' ORDER BY date;")
    count=0
    while IFS= read -r date; do
      [[ -z "$date" ]] && continue
      sqlite3 "$DB" "SELECT content FROM daily_notes WHERE date='$date' AND type='daily' ORDER BY id DESC LIMIT 1;" > "docs/archives/sesiones/$date.md"
      count=$((count + 1))
    done <<< "$dates"
    echo "Exportados $count dailies a docs/archives/sesiones/"
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
      echo "| PRs abiertos | $(sqlite3 "$DB" "SELECT count(*) FROM contributions WHERE tipo='pr' AND status IN ('open','waiting_review');") |"
      echo "| PRs mergeados | $(sqlite3 "$DB" "SELECT count(*) FROM contributions WHERE tipo='pr' AND status='merged';") |"
      echo "| PRs cerrados sin merge | $(sqlite3 "$DB" "SELECT count(*) FROM contributions WHERE tipo='pr' AND status='closed';") |"
      echo "| Colaboraciones no-codigo | $(sqlite3 "$DB" "SELECT count(*) FROM contributions WHERE tipo='collab';") |"
      echo "| Repos con contribuciones | $(sqlite3 "$DB" "SELECT count(DISTINCT repo) FROM contributions;") |"
      echo ""
      echo "## PR Registry"
      echo ""
      sqlite3 "$DB" "SELECT repo FROM contributions WHERE tipo='pr' GROUP BY repo ORDER BY repo;" | while read -r repo; do
        echo "### $repo"
        echo ""
        echo "| Eslabón | Link | Detalle |"
        echo "|---------|------|---------|"
        sqlite3 "$DB" "SELECT issue, issue_url, pr, pr_url, status, detail, context FROM contributions WHERE repo='$repo' AND tipo='pr' ORDER BY id;" | while IFS='|' read -r issue iurl pr purl status detail context; do
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
      echo "## Colaboraciones no-codigo"
      echo ""
      echo "> Contribuciones donde el aporte de Gonzo fue comentario, review, audit o diagnostico (no un PR con merge a su nombre). Impacto real via PRs de otros o conversaciones."
      echo ""
      echo "| Repo | Eslabón | Detalle |"
      echo "|------|---------|---------|"
      sqlite3 "$DB" "SELECT repo, issue, issue_url, pr, pr_url, detail, context FROM contributions WHERE tipo='collab' ORDER BY repo, id;" | while IFS='|' read -r repo issue iurl pr purl detail context; do
        # armar link del eslabon (issue o pr)
        if [ -n "$issue" ] && [ -n "$iurl" ]; then
          eslabon="[$issue]($iurl)"
        elif [ -n "$pr" ] && [ -n "$purl" ]; then
          eslabon="[$pr]($purl)"
        else
          eslabon="-"
        fi
        echo "| $repo | $eslabon | $detail |"
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
  oss-rows)
    # Filas en formato pipe para consumo programatico (widget/sync): id|repo|pr|tipo|status|detail|context|pr_url
    # Filtro opcional por tipo (pr|collab); sin filtro lista todo.
    filter="${2:-}"
    if [ -n "$filter" ]; then
      sqlite3 "$DB" "SELECT id, repo, COALESCE(pr,'-'), tipo, status, detail, COALESCE(context,''), COALESCE(pr_url,'') FROM contributions WHERE tipo = '$filter' ORDER BY repo, id;"
    else
      sqlite3 "$DB" "SELECT id, repo, COALESCE(pr,'-'), tipo, status, detail, COALESCE(context,''), COALESCE(pr_url,'') FROM contributions ORDER BY repo, id;"
    fi
    ;;
  update-contribution)
    # Firma: update-contribution <id> <status> ["<detail>"] ["<context>"] ["<pr_url>"]
    # Actualiza solo los campos pasados no vacios; status es obligatorio (usar '-' para no tocar).
    id="$2"; status="${3:-}"
    detail="${4:-}"; context="${5:-}"; pr_url="${6:-}"
    if [ -z "$id" ] || [ -z "$status" ]; then
      echo "Error: faltan id o status." >&2
      echo "Uso: $0 update-contribution <id> <status> [detail] [context] [pr_url]" >&2
      exit 1
    fi
    sets="status='$(sql_escape "$status")'"
    if [ -n "$detail" ]; then sets="$sets, detail='$(sql_escape "$detail")'"; fi
    if [ -n "$context" ]; then sets="$sets, context='$(sql_escape "$context")'"; fi
    if [ -n "$pr_url" ]; then sets="$sets, pr_url='$(sql_escape "$pr_url")'"; fi
    db "UPDATE contributions SET $sets WHERE id='$(sql_escape "$id")'; SELECT 'Contribucion actualizada: ' || changes() || ' fila(s).';"
    ;;
  oss-sync-status)
    # Muestra la metadata de sync de la tabla oss_sync.
    sqlite3 -header -column "$DB" "CREATE TABLE IF NOT EXISTS oss_sync (repo TEXT NOT NULL, pr TEXT NOT NULL, last_checked TEXT, state TEXT, merged TEXT, mergeable_state TEXT, comments INTEGER, updated_at TEXT, PRIMARY KEY (repo, pr));"
    sqlite3 -header -column "$DB" "SELECT repo, pr, last_checked, state, mergeable_state, comments, updated_at FROM oss_sync ORDER BY repo, pr;"
    ;;
  add-todo)
    text="$2"; project="${3:-}"
    text_esc=$(sql_escape "$text")
    project_esc=$(sql_escape "$project")
    db "INSERT INTO todos (text, project) VALUES ('$text_esc', '$project_esc');"
    echo "Todo agregado."
    ;;
  add-inbox)
    idea="$2"
    idea_esc=$(sql_escape "$idea")
    db "INSERT INTO inbox (idea) VALUES ('$idea_esc');"
    echo "Idea agregada al inbox."
    ;;
  done-todo)
    # Firma: done-todo <id> - marca un todo como hecho y regenera el .md
    id="$2"
    if [ -z "$id" ]; then
      echo "Error: falta el id." >&2
      echo "Uso: $0 done-todo <id>" >&2
      exit 1
    fi
    # Sin pipe: el `exit 1` tiene que correr en el shell principal, no en un
    # subshell (dentro de un pipe no cambia el exit code del script).
    n=$(db "UPDATE todos SET status='done', done_at=datetime('now') WHERE id='$(sql_escape "$id")'; SELECT changes();")
    if [ "$n" = "0" ]; then
      echo "Error: no existe un todo con id $id." >&2
      exit 1
    fi
    echo "Todo $id marcado como hecho."
    "$0" export-todos > /dev/null
    ;;
  reopen-todo)
    # Firma: reopen-todo <id> - vuelve un todo a 'open' y regenera el .md
    id="$2"
    if [ -z "$id" ]; then
      echo "Error: falta el id." >&2
      echo "Uso: $0 reopen-todo <id>" >&2
      exit 1
    fi
    n=$(db "UPDATE todos SET status='open', done_at=NULL WHERE id='$(sql_escape "$id")'; SELECT changes();")
    if [ "$n" = "0" ]; then
      echo "Error: no existe un todo con id $id." >&2
      exit 1
    fi
    echo "Todo $id reabierto."
    "$0" export-todos > /dev/null
    ;;
  triage-inbox)
    # Firma: triage-inbox <id> - marca una idea del inbox como triaged y regenera el .md
    id="$2"
    if [ -z "$id" ]; then
      echo "Error: falta el id." >&2
      echo "Uso: $0 triage-inbox <id>" >&2
      exit 1
    fi
    n=$(db "UPDATE inbox SET status='triaged' WHERE id='$(sql_escape "$id")'; SELECT changes();")
    if [ "$n" = "0" ]; then
      echo "Error: no existe una idea con id $id." >&2
      exit 1
    fi
    echo "Idea $id marcada como triaged."
    "$0" export-inbox > /dev/null
    ;;
  set-todo-priority)
    # Firma: set-todo-priority <id> <high|medium|low> - cambia la prioridad y regenera el .md
    id="$2"; prio="$3"
    case "$prio" in
      high|medium|low) ;;
      *) echo "Error: prioridad invalida '$prio' (usar high|medium|low)." >&2; exit 1 ;;
    esac
    n=$(db "UPDATE todos SET priority='$(sql_escape "$prio")' WHERE id='$(sql_escape "$id")'; SELECT changes();")
    if [ "$n" = "0" ]; then
      echo "Error: no existe un todo con id $id." >&2
      exit 1
    fi
    echo "Todo $id -> prioridad $prio."
    "$0" export-todos > /dev/null
    ;;
  edit-todo)
    # Firma: edit-todo <id> "texto" - reescribe el texto de un todo y regenera el .md
    id="$2"; text="$3"
    if [ -z "$id" ] || [ -z "$text" ]; then
      echo "Error: falta el id o el texto." >&2
      echo "Uso: $0 edit-todo <id> \"texto\"" >&2
      exit 1
    fi
    n=$(db "UPDATE todos SET text='$(sql_escape "$text")' WHERE id='$(sql_escape "$id")'; SELECT changes();")
    if [ "$n" = "0" ]; then
      echo "Error: no existe un todo con id $id." >&2
      exit 1
    fi
    echo "Todo $id reescrito."
    "$0" export-todos > /dev/null
    ;;
  update-ficha)
    # Firma: update-ficha <id> [--title <t>] [--tags <a,b>]
    # Solo toca campos pasados. Los tags se normalizan a JSON array.
    id="$2"; shift 2 2>/dev/null || true
    sets=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --title)
          t="$(sql_escape "$2")"
          sets="$sets, title='$t'"
          shift 2
          ;;
        --tags)
          j="[$(printf '%s' "$2" | tr ',' '\n' | sed '/^$/d' | sed 's/^ *//; s/ *$//' | sed 's/"/\\"/g' | sed 's/.*/"&"/' | paste -sd, -)]"
          jesc="$(sql_escape "$j")"
          sets="$sets, tags='$jesc'"
          shift 2
          ;;
        *)
          echo "Error: opcion desconocida '$1'." >&2
          echo "Uso: $0 update-ficha <id> [--title <t>] [--tags <a,b>]" >&2
          exit 1
          ;;
      esac
    done
    if [ -z "$sets" ] || [ -z "$id" ]; then
      echo "Error: falta id o ningun campo para actualizar." >&2
      echo "Uso: $0 update-ficha <id> [--title <t>] [--tags <a,b>]" >&2
      exit 1
    fi
    sets="${sets#, }"
    n=$(db "UPDATE sessions_relacional SET $sets WHERE id='$(sql_escape "$id")'; SELECT changes();")
    if [ "$n" = "0" ]; then
      echo "Error: no existe una ficha con id $id." >&2
      exit 1
    fi
    echo "Ficha $id actualizada."
    ;;
  add-contribution)
    # Firma: add-contribution <repo> <pr> <pr_url> <status> "<detail>" ["<context>"] ["<issue>"] ["<issue_url>"] ["<tier>"] ["<tipo>"]
    # Campos opcionales: context, issue, issue_url, tier (default 1..3), tipo (default 'pr', collab para no-codigo).
    repo="$2"; pr="$3"; pr_url="$4"; status="$5"; detail="$6"
    context="${7:-}"; issue="${8:-}"; issue_url="${9:-}"; tier="${10:-}"; tipo="${11:-pr}"
    if [ -z "$repo" ] || [ -z "$pr" ] || [ -z "$pr_url" ] || [ -z "$status" ] || [ -z "$detail" ]; then
      echo "Error: faltan argumentos obligatorios." >&2
      echo "Uso: $0 add-contribution <repo> <pr> <pr_url> <status> \"<detail>\" [context] [issue] [issue_url] [tier] [tipo]" >&2
      exit 1
    fi
    repo_esc=$(sql_escape "$repo"); pr_esc=$(sql_escape "$pr"); pr_url_esc=$(sql_escape "$pr_url")
    status_esc=$(sql_escape "$status"); detail_esc=$(sql_escape "$detail"); context_esc=$(sql_escape "$context")
    issue_esc=$(sql_escape "$issue"); issue_url_esc=$(sql_escape "$issue_url"); tier_esc=$(sql_escape "$tier"); tipo_esc=$(sql_escape "$tipo")
    db "INSERT INTO contributions (repo, issue, issue_url, pr, pr_url, status, detail, context, tier, tipo) VALUES ('$repo_esc', '$issue_esc', '$issue_url_esc', '$pr_esc', '$pr_url_esc', '$status_esc', '$detail_esc', '$context_esc', '$tier_esc', '$tipo_esc'); SELECT 'Contribucion agregada (id ' || last_insert_rowid() || ').';"
    ;;
  learnings)
    cat_filter="${2:-%}"
    sqlite3 -header -column "$DB" "SELECT id, category, substr(title,1,60) AS title, substr((SELECT group_concat(t.name, ',') FROM learning_tags lt JOIN tags t ON t.id=lt.tag_id WHERE lt.learning_id=learnings.id),1,40) AS tags FROM learnings WHERE category LIKE '$cat_filter' ORDER BY category, id;"
    ;;
  add-learning)
    cat="$2"; title="$3"; content="$4"; tags="${5:-}"
    # Contenido multilinea: soporte para archivo (@ruta) o stdin (-)
    # Si $4 empieza con @, lee de ese archivo; si es -, lee de stdin; si no, usa el arg directo
    case "$content" in
      @*)
        f="${content#@}"
        [ -r "$f" ] || { echo "Error: no se puede leer el archivo: $f" >&2; exit 1; }
        content="$(cat "$f")"
        ;;
      -)
        content="$(cat)"
        ;;
    esac
    cat_esc=$(sql_escape "$cat")
    title_esc=$(sql_escape "$title")
    content_esc=$(sql_escape "$content")
    # Solo tokens validos en la columna. La prosa en `tags` fue el sintoma de
    # que el cuerpo terminara ahi (clase C1 del guard de integridad).
    tags_clean=$(printf '%s' "$tags" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -E '^[a-z0-9._-]+$' | paste -sd, -)
    tags_esc=$(sql_escape "$tags_clean")
    # Una sola invocacion: `db` abre un proceso sqlite3 nuevo cada vez, asi que
    # last_insert_rowid() en una llamada aparte devuelve 0 y viola la FK.
    # La tabla temporal conserva el id dentro de la MISMA sesion.
    sql="INSERT INTO learnings (category, title, content, tags) VALUES ('$cat_esc', '$title_esc', '$content_esc', '$tags_esc');
CREATE TEMP TABLE _nid AS SELECT last_insert_rowid() AS id;"
    for t in $(printf '%s' "$tags_clean" | tr ',' '\n' | grep -v '^$'); do
        tag_esc=$(sql_escape "$t")
        sql="$sql
INSERT OR IGNORE INTO tags (name) VALUES ('$tag_esc');
INSERT OR IGNORE INTO learning_tags (learning_id, tag_id) SELECT (SELECT id FROM _nid), id FROM tags WHERE name='$tag_esc';"
    done
    sql="$sql
DROP TABLE _nid;"
    db "$sql"
    # Los tags tienen que existir en la JUNCTION (learning_tags), no solo en la
    # columna: el export a docs/learnings/*.md lee la junction, no la columna.
    # Antes esto no pasaba y toda leccion agregada por este comando quedaba
    # sin tags en cualquier vista (medido: 79 filas). Ver
    # scripts/check-learnings-integrity.py, clase C4.
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
        echo "- **[$cat](./$cat.md)** - $n lecciones"
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
        tags=$(sqlite3 "$DB" "SELECT COALESCE(group_concat(t.name, ','), '') FROM learning_tags lt JOIN tags t ON t.id=lt.tag_id WHERE lt.learning_id=$id;")
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
    # Purgar los .md de categorias que ya no existen en la DB. Sin esto, una
    # categoria que se vacia o se renombra deja su archivo huerfano para siempre y
    # el directorio deja de reflejar la DB, que es la fuente de verdad. Caso real
    # (2026-09-25): una fila con categoria vacia genero docs/learnings/.md, la fila
    # se borro, y el archivo sobrevivio a la regeneracion.
    for f in docs/learnings/*.md; do
      [ -e "$f" ] || continue
      base=$(basename "$f" .md)
      [ "$base" = "README" ] && continue
      if ! sqlite3 "$DB" "SELECT 1 FROM learnings WHERE category='$base' LIMIT 1;" | grep -q .; then
        if command -v trash >/dev/null 2>&1; then trash "$f"; else rm -f "$f"; fi
        echo "   podado: $f (la categoria '$base' ya no existe)"
      fi
    done
    echo "docs/learnings/ regenerado desde la DB."
    ;;
  *)
    echo "Uso: $0 {export-daily|export-all|export-oss|export-todos|export-inbox|stats|todos|inbox|contributions|add-todo|edit-todo|done-todo|reopen-todo|set-todo-priority|add-inbox|add-contribution|learnings|add-learning|export-learnings|catalog|search|topics|recent}"
    ;;
esac
