# Vectores de amenaza por activo (STRIDE)

| Activo | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | EoP |
|--------|----------|-----------|-------------|-----------------|-----|-----|
| Página pública (p.ej.  / ) | - | - | - | - | X (filtración de UI estado) | X (flood de peticiones) | - |
| API de salud () | X (falsificar estado) | X (alterar respuesta) | - | - | X (flood) | X (si da acceso interno) |
| API de datos (p.ej. ) | X (suplantar usuario) | X (modificar datos) | X (negación de operación) | X (exposición de lista) | X (flood) | X (ESCALADA si faltan checks) |
| Componente UI (Nav.tsx) | X (suplantar nav) | - | X (negación de clic) | X (DOM expone estado) | - | - |
| Static export (next export) | - | - | - | - | - | - | - |

## Notas
- Spoofing: suplantar identidad o estado.
- Tampering: modificar datos o lógica en tránsito o en cliente.
- Repudiation: negar que se realizou uma ação (falta de trazabilidade).
- Info Disclosure: exposição não intencional de dados.
- DoS: esgotar recursos para tornar o serviço indisponível.
- EoP: Elevação de Privilégio (ganhar mais privilégios do que os atribuídos).
