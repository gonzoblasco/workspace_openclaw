# kanam-lab - Brief

- **Proposito:** playground local de IA (Gradio) para explorar modelos, STT y RAG sin salir de la maquina. Experimentar con Python como protagonista en la capa de IA, fuera de React/JS.
- **Fase 1 (2026-09-12):** chat comparativo de 2 modelos de Ollama lado a lado, misma pregunta a ambos. Servidor en `0.0.0.0:7860`.
- **Fase 1.5 (2026-09-12):** un solo input envia el mismo prompt a ambos modelos en paralelo (streaming).
- **Fase 2 (2026-09-14):** tab STT - transcripcion de audio 100% local. Paquete real: `mlx-audio==0.5.3` (el nombre `mlx-stt` no existe en PyPI), modelo `mlx-community/GLM-ASR-Nano-2512-8bit` (~2.3G, cache HF, carga lazy), conversion webm->wav con `afconvert`. Docs: `docs/STT.md`. Commits `e82d86d`, `6ace8a4`.
- **Fase 3 (2026-09-14):** tab RAG - busqueda semantica sobre la memoria del workspace (dailies + learnings). Embeddings locales `qwen3-embedding:0.6b` + coseno (mismo flujo que memory-search.py), sintesis con deepseek-v4-flash. E2E OK: "reindex 451/451, 2857 chunks, fix SHA256->Ollama" recuperado con fuentes reales. Commit `af2863e`.
- **Fases pendientes:** Fase 4 (ideas: resumen automatico de sesion a daily, RAG sobre learnings_enriquecido completo, comparador de respuestas persistente).
- **Stack:** Python 3.12 (Homebrew) + venv propio + Gradio 6 + cliente ollama + mlx-audio (STT). React/TS queda para capa de producto.
- **Repo:** git local, sin remoto (2026-09-14).
