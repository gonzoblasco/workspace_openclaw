# STATUS - Project Status

> **Última actualización:** 2026-08-28

## Estado actual

**In Development** - v1.0.0 funcional y validado contra la máquina real.

## Qué está hecho

- ✅ 5 checks de salud: **disco** (uso %, archivos grandes, caches), **memoria** (`vm_stat` real), **CPU** (load + procesos pesados), **seguridad** (firewall + launch agents), **red** (conectividad, latencia, DNS).
- ✅ CLI con `--json`, filtro por check (`disk,memory`), `--list`, `--help`.
- ✅ **Modo `--fix`** - escanea caches seguros (app, dev, npm, yarn) y los limpia con confirmación explícita por target. Flag `--yes` para scripting. También detecta y mata procesos pesados (>= 20% CPU) con confirmación, excluyendo procesos protegidos (launchd, WindowServer, kernel) y el propio proceso.
- ✅ **Reporte histórico/trend** - cada run se guarda en `~/.system-health-check/history.json` (últimos 100). Flag `--history` muestra historial + tendencia (improving/declining/stable).
- ✅ Reporter terminal (tabla con colores) + JSON.
- ✅ 46/46 tests unitarios en verde (Vitest).
- ✅ **Pulidos:** el CPU check excluye el propio proceso del top de consumidores; el fix de procesos excluye comandos de diagnóstico (du, ps, grep, etc.) para no listar la carga del propio escaneo.
- ✅ Validado en MacBook Air M2: reporte real 82/100, ~10.3 GB de caches recuperables detectados.

## Pendientes / próximos pasos

- [ ] Completar validación de checks en otra máquina (Linux/Windows) si aplica.

## Decisiones clave

- CLI-first, sin Electron.
- Checks aislados (un fallo no tumba la batería).
- Sin acciones destructivas automáticas - solo sugiere.
