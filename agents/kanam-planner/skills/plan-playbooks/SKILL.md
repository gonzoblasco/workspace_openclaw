---
name: "plan-playbooks"
description: "Biblioteca de planes recurrentes listos para instanciar: feature delivery, OSS PR, evaluacion de modelos, postulacion laboral y auditoria/incidente. Usar cuando el objetivo matchea un patron conocido en vez de disenar el plan desde cero."
metadata:
  category: "Crew"
  tags:
    - planner
    - playbooks
    - programs
    - templates
user-invocable: false
---

# plan-playbooks

Un playbook es un programa probado que se instancia con otro objetivo. No es una receta rígida: es un punto de partida con pasos, roles y gates ya pensados. El Planner lo adapta, no lo copia ciego.

## Cómo se usa

1. Elegir el playbook que matchea el objetivo.
2. Crear el programa:
   ```bash
   python3 scripts/program_plan.py init <slug> --title "<titulo>" --objective "<objetivo>" --gates <gates>
   ```
3. Agregar los pasos del playbook, ajustando tarea y criterio de salida al contexto real.
4. Correr `plan_lint.py`.
5. Entregar el brief al CORE.

## 1. Feature delivery

**Cuándo:** una feature nueva o un cambio de producto con UI, lógica y tests.

| # | Paso | Rol | Criterio de salida |
|---|---|---|---|
| 1 | Descubrir y acotar el alcance | planner | Alcance, no-alcance y riesgos escritos |
| 2 | Escribir spec o actualizar la existente | planner / studio | Spec aprobada por Gonzo |
| 3 | Implementar A | dev | Código + tests locales verdes |
| 4 | Revisar B | critic | Hallazgos bloqueantes resueltos o waiver |
| 5 | Auditar superficie (si hay UI) | auditor | Sin hallazgos bloqueantes de a11y/UI |
| 6 | Verificar repo y build | core | Build + tests + lint verdes, salida pegada |
| 7 | Cerrar y documentar | core | CHANGELOG/HANDOFF/ADR si aplica |

**Gates:** auditor (si UI), critic.
**No olvidar:** el CORE verifica el repo; el auto-reporte de A/B no es prueba.

## 2. OSS PR

**Cuándo:** comentar, revisar o abrir un PR en un repo de terceros.

| # | Paso | Rol | Criterio de salida |
|---|---|---|---|
| 1 | Leer el hilo completo y el estado del PR | mind | Resumen con citas y preguntas abiertas |
| 2 | Verificar el claim contra el código/docs | mind | Evidencia textual o reproducción |
| 3 | Redactar el comentario/PR | studio | Borrador listo, sin publicar |
| 4 | Revisión adversarial | critic | Sin afirmaciones sin evidencia |
| 5 | Publicar con OK de Gonzo | core | Comentario/PR publicado y URL |
| 6 | Esperar CI y responder | core | CI verde o respuesta al fallo |
| 7 | Registrar el aprendizaje | mind | Nota en docs/learnings o daily |

**Gate:** critic.
**Regla dura:** nada sale sin OK explícito de Gonzo. Un PR no es un proyecto: no se toca el fork local sin necesidad.

## 3. Evaluación de modelos

**Cuándo:** catar un modelo nuevo o comparar modelos para un rol.

| # | Paso | Rol | Criterio de salida |
|---|---|---|---|
| 1 | Definir rúbrica y tabla de verdad | planner | Criterios medibles y casos |
| 2 | Medir A | dev | Resultados crudos por caso |
| 3 | Evaluar B contra la tabla | critic | Puntajes y discrepancias |
| 4 | Redactar el informe | studio | Informe con evidencia y recomendación |
| 5 | Revisión final | core | Decisión y ADR si cambia un slot |

**Gate:** critic.
**Regla:** no se cambia un modelo por preferencia; se cambia por medición. Si no hay rúbrica, no hay cata.

## 4. Postulación laboral

**Cuándo:** una búsqueda nueva, una propuesta o un follow-up.

| # | Paso | Rol | Criterio de salida |
|---|---|---|---|
| 1 | Analizar el JD contra los hechos de carrera | mind | Match, gaps y riesgos |
| 2 | Decidir si vale la pena | core / Gonzo | Go/no-go explícito |
| 3 | Adaptar CV y carta | studio | Documentos listos, sin inventar hechos |
| 4 | Revisar | critic | Consistencia con `memory/career-facts.md` |
| 5 | Postular con OK | core | Confirmación del sitio o envío |
| 6 | Agendar follow-up | planner | Fecha y próximo paso |

**Gate:** critic.
**Regla:** el relato cambia por puesto; los hechos no. Nada se envía sin OK.

## 5. Auditoría / incidente

**Cuándo:** un bug de producción, una inconsistencia de datos o una auditoría de workspace.

| # | Paso | Rol | Criterio de salida |
|---|---|---|---|
| 1 | Reproducir y acotar | ops / dev | Pasos de reproducción y alcance |
| 2 | Aislar la causa | dev | Causa raíz con evidencia |
| 3 | Diseñar el fix | planner | Opciones, riesgos y decisión |
| 4 | Implementar | dev / ops | Fix + tests de regresión |
| 5 | Verificar | core | Reproducción original ya no falla |
| 6 | Documentar | core | ADR/CHANGELOG/HANDOFF |
| 7 | Prevención | planner | Gate o test que evita la recurrencia |

**Gate:** critic (si el fix toca lógica o seguridad).
**Regla:** primero se estabiliza, después se documenta. No se hace post-mortem antes de cerrar el incidente.

## 6. Weekly planning

**Cuándo:** lunes a la mañana, o cuando Gonzo pide "¿qué hacemos esta semana?".

| # | Paso | Rol | Criterio de salida |
|---|---|---|---|
| 1 | Leer programas activos y el archivo | planner | Estado real, no deseos |
| 2 | Elegir top 3 outcomes | planner / Gonzo | 3 resultados, no 10 tareas |
| 3 | Asignar dueños y fechas | planner | Cada outcome con dueño |
| 4 | Publicar el brief | planner | 10 líneas en Telegram/webchat |

**Regla:** el plan semanal no reemplaza el programa; lo prioriza.

## Anti-patrones

- Instanciar un playbook sin adaptar el criterio de salida.
- Agregar pasos que no producen evidencia.
- Usar un playbook para una tarea de una sesión.
- Saltar el gate porque "ya lo revisé yo".
- Convertir el playbook en una checklist infinita.

## Referencias

- `scripts/program_plan.py` — crear y operar el programa.
- `CAPABILITIES.md` — catálogo de capacidades.
- `docs/PLANNER-INTEGRATION.md` — quién llama a quién.

---

_Un playbook no piensa por vos: te ahorra el primer borrador para que pienses mejor el segundo._
