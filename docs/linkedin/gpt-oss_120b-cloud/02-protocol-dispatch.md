# Kanam OS: El protocolo de despacho entre agentes

**Hook**
> "Los agentes hablan entre sí y hacen el trabajo en equipo" - la clave para escalar IA.

## ¿Por qué delegar?
- Un agente *A* puede generar código, pero necesita que *B* lo pruebe, *C* lo despliegue y *D* lo monitoree.
- El protocolo definido en **ADR-074** permite esa colaboración sin perder trazabilidad.

## Herramientas del protocolo
| Acción | Descripción |
|--------|-------------|
| `sessions_send` | Envía un mensaje a otro agente (p.ej. del agente `dev` al agente `ops`). |
| `sessions_spawn` | Crea un sub-agente aislado (p.ej. ejecutar pruebas unitarias). |
| `agents_wait` | Espera resultados de varios sub-agentes (fan-out). |
| `agentTurn` payload | Mensaje estructurado con `model`, `thinking`, `timeoutSeconds`. |
| `outputSchema` | Define la forma del resultado esperado (JSON). |

## Flujo típico (ejemplo práctico)
1. **Dev** escribe código → `sessions_spawn` con `task:"run-tests"`.
2. **Ops** recibe los resultados mediante `agents_wait`.
3. Si los tests pasan, **Ops** despliega usando `sessions_send` al agente `ops` con payload `deploy`. 
4. **Core** registra todo en la memoria y notifica al usuario.

## Human-in-the-loop
- Acciones destructivas (deploy, delete) requieren **confirmación** (campo `thinking` alto, revisión humana).
- Logs completos accesibles vía `sessions_history`.

---
**CTA**: En el próximo post veremos cómo la memoria compartida y el RAG impulsan la colaboración entre agentes.
