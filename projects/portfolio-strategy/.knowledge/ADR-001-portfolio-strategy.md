# ADR-001: Estrategia de Portfolio y Selección de Proyectos Ancla

**Fecha:** 2026-08-28
**Estado:** Aceptado
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
| **Kanam Mind** | Local-First / Privacidad | Gestión de datos privados, PWA offline, integración de LLMs locales (Ollama). |

## 4. Decisiones de Limpieza y Archivo

Para optimizar la "señal" del portfolio, se toman las siguientes decisiones:

- **create-with-ai $\rightarrow$ ARCHIVAR**: El proyecto fue fusionado técnicamente en `kanam-forge`. Mantener ambos genera redundancia. La evolución es la prueba de crecimiento.
- **accessible-ui $\rightarrow$ ARCHIVAR**: Aunque técnicamente sólido, el mercado de primitivas headless está saturado. El expertise en accesibilidad queda representado con mayor impacto por `a11y-fixer`.
- **SoporteML $\rightarrow$ EXCLUIR**: El proyecto queda fuera de la narrativa pública de portfolio por razones de privacidad/estratégicas hasta nuevo aviso. **NO TOCAR**: este proyecto no se modifica, no se decide su destino, y no se lista como candidato en auditorías de higiene del workspace. La exclusión es una decisión cerrada; no se vuelve a abrir salvo que Gonzo lo pida explícitamente.

## 5. Criterios de Éxito
- El portfolio presenta una narrativa coherente: **Infraestructura $\rightarrow$ Accesibilidad $\rightarrow$ Privacidad**.
- Los proyectos ancla cuentan con READMEs pulidos, documentación de decisiones (ADRs) y tests verdes.
- La actividad de LinkedIn se alinea con los nichos de estos tres pilares.
