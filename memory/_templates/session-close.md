# Plantilla: informe de cierre de sesion

> Destino: se registra como una seccion `## Sesion YYYY-MM-DD (<franja>) - <titulo>` en
> `memory/YYYY-MM-DD.md`, escrito por `scripts/memory-end-session.py` (o el flush de cierre).
> Es la plantilla del informe **detallado** de cierre: hechos verificables, no adjetivos.
> El HANDOFF del proyecto (`scripts/session-handoff.py`) se deriva de este informe.

## Sesion YYYY-MM-DD (<franja>) - <titulo de una linea>

**Fecha:** <dia, fecha> | <hora GMT-3>
**Autor:** Kanam CORE | **Contexto:** <el pedido que abrio la sesion>

### 1. <tema>

<Que paso, que se decidio, con numeros y evidencia. La causa, no solo el sintoma.
Si hubo correccion de Gonzo, se registra. Citar commits, rutas y comandos exactos.>

### 2. <tema>

<...>

### N. <tema>

<...>

### Commits de la sesion (todos pusheados a `<branch>`)

| Commit | Que |
|---|---|
| `<sha corto>` | <cambio> |
| `<sha corto>` | <cambio> |

### Gates / verificacion al cierre

- `<check>`: <resultado>
- `<check>`: <resultado>

### Lecciones durables de la sesion

- <leccion, en una frase, accionable>

### Pendientes abiertos (si hay)

- <pendiente con su disparador de continuacion>

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
