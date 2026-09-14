# kanam-lab - Brief

- **Proposito:** playground local de IA (Gradio) para explorar modelos, STT y RAG sin salir de la maquina. Experimentar con Python como protagonista en la capa de IA, fuera de React/JS.
- **v1 (2026-09-12):** chat comparativo de 2 modelos de Ollama lado a lado, misma pregunta a ambos. Servidor en `0.0.0.0:7860`.
- **v2 (2026-09-12):** un solo input envia el mismo prompt a ambos modelos en paralelo (streaming).
- **v3 (2026-09-14):** tab STT - transcripcion de audio 100% local. Paquete real: `mlx-audio==0.5.3` (el nombre `mlx-stt` no existe en PyPI), modelo `mlx-community/GLM-ASR-Nano-2512-8bit` (~2.3G, cache HF, carga lazy), conversion webm->wav con `afconvert`. Docs: `docs/STT.md`. Commits `e82d86d`, `6ace8a4`.
- **Fases pendientes:** v4 mini-RAG sobre memoria con embeddings locales.
- **Stack:** Python 3.12 (Homebrew) + venv propio + Gradio 6 + cliente ollama + mlx-audio (STT). React/TS queda para capa de producto.
- **Repo:** git local, sin remoto (2026-09-14).
