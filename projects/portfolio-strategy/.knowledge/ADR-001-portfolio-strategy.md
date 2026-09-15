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
1. Definir alcance y propuesta de valor de `kanam-fixer` (que resuelve, para quién).
2. Decidir la relación con el código de `a11y-fixer`: heredar, portar o greenfield.
3. Archivar el repo `gonzoblasco/a11y-fixer` en GitHub (hoy `isArchived=false`) y decidir el destino del paquete npm `@gonzoblasco/a11y-fixer@0.6.0`.
4. Resolver `a11y-playground`, que declara depender de `a11y-fixer` como base.

**Nota sobre la seccion 4:** la justificación para archivar `accessible-ui` invocaba a `a11y-fixer` como el proyecto que representaba mejor el expertise a11y. Esa premisa queda **suspendida** junto con el ancla: se conserva el texto original por trazabilidad, pero la razón ya no aplica tal como está escrita.
