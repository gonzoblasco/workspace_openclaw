# Cata {{FECHA}} — {{MODELOS}} ({{TANDAS}})

{{Una frase: qué se midió y por qué.}}

- Corrida: run_id `{{RUN_ID}}` (si hubo una corrida descartada, decirlo y por qué).
- Candidatos: {{lista}}.
- Tareas: {{T1..Tn con su trampa principal}}.
- Congelado: vía (`{{ENDPOINT}}`), temperatura 0, `num_ctx` {{NUM_CTX}}, prompt verbatim con
  nonce idéntico por celda, `num_predict` {{BUDGETS}} con auto-escalado, timeout {{TIMEOUT}} s,
  warm-up fuera del throughput.

## 1. Validación de la suite (dos direcciones)

```
{{salida de `cata-kit.py check`}}
```

{{Si alguna referencia no dio PASS, NO se mide: se arregla el assert y se re-valida.}}

## 2. La perilla, por candidato (medida, no supuesta)

| Modelo | Niveles declarados | Default de la carta | Tanda `low` usada | Tanda `off` |
|---|---|---|---|---|
| {{modelo}} | {{levels}} | {{default}} | {{valor}} | {{valor o "no apagable: ..."}} |

## 3. Tanda `low` — {{empate / discriminó}}

| Modelo | Pass | Eval tokens | Thinking chars | Wall time |
|---|---|---|---|---|
{{tabla de analyze}}

{{Si todos empatan: "el empate es el resultado; desempata costo y latencia". Si discrimina,
nombrar la tarea que separó y por qué.}}

## 4. Tanda `off` — dónde se rompe y quién razona en el output

{{Tabla. Después: el fallo concreto, citando el artefacto (no el resumen del modelo).}}

## 5. Hallazgos del runner

{{Todo lo que produjo un resultado falso y cómo se detectó: cache, naming, kill del proceso,
timeout corto, etc. Si no hubo, decirlo.}}

## 6. Veredicto

{{Mejor costo/beneficio, quién no sirve para qué, y con qué evidencia.}}

## 7. Límites de esta medición

{{Qué NO mide: agencia, tool calling, multi-turno, varianza entre corridas, etc.}}

## 8. Reproducir

```bash
cd {{DIR}}
python3 {{KIT}} check .
python3 {{KIT}} run .
python3 {{KIT}} analyze .
```

## 9. Validación con evaluador ciego (CONTENT vs CLEANLINESS)

{{Brief: {{DIR}}/blind-eval-brief.md, subagente distinto de los candidatos, contexto aislado,
prohibido leer results*.json / evaluate.py / analyze.py. Pegar su tabla y después:}}
**Convergencia:** {{...}} · **Divergencia:** {{... y por qué eje}}.
