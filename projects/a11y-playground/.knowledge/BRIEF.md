# BRIEF: a11y-playground

**Nombre:** a11y-playground
**Objetivo:** Crear una herramienta *web-based* que, dada una URL, analice su contenido (DOM, metadatos) y genere un reporte de accesibilidad (A11y Report) en formato legible por humanos, ofreciendo sugerencias de mejora accionables.
**Tipo de Proyecto:** Portfolio / Demo / Herramienta de prueba de concepto.
**Alcance inicial:** Validar el flujo de trabajo del agente: entrada (URL) -> procesamiento (simulado o real) -> salida (reporte descargable).
**Diferenciador:** Fusiona el nicho de a11y con la capacidad de la IA para procesar y mejorar contenido.
**Requerimientos mínimos:** Frontend (React/TS), API (Edge Function simulada para la lógica de procesamiento), DB (para persistir reportes), Algoritmo de escaneo DOM.
**Dependencias conocidas:**
- `a11y-fixer` (código fuente será fuente de inspiración para la lógica).
- Memoria de decisión en el workspace.
**Limita-tions:** La versión 0.1.0 NO hará escaneo real de DOM en producción; el escaneo inicial será un análisis de metadatos y estructura HTML base.
**Next Step:** Implementar la primera *feature* (ej. validación de contrastes de color básicos).