# Kanam OS: Arquitectura Multi-Agente

**Hook**
> ¿Un solo agente puede realmente comprender y ejecutar todo un ecosistema? Kanam OS lo muestra con cinco cerebros especializados.

## Problema del monolito
- Un agente único carga cientos de *skills* → contexto saturado, latencia alta, difícil de depurar.
- Los logs y la trazabilidad se pierden entre tareas múltiples.

## Solución (ADR-073)
- **Redistribución de skills** a agentes especializados:
  - `kanam-core` : estrategia, identidad, gobernanza.
  - `kanam-dev` : ingeniería, UI, testing.
  - `kanam-ops` : infraestructura, gateway, sistemas.
  - `kanam-mind` : investigación, datos, RAG.
  - `kanam-studio` : contenido, voz, branding, OSS.
- Cada directorio contiene solo las habilidades relevantes, reduciendo el contexto y favoreciendo paralelismo.

## Comunicación entre agentes (ADR-074)
- **Protocolo de despacho** usando `sessions_send` / `sessions_spawn` con payload `agentTurn`.
- Los agentes esperan resultados con `agents_wait`, manteniendo logs completos y un *human-in-the-loop* para acciones destructivas.

## Beneficios
- **Escalabilidad**: sub-agentes pueden ejecutarse en paralelo.
- **Mantenibilidad**: cada agente tiene su propio ciclo de vida y pruebas.
- **Trazabilidad**: logs por agente, auditoría fácil.

---
**CTA**: Sigue la serie para ver cómo cada agente coopera y cómo aplicar esta arquitectura en tu proyecto.
