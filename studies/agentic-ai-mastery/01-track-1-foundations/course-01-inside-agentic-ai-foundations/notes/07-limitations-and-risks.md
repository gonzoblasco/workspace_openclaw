# Video 7 - Limitations and Risks of Agentic AI

**Curso:** Inside Agentic AI: Foundations and Frontiers
**Track:** 1
**Fecha:** 2026-08-21

---

## Tesis

"Agentic AI es poderoso, pero con la autonomía viene el riesgo. Responsable agent design isn't optional, it's foundational."

## Los riesgos (mapeados por tipo)

### 1. Autonomía sin cheques → misalignment
- Ejecutan planes, llaman APIs, deciden sin human checks.
- **Misalignment entre goals y contexto**: lo que parece lograr el goal puede ser dañino en realidad.
- **Pequeños errores se componen**: una acción fallida dispara un feedback loop defectuoso, escalando el error sin detección.
- → Oversight, safety checks y constraint design son críticos.

### 2. Perception defectuosa = "ciego o engañado"
- Input incompleto o sesgado → percepción defectuosa → malas decisiones.
- Actúa sobre suposiciones viejas, ignora capacidades, reacciona a info alucinada.
- *"La percepción es los ojos y oídos del agente. Si está ciego, las consecuencias se espejan por todo el sistema."*

### 3. Planning failures
- **Overfit a goals locales** (éxito cortoplacista ignorando contexto).
- **Plansos naive o brittle** (falta de world knowledge o foresight).
- **Negligencia de edge cases**: rate limits por API calls excesivas, reuniones en feriados.
- Planar efectivo = *context-aware, cautious, resilient*.

### 4. Tool misuse
- "Solo porque pueden acceder a una función no significa que la usan seguro."
- **Suposiciones incorrectas sobre el tool behavior** (formato de API esperado que no llega).
- **Chain-of-thought NO garantiza ejecución correcta** - un API error, format mismatch o misstep deriva todo.
- Requiere guardrails robustos, validación, error recovery.

### 5. Feedback loops defectuosos
- Sin loop activo (o mal diseñado) los errores quedan sin corregir.
- **Reinforcement fault**: rewards por acciones superficialmente correctas pero profundamente erradas → "aprende la lección equivocada".
- Ej: content filter que bloquea por mislabeling y es recompensado → **más sesgado con el tiempo**.
- **"Adaptation without accountability can harden the wrong instincts."**

### 6. Value misalignment + falta de transparencia
- Lo que optimiza el agente puede no reflejar intenciones del usuario o normas éticas.
- Falta de transparencia en razonamiento multi-step → difícil auditar/intervenir.
- **Safety hazards** en healthcare/finance/defense → consecuencias irreversibles.

## Caso práctico (viaje)

Agente optimizado por **precio** reserva: 3 escalas, llegando a las 3 AM. El usuario odia madrugadas y escalas. **¿Qué falló?** Overfit al metric (precio) en vez de al meaning (intención). Riesgo #3 (planning) + #6 (misalignment).

## Cómo diseñar responsablemente

1. **Alinear goals con intención y valores** - optimizá por meaning, no solo metrics.
2. **Validar acciones antes de ejecutar** - cheques, confirmaciones, dry runs.
3. **Transparencia y oversight** - logs, memory traces, explicaciones.
4. **Monitorear feedback y actualizar** - loops que premien lo bueno y corrijan lo malo.

## Cierre

> "At each stage, risks can creep in: biased input, brittle planning, inappropriate tool use, faulty feedback. Recognizing these potential risk points is the essential first step to building robust, ethical, effective agentic AI."

---

## Conexión con mi experiencia

El video valida mis decisiones de diseño:
- **Perception defectuosa** → verificación contra la fuente real antes de aceptar un fix.
- **Tool misuse** → revisar el stack del tool/skill antes de ejecutar.
- **Feedback loops defectuosos** → cross-review A→B que detecta cuando el Agente B "corrige" mal.
- **Value misalignment** → definir el goal real (no métrica) con Gonzo.
- **Falta de transparencia** → ADRs, HANDOFF, daily notes = log completo del razonamiento.

**"Adaptation without accountability can harden the wrong instincts"** describe el bug del Agente B: sin corrección contra la fuente, se habría reforzado un defecto. El human-in-the-loop es la accountability que el video llama *foundational*. El caso del travel agent = la lección del cross-review en versión demo (optimizar por métrica sin capturar intención).
