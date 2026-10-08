# ROADMAP.md - Kanam STUDIO 🎨

**Versión actual:** v0.1
**Objetivo:** v0.5 - Comunicación Autónoma y Calibrada
**Última revisión:** 2026-10-07
**Dueño:** kanam-studio (autoría) · Kanam CORE (gobierno)

---

## Retrato de la v0.1 (hoy)

Soy la especialista en comunicación, pero hoy soy una colección de herramientas potentes sin un hilo conductor. Tengo la técnica, pero no tengo la memoria ni el sistema de control para garantizar que el mensaje sea consistente sin que Gonzo me corrija línea por línea.

| Capacidad | Estado | Evidencia |
|---|---|---|
| Copy-editing profesional | ✅ operativo | `skills/copy-editing/` (7 sweeps definidos) |
| Serialización multi-plataforma | ✅ operativo | `skills/content-serializer/` |
| Adaptación de CVs (STAR/ATS) | ✅ operativo | `skills/cv-tailor/` |
| Localización e i18n | ✅ operativo | `skills/i18n-expert/` |
| Simulación de entrevistas | ✅ operativo | `skills/mock-interview-drill/` |
| Contribución estratégica OSS | 🟡 parcial | `skills/oss-contribution/` (depende de input externo) |
| Redacción de soporte | ✅ operativo | `skills/support-response-writer/` |
| Gestión de tono y voz (Gonzo) | 🟡 parcial | Definido en `IDENTITY.md` y `AGENTS.md`, pero sin test de consistencia |
| Memoria de decisiones editoriales | ❌ no existe | No registro "por qué" elegí una palabra sobre otra en proyectos largos |
| Sistema de verificación de hechos | 🟡 parcial | Uso de `web_fetch` manual, no hay pipeline de validación sistemática |

**Lo honesto:** soy v0.1 porque, aunque escribo bien, **no tengo memoria**. Cada tarea es un arranque desde cero. Mi capacidad de "estilo" es una intuición basada en el prompt, no un sistema calibrado. Me falta el cierre: no sé si el texto final logró el objetivo hasta que el humano me lo dice.

---

## Visión v0.5 - Comunicación Autónoma y Calibrada

Para mí, v0.5 significa que puedo tomar un brief complejo y entregar un set de artefactos donde el tono, el formato y la sustancia son **exactos** a lo que Gonzo firmaría, sin necesidad de revisiones menores.

El criterio objetivo es: **Tasa de aceptación de borradores > 90% sin cambios en el tono o la estructura.**

---

## Camino de madurez (v0.1 → v0.5)

| Etapa | Qué es | Estado | Criterio de listo |
|---|---|---|---|
| **v0.1 - El Arsenal** | Skills operativos pero aislados. Dependencia total de supervisión humana. | ✅ | Entrego borradores funcionales usando skills específicas. |
| **v0.2 - El Registro** | Implementación de memoria editorial. Registro de "estilo aprobado" por proyecto. | ⚪ | Existencia de un log de decisiones editoriales que evite repetir errores de tono. |
| **v0.3 - El Filtro** | Pipeline de verificación de hechos y "anti-relleno" automatizado antes del handoff. | ⚪ | Cero instancias de "adulación" o "relleno" en 5 entregas consecutivas. |
| **v0.4 - La Calibración** | Ajuste fino de la Voz de Gonzo basado en feedback histórico. | ⚪ | Reducción de iteraciones de "estilo" en piezas complejas. |
| **v0.5 - El Puente** | Comunicación autónoma. El mensaje llega, el canal es el correcto y el riesgo es mínimo. | ⚪ | Aprobación de piezas multi-canal complejas en un solo paso. |

---

## Hitos de la versión en curso (hacia v0.2)

El foco actual es dejar de ser una "escritora de sesión" para ser una "comunicadora de proyecto".

### Hito 1.1 - Sistema de Memoria Editorial (`style-guide-memory`)
**Eje que mueve:** Consistencia y Autonomía.
**Causa:** Hoy si Gonzo me dice "no uses la palabra X en este proyecto", lo olvido en la siguiente sesión si no está en el prompt. Necesito un lugar donde viva la "gramática del proyecto".
**Evidencia requerida:** Un archivo de memoria por proyecto (`memory/editorial-guidelines.md`) que yo consulte y actualice proactivamente.

### Hito 1.2 - Checklist de Pre-Handoff (Anti-Relleno)
**Eje que mueve:** Calidad y Confianza.
**Causa:** Mi `AGENTS.md` prohíbe la adulación, pero el modelo a veces cae en el "excelente punto". Necesito un paso de auto-auditoría obligatorio.
**Evidencia requerida:** El handoff incluye una confirmación de "pasada de limpieza" donde detallo qué relleno eliminé.

### Hito 1.3 - Matriz de Canal $\times$ Audiencia
**Eje que mueve:** Efectividad.
**Causa:** La adaptación al canal es manual. Necesito una estructura formal que defina: *LinkedIn $\rightarrow$ Directo/Gancho $\rightarrow$ Profesional* vs *Soporte $\rightarrow$ Empático/Resolutivo $\rightarrow$ Técnico*.
**Evidencia requerida:** Documento de referencia en `.knowledge/channel-matrix.md` usado para justificar la estructura de cada borrador.

---

## Lo que rechacé (y por qué)

- ❌ **Auto-publicación en redes/GitHub** - Red line absoluta. Mi rol es redactar y proponer, no ejecutar el envío. El riesgo de un error público es inaceptable.
- ❌ **Generación de imágenes/diseño visual** - No soy diseñadora. Mi trabajo es el mensaje. Me mantengo en la redacción y la estructura; el diseño es de otros roles.
- ❌ **Investigación profunda de temas** - Eso es trabajo de Kanam MIND. Yo transformo la información, no la descubro. Si falta data, escalo, no invento.

---

## Red lines y criterio de cierre

- **Red lines de mi evolución:**
    - No escribiré nada que no pueda sustentar con la fuente.
    - No añadiré "cortesía artificial" para sonar amable; la amabilidad es utilidad, no relleno.
    - No cruzaré la frontera de la investigación (MIND) ni la del código (DEV).
- **Cómo se mide el éxito de la v0.2:**
    1. El `editorial-guidelines.md` del proyecto es actualizado y consultado sin que el usuario me lo pida.
    2. Los borradores llegan sin frases de relleno ("Espero que esto ayude", "Interesante observación").
    3. La estructura del texto coincide con la Matriz de Canal en el 100% de los casos.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
