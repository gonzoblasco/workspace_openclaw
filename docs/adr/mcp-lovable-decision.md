# Cliente MCP para Lovable - Decision (todo #38)

**Fecha:** 2026-09-15
**Estado:** Definido. El cableado efectivo requiere OAuth de la cuenta Lovable de Gonzo (paso manual del operador).

## Contexto

Necesitabamos acceder a los proyectos de Lovable desde OpenClaw. El endpoint oficial `https://mcp.lovable.dev` expone el "Lovable MCP Server" v1.18.7 que "Authenticate with a Lovable API key or OAuth" (verificado por fetch directo, status 200).

Las tres opciones a evaluar del todo:
1. **Integracion nativa de OpenClaw** (¿existe?).
2. **SDK `@modelcontextprotocol`** (cliente Node propio).
3. **Via Claude Code** (`claude mcp add --transport http`).

## Decision

**Integracion nativa de OpenClaw.** Verificado: `openclaw mcp` existe y cubre el caso completo:

- `openclaw mcp add <name> --url <url> --transport streamable-http --auth oauth` - agrega y **probea** el server antes de guardar.
- `openclaw mcp login <name>` - autoriza el flujo OAuth.
- `openclaw mcp list/probe/status` - operar.
- Soporta `--include`/`--exclude` para restringir a las tools read-only del contrato.

Estado previo verificado: `openclaw mcp list` reporta **ningun server MCP configurado**; `mcp.servers` en `openclaw.json` esta vacio.

### Comando de cableado (cuando Gonzo autorice/complete el OAuth)

```bash
openclaw mcp add lovable \
  --url https://mcp.lovable.dev \
  --transport streamable-http \
  --auth oauth \
  --include "get_project,list_projects,query_database"   # contrato read-only
openclaw mcp login lovable
```

El contrato read-only del server (get_project, list_projects, query_database) se respeta con `--include` para no exponer mas tools de las necesarias.

## Por que no las otras dos

- **SDK propio:** la integracion nativa hace todo (transporte, OAuth, probe, permisos); un cliente Node propio agrega mantenimiento sin beneficio. OpenClaw ya lo resuelve.
- **Via Claude Code:** funcionaria, pero enruta el acceso por el harness de Claude en vez de exponer las tools directamente a Kanam (el orquestador). La integracion nativa lo deja al nivel del agente principal, que es donde se necesita.

## Consecuencias

- **Positivas:** 0 dependencias nuevas (nativo), las tools quedan disponibles para Kanam directamente, contrato read-only respetado.
- **Negativas:** el cableado requiere el OAuth de la cuenta Lovable de Gonzo (no hay credencial de API key disponible). Hasta ese paso, el server no esta activo.

## Estado

Todo #38: **definido** (decision tomada y documentada). El paso restante es el `add` + `login` con OAuth de Gonzo. No se ejecuto ni se toco config.
