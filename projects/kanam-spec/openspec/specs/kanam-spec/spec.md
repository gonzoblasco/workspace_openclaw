# kanam-spec Specification

## Overview
`kanam-spec` es una herramienta personal que genera especificaciones técnicas a partir de un brief corto, usando IA local vía Ollama. El objetivo es formalizar requisitos de negocio, UX y arquitectura, reducir deuda técnica y evitar scope creep.

## Goals
- Generar spec de alto nivel para el proyecto.
- Definir requisitos funcionales y no‑funcionales.
- Documentar flujos de UI/UX y validaciones de edge cases.
- Establecer criterios de aceptación claros.

## Requirements
### Functional
- **FR-1**: El sistema debe recibir un brief en texto plano y generar un documento spec en Markdown.
- **FR-2**: El spec debe incluir secciones de `Overview`, `Goals`, `Requirements`, `Non-goals`, `Scenarios` y `Acceptance Criteria`.
- **FR-3**: El motor de IA debe correr localmente usando Ollama sin dependencias externas.
- **FR-4**: Input Interface - La UI debe ofrecer un `<textarea>` multilinea, con longitud mínima 10 y máxima 2000 caracteres, y un toggle de idioma (español/inglés).
- **FR-5**: Generation Process - Al pulsar **Generate**, el cliente envía la solicitud a `/api/ollama/generate` y muestra la respuesta en streaming en una vista previa.
- **FR-6**: Preview & Export - La vista previa renderiza Markdown, y la UI provee botones **Copy** y **Download** (archivo `.md`). El spec se guarda automáticamente en `localStorage` bajo la clave `kanam-spec-{timestamp}`.
- **FR-7**: Validation - Tras la generación, el cliente ejecuta `openspec validate <spec-file>` y muestra los errores. Si pasa, muestra un badge `✅ Validation passed`.

### Non-functional
- **NFR-1**: La UI será en español y respetará la convención de guion comun (`-`).
- **NFR-2**: El proyecto usará TypeScript estricto, React 19 y Vite.
- **NFR-3**: Persistencia en `localStorage`; pruebas con Node test runner.
- **NFR-4**: Performance - El tiempo de generación no debe exceder 5 s para briefs ≤ 500 caracteres en un Mac Mini típico (2 CPU, 8 GB RAM).
- **NFR-5**: Seguridad - Todo el procesamiento es local; el servidor escucha solo en localhost.
- **NFR-6**: Accesibilidad - Cumplir con WCAG 2.1 AA (etiquetas ARIA, foco lógico, contraste).
- **NFR-7**: Compatibilidad - Chrome, Safari y Firefox (últimas versiones macOS).

## Non‑goals
- No se proveerá una interfaz gráfica completa para edición de specs; el flujo es CLI‑driven.
- No se integrará con servicios externos de terceros.

## Scenarios
1. **Brief simple**: El usuario ingresa “Agregar botón de login” → el sistema genera spec con requisitos y diseño UI.
2. **Brief complejo**: Incluye múltiples secciones y dependencias; el spec incluye diagramas de flujo y validaciones.

## Acceptance Criteria
- El spec generado pasa `openspec validate` sin errores.
- Cada requisito está marcado con `SHALL` o `MUST`.
- El documento está versionado en Git y refleja el cambio en `CHANGELOG.md`.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->