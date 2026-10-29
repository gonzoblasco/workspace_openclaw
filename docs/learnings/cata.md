# Learnings - cata

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## Un control que falla por infra es una AUSENCIA, no un 0: hay que verificar los harnesses ANTES de medir

El 2026-10-28, al reiniciar Docker se llevaron por delante los containers 'opencode' y 'openhands-canvas' (el runner los USA, no los levanta). La cata arranco igual: el control de claude dio ok=True, el de opencode 'No such container' y el de openhands 'Connection refused', y las 27 celdas de la fase cloud quedaron sin medir. Peor todavia: un reinicio de Docker deja el catalogo de providers de opencode cargandose, y el mismo comando responde 'Model unavailable: ollama/<modelo>' aunque el container este sano y el modelo exista en Ollama (verificado a mano: el mismo 'opencode run --model ollama/minimax-m3.1-flash:cloud' funciono un minuto despues). QUE HACER: un PREFLIGHT antes del primer runner.py, con DOS verificaciones: (1) que el container responde (docker ps por nombre + health del compose) y (2) que el harness RESUELVE el modelo que se va a medir ('docker exec opencode sh -c opencode models' contiene 'ollama/<modelo>'). Si el preflight falla, la tanda NO arranca (exit 1): un preflight que solo avisa y deja seguir no previene nada. El preflight vive en scripts/preflight-cata.sh (playground/ esta en .gitignore, asi que la copia de la cata es un wrapper). Ojo: si quedo un container parado de una corrida anterior, 'docker compose up' responde 'container name is already in use' y deja el viejo en pie, que es lo que se quiere: verificar por docker ps, no por el exit code del compose.

**Tags:** docker,cata,preflight,infra,control,ausencia,opencode,openhands,fairness

---

