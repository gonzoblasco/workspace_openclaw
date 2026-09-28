# Kanam OS: Seguridad y gestión de secretos

**Hook**
> “Tus credenciales no son un dato más, son la llave que protege todo el ecosistema.”

## Por qué los secretos son críticos
- Cada agente que interactúa con APIs externas necesita credenciales (GitHub, OpenAI, Stripe, etc.).
- Exponerlas en código o logs rompe la regla de “no exfiltrar datos privados”.

## Herramienta `secrets`
| Acción | Qué hace |
|--------|----------|
| `request` | Pide al operador que ingrese un valor (oculto, sin eco). |
| `list` | Muestra solo metadatos (nombre, tipo, última actualización). |
| `delete` | Elimina el secreto del almacén seguro. |

### Flujo típico de uso
1. **DEV** necesita el token de GitHub → `sessions_send` al agente **CORE** con payload `secrets request` (nombre `GITHUB_TOKEN`, razón “Clonar repositorio para generar artículo”).
2. El operador ingresa el token en el prompt de aprobación.
3. El secreto se almacena en el vault con `allowedHosts` (p. ej. `api.github.com`).
4. **OPS** usa el secreto en una llamada a la API sin exponerlo en los logs.

## Buenas prácticas
- **Principio del menor privilegio:** habilitar solo los hosts estrictamente necesarios.
- **Rotación periódica:** programar una automatización (`automations`) que recuerde cambiar tokens cada 90 días.
- **Auditoría:** registrar cada request/uso en la vault (consultable con `memory_search`).

---
**CTA**: En el próximo post vemos cómo cerrar el ciclo de feedback con ADRs y validaciones humanas.
