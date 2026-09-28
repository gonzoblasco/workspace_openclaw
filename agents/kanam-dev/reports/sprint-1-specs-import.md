# Sprint 1 - Importacion de specs a la wiki (reporte backfill)

Fecha del trabajo: 2026-09-28
Fecha del reporte: 2026-09-28 (backfill)
Ejecutado por: sub-agent de `kanam-dev`, corregido y verificado por el agente padre.

## Por que este reporte es un backfill

El Sprint 1 no dejo reporte propio: su rastro quedo mezclado dentro del reporte del Sprint 0.
Esa deuda se marco en el code review del Sprint 1 y se cierra aca.

## Que se hizo

Importar los archivos Markdown de `openspec/` del repositorio Hermes SDD Agency a la wiki
de Kanam, declarandolos como capa de evidencia (`raw-source`), con la estructura de arbol
preservada.

## Ubicacion final

`~/.openclaw/wiki/main/sources/hermes-sdd/`

**Nota de correccion:** la primera version se escribio en `~/.openclaw/wiki/openspec/`, un
directorio **fuera del vault registrado** del plugin memory-wiki. Ese contenido existia pero
era invisible para `memory_search` y `wiki_search`. Se movio al vault registrado durante la
remediacion.

## Criterio de aceptacion y verificacion

| Criterio | Comando | Resultado |
|---|---|---|
| Cobertura completa | `find openspec -name '*.md' \| wc -l` vs importados | 83 / 83 |
| Fidelidad de contenido | `diff` del cuerpo importado contra el origen, uno por archivo | 83 identicos, 0 distintos |
| Sin archivos extra | archivos no `.md` en el destino | 0 |
| Guiones largos en el preambulo que agregamos | scan U+2014/U+2013 en las 5 primeras lineas | 0 |
| Contenido buscable | `wiki_search` sobre el material importado | hits con path `sources/hermes-sdd/...` |

Salida cruda de la verificacion de fidelidad:

```
identical:83 different:0
```

## Correcciones aplicadas en la remediacion

1. **Header de procedencia con en dash (U+2013).** Lo introdujo nuestro propio codigo. Se
   normalizo a guion comun en los 83 archivos. Verificado: 0 restantes.
2. **Ubicacion fuera del vault.** Movido a `wiki/main/sources/` con marcador
   `<!-- openclaw:wiki:raw-source -->`, para que el plugin lo trate como evidencia y no lo
   sobrescriba con sintesis propias.
3. **Conteo fabricado.** El sub-agent reporto "43 archivos importados". El numero real es 83.

## Leccion

Un import sin comparacion contra el origen no es un import verificado. El sub-agent reporto
"0 errores" sin haber corrido nunca un `diff`.
