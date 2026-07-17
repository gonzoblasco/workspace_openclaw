# ROADMAP (V0.1) - UmbraWriter

## **ESTADO:**
*   Fase 0 (Diagnóstico): ✅ Completada. El proyecto está definido en términos de su *propósito*.
*   Fase 1 (Evaluación): ✅ Completada. La visión se centró en la Co-Creación, no en la herramienta.
*   **Fase 2 (Definición - MVP): 🔥 IN_PROGRESS.** Especificando arquitectura del Motor Dialógico y comenzando implementación técnica.

## **✅ METAS DEL MVP v0.1 (El Objetivo)**

Construir el núcleo fundamental que transforma UmbraWriter de un PoC a una herramienta dialógica real:

**Motor Dialógico Central:**
- Recibir y procesar Beats files existentes desde múltiples fuentes (archivos, clipboard, paste)
- Detectar alteraciones narrativas del usuario en contexto inmediato
- Generar 2-3 ramificaciones lógicas que respeten el canon establecido
- Ofrecer caminos con diferentes cargas dramáticas (sublime, cómic, trágico, etc.)

## **🔑 TAREAS PRIORITARIAS (Fase 2 - Implementación)**

1.    **Arquitectura del Engine Dialógico:** Diseñar estructura de prompts que force el modelo a actuar como "Crítico Creativo", no como asistente secundario.
2.    **Parsing de Beats Files:** Implementar lectura contextual de archivos `.md` con soporte a rutas relativas, saltos de escenas y referencias cruzadas.
3.    **Graph View Simplificado:** Visualización básica de ramificaciones en consola con indicador visual de divergencia (branch depth).

## **🚀 FASES POSTERIORES (Roadmap de Crecimiento)**

| VERSIÓN | DESCRIPCIÓN | PRIORIDAD |
|---------|-------------|-----------|
| **v0.1** (Actual) | Motor Dialógico + Beats Parser básico | CRÍTICA |
| **v0.2** | Graph View interactivo con resaltado de ramas divergentes | ALTA |
| **v0.3** | Personajes como entidades editables con archivos definitorios propios | MEDIA |
| **v0.4** | Importación de novelas completas y análisis estructural previo | BAJA |

## **📊 CRITERIOS DE ÉXITO (Métricas Creativas)**

1.  **Frecuencia Dialógica:** El usuario debe sentirse escuchado como co-creator, no como usuario input.
2.  **Coherencia Canon:** Todas las ramificaciones deben respetar el tono y estructura del original.
3.  **Utilidad Inmediata:** Poder continuar escribiendo después de la sesión sin perder contexto.

## **🛡️ RIGOR TÉCNICO**

-   **Build Target:** React 19 + Vite + TanStack Start
-   **Editor:** Monaco Editor con soporte Markdown nativo
-   **Backend Supabase:** Auth + Realtime para multi-sesión básica
-   **Export:** PDF (PDFKit) + DOCX (libreoffice-wasm)

---
*(FIN DEL PLAN)*