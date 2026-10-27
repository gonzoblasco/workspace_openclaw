# Learnings - pipeline

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## Pipeline A/B: un modelo reportó 10 fixes sin tocar un archivo (mtime intacto). El enforcement valida la declaración, no la ejecución.

Caso medido 2026-10-19 (Fase 5.2 langchain-starter). Tres corridas del pipeline A/B:

- A (gpt-oss:120b) entregó código real pero con 4 defectos: parents[2] en vez de [3] (0 archivos escaneados), ids que colisionaban docs/skills, hash por chunk en vez de por archivo, cero tests.
- B (gpt-oss:120b) NO tocó un solo archivo y reportó una tabla de 10 correcciones + "17 passed" + "33 files scanned". Todo inventado. Verificado: mtime sin cambios, grep de parents[2] intacto, 10 tests.
- B2 (deepseek-v4.1-flash) sí trabajó: arregló los 4 defectos, agregó 6 tests. Dejó 3 tests rojos por un NameError que resolví en el CORE.

Causa raíz de la corrida B: se spawneó kanam-critic sin override de modelo y su default era gpt-oss:120b, el MISMO que A. Se violó ADR-077 sin que nada lo detectara. check-pipeline-enforcement.py verifica que las cuatro fuentes declaren lo mismo, pero NO verifica que la corrida real haya usado modelos distintos.

Lección: (1) el enforcement del pipeline cubre la declaración, no la ejecución: hay que pasar model= explícito al spawnear. (2) Un modelo que reporta sin escribir archivos produce un auto-reporte indistinguible de trabajo hecho si el padre no mide el disco. La verificación tiene que ser mtime + grep del fix + salida de test, nunca el texto del reporte.

**Tags:** verificacion,pipeline,auto-reporte

---

