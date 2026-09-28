# Cómo Kanam OS Despacha Tareas entre Agentes Especializados

**El protocolo Router Pattern: Orquestación sin saturación** 🎯

La verdadera magia de Kanam OS no está en *qué* pueden hacer los agentes individualmente, sino en **cómo coordinan** sin que el orquestador se sature.

---

## El Problema de la Saturación

Imagina un equipo donde:
- El líder intenta ejecutar todas las tareas personalmente
- Se pierde el tiempo haciendo cosas operativas que otros podrían resolver mejor
- La calidad disminuye porque cada tarea recibe atención fragmentada

**Esto es exactamente lo que había en Kanam OS 1.0.** Un agente generalista cargaba todas las skills y intentaba hacer todo, perdiendo eficiencia y precisión. 📉

---

## La Solución: Router Pattern (ADR-074)

Hoy implementamos un **protocolo de despacho** que separa claramente responsabilidades. No es magia negra -es arquitectura limpia. 🔧

### 1. Interpretación
```javascript
// Kanam CORE recibe el prompt del usuario
const userIntent = await parseUserPrompt("Crear un nuevo skill de accesibilidad para React");

// Resultado: { type: "skill-creation", category: "a11y", complexity: "high" }
```

### 2. Selección de Especialista
```javascript
// El Core consulta el Mapa de Orquestación
const requiredSkill = await mapUserIntent(userIntent); 
// → "kanam-dev/skill-creation"

const specialist = await findAgentWithCapability(specialists, requiredSkill);
// → Kanam DEV (especializado en ingeniería)
```

### 3. Delegación Contextual
```javascript
// El CORE invoca con contexto específico
await sessions_spawn({
  target: "kanam-dev",
  context: {
    taskType: "skill-creation",
    domain: "a11y",
    requirements: ["WCAG 2.2", "react-aria", "unit-tests"],
    summary: "Crear un skill que genere componentes React accesibles"
  },
  prompt: "Como especialista en ingeniería de software, crea..."
});
```

### 4. Retorno para Síntesis
```javascript
// El especialista devuelve el resultado al Core
const devResult = await sessions_yield(); 
// → Skill creado y testeado por DEV

// El CORE hace síntesis final
await core_synthesize(devResult);
// → "✅ Skill 'a11y-accessible-component' listo para producción"
```

---

## Protocolo de Despacho por Especialidad

| Tarea | Agente Responsable | Criterio de Delegación |
|-------|-------------------|------------------------|
| Escribir código, refactorizar, implementar specs | **Kanam DEV** 💻 | Skill requiere conocimiento técnico profundo |
| Deploy, CI/CD, servidores, configuración infraestructura | **Kanam OPS** 🛠️ | Toca infraestructura, gateway, tooling |
| Análisis de corpus, minería de datos, resúmenes de contexto | **Kanam MIND** 🧘 | Requiere investigación, insights, conocimiento |
| Diseño UI, narrativa, generación de activos creativos | **Kanam STUDIO** ✍️ | Toca comunicación, marca, creatividad |

---

## El "Context Handover" - Previniendo la Pérdida de Contexto

Uno de los mayores riesgos en sistemas multi-agente: que cada uno re-descubra lo que otro ya hizo. Para evitar esto, **cada finalización de tarea incluye un bloque de Estado de Contexto**:

```markdown
---
### Summary
Se implementó el sistema de autenticación con JWT en frontend y backend. Los componentes básicos están funcionales.

### Status
✅ Draft → ✅ Ready para integración

### Next Steps
- Integrar con el sistema de billing
- Agregar refresh tokens
- Testeear flujo completo de sesión

### Resources
📁 /workspace/agents/kanam-dev/auth/jwt-system/
🔗 Link a PR mergeado: https://github.com/gonzoblasco/workspace_openclaw/pull/10517
---
```

Este formato asegura que cualquier agente que entre en la tarea entienda:
- Qué se logró antes (sin tener que investigar)
- El estado actual del activo
- Qué falta para completar el trabajo
- Qué recursos ya existen

---

## Gestión de Conflictos: ¿Quién Decide?

¿Qué pasa cuando una tarea requiere múltiples especialistas?

### Flujo de Decisión:

```
1. CORE identifica la Tarea Primaria
   → "Implementar autenticación OAuth"

2. CORE selecciona el especialista principal
   → Kanam DEV (escribe código)

3. CORE solicita al DEV que identifique si necesita apoyo
   "Este módulo requiere configuración del gateway para middleware de auth"

4. CORE coordina intervención del segundo agente
   → Kanam OPS configura el gateway
```

**La clave:** El principal especialista **debe identificar** los gaps y pedir ayuda. No es automático -requiere comunicación clara dentro del sistema.

---

## Ventajas Claras

✅ **Eficiencia Operativa** - Cada experto hace lo suyo sin saturar al orquestador  
✅ **Precisión Técnica** - Menos ruido cognitivo = mejor calidad de entrega  
✅ **Escalabilidad** - Podemos agregar especialistas sin afectar el núcleo estable  
✅ **Versionado Completo** - Git tracking en cada workspace aislado  

---

## Conclusión

Kanam OS no es magia. Es arquitectura bien definida donde:
- Un solo punto de entrada (CORE) mantiene la coherencia estratégica
- Agentes especializados ejecutan con contexto relevante
- Memoria compartida via RAG evita que se pierda conocimiento
- Protocolos claros previenen pérdida de contexto

**Sígueme** para ver cómo funcionan los 5 cerebros especializados en acción: qué hace cada uno, cómo comparten memoria y qué tipo de tareas delegan entre sí. 🧠🔥

---

*Publicado 28/09/2026 | #KanamOS #MultiAgentArchitecture #RouterPattern #SoftwareArchitecture #AI #DevOps #Orchestration*
