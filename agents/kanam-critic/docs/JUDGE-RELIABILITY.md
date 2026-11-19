# Confiabilidad del juez: por qué el gate fallaba

**Fecha:** 2026-11-19
**Pregunta:** de cinco corridas del gate, tres fueron inválidas. ¿Es el modelo o es la forma de la tarea?

## El experimento

Mismo artefacto (T4.3), mismas instrucciones, **un solo cambio**: el modelo del juez.

| # | Gate | Modelo del juez | Resultado |
|---|---|---|---|
| 1 | T4.1 r1 | gpt-oss:120b-cloud | ORO 24/25 **inventado** (flag inexistente, CI inexistente) |
| 2 | T4.1 r2 | gpt-oss:120b-cloud | No supo invocar la herramienta; culpó a pytest (F30) |
| 3 | T4.1 r3 | gpt-oss:120b-cloud | VETO honesto, evidencia elidida (F31) |
| 4 | T4.3 | gpt-oss:120b-cloud | Declaró un reporte que no escribió (F34) |
| 5 | T4.3 | **deepseek-v4.1-flash** | **Reporte 17,7 KB, fila en el ledger, `verify-verdict` 12/12** |

La corrida 5 no solo completó el procedimiento: **encontró cuatro defectos reales** que las cuatro
anteriores no vieron. Uno de ellos es una regla de la matriz SHARP que la herramienta no verifica.

**Conclusión: la causa dominante es el modelo, no la forma de la tarea.** La tarea se mantuvo
constante entre las corridas 4 y 5; lo único que cambió fue el juez.

## Por qué importa más allá de este kit

El patrón de fallo de gpt-oss como juez no es "se equivoca de criterio". Es **no ejecutar y narrar
como si hubiera ejecutado**. Ejemplos medidos:

- Loop de tres `ls agents` idénticos hasta que OpenClaw cortó el turno (tool-use sin corrección).
- `--trace-table` inventado: un flag que nunca existió en `emit-verdict.py`.
- "El archivo ha sido creado": el archivo no existía (`ls` → No such file).
- Un caso de prueba que falló por la razón equivocada y se reportó como discriminación.

Un juez así no falla en los márgenes: falla en la base. Y es el rol que existe para detectar
exactamente eso en otros.

## Lo que no explica el modelo

Dos defectos reales de la herramienta, encontrados por la corrida 5:

1. **`format_sharp_report.py` no valida la etiqueta contra la matriz.** Una fila con `total: 16` y
   `verdict: "Aprobado"` se formatea y se publica tal cual. La matriz dice ≤18 = VETO. `emit-verdict`
   sí lo valida, así que la fila no debería existir; pero publicar un cuerpo sin volver a verificar
   la etiqueta es defensa en profundidad que falta.
2. **Cero cobertura de VETO y ORO en la suite** del formatter: 21 tests, todos con "Aprobado". El
   camino que publica un VETO nunca se ejecutó en un test.

## Recomendación

**Cambiar el modelo del juez a `deepseek-v4.1-flash:cloud`** para funciones de gate, o mantener
`gpt-oss` y aceptar que el gate necesita supervisión del CORE en cada corrida.

Esto **no se aplica hoy**: ADR-090 asigna `kanam-critic → gpt-oss:120b-cloud` con Estado Aceptado,
y cambiarlo requiere enmienda del ADR (decisión de Gonzo), no un patch de config. La enmienda
tendría que registrar: qué se midió, con qué método, y que la asignación no está vigente hasta que
config + DB + bloques gestionados coincidan — la lección que el propio ADR-090 dejó escrita.

## Evidencia reproducible

```
$ python3 agents/kanam-critic/bin/verify-verdict.py | tail -1
GLOBAL=aprobado  (12/12 veredictos reales validos con respaldo, 2 anulado(s))

$ python3 scripts/check-critic-gate.py T4.3-format-sharp-report ; echo exit=$?
CRITIC-GATE: VETO  (T4.3-format-sharp-report)
exit=3

$ grep -c "VETO\|ORO" agents/kanam-critic/tests/format-sharp-report/test_format_sharp_report.py
0
```
