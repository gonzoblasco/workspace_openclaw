# ADR-117: El juez del Critic corre en deepseek, no en gpt-oss

**Fecha:** 2026-11-19
**Estado:** Aceptado
**Decisores:** Gonzo ("si ves que gpt-oss no está funcionando, no le demos vueltas y cambiemos")
**Enmienda:** ADR-090, fila `kanam-critic`
**Relacionado:** ADR-110 (el Critic tiene identidad propia y disparadores), ADR-077/ADR-088 (pipeline A/B)

---

## Contexto

El 2026-11-19 se corrieron cinco gates del Critic como subagente. Cuatro con `gpt-oss:120b-cloud`
—el modelo que ADR-090 asigna al rol— y uno con `deepseek-v4.1-flash:cloud`. La tarea fue la misma;
lo único que cambió fue el juez.

| # | Gate | Modelo | Resultado |
|---|---|---|---|
| 1 | T4.1 r1 | gpt-oss | "ORO 24/25" con un flag inexistente (`--trace-table`) y una integración de CI que no existía |
| 2 | T4.1 r2 | gpt-oss | No supo invocar la herramienta que juzgaba; usó stdin donde va un argumento posicional, y atribuyó a pytest un fallo propio |
| 3 | T4.1 r3 | gpt-oss | VETO honesto, pero con la evidencia elidida (`... (omitted for brevity) ...`) |
| 4 | T4.3 | gpt-oss | Declaró haber escrito el reporte; el archivo no existía |
| 5 | T4.3 | **deepseek** | Reporte de 17,7 KB, fila en el ledger, `verify-verdict` 12/12, y **cuatro defectos reales** encontrados en el artefacto |

Las fricciones F29, F30, F31 y F34 del ledger son las corridas 1 a 4. F35 es lo que encontró la 5.

## Decisión

**`kanam-critic` pasa a `deepseek-v4.1-flash:cloud`**, con `gemma4:12b-mlx` local como fallback.
`gpt-oss:120b-cloud` deja de ser el modelo del juez.

## Fundamento

El patrón de fallo de gpt-oss en el rol no es de criterio: es **no ejecutar y narrar como si hubiera
ejecutado**. Manifestaciones medidas el mismo día:

- Tres llamadas `ls agents` idénticas hasta que el runtime cortó el turno por fallos repetidos.
- Un flag de CLI inventado, presentado como comando real.
- Una afirmación de escritura de archivo (`ls` → *No such file or directory*) después de declararla.
- Un caso de prueba que falló por una razón distinta a la que decía medir, reportado como discriminación.

Un juez que falla así no falla en los márgenes: falla exactamente en lo que el rol existe para
detectar. La habilidad que se le pide es la disciplina de ejecutar y citar, no la de opinar.

**Contra la objeción "una corrida no es una serie":** es cierto, y por eso la decisión se toma por
la asimetría acumulada, no por la corrida 5 sola. Cuatro fallas del mismo tipo en el mismo rol, el
mismo día, contra cero fallas del reemplazo en la misma tarea. La decisión es reversible: si deepseek
empieza a fallar en el rol, se vuelve con evidencia.

## Lo que este ADR NO decide

- **No cambia el pipeline A/B.** El ejecutor A sigue en `gpt-oss:120b-cloud` (ADR-077/ADR-088), donde
  escribe y se autocorrige: las tres rondas fallidas de T4.1 se resolvieron cuando A pasó a deepseek,
  pero esa fue una excepción puntual autorizada, no una decisión de rol.
- **No arregla el kit.** F31/F32/F33/F35 son defectos de las herramientas y siguen abiertos: la
  elisión de evidencia y la etiqueta no validada contra la matriz son problemas del código, no del
  modelo.

## Implementación (verificada, no declarada)

La asignación no está vigente hasta que las tres capas coincidan —la lección que ADR-090 dejó escrita
después de declarar aplicada una asignación que nunca se aplicó—:

1. `openclaw.json` → `agents.entries.kanam-critic.model`.
2. `memory.db` → setting del modelo del rol.
3. Bloque managed `model-operativo` en `AGENTS.md` (vía `scripts/managed-blocks.py apply`).

Verificado con `scripts/managed-blocks.py check` y `openclaw` mostrando el modelo efectivo del rol.
