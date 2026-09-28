# Kanam OS: Los cinco agentes especializados

**Hook**
> "Cinco cerebros, un objetivo: hacer que la IA sea tan productiva como un equipo de desarrollo humano."

## Los agentes y sus dominios
| Agente | Área de enfoque | Skills típicas |
|--------|----------------|----------------|
| **CORE** | Estrategia, identidad, gobernanza, memoria global. | `agent-identity-provisioning`, `memory-wiki-vault`, `rule-enforcement-audit` |
| **DEV** | Ingeniería de producto, UI, pruebas, CI. | `react-ui-verification`, `nest-migration`, `spec-validation` |
| **OPS** | Infraestructura, gateway, sistemas, despliegues. | `gateway status`, `automations`, `process` |
| **MIND** | Investigación, datos, RAG, generación de conocimiento. | `memory_search`, `wiki_get`, `knowledge-graph-builder` |
| **STUDIO** | Contenido, voz, branding, OSS. | `image_generate`, `music_generate`, `video_generate` |

## Cómo cooperan (ADR-074)
1. **CORE** agenda una tarea semanal y envía a **DEV** mediante `sessions_send`. 
2. **DEV** genera el borrador, lo guarda y notifica a **OPS**. 
3. **OPS** crea el job de publicación y guarda el log en la vault. 
4. **MIND** consulta la vault para enriquecer el contenido con datos actualizados. 
5. **STUDIO** produce la imagen y el video de portada que **DEV** inserta antes de la publicación.

## Ventajas de la separación
- **Escalabilidad**: Cada agente puede escalar de forma independiente (p. ej. `MIND` en un nodo con GPU). 
- **Mantenibilidad**: Cambiar una funcionalidad solo implica actualizar el skill del agente correspondiente. 
- **Trazabilidad**: Logs por agente, cada paso registrado en `sessions_history`.

---
**CTA**: En el próximo post veremos cómo generar imágenes y videos de alta calidad con los agentes de **STUDIO**.
