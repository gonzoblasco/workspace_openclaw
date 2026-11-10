# HANDOFF - workspace

**Fecha:** 2026-11-10 18:25 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-10). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-10.md`.

---
## Que se hizo en esta sesion

### 2026-11-10 18:25
Sesion corta: arranque + montaje de la clase studies/n8n-ai-automations desde el video YY-egxTQirA (n8n Full Course, freeCodeCamp.org, Rahul Joshi, 43:05). Caption automatico en ingles via youtube-transcript-api (1173 cues), agrupado en 153 bloques con timestamp; transcripcion.md con glosario ASR de 20 filas y los 14 capitulos oficiales; outline.md con 14 modulos 1:1, 14 ejercicios y 9 preguntas. Todos los timestamps verificados por grep de la cita literal; dos citas corridas corregidas (polling 27:41 -> 27:32 y 27:49; 'flagging exactly' en 14:52). README de studies actualizado. Commits locales 49456dadd2 (clase) y ff17d12a25 (memoria + HANDOFF del curso), sin push. Queda pendiente: los dos scripts de gateway sin trackear (scripts/reinstall-gateway-service.sh, scripts/reload-gateway-service.sh) NO son de esta sesion, se dejan como estan.

### 2026-11-09 23:27
POLITICA DE MODELOS: beam:cloud fuera de toda asignacion de primario (dejo de ser gratuito y produjo errores en dos sesiones de cursos de YouTube); deepseek-v4.1-flash:cloud vuelve a primario del CORE y de los defaults; gemma4:12b-mlx (local) queda como UNICO fallback de los nueve agentes, sin escalones cloud intermedios. Escrito como ADR-112 con verificacion ejecutable. GATEWAY E IPAD: el iPad no conectaba al gateway; la causa era triple (Tailscale sin perfil VPN, hostname apuntando a la Mac apagada mac-mini-de-gonzalo sin -1, y Tailscale Serve enrutando por nombre y no por IP). Se cambio gateway.bind a tailnet y tailscale.mode a off; el gateway ahora escucha en 100.126.255.95:18789 y la app entra con ws:// sin cifrar. Drift aceptado (3 campos, los tres del cambio). AUDITORIA DEL CORE: 9 sesiones de main corrieron con beam entre el 07 y el 08 (1,71M tokens, 4 commits). Se ejecuto cada artefactoC y se contrasto cada flag documentado contra --help: 3 defectos, todos corregidos (typo 'gobnar' en AGENTS.md, presupuesto de bootstrap a 5 caracteres del limite, y el flag inexistente --dry-run en el LEARNINGS del auditor). CVS: Gonzo corrigio el rumbo; dos referencias de contribuciones apuntaban a issues sin comentarios (#9868 y #9866 en vez del PR #9869 y el issue #9865) y el ATS declaraba UADE (carrera universitaria, prohibida por la regla del 2026-11-04). Corregidas las tres referencias, carrera fuera del ATS, y career-facts gana la seccion 5.2.1 con las siete contribuciones verificadas por API de GitHub. check-cv-facts.py ahora valida referencias contra el corpus y carreras en cualquier salida de postulacion.

## Estado actual

Workspace limpio salvo esos dos scripts ajenos. Clase n8n cerrada y commiteada.

### Estado previo (heredado)

ADR-112 aceptado y commiteado; gateway en tailnet; CVs de Feltsense y Mercado Libre corregidos y regenerados (ML en 2 paginas); gate de CV extendido.

## Proximos pasos

1. Retomar studies/n8n-ai-automations cuando Gonzo elija el primer workflow real a implementar (modulos 3/6/11 son el mismo patron). Pendientes de otra sesion: integracion de assets CC0 en projects/edad-de-los-reinos.

### Pendientes heredados (sin cambios)

1) Verificar contra GitHub las 19 referencias de CVs historicos que no estan en el corpus y agregarlas a career-facts 5.2.1. 2) Limpiar las carreras universitarias de los 5 CVs historicos (EIT/HTC, Mercor, Sol, TEMPO) - son de otras sesiones. 3) Confirmar con Gonzo que el iPad quedo operativo con ws://100.126.255.95:18789. 4) Watchdog de canales: el timeout del trigger sigue sin resolver si se repite.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-10.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*

## Decisiones y contexto que no debe perderse

- Fallback unico local por decision de Gonzo: 'el fallback no puede ser otro modelo en la nube'. Primario deepseek y no beam: dejo de ser gratuito y su calidad ya estaba descartada por ADR-105 (3/4 bugs, auto-aprobacion con defecto vivo). Ninguna carrera universitaria va a CV ni ATS (regla 2026-11-04). Una referencia de CV se verifica abriendo el hilo en GitHub, no contra el corpus.

## What This Is

OpenClaw personal workspace

## Tech Stack

OpenClaw, AI-assisted dev

## Current Goal

Manage Gonzo's projects, memory, and daily work

## Where I Left Off

v0.4 cerrada: dev-pipeline.yml corre 11 suites, gate de skills, rutas, copias de dash, docs del rol y roadmap del rol. runs.db persiste corridas y weekly cuenta por semana ISO. Una corrida real completa (task #5) registrada. Los cuatro ejecutables de medicion (metrics_scan, dep_inventory, compat_matrix, bench_compare) verificados contra repos reales.

## Next Steps

1. Usar el pipeline en el proximo trabajo real que asigne CORE, sin evidencia declarada a mano, para probar v0.5 con un cambio que pueda fallar
2. Medir demanda real desde sesiones y memoria a las dos semanas (hito 5.4 quedo con una sola corrida, no mide uso)
3. Decidir si se limpian las 91 skills de otros roles sin verificacion y las 87 rutas ambiguas fuera del arbol de dev

## Blockers

- La corrida #5 tardo 0s y verify solo corrio tests que ya pasaban: el pipeline no se probo contra un cambio que pueda fallar de formas interesantes
- La metrica de demanda tiene una sola corrida: no mide uso todavia

## Decisions Made

| Decision | Why | Date |
|----------|-----|------|
| Los gates de CI se acotan al arbol de kanam-dev, no al workspace | docs_sync da 409 desalineaciones y check-roadmaps falla por studio; bloquear por deuda ajena empuja al --no-verify, que es peor que no tener gate | 2026-11-10 |
| El registro en runs.db es best-effort: si falla, el pipeline sigue | Un fallo de telemetria no puede tumbar un pipeline que ya hizo el trabajo; se avisa por stderr, no se calla | 2026-11-10 |
| runs.db inserta una vez y actualiza la misma fila en cada guardado | El runner guarda por estacion para poder retomar; insert-only dejaba una corrida que murio a mitad marcada como completo para siempre | 2026-11-10 |
| audit y docs_sync detectan Python sin manifiesto por los test_*.php presentes, incluidos los de bin/ | El rol no tiene pyproject ni package.json y el pipeline no podia verificar su propio repo | 2026-11-10 |
| Un 0 de unittest discover es error de medicion, no realidad: 0 | El cero significa que no busco donde estan los tests; aceptarlo como conteo real es un falso positivo del verificador | 2026-11-10 |

## Session History

### 2026-08-02 - Configured session-context on workspace
**Left off:** Showing usage example to Gonzo
### 2026-08-02 - Testing session-context save
**Left off:** Writing save.mjs script
### 2026-11-06 - Sesion de demanda de Kanam DEV: diagnostico (el cuello era invocacion, no skills), construccion de la superficie de pipeline completa y cierre del roadmap v0.2.
_1971 commits, 114 files changed_
**Left off:** Superficie del pipeline terminada y commiteada: intake (S1), despachador kanam-dev con 8 subcomandos, runner con plantillas y resume, slice-commit, docs-sync y handoff gate. 134 tests verdes. Skill kanam-dev-surface registrada. Roadmap v0.2 commiteado con indice y tracking sincronizados.
### 2026-11-10 - Auditoria de la ventana de cambio de modelo (beam a deepseek), correccion de los defectos medidos, U4 completo con cuatro ejecutables, runs.db (hitos 5.1-5.5) y CI del rol (v0.4). De 134 a 254 tests.
_61 commits, 165 files changed_
**Left off:** v0.4 cerrada: dev-pipeline.yml corre 11 suites, gate de skills, rutas, copias de dash, docs del rol y roadmap del rol. runs.db persiste corridas y weekly cuenta por semana ISO. Una corrida real completa (task #5) registrada. Los cuatro ejecutables de medicion (metrics_scan, dep_inventory, compat_matrix, bench_compare) verificados contra repos reales.
