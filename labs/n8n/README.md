# Lab n8n self-hosted (local)

Instancia de practica del curso `studies/n8n-ai-automations/`. Docker, solo loopback (127.0.0.1:5678).

    docker compose up -d      # levantar
    docker compose logs -f    # ver logs
    docker compose down       # bajar (los datos quedan en ./data)

- UI: http://localhost:5678
- Datos (SQLite + encryption key + binarios): `./data` — **no se commitea**.
- La API publica se habilita por workflow con un token propio en la UI.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
