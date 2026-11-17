# HANDOFF - workspace

**Fecha:** 2026-11-17 19:44 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-17). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-17.md`.

---
## Que se hizo en esta sesion

### 2026-11-17 19:44
Auditoría de superficie del agente kanam-auditor: dos ítems de roadmap cerrados con evidencia. (1) El oracle dejó de delegar el contraste en axe: src/checks/contrast.js mide el ratio WCAG real (luminancia relativa, composición de fondos con alpha, umbral 4.5/3 por rol, opacidad) y el estado :focus; hallazgo inmediato --k-brand-primary con blanco da 3.74:1 (bajo 4.5:1 AA), anotado para el dueño del DS. De paso se corrigió un stall de 30s del check de teclado (clickeaba modales display:none): la corrida pasó de ~33s a 2.7s. (2) C.3 cerrado: surface-pipeline/bin/audit-due conecta check-audit-due.py con audit-surface y escribe .knowledge/AUDIT.md; reglas: sin config no hay auditoría, sin report.json no se acredita, un RECHAZADO sí se escribe (acreditado != aprobado). Verificado en las dos direcciones con un proyecto descartable (con config -> AL DIA leído de vuelta por el script; sin config -> no-config, exit 1, sin AUDIT.md). Tests 60/60. Commits 633b8fd2c5 y 7969abc97f.

### 2026-11-17 10:20
Sesion de auditoria de contexto de una conversacion vieja de Medallia (1/10) y su estado real al 17/11. Pregunta de Gonzo: si habia motivo para dejar archivada la conversacion o si podia borrarla. Verificado contra el repo y no contra memoria: (1) la conversacion produjo el kit de prep en docs/entrevistas/medallia/medallia-2026-10-01.md, que sigue vivo e indexado en el README de entrevistas; (2) la entrevista ocurrio el 19/10 (no el 1/10) y en esa call Gonzo entro sin saber que Brighthire era la grabadora, no la empresa; (3) CORRECCION PROPIA: en un mensaje intermedio afirme que Medallia era el cliente de Infjini. Es falso: el cliente de Infjini es Disney. Medallia fue un proceso aparte que cerro su etapa de entrevista. (4) El proceso Infjini/Disney: commit 7418097178 (16/11 15:44) lo cerro por silencio y gonzo lo revirtio en f379bb1cf0 (16/11 15:48) con la regla 'no dije nunca hubo noticias, digo que aun no coordinamos'. Estado vigente: ABIERTO - fecha sin coordinar, ultimo contacto humano con Siraj el 26/10 (21 dias). (5) Sin automatizacion ni cron atado a la sesion (16 jobs revisados): borrar el chat no pierde nada. Gonzo respondio 'cerrado... guardar' sobre el proceso. NO se edito el tracker: queda como decision suya si marcarlo sin actividad desde 26/10, porque la vista diaria no lo registra y ya se intento cerrarlo una vez en falso.

### 2026-11-17 08:57
Research pedido por Gonzo sobre que cuota de LLM/API trae Google AI Pro (USD 19,99, ex Gemini Advanced) para poder cambiar el motor del sistema (hoy Ollama cloud) por Gemini. Respondido con fuentes de Google y de la doc local del gateway. Hallazgos clave: (1) el plan NO incluye uso de API; "direct use of the Gemini API (API keys or external applications) is billed and managed separately"; (2) si aporta USD 10/mes de credito Google Cloud via Google Developer Program, aplicable a facturacion de Gemini API, con prepago minimo de USD 5 y validade de 12 meses acumulables, solo titular; (3) Gemini CLI y Code Assist individual dejaron de servir a AI Pro/Ultra el 18-jun-2026, todo migro a Antigravity; (4) los USD 300 de bienvenida de Google Cloud NO cubren Gemini API desde marzo 2026; (5) el plan da cuota generosa SOLO dentro de superficies Google (app Gemini, Antigravity, playground web de AI Studio). Segundo hilo: la via legal. Terms de Antigravity prohiben explicitamente third-party tools con Antigravity OAuth y nombran a OpenClaw como ejemplo de breach, con riesgo de suspension; el FAQ agrega que wrappear agy en agentes de terceros no esta soportado en planes consumer y recomienda API key. Verificado en la doc local /opt/homebrew/lib/node_modules/openclaw/docs/providers/google.md que OpenClaw solo soporta AI Studio API key o Vertex ADC, sin OAuth nuevo. Tercer hilo: catalogo real. Gemini 3.8 Flash existe y esta GA desde 2-sep-2026 (ID gemini-3.8-flash, 1M ctx, thinking LOW/MEDIUM/HIGH, sin MINIMAL, ignora temperature/top_p). Precios verificados en la pagina de pricing de AI Studio: 3.1 Flash-Lite 0,25/1,50; 3.5 Flash-Lite 0,30/2,50; 3.8 Flash 0,75/3,75 (sube a 1,50/7,50 el 1-ene-2027); 4 Hydrogen 1,50/7,50; 4 Argon 2/10 (sube a 4/20 el 1-dic-2026); 4 Carbon 2/10. Correccion importante: Hydrogen NO es mas barato que la linea 3, es 5x Flash-Lite y 2x 3.8 Flash, y su free tier entrena con los datos. Free tier: 3.8 Flash 5 RPM/20 RPD; Flash-Lite 15 RPM/500 RPD; Argon y Pro 0; datos usados para entrenar. Tier 1 con 5 USD de prepago: 1.000 RPM/10.000 RPD en 3.8 Flash, tope 250 USD/mes. Verificado tambien que el catalogo bundled de OpenClaw ya trae google/gemini-3.8-flash (alias gemini-flash) y google/gemini-3.5-flash-lite (alias gemini-flash-lite), y que el catalogo se refresca en vivo contra models.list. Estado del gateway: plugin google habilitado y perfil auth google:default en modo api_key pero SIN provider configurado, cero modelos Google en openclaw models list. Decisiones tomadas por Gonzo en la sesion: OpenRouter queda como revisor B del pipeline A/B como veedor independiente (no compartir un solo modelo); primario con mix (Flash en CORE/dev, Flash-Lite en auditor/mind/studio); arrancar por free tier Flash-Lite para validar el cableado y pasar a paga recien cuando el volumen lo pida. Riesgo registrado: si se corta Ollama Pro, todos los modelos :cloud del gateway caen y solo quedan gemma4:12b, qwen3.8:27b y OpenRouter. Pendiente: brief para OPS con el diff de config (crear key, apuntar CORE a Flash-Lite u 3.8 Flash, OpenRouter de fallback) - no ejecutado.

### 2026-11-17 00:15
Arranque: Gonzo pregunto que hace la skill memory-wiki-vault, la menos usada y nunca entendida. Analisis con evidencia del disco: memory-wiki estaba enabled, doctor healthy, 86 fuentes ingestadas pero UNA sola entity con 4 claims, por eso todos los reports daban cero. Verificado en negativo que los detectores SI funcionan (sonda sembrada, cada report nombro su defecto, se limpio sola): no era un fallo del plugin, era la capa de claims vacia. Escribir un claim a mano era el paso caro y nadie lo paga para un vault fuera de git (716K, sin versionado). Decision: adoptar la IDEA (claim + evidencia + status + confidence) y descartar el vehiculo. Creado docs/claims/ con README, y tres archivos sembrados: models.md (10 claims, los 8 roles de ADR-090 + thinking off/low), pipeline.md (6 claims: A/B/C, pre-filtro, asimetria, gate) y workspace.md (7 claims). Creado scripts/check-claims.py: resuelve evidencia contra settings/file/managed-block/adr, valida updatedAt, confianza, contested y contradicciones; --negative siembra un claim roto y prueba que cada detector dispare. Cableado al pre-commit sin condicion. Segundo trabajo: el commit quedo bloqueado por check-refs.py porque docs/pipeline/roadmap-ingresos-a11y-2026-11.md declara 'Script propuesto scripts/watch-devto-trends.sh (a crear)' y el gate lo leia como ruta rota - bloqueaba cualquier commit, no solo el mio (el CI del commit fbb10ca9fc ya estaba en rojo por lo mismo). Arreglado con exencion de rutas declaradas propuestas, match por palabra completa y ventana de dos lineas; encontre un bug en mi propio primer intento ('propuesto' es substring de 'sin decir propuesto') y lo corregi. Tercer trabajo: el claim layer destapo de inmediato que settings.model.triple decia minimax-m3.1-flash mientras model_by_agent y model_triple decian deepseek - 12 dias de drift, la trampa que ADR-090 documenta y que ya habia pasado dos veces el 2026-11-04. Primero alinee las tres claves y agregue check-settings-aliases.py que las vigilaba. Despues, a pedido de Gonzo, se cerro DE RAIZ: se borraron model_triple y model.triple de la DB (12 a 10 claves), managed-blocks.py set ahora escribe UNA sola clave y acepta un alias solo como nombre de entrada, se agrego retire-aliases [--force] que se frena si un alias difiere del canonico, seed nunca crea alias, y el gate invirtio su regla: ahora exige que NO exista ninguna copia. Verificado en negativo tres veces. ADR-090 actualizado en el lugar con la decision estructural. Detalle del proceso: el commit bloqueo por CHANGELOG desfasado (entradas viejas fuera de la ventana), corri changelog-rotate.py: 51 activas, 258 archivadas. Tres commits, tres pushes, tres CI en verde. Limpieza: 6 backups temporales de la DB en /tmp eliminados, uno conservado en ~/backups/memory.db.bak-2026-11-17-pre-retire-aliases.db. Vault de memory-wiki intacto en disco (solo historico, no se borro nada).

### 2026-11-16 10:49
Descubrimiento y armado de un producto de reservas para una aeronave compartida por dos socios (Romero y Federico). El planteo inicial del cliente (Excel compartido, Google Sheets) se reviso contra seis puntos debiles: no es un slot de calendario sino un residual operativo; Sheets falla por integridad y no por privacidad; Calendly no modela un recurso compartido; falta politica de prioridad; el uso personal es registro fiscal; y probablemente ya existe un sistema de operaciones detras. Se cerro el modelo: activo compartido, dos socios que reservan con confirmacion inmediata y sin aprobacion mutua, invitados que piden y requieren aprobacion de un socio, solicitud que retiene el lugar 48 horas y vence sola, tope de dos solicitudes abiertas por invitado, mantenimiento como reserva (kind mantenimiento) con responsable, e historial inmutable con saldo de uso por socio. Tres artefactos escritos en docs/propuestas/reservas-avion-compartido/: brief-socios.md (documento para que los socios aprueben, sin precio y sin proveedor a la vista), spec-tecnico.md y plan-piloto.md. Descartados: Google Sheets, Google Calendar, Calendly y Cal.com/cal.diy (edicion comunitaria, no produccion). Booked Scheduler queda como plan B para un piloto express; se verifico en su documentacion que soporta recursos, permisos, aprobacion con estado pendiente y bloqueos. Decision tecnica: Next.js con Supabase, permisos en la base con RLS, y el no-solapamiento garantizado por una restriccion de exclusion de Postgres sobre el rango de fechas. Modelo comercial: producto enlatado, un deploy por cliente, piloto sin costo en free tiers con transferencia de titularidad al dia 30. Tambien se limpio docs/voz-gonzo.md: se elimino la regla 8 tachada y se comprimio la 13 a la decision, y se registro el caso del 2026-11-16 con la edicion real del mensaje.

## Estado actual

v0.1. Cuatro skills ejecutables reales + surface-alignment-audit procedimental. Suites 60/60. audit-surface corre y emite report.html+json.

### Estado previo (heredado)

Conversacion de Medallia auditada y declarada borrable sin perdida (kit ya esta en repo, sin cron atado). Infjini/Disney: ABIERTO - fecha sin coordinar, sin contacto humano desde 26/10. Gonzo lo declaro 'cerrado' verbalmente; el tracker lo tiene abierto por su propio revert del 16/11. Tracker sin editar: falta decision explicita sobre marcarlo con nota de inactividad.

### Estado previo (heredado)

Research cerrado con fuentes; integracion NO ejecutada. Gateway sin provider google configurado (solo el perfil auth en modo api_key). Sin key creada, sin cambio de modelo primario, sin diff de config aplicado.

### Estado previo (heredado)

docs/claims/ operativo con 25 claims y gate en el pre-commit. settings con una sola clave de asignacion de modelos (model_by_agent), managed-blocks.py escribe en una y retire-aliases borra copias. ADR-090 documenta la correccion estructural. Tres CI en verde. Vault de memory-wiki sin uso, conservado como archivo.

### Estado previo (heredado)

Tres artefactos escritos y commiteados; esperando la respuesta de los socios.

### Estado previo (heredado)

Migración congelada en Fase 5 hasta el 2026-12-01 (quota Gemini Starter agotada; Ollama Pro activo hasta 2026-11-30). OpenClaw sigue siendo el entorno operativo maestro y Kanam sigue trabajando normal acá.

### Estado previo (heredado)

CV final entregado y enviado por Gonzo. Llamada con Agustín Bermúdez acordada para mañana 16/11.

### Estado previo (heredado)

Material listo, no enviado: falta el OK de Gonzo para mandar el mensaje y el CV.

### Estado previo (heredado)

Error de carga de la skill evidence-hunter resuelto; frontmatter válido.

### Estado previo (heredado)

Modulo 0 dado y verificado. Research de Vane auditado contra fuente: dos papers leidos, el resto marcado. Modulo 1 no empezado. Sin linea base grabada todavia.

### Estado previo (heredado)

Lab local operativo y versionado sin secretos. Curso en modulo 4. Instancia arriba.

### Estado previo (heredado)

Sesion cerrada. Clase commiteada; nada pendiente de esta sesion. Otras sesiones concurrentes montaron godot-3d-rpg-curso, godot-2d-platformer-beginners y creative-web-threejs-blender en la misma franja horaria.

### Estado previo (heredado)

- Estado: sesion cerrada; clase y gate retirados por pedido. Cambio propio pendiente de commit: solo el borrado de la linea del README.
- Modulo actual: n/a (curso retirado).
- Ejercicios hechos: n/a.
- Preguntas abiertas: ninguna del curso.
- Proximo bloque: n/a.

### Estado previo (heredado)

Workspace limpio salvo esos dos scripts ajenos. Clase n8n cerrada y commiteada.

### Estado previo (heredado)

ADR-112 aceptado y commiteado; gateway en tailnet; CVs de Feltsense y Mercado Libre corregidos y regenerados (ML en 2 paginas); gate de CV extendido.

## Proximos pasos

1) Una .kanam/pipeline.config.yaml por producto: es el bloqueo real (4 pendientes, 0 con config), sin eso el gate no audita nada. 2) Auth en el oracle (requires_auth). 3) Baselines por producto (C.2). 4) JUnit queda RECHAZADO hasta que exista un CI que corra el oracle.

### Pendientes heredados (sin cambios)

1) Decidir con Gonzo si Infjini/Disney se marca 'sin actividad desde 26/10, ventana vencida, sigue solo si Siraj escribe' en docs/entrevistas/_general/job-search-tracker.md; 2) Borrar esta conversacion (sin perdida); 3) El gap real del proceso es ingles hablado: el plan del CUI hasta el 22/12 sigue, con o sin Disney.

### Pendientes heredados (sin cambios)

1) Gonzo crea la key en aistudio.google.com/apikey con su cuenta. 2) Brief a kanam-ops con el diff: cargar key via openclaw models auth paste-api-key --provider google, definir modelos google/gemini-3.8-flash y google/gemini-3.5-flash-lite, dejar openrouter de fallback, y actualizar ADR-090 mas el bloque managed model-operativo. 3) Validar una sesion real con Flash-Lite en free tier antes de habilitar billing. 4) Si funciona, prepago de 5 USD y aplicar el credito mensual de 10 del plan.

### Pendientes heredados (sin cambios)

1) Evaluar si el claim layer escala: sumar topics (career facts ya existe en prosa en memory/career-facts.md, estado de todos por proyecto) o quedarse en los tres criticos. 2) La skill memory-wiki-vault fue reescrita por el skill review a default repo-first: revisarla para que no mande a revivir el plugin retirado. 3) El vault tiene 13 paginas stale por missing updatedAt del import de hermes-sdd; si nunca se usa, decidir si se borra o se deja como archivo. 4) Considerar si el mismo formato de claims aplica a .knowledge/HANDOFF de proyectos.

### Pendientes heredados (sin cambios)

1. Respuesta de los socios sobre el brief. Llamada con Agustin (EFISAT) el 2026-11-16. Si aprueban, el trabajo pasa por Planner y despues por DEV. Al dia 20 del piloto se acuerda el mantenimiento y al dia 30 se transfiere la titularidad.

### Pendientes heredados (sin cambios)

1) 2026-12-01: activar Google AI Pro y retomar Fase 5 final (sesión de prueba real en Gemini). 2) Decisión pendiente: laptop MacBook Air consume solo MD/HANDOFF, sin memory.db (evita split-brain SQLite). 3) Formalizar Vane como deprecado (desplazado por Gemini cloud + image-generator nativo) con un ADR corto cuando se haga el corte a Google AI Pro.

### Pendientes heredados (sin cambios)

1. Preparar la llamada del 16/11: 3 preguntas clave (dolor de mantenimiento, tareas manuales, equipo propio o tercerizado). Si responde, no poner precio en la primera charla.

### Pendientes heredados (sin cambios)

1. Enviar mensaje.md (versión WhatsApp) cuando Gonzo confirme; completar el placeholder [nombre del vínculo]; si responde, agendar 20 minutos.

### Pendientes heredados (sin cambios)

1. Continuar con las tareas de Kanam Critic o workspace general.

### Pendientes heredados (sin cambios)

1. Elegir camino: (a) linea base grabada de «contame sobre vos» en ingles, (b) Modulo 1.1 auditoria de LinkedIn, (c) plan de 4 semanas ajustado. Recomendacion de Kanam: linea base primero.
2. Commit local de `studies/entrevistas-tecnicas/` (research/ + ejercicio-0-gonzo.md).
3. Push cuando Gonzo lo autorice.
4. Deuda: leer Brooks (2014) y McCarthy & Goffin (2004) para cerrar las dos citas sin verificar; sin esas, no enseñar sus tamanos de efecto.
5. HEREDADOS (sin cambios):
1. Gonzo hace 3.A (tipo number vs campo ausente en el IF). Luego modulo 4: dos Google Sheets como tools de un agente. Si se muda a VPS, el endpoint de Ollama cambia de host.docker.internal al host destino.
7. ### Pendientes heredados (sin cambios)
1. Decidir si cute-room-portfolio-3d se estudia: modulos 1 y 2 para escena, modulo 8 (baking) es el que justifica el curso. En reinos-de-la-frontera: convertir PNG a WebP cuando exista pipeline web y decidir si se retira assets/quaternius/_download/.
9. ### Pendientes heredados (sin cambios)
10. ### PENDIENTE - servicio del gateway: `partial import` (registrado 2026-11-10 20:54)
11. **Estado:** el gateway esta sano y estable (pid 63535, uptime > 2h, loopback 200, https 200, escuchando solo en 127.0.0.1 y [::1]). Lo que NO esta resuelto es la definicion del servicio:
12. ```
13. launchctl print gui/501/ai.openclaw.gateway
14. properties = partial import | keepalive | runatload | inferred program
15. ```
16. Consecuencia: la proxima actualizacion de OpenClaw puede negarse a activar el servicio (`service-ownership-changed`). No rompe la operacion hoy; rompe un update futuro.
17. **Plan acordado (no ejecutado):**
1. Correr `/opt/homebrew/bin/openclaw gateway install --force` **con PATH seteado** y ruta absoluta.
- El intento del 2026-11-10 fallo porque `launchctl submit` ejecuta con `PATH=/usr/bin:/bin:/usr/sbin:/sbin` y `openclaw` vive en `/opt/homebrew/bin`: 363 corridas con `openclaw: command not found`, mas un bucle de SIGTERMs de 3 horas.
2. Verificar que `properties` deje de decir `partial import`.
3. Si `bootstrap` sigue devolviendo EIO (`Bootstrap failed: 5: Input/output error`), usar `sudo` - el propio error pide privilegios: *"Try re-running the command as root for richer errors"*.
22. **Regla de disparo:** el humano corre la palabra clave **`nuevamente`** cuando vuelva a aparecer un mensaje extraño o quiera retomar este plan. Al escucharla, retomar este pendiente y no otro.
23. **Por que no se ejecuto ahora:** el ultimo intento a ciegas costo tres horas de inestabilidad. Se hace con Gonzo frente a la maquina o cuando el gateway pueda caerse sin costo.
24. ---
1. Retomar studies/n8n-ai-automations cuando Gonzo elija el primer workflow real a implementar (modulos 3/6/11 son el mismo patron). Pendientes de otra sesion: integracion de assets CC0 en projects/edad-de-los-reinos.
26. ### Pendientes heredados (sin cambios)
1) Verificar contra GitHub las 19 referencias de CVs historicos que no estan en el corpus y agregarlas a career-facts 5.2.1. 2) Limpiar las carreras universitarias de los 5 CVs historicos (EIT/HTC, Mercor, Sol, TEMPO) - son de otras sesiones. 3) Confirmar con Gonzo que el iPad quedo operativo con ws://100.126.255.95:18789. 4) Watchdog de canales: el timeout del trigger sigue sin resolver si se repite.

### Pendientes heredados (sin cambios)

1. Gonzo hace 3.A (tipo number vs campo ausente en el IF). Luego modulo 4: dos Google Sheets como tools de un agente. Si se muda a VPS, el endpoint de Ollama cambia de host.docker.internal al host destino.

### Pendientes heredados (sin cambios)

1. Decidir si cute-room-portfolio-3d se estudia: modulos 1 y 2 para escena, modulo 8 (baking) es el que justifica el curso. En reinos-de-la-frontera: convertir PNG a WebP cuando exista pipeline web y decidir si se retira assets/quaternius/_download/.

### Pendientes heredados (sin cambios)

### PENDIENTE - servicio del gateway: `partial import` (registrado 2026-11-10 20:54)

**Estado:** el gateway esta sano y estable (pid 63535, uptime > 2h, loopback 200, https 200, escuchando solo en 127.0.0.1 y [::1]). Lo que NO esta resuelto es la definicion del servicio:

```
launchctl print gui/501/ai.openclaw.gateway
  properties = partial import | keepalive | runatload | inferred program
```

Consecuencia: la proxima actualizacion de OpenClaw puede negarse a activar el servicio (`service-ownership-changed`). No rompe la operacion hoy; rompe un update futuro.

**Plan acordado (no ejecutado):**

1. Correr `/opt/homebrew/bin/openclaw gateway install --force` **con PATH seteado** y ruta absoluta.
   - El intento del 2026-11-10 fallo porque `launchctl submit` ejecuta con `PATH=/usr/bin:/bin:/usr/sbin:/sbin` y `openclaw` vive en `/opt/homebrew/bin`: 363 corridas con `openclaw: command not found`, mas un bucle de SIGTERMs de 3 horas.
2. Verificar que `properties` deje de decir `partial import`.
3. Si `bootstrap` sigue devolviendo EIO (`Bootstrap failed: 5: Input/output error`), usar `sudo` — el propio error pide privilegios: *"Try re-running the command as root for richer errors"*.

**Regla de disparo:** el humano corre la palabra clave **`nuevamente`** cuando vuelva a aparecer un mensaje extraño o quiera retomar este plan. Al escucharla, retomar este pendiente y no otro.

**Por que no se ejecuto ahora:** el ultimo intento a ciegas costo tres horas de inestabilidad. Se hace con Gonzo frente a la maquina o cuando el gateway pueda caerse sin costo.

---

1. Retomar studies/n8n-ai-automations cuando Gonzo elija el primer workflow real a implementar (modulos 3/6/11 son el mismo patron). Pendientes de otra sesion: integracion de assets CC0 en projects/edad-de-los-reinos.

### Pendientes heredados (sin cambios)

1) Verificar contra GitHub las 19 referencias de CVs historicos que no estan en el corpus y agregarlas a career-facts 5.2.1. 2) Limpiar las carreras universitarias de los 5 CVs historicos (EIT/HTC, Mercor, Sol, TEMPO) - son de otras sesiones. 3) Confirmar con Gonzo que el iPad quedo operativo con ws://100.126.255.95:18789. 4) Watchdog de canales: el timeout del trigger sigue sin resolver si se repite.

## Decisiones y contexto que no debe perderse

- JUnit no se implementa: no hay consumidor (surface-audit.yml corre solo el stage estático; la única mención de junit era un ejemplo escrito por mí en octubre). Una casilla vacía no es razón para construir. El token brand-primary/blanco es decisión del dueño del DS, no mía.

### Heredadas (sin cambios)

- Un proceso con ventana prometida vencida y 21 dias de silencio NO se cierra automaticamente: el 16/11 ya se cerro por silencio y Gonzo lo revirtio en 4 minutos. La distincion que vale es 'sin noticias' (no hay respuesta) vs 'aun no coordinamos' (depende de coordinar). Cerrar un proceso es de Gonzo, no de la regla de 10 dias. Ademas: nunca inferir el cliente de un bench (Infojini -> Disney, no Medallia) sin fuente; Brighthire es la grabadora, no la empresa contratante.

### Heredadas (sin cambios)

- Google AI Pro no da API incluida; da 10 USD/mes de credito Cloud (prepago 5 obligatorio) y cuota solo en superficies Google. Antigravity OAuth con OpenClaw es breach de terms: prohibido, se usa API key. 3.8 Flash es el workhorse elegido; Hydrogen descartado por caro (2x). OpenRouter queda en B del pipeline A/B como veedor independiente. Mix por rol: Flash en CORE/dev, Flash-Lite en auditor/mind/studio. Arrancar gratis con Flash-Lite, pagar cuando el volumen lo exija.

### Heredadas (sin cambios)

- La idea de memory-wiki se conserva, el vehiculo no: claim + evidencia + status + confidence vive en docs/claims/ dentro del repo, versionado, con gate propio. Un detector que nunca dispara es indistinguible de uno ausente: --negative en cada gate nuevo. Un dato, un dueno: tres claves con el mismo valor siguen siendo tres duenos, se retira la copia en vez de vigilarla. Un gate que falla por un archivo ajeno es un gate que enseña a usar --no-verify: se corrige la causa, no se saltea.

### Heredadas (sin cambios)

- Producto enlatado, no servicio por hora. Un deploy por cliente (single-tenant). Next.js + Supabase con RLS y exclusion constraint de Postgres para impedir solapamiento. La solicitud de invitado retiene el lugar 48 horas. La titularidad se transfiere despues de acordar el mantenimiento, nunca antes.

### Heredadas (sin cambios)

- Coexistencia temporal sana: OpenClaw = maestro; Antigravity = espejo de solo lectura hasta activar Pro. En la laptop Air: NO sincronizar memory.db, solo markdown derivado (dailies, HANDOFFs, career-facts, ADRs) y lo que deba persistir va por HANDOFF a la Mini. Vane queda sin sentido funcional al perder Ollama Pro y ganar Gemini Notebook.

### Heredadas (sin cambios)

- Sin titulo de ingeniero; liderazgos tono bajo; sin carreras universitarias; EY es frontend, no full stack; CV corto y la profundidad va a la llamada.

### Heredadas (sin cambios)

- Sin título de ingeniero; liderazgos tono bajo; OSS dentro del CV; formación sin universidades (career-facts 7-bis).

### Heredadas (sin cambios)

- Se corrigió sintaxis YAML en agents/kanam-critic/skills/evidence-hunter/SKILL.md eliminando un paréntesis de cierre fuera de comillas.

### Heredadas (sin cambios)

- El research externo se audita leyendo la fuente, no se adopta por plausible. Aprobar una cita sin abrir el paper es el mismo error que citar un README como especificacion.
- Reappraisal no reduce el estres subjetivo: cambia fisiologia y atencion. Ensenarlo como «calmate» es falso.
- Acento leve penaliza credibilidad por fluidez y el oyente puede corregirlo si lo nota; acento fuerte no. La palanca practica es fluidez del contenido, no borrar el acento.
- No hay literatura que sostenga «rechazo por ansiedad» como criterio formal en examenes de conducir; se rechaza por errores observables.
- Vane devuelve borradores: lo que la clase cita tiene que estar leido.
- HEREDADAS (sin cambios):
- Fallback unico local por decision de Gonzo: 'el fallback no puede ser otro modelo en la nube'. Primario deepseek y no beam: dejo de ser gratuito y su calidad ya estaba descartada por ADR-105 (3/4 bugs, auto-aprobacion con defecto vivo). Ninguna carrera universitaria va a CV ni ATS (regla 2026-11-04). Una referencia de CV se verifica abriendo el hilo en GitHub, no contra el corpus.

### Heredadas (sin cambios)

- Fallback unico local por decision de Gonzo: 'el fallback no puede ser otro modelo en la nube'. Primario deepseek y no beam: dejo de ser gratuito y su calidad ya estaba descartada por ADR-105 (3/4 bugs, auto-aprobacion con defecto vivo). Ninguna carrera universitaria va a CV ni ATS (regla 2026-11-04). Una referencia de CV se verifica abriendo el hilo en GitHub, no contra el corpus.

## Archivos tocados

```
agents/kanam-auditor/LEARNINGS.md
agents/kanam-auditor/MEMORY.md
agents/kanam-auditor/ROADMAP.md
memory/2026-11-17.md
memory/devto/2026-W47.md
memory/memory.db
docs/CHANGELOG.md
.knowledge/handoff-history/2026-11-09-1700-HANDOFF.md
memory/2026-11-15.md
docs/entrevistas/_general/job-search-tracker.md
memory/career-facts.md
agents/kanam-critic/skills/evidence-hunter/SKILL.md
studies/ai-agents-for-beginners/m1-llm-en-10-lineas.md
.knowledge/handoff-history/2026-11-06-1805-2-HANDOFF.md
.knowledge/handoff-history/2026-11-06-1805-HANDOFF.md
studies/sql-full-course/HANDOFF.md
studies/sql-full-course/SESSIONS.md
memory/2026-11-12.md
studies/dsa-mega-course/HANDOFF.md
studies/godot-2d-platformer-beginners/HANDOFF.md
studies/godot-2d-platformer-beginners/SESSIONS.md
studies/godot-3d-rpg-curso/HANDOFF.md
studies/godot-3d-rpg-curso/PROGRESO.md
studies/godot-3d-rpg-curso/SESSIONS.md
docs/archive/CHANGELOG-archive.md
studies/README.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-17.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*

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
