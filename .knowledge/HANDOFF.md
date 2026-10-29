# HANDOFF - workspace

**Fecha:** 2026-10-28 21:31 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-28). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-28.md`.

---

## Que se hizo en esta sesion

Exploracion del menu de integraciones de Ollama (ollama launch, 18 harness) y verificacion independiente de dos informes de agente sobre Breacorp/Moderno-Diffusion. (1) Se arreglo el launcher de OpenCode 2.x: Ollama 0.40.11 le pasaba --model a nivel raiz, flag que v2 elimino; el fix real es 0.40.12 (commit 8ec9ecdf, PR #19310), que detecta la version mayor y usa --standalone para v2. El bundle ya estaba descargado en ~/Library/Caches/ollama/updates pero no se aplicaba porque la app corria en modo hidden con --fast-startup, que difiere el upgrade pendiente; se relanzo sin ese flag y quedo en 0.40.12, verificado con pruebas de launch de opencode, claude, qwen y cline. Ojo: el servicio compartido de opencode (serve --service) no hereda la config inline del launch, hay que matarlo antes de medir. (2) Verificacion de dos informes sobre Moderno-Diffusion: pi (26 commits, 76% de solapamiento exacto con DiffusionBee, 24/30 aciertos) y Hermes (~28/30, 93% de precision). Hermes gano por ALCANCE no por precision: bajo y audito el DMG publicado (firma ad-hoc, spctl rechaza, TeamIdentifier ausente, 342 MB de core/ con binarios sin fuente), corrio npm ci y lo encontro FALLANDO por lockfile desincronizado, verifico que TF 2.10.0 no tiene wheel arm64 en PyPI, y reviso la postura de seguridad Electron (webSecurity false, enableRemoteModule true, preload exponiendo ipcRenderer). pi gano en cuantificacion (76,0% exacto, lint 23 con desglose, 77 console.log). Error de fondo de Hermes: afirmo que bridge.js es identico al upstream, y los hashes difieren (53ff6e40 vs 7318582c) - se contradice con su propio hallazgo de la ruta hardcodeada. Correccion de mi propio error: al validar el informe de pi di el hallazgo del lockfile por confirmado leyendo mal git ls-files, cuando el lockfile SI esta commiteado (blob bdee174, 850.289 bytes); el defecto real que encontro Hermes es otro, que npm ci falla por desincronizacion. (3) Medicion propia de los pesos del modelo publicado: 2.440.763.520 bytes identicos al SD1.5 fp16, header de 512 bytes identico, y en 12 muestras de 1 KB distribuidas 1 coincidio y 11 no (~92% distinto) -> mismo layout, pesos distintos: no es renombre ni hay evidencia de destilacion. (4) Observacion metodologica de la tanda de prueba de harness: Cline sorprendio con un demo (3 sub-agentes con presets que fallaron por auth, fallback a spawn_agent con el provider de sesion, integracion y verificacion con Playwright) y dejo ~/agent-demo con 17 modelos de API verificados y 3 marcados unverified a proposito. Pero el confusor quedo a la vista: Cline corre con auto-approve true por defecto, OMP con always-ask, Qwen Code con approval-mode default, y ollama launch no pasa ninguna bandera de aprobacion. Qwen se descarto por 'trabado' cuando lo que pasaba era un prompt de aprobacion por edicion y por comando: se midio la politica de permisos, no el harness. Criterio para futuras catas: normalizar el modo de aprobacion antes de comparar.

## Estado actual

Workspace limpio salvo la eliminacion del informe de Moderno-Diffusion (Gonzo lo borro y pidio no seguir: 'nada mas, ya elimine casi todo lo hecho'). Se liberaron 3,3 GB de /private/tmp (clon de pi 1,0 GB, upstream 39 MB, model.tdict 2,3 GB) y se desmonto el DMG. Ollama quedo en 0.40.12 con opencode, claude, qwen y cline verificados.

## Proximos pasos

1) Si se retoma la cata de harness: normalizar el modo de aprobacion en los seis (auto-approve/always-ask) antes de medir, y matar el servicio compartido de opencode para que el launch no mida el modelo del servicio viejo. 2) Si vuelve Moderno-Diffusion: el informe verificado existio y se borro por decision de Gonzo; los hallazgos estan en este daily (licenciamiento AGPL incumplido en tres clausulas, DMG sin notarizar, npm ci roto, TF sin wheel arm64). 3) El criterio 'el agente que audita el artefacto publicado encuentra mas que el que lee el repo' queda como referencia para elegir revisor.

## Decisiones y contexto que no debe perderse

- OpenCode 2.x requiere Ollama >= 0.40.12: el launcher de 0.40.11 usa --model en la raiz, flag que v2 elimino. El upgrade pendiente de Ollama no se aplica con la app en modo hidden + --fast-startup; hay que relanzar sin ese flag. En comparacion de harnesses el modo de aprobacion es una variable a fijar, no un detalle: Cline (auto-approve) vs Qwen (default) mide permisos, no capacidad. Un informe de agente sin verificar no se entrega; dos agentes distintos dieron 80% y 93% de precision con un error de fondo cada uno.

## Archivos tocados

```
docs/moderno-diffusion/informe-estado-2026-10-28.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-28.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
