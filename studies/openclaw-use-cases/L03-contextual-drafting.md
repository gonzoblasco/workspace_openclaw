# Lección 3: Redacción de Respuestas Conscientes del Contexto en Nombre del Usuario
Clase: OpenClaw Use Cases

## Concepto Central
La transición de un bot que responde dudas a un asistente que actúa en representación del usuario. El principio fundamental es la **Preservación de la Agencia Humana**, asegurando que el asistente nunca tome decisiones comprometedoras sin supervisión.

## El Patrón de Artefacto Etapificado (Staged Artifact)
En lugar de enviar mensajes directamente, OpenClaw implementa un flujo de revisión:
1. **Generación de Borrador**: El agente redacta una propuesta de respuesta basada en el contexto recuperado.
2. **Justificación (Rationale)**: El agente anota por qué escribió el mensaje de esa forma y qué datos utilizó (o cuáles faltaron).
3. **Etapificación (Staging)**: El borrador se coloca en un estado de "pendiente de revisión".
4. **Aprobación Humana**: El usuario revisa, edita y confirma el envío.

## Reglas de Oro para la Redacción
- **Cero Suposiciones**: Si el dato no está explícito en las herramientas (ej. calendario), el agente no puede inventarlo ni asumirlo.
- **Evitar la Deriva de Voz (Voice Drift)**: Uso de prompts negativos y ejemplos few-shot para mantener el tono del usuario en todos los canales.
- **Manejo de Ambigüedad**: Ante la falta de contexto, el asistente debe redactar preguntas aclaratorias en lugar de dar respuestas genéricas o incorrectas.

## Detalles Técnicos Clave
- **Drafts Stage**: El mecanismo técnico que separa la generación del envío.
- **Context Envelope**: El conjunto de datos (emails previos, calendario, notas) que el agente debe procesar antes de proponer el borrador.

## Notas
Este patrón es crítico para la confianza. Un asistente que alucina una cita en el calendario es un asistente que deja de ser útil. La seguridad reside en el loop: Generar $\rightarrow$ Justificar $\rightarrow$ Revisar $\rightarrow$ Enviar.
