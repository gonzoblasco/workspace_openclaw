# ADR-001: Estrategia de Portfolio y Selección de Proyectos Ancla

**Fecha:** 2026-08-28
**Estado:** Aceptado
**Ultima enmienda:** 2026-09-14 (ver seccion 6)
**Contexto:** Definición de la narrativa profesional para búsqueda laboral y posicionamiento de marca personal.

## 1. El Problema
La dispersión de proyectos en el portfolio (repositorios activos, archivados y experimentales) genera ruido y diluye el mensaje profesional. Para un perfil "AI-Native Fullstack", es más valioso demostrar la construcción de **infraestructura de trabajo con IA** que presentar una colección de apps aisladas.

## 2. El Pitch Estratégico
El posicionamiento se centra en tres pilares:
1. **IA como Infraestructura**: No solo uso la IA, construyo los sistemas que permiten trabajar con ella de forma eficiente y local.
2. **Accesibilidad como Diferenciador**: La a11y no es un checkbox, es una especialización técnica profunda que garantiza calidad y alcance.
3. **Arquitectura Local-First**: Dominio de la privacidad, persistencia en cliente (IndexedDB) y despliegues sin dependencia de cloud.

## 3. Proyectos Ancla (The Pillars)

Se definen tres proyectos como los estandartes del portfolio. Estos son los que se priorizan en el pitch, LinkedIn y entrevistas:

| Proyecto | Pilar | Valor Demostrado |
| :--- | :--- | :--- |
| **kanam-forge** | Infraestructura AI | Orquestación de contenedores, sandboxing local, pipeline de construcción de apps asistida por IA. |
| **a11y-fixer** | Especialización a11y | Automatización de auditorías WCAG, integración en CI/CD, dominio de axe-core y Playwright. |
| **kanam-pulse** | Local-First / Privacidad | Monitor de salud y limpieza de macOS local-first: dashboard web que lee el pulso real de la máquina (disco, memoria, CPU, seguridad, red) y actúa con consentimiento explícito y granular. Sin telemetría ni cuentas; IA local opcional (Ollama) que explica la auditoría en lenguaje simple; accesibilidad WCAG 2.2 AA desde el día uno. |

## 4. Decisiones de Limpieza y Archivo

Para optimizar la "señal" del portfolio, se toman las siguientes decisiones:

- **create-with-ai $\rightarrow$ ARCHIVAR**: El proyecto fue fusionado técnicamente en `kanam-forge`. Mantener ambos genera redundancia. La evolución es la prueba de crecimiento.
- **accessible-ui $\rightarrow$ ARCHIVAR**: Aunque técnicamente sólido, el mercado de primitivas headless está saturado. El expertise en accesibilidad queda representado con mayor impacto por `a11y-fixer`.
- **Kanam Mind $\rightarrow$ ARCHIVAR (2026-08-29)**: Deja de ser ancla del pilar Local-First / Privacidad, reemplazado por `kanam-pulse`. Kanam pulse cubre el mismo pilar con mayor impacto (local-first + privacidad + a11y + IA local en un solo producto). Kanam Mind se archiva del portfolio; su repo queda conservado.
- **SoporteML $\rightarrow$ EXCLUIR**: El proyecto queda fuera de la narrativa pública de portfolio por razones de privacidad/estratégicas hasta nuevo aviso. **NO TOCAR**: este proyecto no se modifica, no se decide su destino, y no se lista como candidato en auditorías de higiene del workspace. La exclusión es una decisión cerrada; no se vuelve a abrir salvo que Gonzo lo pida explícitamente.

## 5. Criterios de Éxito
- El portfolio presenta una narrativa coherente: **Infraestructura $\rightarrow$ Accesibilidad $\rightarrow$ Privacidad**.
- Los proyectos ancla cuentan con READMEs pulidos, documentación de decisiones (ADRs) y tests verdes.
- La actividad de LinkedIn se alinea con los nichos de estos tres pilares.

## 6. Enmienda - 2026-09-14

**Estado:** Aceptada. Esta seccion modifica la seccion 3. **El texto original se conserva sin cambios** (el historial de decisiones importa), pero la tabla de anclas vigente es la de acá abajo.

**Decision (Gonzo, 2026-09-14):** `a11y-fixer` **queda archivado** y su sucesor es **`kanam-fixer`, un proyecto nuevo** - no un renombre del anterior. Palabras textuales: "ya no se llama a11y-fixer.. esta ya queda archivada.. es un proyecto nuevo, el kanam-fixer".

| Proyecto | Pilar | Estado |
| :--- | :--- | :--- |
| **kanam-forge** | Infraestructura AI | Ancla vigente, sin cambios. |
| **kanam-pulse** | Local-First / Privacidad | Ancla vigente, sin cambios. |
| **a11y-fixer** | Especialización a11y | **Archivado (2026-09-14).** Sale de la tabla de anclas. |
| **kanam-fixer** | Especialización a11y | **Candidato a ancla.** Alcance y propuesta de valor **sin definir** a la fecha de esta enmienda. |

**Consecuencia inmediata:** el pilar **Accesibilidad como Diferenciador** queda **sin ancla formal** hasta que el alcance de `kanam-fixer` se defina y se acepte. **No se asume** que `kanam-fixer` hereda el rol de "engine de fixes de accesibilidad": eso es justamente lo que falta decidir.

**Pendientes para cerrar esta enmienda** (seguimiento en la DB de memoria, todo id=54):
1. ~~Definir alcance y propuesta de valor de `kanam-fixer`~~ - **RESUELTO 2026-09-14/15:** alcance definido en `kanam-fixer/.knowledge/BRIEF.md` + `ROADMAP.md` (asercion sobre el anuncio del lector de pantalla; virtual en CI, real en local). Direccion **confirmada por Gonzo** el 2026-09-15.
2. ~~Decidir la relación con el código de `a11y-fixer`: heredar, portar o greenfield~~ - **RESUELTO:** **greenfield**. El BRIEF lo declara explicito: "No hereda su codigo ni su alcance". Si algo del codigo sirve, se porta con decision explicita, no por inercia.
3. ~~Archivar el repo `gonzoblasco/a11y-fixer` en GitHub~~ - **HECHO 2026-09-15:** `isArchived=true` (mas banner de archivo en el README y en los 6 headers de docs). **Pendiente acotado:** el paquete npm `@gonzoblasco/a11y-fixer@0.6.0` sigue publicado - deprecarlo requiere `npm login` y no hay credencial en la maquina.
4. ~~Resolver `a11y-playground`~~ - **RESUELTO 2026-09-15: archivado.** Era un scaffold que nunca paso de M0: repo privado creado el 2026-08-30, **un solo commit** (`chore: initial scaffold`), **size 0** (solo `.gitignore` + README, cero codigo). Su unica dependencia declarada era `a11y-fixer`, hoy archivado. Se archivo el repo en GitHub (`isArchived=true`).

**Estado de la enmienda:** los 4 pendientes cerrados (el punto 3 con el resto acotado a npm). El pilar *Accesibilidad* tiene ancla candidata formalizada en `kanam-fixer` con alcance ya definido; la validacion real del ancla sigue siendo el criterio de NORTH.md Horizonte 1 (usuarios que no sean Gonzo).

**Nota sobre la seccion 4:** la justificación para archivar `accessible-ui` invocaba a `a11y-fixer` como el proyecto que representaba mejor el expertise a11y. Esa premisa queda **suspendida** junto con el ancla: se conserva el texto original por trazabilidad, pero la razón ya no aplica tal como está escrita.

## 7. Enmienda - 2026-09-24 (SoporteML: se reabre su destino)

**Estado:** Aceptada. Esta seccion **enmienda la seccion 4** en lo que respecta a SoporteML. El texto original se conserva sin cambios.

**Decision (Gonzo, 2026-09-24):** SoporteML **se reabre** como producto nuevo - una aplicacion SaaS CRM y contable para pymes, con las mismas features que v1 y el alcance ampliado al contable. Palabras textuales: *"reabramos soporteml, la version completa"*.

**Base de esta enmienda:** la seccion 4 decia textualmente que la exclusion *"no se vuelve a abrir salvo que Gonzo lo pida explicitamente"*. **Lo pidio explicitamente**, asi que se cumple la condicion prevista. No es una excepcion ni una violacion del ADR: es la clausula de reapertura de ese mismo ADR, ejercida.

### Que cambia y que no

| Punto de la seccion 4 | Estado |
|---|---|
| **"NO TOCAR: este proyecto no se modifica, no se decide su destino"** | **Levantado.** El destino del proyecto se esta decidiendo (ADR-068). |
| **"No se lista como candidato en auditorias de higiene del workspace"** | **Sigue vigente.** El proyecto no entra en barridos automaticos de limpieza. |
| **Fuera de la narrativa PUBLICA de portfolio / del CV** | **Sigue vigente.** El motivo era privacidad y estrategia, y esa razon no la toca esta reapertura. |

**El encuadre que resuelve las dos cosas a la vez:** la nueva generacion se construye como **producto privado**, no como ancla de portfolio. No contradice la decision de privacidad del 2026-09-14 y permite construir sin deshacerla.

### Efecto sobre las anclas

**Ninguno.** La tabla de anclas de la seccion 6 no se modifica: `kanam-forge` y `kanam-pulse` siguen vigentes, `kanam-fixer` sigue como candidata con alcance definido. SoporteML **no entra** a la tabla de anclas. El pilar *Accesibilidad* sigue con su pendiente de validacion.

### Relacion con otros documentos

- **ADR-068** (workspace): encuadre de la nueva generacion - greenfield, base v1, y los 6 puntos pendientes.
- **ADR-067** (workspace): por que ningun ADR del workspace pertenece a SoporteML, con la medicion que lo prueba (0 de 68 como sujeto).
- **`MEMORY.md`:** la entrada que decia *"FUERA de la narrativa... es hora de dejarlo ir"* requiere nota de actualizacion (hecha el 2026-09-24).
- **`memory/user-profile.md`:** la linea de 2026-09-14 sobre SoporteML fuera del perfil **sigue vigente** (es la parte de narrativa publica).
