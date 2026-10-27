# Veredicto: NO abrir PR upstream a browser-use (2026-10-26)

> Decisión de Gonzo. El parche local (7 commits, `fix/ollama-structured-output`,
> tag `v0.13.13-ollama-local`) se queda **local**.
> Detalle del por qué en la sección "Datos que lo sostienen".
> Complemento técnico del 2026-10-27: `docs/browser-use-perfil-docker.md`.

## Datos que lo sostienen

**(a) El fence bug YA tiene dueño upstream.** Dos intentos previos (#4986
jun-2026, #5466 ago-2026) más el PR de un mantenedor (#5023, cerrado sin
mergear) para nuestro síntoma exacto: 3 intentos muertos. Un cuarto PR
nosotros sería el cuarto intento, contra la regla del repo: *"nunca piso: si
alguien ya tiene un PR o reclamó un finding, no abro otro"*.

**(b) El P1 de #5466 anticipó exactamente el edge case** que se encontró
después en el parche propio (fence legítimo dentro de un valor JSON): señal
de que la zona está en disputa y el fix necesita más custodia de la que
puede dársele ahora.

**(c) 4 de los 7 commits son config local de Ollama** (ruta nativa, env
flags, `ollama_think`, refactor). No son bugs de upstream: un PR sería
mayormente ruido.

**(d) El repo no tria issues.** 188 issues abiertas y solo 5 cerradas desde
septiembre. Pero mergea 142 PRs desde agosto: si alguna vez vamos, es PR, no
issue.

**(e) La evidencia era una tarea en example.com**, no uso real.

## Candidato más fuerte para un PR futuro

El bug de **page title stale** (`browser/session.py`, provider-agnostic, sin
nadie lo reporto). Vive en la capa de browser, no en la de LLM, donde
upstream está moviendo fichas.

**Trigger para revisitarlo:** haberlo sufrido de verdad en uso real (no en
test sintético), tener una reproducción mínima y un parche limpio.

Precedente: PR-Agent, descartado con "no volver a proponerlo".

## Hallazgo del 2026-10-27 (no cubierto arriba)

El bug del **perfil de Chrome compartido entre host y contenedor** (uid 501
vs 911) y el **`SingletonLock` stale** que envenena un volumen compartido
**no los encontramos reportados** en el issue tracker. Son candidatos más
nuevos que el del page title, pero la decisión de no abrir PR sigue vigente
hasta que Gonzo la revise con el trabajo real encima.
