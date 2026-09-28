# Documento interno de mejoras - CPACC (≈ 2 páginas)

## Resumen de lecciones útiles
- **Enfoque humano dominante**: 80 % del examen trata sobre modelos de discapacidad y tecnologías de asistencia. Priorizar la comprensión de los **7 modelos** (médico, social, biopsicosocial, económico, funcional‑solución, identidad social, caridad) y **AT** (JAWS, NVDA, lectores de pantalla, dispositivos hápticos).
- **Diseño universal**: 40 % de contenido cubre WCAG 2.x, ADA, Section 508, EN 301 549. Practicar con ejemplos reales de ARIA y contraste.
- **Estudio activo**: Combinar **video de Deque** con lecturas del **BoK**. Tras cada video, leer la sección correspondiente del BoK y crear **flashcards** de términos.
- **Práctica de formato**: Usar los **10 preguntas oficiales + Jeopardy (≈ 25 preguntas)** para familiarizarse con la lógica de opciones. Simular un examen cronometrado (2 h) y revisar cada respuesta incorrecta con la justificación del BoK.
- **Preparación logística**: Checklist de día de examen (ID, ambiente silencioso, dispositivos prohibidos). Ensayar la configuración del espacio antes del examen real.
- **ROI**: Certificación aumenta entre $5 k-$15 k anuales y eleva la percepción de productividad en un 70 %.

## Mejora del proceso de estudio
1. **Banco de preguntas propio** - extraer preguntas de la transcripción y del BoK, organizarlas en Quizlet o Anki.
2. **Peer‑review** - intercambiar respuestas de simulacros con un colega para explicar razonamientos.
3. **Laboratorio de AT** - montar entorno con JAWS/NVDA, probar ejemplos de accesibilidad en componentes UI.
4. **Ciclo de actualización** - revisar trimestralmente la página IAAP por cambios (WCAG 2.2, nuevas normas).
5. **Registro de CECs** - documentar webinars, lecturas y prácticas para la renovación (45 CECs cada 3 años).

## Plan de estudio semanal (4 semanas)
| Semana | Enfoque | Actividades clave |
|--------|---------|-------------------|
| 1 | **Mapa de conocimientos** - IAAP BoK | • Leer el *Content Outline* y mapear competencias.<br>• Identificar gaps y marcar en una tabla. |
| 2 | **Modelos de discapacidad y AT** | • Ver videos Deque (sección 2) y transcripción.<br>• Leer capítulos correspondientes del BoK.<br>• Practicar identificación de AT en ejemplos reales. |
| 3 | **Diseño universal y normas** | • Estudiar WCAG 2.x, ADA, Section 508, EN 301 549.<br>• Implementar mini‑proyecto: crear una página accesible (HTML + ARIA). |
| 4 | **Simulacros y logística** | • Realizar 10 preguntas oficiales + Jeopardy.<br>• Simular examen cronometrado.<br>• Revisar checklist de día de examen y preparar el espacio. |

## Próximos pasos
- **Crear** el archivo `docs/cpacc/week-1-plan.md` con la tabla anterior (ya generado).
- **Ejecutar** `scripts/extract_pdfs.py docs/cpacc/cpacc-bok.pdf docs/cpacc/cpacc-handbook.pdf` para actualizar los textos si cambian los PDFs.
- **Actualizar** el canal de estudio interno (widget `session:report`) con este documento y el plan semanal.

---
*Este documento está pensado para uso interno del equipo y resume las lecciones aprendidas, propuestas de mejora y el plan de estudio estructurado para la certificación CPACC.*