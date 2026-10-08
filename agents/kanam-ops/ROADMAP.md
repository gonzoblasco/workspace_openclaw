# ROADMAP.md - kanam-ops 🛠️

**Versión actual:** v0.1  
**Objetivo:** v0.5 - Substrato autónomo y reversible  
**Última revisión:** 2026-10-07  
**Dueño:** kanam-ops autoría / Kanam CORE gobierno  

## 2. Retrato verificado de mi v0.1 (hoy)

| Capacidad | Estado | Comentario |
|---|---|---|
| Skill **background‑execution** | 🟡 parcial | Definido en `skills/background-execution/SKILL.md`; documentación completa, pero sin pruebas de ejecución real ni uso en producción. |
| Skill **clawdstrike** | ✅ operativo | Puede lanzar auditoría de seguridad del gateway y genera reporte OK/VULNERABLE. |
| Skill **gateway‑config** | 🟡 parcial | Provee UI Docker y API, pero la UI aún no está integrada en CI y depende de Docker en local. |
| Skill **skill‑vetter** | ✅ operativo | Protocolo de vetado de skills, detección de red flags y generación de informe. |
| Script **gateway‑audit.sh** | ✅ operativo | Genera snapshot de estado del gateway, canales y drift (JSON opcional). |
| Script **gateway‑config‑drift.sh** | 🟡 parcial | Produce JSON de drift; requiere revisión manual para aceptar cambios. |
| Script **gateway‑jobs‑check.sh** | ✅ operativo | Lista y verifica jobs del gateway. |
| Script **aggregate‑sync.sh** | 🟡 parcial | Sin pruebas automatizadas; usado manualmente para sincronizar estado. |

**Honestidad:** Falta automatizar pruebas de los skills y scripts, integrar `gateway‑config` en CI, y migrar toda la gestión de secretos a `SecretRef`. Estas carencias mantienen mi versión en v0.1.

## 3. Visión v0.5

En v0.5 seré capaz de sostener el sustrato del Gateway sin supervisión línea‑por‑línea. Cada cambio que realice quedará automáticamente respaldado (`cp ~/.openclaw/openclaw.json …`), verificado mediante `openclaw status`, logs de procesos y auditoría de drift, y será reversible con un único comando. Las configuraciones sensibles usarán referencias de secreto (`SecretRef`) y ningún token aparecerá en texto plano. Además, mis skills se ejecutarán bajo el patrón de **background‑execution**, permitiendo auditorías continuas y notificaciones automáticas cuando el estado se degrade.

## 4. Camino de madurez v0.1 → v0.5

| Etapa | Qué es | Estado actual | Criterio de listo |
|---|---|---|---|
| **v0.1 - Base** | Skills y scripts existentes, pero sin pruebas ni integración CI. | ✅ (presente) | Ninguno - versión base. |
| **v0.2 - Pruebas y CI** | Suite de pruebas automatizadas para *background‑execution*, *clawdstrike*, *gateway‑config*, *skill‑vetter* y los cuatro scripts; CI que ejecuta `gateway‑audit.sh --json`. | 🟡 parcial (solo pruebas manuales) | CI pasa 100 % de tests, incluye prueba de wake‑event para background‑execution. |
| **v0.3 - Gestión de configuración sin reinicio** | `gateway‑config` habilita edición segura con `--dry‑run`, usa `SecretRef` para credenciales, y acepta drift con `gateway‑config‑drift.sh --accept`. | 🟡 parcial (UI incompleta, secretref aún manual) | Demo de cambio de plugin que se revierte automáticamente si `status` muestra drift; secretref migrado al menos 3 credenciales. |
| **v0.4 - Pipeline de auditoría unificado** | Script `audit-pipeline.sh` orquesta *clawdstrike*, *gateway‑audit*, *gateway‑config‑drift* y genera reporte HTML/JSON con veredicto bloqueante; integrado en GitHub Actions. | ⚪ pendiente | Pipeline ejecuta end‑to‑end en CI, falla la build si vulnerabilidad crítica o drift no aceptado. |
| **v0.5 - Operación autónoma** | Todas las capas (ejecución, config, auditoría) funcionan en modo background, con notificaciones por wake, backup automático y reversión sin intervención humana. | ⚪ pendiente | 1️⃣ Background‑execution está en producción (al menos 5 auditorías diarias). 2️⃣ `gateway‑config` funciona con SecretRef y sin reinicio manual. 3️⃣ Pipeline de auditoría está en CI y bloquea merges críticos. |

## 5. Hitos de la versión en curso (v0.5)

| Hito | Capacidad que desbloquea | Evidencia requerida |
|---|---|---|
| **5.1** - Automatizar pruebas unitarias y de integración para todos los skills y scripts | Permite lanzar cambios con confianza de que no rompen el gateway. | Archivo `ci.yml` en `.github/workflows/` con 100 % de pass; reporte de CI archivado. |
| **5.2** - Integrar `gateway‑config` con `SecretRef` y validar sin reinicio | Elimina exposición de credenciales y permite cambios sin downtime. | `openclaw config set … --ref-id <NAME>` aplicado y verificado con `openclaw status`; registro de backup. |
| **5.3** - Implementar `audit‑pipeline.sh` que orqueste los scripts y genere veredicto único | Centraliza auditoría, produce bloqueos automáticos en CI. | Pipeline ejecutado en CI, produce `report.html` y falla la job si vulnerabilidad > “high”. |
| **5.4** - Activar notificaciones de wake para background‑execution | Notifica al operador cuando una auditoría ha finalizado o ha fallado. | Mensaje de wake visible en el UI de OpenClaw y en logs de sesión. |
| **5.5** - Migrar todas las credenciales a `SecretRef` (gateway‑config, plugins, modelos) | Refuerza seguridad y cumplimiento de política de secretos. | `openclaw config get …` muestra solo referencias; ausencia de tokens en `openclaw.json`. |

## 6. Lo que rechazo (y por qué)

- **UI completa de gestión de plugins dentro de `gateway‑config`.** La gestión de plugins ya está cubierta por `openclaw plugins enable/disable`; duplicar la UI dispersa responsabilidad y rompe la regla de “una vía oficial”.
- **Skill de auto‑reparación del gateway sin revisión humana.** Un proceso que modifica la configuración sin validar el outcome puede introducir drift irreparable; prefiero backups y verificación explícita.
- **Integración de Kubernetes‑operator para despliegue del gateway.** El rol está centrado en MacOS local; Kubernetes está fuera del alcance y sería dominio de otro rol (infra‑cloud). 

## 7. Red lines + cómo se mide el éxito

**Red lines (líneas rojas):**
1. Nunca editar `openclaw.json` a mano; siempre usar `openclaw config set/patch`.
2. Nunca almacenar secretos en texto plano dentro de código, README o variables de entorno.
3. No ejecutar cambios que requieran reinicio del gateway sin aprobación explícita del CORE.
4. No delegar tareas de auditoría a otros roles (Dev, Auditor) sin coordinación.

**Métricas de éxito** (todas deben cumplirse para declarar v0.5):
1. **100 % de cambios respaldados** - Cada `openclaw config set` genera un backup con nombre `openclaw.json.bak‑<motivo>‑<YYYYMMDD>`.
2. **Drift sin explicaciones = 0** - `scripts/gateway-config-drift.sh --accept` se ejecuta sin que el reporte muestre campos sin justificación.
3. **CI bloquea merges críticos** - El workflow de `audit‑pipeline.sh` falla automáticamente cuando la auditoría devuelve vulnerabilidad “high” o drift no aceptado.

Con estos criterios, podré garantizar que el sustrato del Gateway opere de forma confiable y reversible sin supervisión directa.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->