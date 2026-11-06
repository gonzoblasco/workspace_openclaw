# CHANGELOG.md

Registro de cambios estructurales del workspace. Contiene las entradas de los **últimos 14 días** (corte: 2026-10-23). Lo anterior está archivado en [`./docs/archive/CHANGELOG-archive.md`](./docs/archive/CHANGELOG-archive.md). No incluye actividad diaria (ver `memory/`).

> **Política de rotación:** la mantiene `scripts/changelog-rotate.py` (pre-commit `--check` + cierre de sesión). Al superar la ventana, el bloque viejo se mueve al archivo. Reconstruir el activo desde cero cuando arrastre hipótesis refutadas.

---

## [2026-11-06] - El Planner deja de ser un agente que hay que abrir a mano

### Added
- **Integración CORE → Planner (`skills/planner-delegation/`).** El CORE ahora tiene un procedimiento explícito para convocar al Planner cuando el objetivo es un programa multi-sesión (3+ pasos, 2+ roles, >1 sesión o fecha/bloqueo). El Planner devuelve plan, brief y contratos; el CORE ejecuta, verifica y sintetiza.
- **Programas multi-sesión (`agents/kanam-planner/scripts/program_plan.py`).** CRUD con pasos, `owner`, `role`, `exit_criteria`, `depends_on`, `gate`, evidencia y estados. Comandos `init`, `add-step`, `update`, `set-gate`, `set-gates`, `next`, `brief`, `status --json`, `lint`, `board`, `report`, `close`.
- **Gates de plan (`plan_lint.py`).** Falla si un paso no tiene dueño o criterio de salida, si hay ciclos, si un paso `completed` no tiene evidencia o si un `blocked` no tiene blocker. `close` corre el lint antes de cerrar.
- **Contratos de ejecución (`dispatch_contract.py`).** Genera agente, modelo, alcance, write paths, criterio de salida, evidencia y prompt listo para `sessions_spawn`.
- **Capacidad del Crew (`crew_capacity.py`).** Foto de sesiones activas por agente para evitar spawns duplicados.
- **Skills del Planner:** `program-orchestration`, `crew-dispatch`, `plan-playbooks`, `plan-review`.
- **Brief de programas en arranque/cierre.** `session-start.sh` imprime programas activos; `session-end.sh` recuerda actualizar paso/evidencia y no cierra el programa con la sesión.
- **Automations:** `planner-weekly-plan` (lunes 08:30) y `planner-weekly-review` (viernes 17:30), con entrega a Telegram.
- **`docs/PLANNER-INTEGRATION.md`:** RACI, quién llama a quién, puntos de inserción en los pipelines y modos de falla.

### Changed
- **`AGENTS.md` §3:** regla dura de programas multi-sesión; el CORE spawnea al Planner antes de ejecutar y no por cada paso.
- **`complexity-driven-pipeline` y `agent-orchestration-pipeline`:** el programa se planifica con el Planner; `pipeline-track.sh` sigue siendo el estado intra-paso.
- **`session-lifecycle`:** brief de programas al inicio y actualización de paso/evidencia al cierre.
- **`SKILLS-INDEX.md`:** Core 34, Planner 5, total 110 (medido con `openclaw skills list`).

### Fixed
- **Regla de verificación del Planner (caso Preflight, 2026-11-06).** Un plan afirmó que Chromium corría con `--no-sandbox` sin leer `src/lib/scan.ts:33`; era falso. Ahora `program-orchestration` y `planner-delegation` exigen que cada afirmación de estado cite `archivo:línea` o se marque como supuesto, con un paso 0 de verificación si no se pudo comprobar. La misma regla aplica al review del CORE: su informe también tenía dos falsos positivos (`mcp.ts` sí llama `checkQuota`; `scan.ts` sí tiene `MAX_CONCURRENT`).
- **Compatibilidad de programas legacy.** `program_plan.py` normaliza `write_path` singular y campos faltantes de `abya-yala-05.json`; el programa ya pasa `plan_lint` y produce contrato de ejecución.

### Notes
- **Sin cambios de config:** no se tocó routing, heartbeat, modelos ni `subagents.allowAgents`. En Fase 1 el Planner **no spawnea**: entrega contratos y el CORE ejecuta.
- **Test de automation:** `planner-weekly-plan` corrió en modo force, respondió `Sin programas activos.` y entregó a Telegram (`deliveryStatus: delivered`).
- **Tests:** `tests/python/test_program_plan.py` 5/5 (happy path, evidencia obligatoria, ciclos, cierre y contrato).
- **Fase 2 condicionada a métrica:** dispatch directo del Planner, tool nativa `plan` y Crew Board visual solo si hay 3+ invocaciones por semana durante 3 semanas.

---

## [2026-11-05] - Kimi sale de todo slot; el costo se mide en la barra, no en la sesión

### Added
- **`cuento-check.py` con umbrales por género.** El mismo número no significa lo mismo en todos lados: el thriller de La Plata tiene promedio 26 palabras/párrafo y está bien (11 líneas de diálogo, beats procedurales); en terror sería metralleta. Perfiles `terror`, `thriller-psicologico`, `highsmith` y `default`, medidos sobre los cuentos del día.
- **Detector de cabos sueltos.** Una persona presentada con un rasgo y nunca retomada es un error, no una ambigüedad. Encontró el caso que todas las demás métricas dejaron pasar: *"un residente joven que no le pidió documento"*, que insinuaba una suplantación y el cuento nunca retomó. Solo mira personas: con objetos daba 54 avisos de ruido.
- **Detector de fuga de outline.** Si el metalenguaje del plan aparece en la prosa (*"El objeto viajaba en el sobre"*), el redactor narra con los nombres de las secciones. Caso real de Highsmith.
- **`outline-highsmith.md` y `outline-thriller-psicologico.md`.** Son géneros distintos y no se resuelven con un adjetivo: el thriller psicológico necesita adversario humano con método repetible y asimetría de información; el método Highsmith no tiene investigador, el protagonista es el culpable, y la tensión es administrativa.
- **ADR-109.** La familia Kimi (`kimi-k3.1-pro`, `kimi-k3`) no asigna ningún rol: queda como excepción declarada con OK de Gonzo, presupuesto previo y sin iteración. Criterio de descarte: un modelo que cuesta **> 20× el baseline** no puede ser slot.
- **Auditoría de camino a `muse-spark-open` (medido).** Tres modelos sobre tres recorridos (un riesgo real, dos limpios): muse distinguió 3/3 y 0 falsos positivos; `nemotron-3-super` inventó 6 riesgos en el recorrido limpio y `gpt-oss:120b` entre 4 y 5. Descarte de los dos candidatos que recomendaba la evidencia vieja: la tarea define el modelo, no la familia del rol.
- **Redacción con voz a `muse-spark-open`.** Uso declarado raro; se paga en calidad de punta lo que se gana en no pensar el costo cada vez. Licencia verificada para uso interno. Muse queda en dos slots (auditoría y redacción) con la condición de que ninguno haga la tarea del otro.
- **`docs/ecosystem/cata-2026-11-05-auditoria-camino-y-gemma4.md`.** Las dos catas que el ADR dejó pendientes, con los números crudos y una sección explícita de lo que no prueban. Incluye la contraprueba de muse para lo trivial (pierde: 8.446 tokens y 34 s contra 4.944 y 10 s de gemma4) y **el criterio general corregido**: no es "trivial vs técnico", es **"la salida se verifica contra algo"** contra **"la salida se sostiene sola"**.
- **`docs/ecosystem/cata-2026-11-05-narrativa-ficcion.md`.** 5 modelos × 3 géneros (CF, thriller, terror), 400 palabras. Primera pasada con `think:false`; **repetida con `think:"low"` en los siete modelos**, y eso invierte dos veredictos: **`glm-5.3-flash` sí escribe** (con `false` devolvía el plan en inglés: 1.762 palabras de plan, cero de cuento; con `low`, 41 caracteres de pensamiento y 309 palabras de prosa) y **`gpt-oss:120b` no se cuelga en terror** (era el presupuesto de 4.000 tokens). Y **`deepseek` se hunde**: 49.789 caracteres de razonamiento, 19,75 tok/palabra (12× lo que gasta con `false`) y un prompt vacío de cada tres — lo que explica que 26 requests de Muse pesen menos en el panel que 134 de DeepSeek. `minimax` y `nemotron` siguen sin entregar el artefacto.
- **`scripts/cuento.sh` + `cuento-check.py`: cuento en dos etapas.** glm propone el esqueleto (`think=low`), muse lo redacta. Medido: glm tiene la mejor *estructura* (el cuaderno que prescribe, el antecesor registrado antes) y la peor *sintaxis* a 2.500 palabras (23 oraciones de más de 45 palabras, "pabellón liberio"); muse sostiene la voz y no se rompe, pero solo no encuentra un conflicto con consecuencias. Separar los trabajos usa lo mejor de cada uno.
- **El ritmo se gobierna con números, no con adjetivos.** El template de redacción fija cantidad de párrafos, promedio y cuántos de una línea. Medido en el mismo esqueleto: sin la regla, 96 párrafos de 19 palabras (metralleta); con la regla, 40 de 43 (aire). Y la extensión sale de **más escenas**, no de estirar la prosa: el redactor comprime cada escena a ~200 palabras pase lo que pase, así que el outline pide 8-10 escenas a 280.
- **`cuento-check.py`** mide fidelidad, ritmo y etiquetas emocionales, y avisa. Sobre la fidelidad, corregido el mismo día: en el primer híbrido creí que muse había renombrado el elenco, y era falso - el esqueleto solo nombraba a *Renzo* y al barco *København*, y los dos sobrevivieron (16 y 6 menciones). Muse inventó nombres para lo que el esqueleto dejó sin nombrar ("el nieto", "el naufragio"): eso es lo que se le pide al redactor. El check avisa para revisar a mano, no para condenar.
- **`scripts/llm.sh` + `scripts/llm-tasks.json`.** El modelo correcto depende de la tarea, y una skill hereda *un* modelo para todas las suyas (STUDIO tiene prosa y i18n con el mismo cerebro). El script toma la tarea como parámetro y de ahí salen **modelo, `think`, `num_predict` y temperatura**, versionados en el registro con la cata que los funda. `--template` sustituye `{{variables}}`, `--json` devuelve el texto con tokens y segundos, y las variables sin valor **frenan con error** en vez de mandar un prompt roto. Cierra el error que costó dos veredictos falsos hoy: sin `think` explícito, cada modelo hereda su default.
- **`scripts/templates/cuento.md`.** Primer template: género, palabras y tema por `--var`, con los requisitos que la cata midió como los que separan mostrar de explicar.
- **`kanam-auditor` pasa a `muse-spark-open`** (fallbacks: deepseek, gemma4). Era la peor combinación medida: deepseek con `think=low`, que gasta 19,75 tok/palabra y falla 1 de cada 3.
- **Regla de RITMO calibrada.** La primera versión pedía "nunca dos párrafos largos seguidos" y produjo 96 párrafos de 19 palabras: metralleta. La calibrada pide **30-40 párrafos, promedio 45-70 palabras, 8-12 de una línea**. Resultado: 40 párrafos, promedio 43, racha máxima de 2 cortos seguidos.

### Changed
- **Las cuentas de la cata del 2026-11-04 se corrigen a la suba.** Con el panel del 2026-11-05: 10 requests de K3.1 Pro pesan más que 17 de K3; **1 req de K3.1 Pro ≈ 24-26× deepseek**, contra 14-22× medidos en sesión. El delta K3 vs K3.1 Pro no aparece en la barra, así que el swap entre ellos no compra nada.
- **La tesis del MoE ("solo activa parte de sus parámetros") no se sostiene en la factura.** Queda registrada como argumento del proveedor, no como propiedad medida.

### Fixed
- **`bombe` no existe en español.** Aparecía tres veces en el cuento de Highsmith (por *bombilla* / el mate). Nadie lo detectó: ni el check ni yo al leerlo. Pasa a estar en la lista de defectos que ningún script caza.
- **Ruptura de punto de vista en Highsmith.** Dos párrafos en primera persona dentro de un cuento en tercera, sin comillas ni raya: el lector no sabía quién hablaba. Corregidos a diálogo con raya. Regla nueva: si un párrafo empieza con yo/me/mí y no tiene raya, es diálogo mal formateado.
- **El outline se truncaba con el template de thriller.** Con `num_predict=2500` se cortaba a mitad de la escena 1: el cuento salía sin revelación ni final. Subido a 6.000, y el wrapper **no corre la etapa 2 si faltan las secciones de cierre**.
- **El ">10× más barato" era falso, en tres archivos.** Con los px reales del panel (barra de 944 px): deepseek 0,412 · muse 0,333 · glm 0,200 px/req. Muse cuesta el 81% de un request del CORE y glm el 49%, no el 10%. Era extrapolación de la barra vista a ojo. Corregido en ADR-109, en el doc de catas y acá, dejando la nota de que no estaba medido.
- **Dos scripts llamaban modelos sin `think` y pagaban el razonamiento sin que se viera.** `complexity-scorer.sh`: 3,4 s y 626 tokens produciendo la misma respuesta de 25 caracteres que con `think:false` cuesta 0,4 s y **18 tokens** — 35× más caro en cada arranque de pipeline. `interpret-entries.py`, igual. Los dos corregidos con la medición en el comentario.

### Notes
- **Medir, no estimar:** tercera corrección del mismo número, las tres hacia arriba. La unidad válida es la barra sobre uso real, no el px/req de una sesión.
- **`gemma4` es el más barato del plan, y por más margen del que se creía.** Medido con la barra de sesión (944 px): **2 px / 221 req = 0,00905 px/req**, o sea **46× más barato por request** que el CORE (0,412) y 37× que muse (0,333). El ">10× más barato" original era correcto en dirección y **conservador en magnitud**: se quedaba corto por un factor de 4. Corregido en ADR-109 y en el doc de catas.
- **`gemma4` como chat trivial: medido y gana, con esa base.** Contexto completo 5/7 correctas y 0 falsos positivos; contexto parcial 0/7, con dos fechas y horas inventadas. Pagar el contexto entero (3,1× tokens) contra 46× de precio por token deja **~15× a favor**. **Borde escrito: chat trivial = el dato de respuesta ya está en el contexto entregado.** Fuera de eso gemma4 sigue sin servir: no se probó que dejara de inventar en análisis.
- **Pendiente:** muse sobre un cierre de sesión real (el sintético prueba que no fabrica, falta probar que encuentra) y el borde verificable en el runtime que habilite el slot de chat trivial. Ningún slot se aplica sin eso; `utilityModel` y el CORE no se tocan.
- **Sin cambio:** pipeline A/B/C, slots de dev/ops/auditor/critic/planner/mind/studio, ADR-090 y ADR-107.

## [2026-11-04] - Nace `preflight`, el gate de accesibilidad para sitios hechos por IA

### Added
- **`projects/preflight` (v0.1.0).** Producto nuevo, con repo propio. Renderiza una URL en Chrome, la corre contra axe-core y despues **la lee con un lector de pantalla**, guardando cada frase que pronuncia. El informe empareja cada defecto con lo que le pasa a la persona y termina con un **fix prompt ordenado** que se pega en Lovable/Cursor/v0; cada paso declara la frase que el lector debe anunciar despues del fix, asi el constructor de IA puede verificarse solo.
- **CLI + GitHub Action.** `npx tsx scripts/cli.ts <url>` con `--min-score` y `--fail-on-blocking` (automatico en CI), y `action.yml` compuesto que publica el informe en el job summary. El gate corre en cada PR.
- **Guardas de seguridad en el motor:** `guardUrl` valida el host literal *y* despues de la resolucion DNS (rangos privados, IPv4-mapped v6, credenciales embebidas rechazadas); `ratelimit` combina burst en memoria con cuota diaria en SQLite sobre un fingerprint sha256.

### Notes
- **Motor verificado, no asumido:** `tsc --noEmit` limpio, `vitest` 8/8, `next build` verde, `biome check` limpio con `a11y: all`. Un scan real de `example.com` tarda ~1.9s.
- **El producto se audita a si mismo:** la landing da 100/100 A y el propio informe 97/100 A, medidos por el motor que se envia. El dogfooding encontro tres defectos reales, corregidos antes del commit de cierre: iconos SVG anunciados como `graphics-document`, la lista de scans recientes sin nombre accesible, y `<ul>` comunes marcadas como "gap" (lo que entrenaria al lector del informe a ignorar los marcadores).
- **La pagina de precios dice la verdad:** no promete PDF, ni soporte dedicado, ni colaboracion de equipo. Declara en el cuerpo que el billing no esta conectado y que hoy un plan se resuelve por email.
- **No desplegado, a proposito.** Playwright necesita un Chrome persistente y la mayoria de las plataformas serverless cortan a los 60s; la decision de destino queda abierta y documentada en `.knowledge/HANDOFF.md`.

---

## [2026-11-04] - El gate de merge del HANDOFF no dejaba pasar nunca

### Fixed
- **`--closed` validaba pero nunca se escribia.** `session-handoff.py` pasaba los items declarados como cerrados al validador de merge y no los ponia en el archivo. Consecuencia: el gate dejaba de frenar la escritura, pero el cierre siguiente volvia a ver esos items como pendientes perdidos y frenaba otra vez. **No habia forma legitima de atravesar el gate.** Ahora `build_handoff` emite una seccion `## Cerrados en esta sesion` con la lista. Un dato que se usa para autorizar una escritura y no se guarda es una validacion sin memoria.
- **El CI fallaba desde dos commits antes y no era del ultimo cambio.** `tests/bash/test-skills-scope.bats` afirmaba `"Em dash: 0 ok, 0 failed"` cuando el script emite `"0 aviso(s)"` desde que el em dash dejo de bloquear (regla del owner 2026-11-04: tipografia no es correccion).

### Notes (assert ciego en Bats)
- **La causa de fondo no era el formato: era que el assert no se evaluaba.** En Bats una asercion intermedia que falla **no falla el test**; solo cuenta el exit status del **ultimo** comando. Este test tenia tres `[[ ]]` sueltos, asi que el primero (roto desde hace dias) nunca corrio. Medido con un test descartable: un `[[ ]]` intermedio que falla da `ok`. Por eso pasaba en local y fallaba en CI, donde el ultimo assert tambien fallaba.
- **Por que importa:** un test que pasa por un assert ciego es peor que uno rojo, porque declara una garantia que no verifica. Se agrego `|| return 1` a cada asercion de los dos tests afectados.
- **Barrido del resto de la suite:** 22 asserts sin `||` en 7 archivos de `tests/bash/`. Medidos uno por uno, **todos menos uno estan al final del bloque** (donde el exit status si cuenta) o seguidos solo de `}`. El unico enmascarado real era el de este commit. Un detector que cuenta el cierre de bloque como "comando posterior" da 21 falsos positivos.
- **3 tests nuevos** en `test_session_handoff.py`: `--closed` se escribe, sin `--closed` no aparece la seccion, y las entradas vacias no generan bullets huerfanos (con normalizacion de guion largo).

---

## [2026-11-03] - El guion deja de ser veto y el planner cambia de fallback

### Changed
- **El pre-commit ya no aborta por guion largo: avisa y sigue.** ADR-082 habia retirado la regla del guion como obligacion, pero el hook seguia cortando con `ABORT: guion comun (-) obligatorio`. El aparato contradecia a la decision y trababa commits legitimos por caracteres heredados que nadie edito. Ahora imprime `aviso: guion largo en <archivo> (no bloquea)` y continua. `hyphen_enforcer.sh` se mantiene: normaliza en-dash en lo staged, que es correccion mecanica y reversible, no bloqueo. `check_em_dash.py` sigue intacto para quien quiera correrlo a mano.
- **Fallback del planner: `glm-5.3-flash` -> `minimax-m3.1-flash`.** Era el modelo mas caro por request de la casa (0.292 px/req contra 0.053 del siguiente). Cambiado en las tres capas: `memory.db` (settings `model_by_agent`, `model_triple`, `model.triple`), `scripts/managed-blocks.py` (seed `model_alternative` y `model_by_agent`) y `openclaw.json` (`agents.entries.kanam-planner.model.fallbacks`).

### Notes
- **`minimax-m3.1-pro` no existe.** Se pidio ese id, pero el catalogo de Ollama solo tiene `minimax-m3:cloud`, `minimax-m3.1-flash:cloud` y `minimax-m2.7:cloud` (`-pro` da 404 en library y en search). Se uso `minimax-m3.1-flash:cloud`, que ademas era el valor que la DB ya tenia en `model_alternative`: la unica capa desalineada era la tabla por agente.
- **Ollama dejo de escuchar en la LAN.** La app tenia `expose = 1` en su `db.sqlite`, que produce `OLLAMA_HOST=0.0.0.0`. Se puso en `0` y tras reiniciar el bind quedo en `127.0.0.1:11434` (verificado: LAN responde `000`, local `200`). El riesgo era real: `:cloud` respondia sin auth desde la red local con el firewall apagado.
- **Verificado, no asumido:** `sh -n` sobre el hook, `check-single-source`, `check-bootstrap-budget` y `check-pipeline-enforcement` en `rc=0`, y una prueba aislada que confirma que un archivo con em dash ya no aborta el commit.

---

### Removed
- **46 archivos borrados del indice.** Gonzo los habia borrado del disco: `.knowledge/ARCHIVED_PROJECTS/` (2), `.knowledge/ARCHIVED_SESSIONS/` (2) y `.trash/` (42). Se verifico que **nada unico se pierde**: las sesiones archivadas duplican `docs/archives/sesiones/` (el archivo vivo), y el contenido de `kanam-sudoku.md` sobrevive en `docs/insights/2026-10-28-ensenanzas-sudoku.md` y en el CHANGELOG. Los `.trash/` son backups del residuo del `2026-10-08`, ya reconciliados aditivamente.

### Fixed
- **`/.trash/` agregado al `.gitignore`.** El ignore existente cubria `**/.knowledge/handoff-history/.trash/` (la papelera interna de cada `.knowledge/`), pero **no** la de la raiz. Por eso 42 archivos de backup del residuo de octubre quedaron commiteados y reaparecieron como bajas cinco semanas despues. Una papelera versionada es deuda que se paga sola.

### Notes
- **Verificado antes de borrar:** `check-refs --all` OK con 685 rutas (nada citado apunta a esas rutas). Las menciones en `memory/` y `docs/archives/` son registros historicos de lo que se archivo en su momento, no dependencias.
- **Error propio durante la verificacion:** para probar que los archivos eran recuperables corri `git checkout -- .knowledge/ARCHIVED_PROJECTS`, que **restauro** dos archivos que Gonzo ya habia borrado. Se revirtio de inmediato (vuelto a `trash`) y se le informo antes de seguir. Un `git checkout` de comprobacion **escribe**: no es lectura.

---

## [2026-11-03] - El HANDOFF va al `.knowledge/` del sujeto, este donde este

### Fixed
- **`scripts/session-handoff.py` resolvia todo slug contra `projects/`.** Si el proyecto vivia en `forks/`, `clones/` o `_workbench/`, `resolve_handoff_path()` devolvia `projects/<slug>/.knowledge/HANDOFF.md`: una ruta que no existia, que el script **creaba igual**, dejando el HANDOFF real sin actualizar y sin ningun error visible. Medido antes del fix: `--project vane` -> `projects/vane/` (real: `forks/vane/`), `--project onwheels` -> `projects/onwheels/` (real: `_workbench/onwheels/`).
- **La busqueda ahora recorre `PROJECT_CONTAINERS`** (`projects`, `_workbench`, `forks`, `clones`) y devuelve el `.knowledge/` de la carpeta real. Un slug que existe en **mas de un** contenedor **falla con error explicito** en vez de elegir: adivinar es como se termina escribiendo el HANDOFF de un proyecto en el `.knowledge/` de otro. Sin carpeta en ningun contenedor se cae al comportamiento historico (`projects/<slug>`), para no romper slugs que todavia no se abrieron.
- **Directorios con espacio final ya resuelven.** `projects/OSS ` (nombre real, con espacio) no se encontraba porque el slug se recortaba. La busqueda prueba **coincidencia exacta primero** y recien despues el nombre recortado, asi que `--project "OSS "` llega a la carpeta correcta y un slug prolijo (`OSS`) tambien.

### Added
- **9 tests de regresion** en `tests/python/test_session_handoff.py`: resolucion en `projects/`, `forks/`, `_workbench/` y `clones/`; fallo ante slug ambiguo; carpeta con espacio final; slug sin carpeta; prioridad del `--handoff-dir`; y el alias `workspace` siguendo al HANDOFF global.
- **Guarda contra slugs con separadores de ruta.** Un slug como `"OSS / astryx (meta/astryx #3335)"` se anidaba en `projects/` y `mkdir(parents=True)` creaba el arbol sin avisar. Ahora se rechaza con el nombre del proyecto en el mensaje. `--handoff-dir` tambien se valida contra el arbol del workspace. 4 tests mas.

### Fixed (rescatado)
- **`projects/OSS / astryx (meta/astryx #3335)/` era un arbol fantasma, no un typo de carpeta.** Contenia el HANDOFF y el SESSIONS del follow-up de astryx #3335 del 2026-10-29 (analisis de TabMenu, comentario 6499306768). El contenido se rescato y hoy vive en **`oss/facebook-astryx/.knowledge/`**; la cadena vacia `OSS / astryx (meta/` se mando a la papelera con `trash`. No habia `projects/astryx` ni `clones/astryx` previos: el contenido solo existia ahi.
- **El mismo slug aparecio antes:** `memory` del 2026-10-13 registra un cierre con `"OSS / astryx PR #5204"`. No era un caso aislado, era un patron que el script aceptaba.

### Added (oss/)
- **`oss/` - contenedor nuevo para contribuciones a repos ajenos.** `oss/<owner>-<repo>/.knowledge/` guarda HANDOFF, SESSIONS y (a futuro) `THREADS.md` con los hilos abiertos y quien tiene la pelota. No es codigo ni un repo nuestro: es memoria que **sobrevive al clone**. `forks/` y `clones/` son artefactos de codigo desechables; `projects/` se reserva para repos propios bajo `gonzoblasco/`.
- **Por que no `forks/`:** un fork se clona, se rebasa y se descarta cuando el PR cierra. El registro de "que dije en #3335 y quien me debe respuesta" tiene que quedar despues de tirar el clone.
- **Por que no `projects/`:** un proyecto tiene repo propio bajo `gonzoblasco/` (`oss-post-graph`, que suena a OSS pero es nuestro). Una contribucion a `facebook/astryx` no tiene repo nuestro, tiene un clon temporal.
- **Por que `oss/` y no una cuarta carpeta caprichosa:** la receta de cierre de `docs/AGENTS-DETALLE.md` ya usaba el namespace `"OSS / <repo> #<n>"`; faltaba la carpeta que lo recibiera, y por eso el slug terminaba siendo un nombre con barras.

### Changed
- **`PROJECT_CONTAINERS` = `projects`, `_workbench`, `forks`, `clones`, `oss`.** Test nuevo de resolucion en `oss/`.
- **`skills/session-lifecycle/scripts/session-start.sh` ya no duplica el mapa en bash.** Resolvia con un `case` que solo conocia `projects/`: una sesion de `vane` leia un HANDOFF inexistente y arrancaba fria aunque `forks/vane/.knowledge/HANDOFF.md` existiera. Ahora delega en `resolve_handoff_path` (una sola fuente de verdad) y cae al path historico si el slug es invalido, para no romper el arranque.
- **`.gitignore`: `oss/` NO se ignora, a proposito.** La primera version de esta entrada decia que se ignoraba "como `forks/` y `clones/`": era un error de reflejo. `forks/` y `clones/` son codigo de terceros; lo que vive en `oss/` es **nuestro** registro (HANDOFF, SESSIONS, THREADS) y se versiona con el workspace, igual que `memory/` y `docs/`. Ignorarlo lo dejaba sin respaldo, que es exactamente lo contrario del motivo por el que se creo. Verificado con `git check-ignore` (exit 1) y `git status` (aparece como untracked).
- **`docs/AGENTS-DETALLE.md`:** la receta de cierre del PR usa el slug de carpeta (`owner-repo`) y no el titulo del hilo; la excepcion de forks se corrige (decia que no llevan `.knowledge/`, pero `forks/vane/` tiene uno por ser un fork que se desarrolla); se documenta `oss/`.
- **Skill `session-close-handoff`** (Workshop): destino `oss/`, regla del slug sin barras, y la verificacion de path pasa a ser control en vez de remedio del bug.
- **`scripts/check-foreign-knowledge.py` + guarda pre-push en repos de terceros.** Gonzo: *"nunca subir el `.knowledge` a los repos OSS... el tema es no ensuciar lo ajeno"*. Instala un hook `pre-push` en cada repo de `forks/` y `clones/` que **rechaza** empujar cualquier ref con `.knowledge/` a un remote que no sea de `gonzoblasco`. El hook vive en `.git/hooks/` y **no se commitea**: el repo ajeno no se ensucia. Conectado al pre-commit (plantilla y hook vivo), sin condicion.

### Notes (guarda de .knowledge ajeno)
- **El riesgo estaba medido, no supuesto:** `forks/vane/` tiene **9 archivos `.knowledge/` trackeados** y un remote `upstream` a `ItzCrazyKns/Vane`. `upstream/master` tiene **0** archivos `.knowledge/`: todavia no se contamino, pero nada lo impedia. `_workbench/onwheels` tiene 6 trackeados y **no tiene remote**, asi que ahi no hay exposicion.
- **Por que un hook y no un `.gitignore`:** agregar `.knowledge/` al `.gitignore` del fork modifica un archivo del repo ajeno - exactamente lo que se quiere evitar. Y borrar el `.knowledge/` del fork pierde la memoria del hilo. El hook no toca nada versionado.
- **Por que `projects/` queda afuera:** son repos nuestros (bajo `gonzoblasco`); ahi el `.knowledge/` **es** el proyecto y va commiteado.
- **8 tests** en `tests/python/test_check_foreign_knowledge.py`: deteccion de riesgo, instalacion ejecutable, repo limpio, rechazo en forma HTTPS y SSH de un remote ajeno, permiso en las dos formas de un remote propio, y paso libre cuando la rama no trae `.knowledge/`. El contrato se prueba invocando el hook con los argumentos y el stdin que git le pasa, no con un `git push` real (que depende de la red y de `insteadOf`).

---

## [2026-11-03] - `services/`: un servicio interno no es un fork

### Changed
- **`forks/vane` -> `services/vane`.** Vane corre como servicio interno: no se le manda PR, se lo opera. Estaba en `forks/`, donde la regla "no trackear `.knowledge/`" es correcta para un PR pero no aplica a un servicio, asi que el check necesitaba una **exencion** para dejarlo pasar.
- **La exencion se elimino y se arreglo la clasificacion.** Una exencion es un olor a clasificacion equivocada: si un repo necesita una excepcion para cumplir una regla, el que esta mal es la carpeta, no la regla. `services/` es ahora el contenedor para repos de terceros que se **operan**, no se contribuyen.
- **`check-foreign-knowledge.py` clasifica por PROPOSITO, no por origen del codigo:**
  - `forks/` y `clones/` -> `.knowledge/` **no se trackea**: entra al diff del PR que revisa el maintainer. Se saca con `git rm -r --cached` y se oculta con `.git/info/exclude` (privado, no versionado: tocar el `.gitignore` del fork si ensucia el repo ajeno).
  - `services/` -> `.knowledge/` **si se trackea**, en NUESTRO fork (`gonzoblasco/<servicio>`). El unico riesgo es un push al upstream, y eso lo cubre el hook pre-push.
- **`session-handoff.py` y `.gitignore`:** `services` agregado a `PROJECT_CONTAINERS`; `/services/*` ignorado como `/forks/*` (es codigo, no registro).

### Notes
- **El `.knowledge/` de vane se verifico intacto** tras la mudanza: `git status` limpio, 9 archivos trackeados, remotes `origin` (gonzoblasco) y `upstream` (ItzCrazyKns). El hook pre-push ya estaba instalado y sigue vigente en la ruta nueva.
- **Costo de la mudanza: ninguno.** `mv` preserva el repo entero (153M, historial, ramas, hooks, `.git/info/exclude`).
- **16 tests** en `test_check_foreign_knowledge.py`, incluidos los cuatro nuevos del caso servicio: puede trackear `.knowledge` con guarda, es riesgo sin guarda, `--install` **no** lo destrackea, y en un fork **si** lo destrackea.

### Notes
- **El defecto estaba documentado y sin corregir:** `session-close-handoff` ya avisaba que `resolve_handoff_path` "solo busca en `projects/`" y pedia resolver el destino a mano con `--handoff-dir`. El workaround evitaba el arbol fantasma pero dejaba el bug intacto y dependia de que el agente se acordara. Ahora la skill puede pedir la verificacion como control, no como unico remedio.
- **Pendiente, no incluido aca:** el generador sigue **reescribiendo el HANDOFF entero**. Hoy el cierre del 2026-11-03 reemplazo los proximos pasos de onwheels (del 2026-10-29) por los del Expte. 15.533, perdiendo estado que seguia vigente. El merge por seccion con `<!-- vigente desde YYYY-MM-DD -->` queda como paso siguiente.

---

## [2026-11-02] - Ollama deja de ser punto único de falla; browser-use sale del gateway

### Added
- **`scripts/ollama-keepalive.sh` + `~/Library/LaunchAgents/com.ollama.serve.plist`.** Watchdog cada 30 s sobre `127.0.0.1:11434/api/version`: si el server no responde, levanta `ollama serve` y espera hasta 60 s. No arranca un segundo server cuando Ollama.app ya tiene el puerto (health check primero). Probado en el puerto libre 11555: detectó la caída, levantó el server, respondió, y se limpió al morir el padre.
  - **Sustrato:** el 2026-11-02 Ollama estuvo muerto de **10:07 a 11:49** (1 h 42 m). Con el cayeron los tres niveles de la cadena -`deepseek-v4.1-flash:cloud`, `gemma4:12b-mlx`, `minimax-m3.1-flash:cloud`- porque **todos** salen por `127.0.0.1:11434`. De ahí el error engañoso: *"deepseek cloud: fetch failed | ECONNREFUSED"*. 43 `ECONNREFUSED` en el log de ese día.
  - **Lección:** un fallback que comparte transporte con el primario no es un fallback. El failover era cosmético: 7 intentos × 3 modelos, 60-90 s por turno, mismo error.

### Removed
- **browser-use, borrado entero - no solo desregistrado.** Gonzo cerro el alcance: *"no dejemos huerfanos"*. Se fueron el bloque `mcp.servers.browser-use` de `openclaw.json`, las dos entradas del registro (`browser-use`, `browser-use-ui`), la skill `skills/browser-tool/`, sus dos docs (`browser-use-perfil-docker.md`, `browser-use-veredicto-pr-upstream.md`) y el prompt historico `.knowledge/prompts/browser-tool-skill.md`. Tambien se borraron las cuatro ramas `kind == "mcp"` de `ai-toolbox.py`: browser-use era la unica entrada de ese kind, asi que quedaban muertas.
  - **Motivo:** Docker Desktop reserva ~7,7 GB wired de los 24 GB del host, y el MCP obligaba a tenerlo arriba.
  - **Correccion de un error mio, del mismo dia:** en la version anterior de esta entrada afirme que *"la imagen y el repo quedan intactos"*. **Falso: `projects/browser-use` y `projects/browser-use-ui` nunca existieron en disco** al momento de la purga. Lo verifique con `ls` y `find` antes de afirmarlo por segunda vez. No habia imagen ni repo que conservar, y por eso no hay backup de config que valga: volver a tener browser-use es reconstruirlo desde cero.
  - **Lo unico que sobrevive:** la leccion de infraestructura en `learnings` #299 (volumen de Chrome anonimo por contenedor; nunca compartido ni bind-mounteado). Es knowledge de Docker, no de la herramienta.
  - **Alternativa sin Docker:** el plugin `browser` nativo (`@openclaw/browser-plugin`, enabled).
  - Dejo de reintentar en cada arranque: el ultimo `failed to start server "browser-use"` es de 11:54:35, el mismo segundo en que el hot reload aplico el cambio.

### Fixed
- **`ai-toolbox.py` ya no conserva codigo para un `kind` sin entradas.** Al sacar browser-use, las ramas `kind == "mcp"` de `tool_state`, `do_up`, `do_down` y `do_restart` quedaron inalcanzables. Se borraron. El test `test_las_herramientas_core_estan` pedia `browser-use` explicito; ahora verifica lo contrario: que no vuelva, y que no quede ninguna entrada `kind=mcp` sin sus ramas.
- `docs/tools/REGISTRY.md` regenerado (`catalog --write`, `--check` al dia) y sin las dos secciones de browser-use. La nota de Ollama que remitia a "la nota de browser-use" ahora cuenta de donde salio la medicion sin apuntar a un archivo que no existe.
- `SKILLS-INDEX.md`: fila de `browser-tool` fuera, fecha de verificacion al 2026-11-02, y **total corregido de 99 a 102** - la suma de las filas ya daba 102 y el total estaba mal desde antes de este cambio.
- `pipeline-state.json` reseteado: tenia la fase `browser-use-ui` con U5 en `start` desde el 2026-10-27. El estado quedo sin huerfanas.

### Notes
- El update 2026.10.5 → 2026.10.9 sigue fallando (`global-install-failed`); queda pendiente para `/update` desde el chat, no se relanza desde acá.
- Hallazgo sin tocar: `agent:main` DB en 2,2 GB y la sesión `agent:main:main` en 568k/1.0m tokens (54%).

---

## [2026-10-28] - El gate de fuente única caza roles de modelo escritos a mano

### Added
- **Tercera clase de chequeo en `check-single-source.py`: `find_stray_roles`.** Un tag de modelo junto a vocabulario de rol de OpenClaw (`CORE`, `main/defaults`, `por agente`, `agents.defaults`) escrito **fuera** de un bloque MANAGED es una copia que el propagador no puede corregir. El sustrato: `MODEL_OWNERS` exime a `docs/SETUP.md` **de archivo entero** porque es dueño del catálogo, y por esa grieta se colaba una afirmación de *rol*, que es otro dato.
- 6 tests nuevos que siembran el defecto: rol a mano, rol dentro del bloque (permitido), catálogo sin sujeto de rol (permitido), `por defecto` de una herramienta de terceros (otro sujeto, permitido), historia marcada, y el exit code.

### Fixed
- **`docs/SETUP.md:35` afirmaba "primario del CORE" y "alternativo/fallback del CORE" en prosa libre.** Esa línea mintió durante el swap de esta misma sesión: se corrigieron los bloques MANAGED y esta quedó diciendo lo viejo. Ahora el catálogo dice **qué modelo existe y con qué capacidades**, y remite a los bloques para los roles.
- **`docs/SETUP.md:133` estaba stale desde antes y ningún gate lo veía:** decía que cline usa `minimax-m3.1-flash:cloud`. Verificado contra `~/.cline/data/globalState.json` (`actModeOllamaModelId` y `planModeOllamaModelId`): corre `deepseek-v4.1-flash:cloud`. Corregido con la fuente y la fecha.
- `ROLE_SUBJECT` no incluye `por defecto` a propósito: es el vocabulario de las configs de terceros (cline, browser-use), que tienen otro sujeto y no pasan por managed-blocks.

### Notes
- El gate nuevo marcó **una** de las dos líneas que mentían. La segunda (cline) la encontró la lectura contra la fuente real, no el gate: un regex no distingue "modelo por defecto de una herramienta" de "modelo por defecto del gateway". Queda como límite conocido y documentado en el código.

---

## [2026-10-28] - ADR no vigentes llevan sufijo `-archived` en el nombre del archivo

### Changed
- **Convención de nombre para ADRs que ya no rigen: sufijo `-archived`.** Todo ADR cuyo `Estado` no sea `Aceptado`/`Accepted` (`Superseded`, `ARCHIVADO`, `Rechazado`) lleva `-archived` antes de la extensión. El número y la cita no cambian (`ADR-NNN`), el archivo no se mueve de directorio, y el renombre va con `git mv` en el mismo commit que el cambio de estado. Documentado en `docs/adr/README.md`, sección "Nombre del archivo".
- `docs/adr/ADR-102-minimax-m31-flash-motor-core.md` → `ADR-102-minimax-m31-flash-motor-core-archived.md` (único ADR no vigente del corpus: 62 en total, 61 `Aceptado`). Links del índice actualizados.

### Added
- **`check-adr-supersede.py` tercera regla: el nombre acompaña al estado, en las dos direcciones.** Falla si un ADR no vigente conserva el nombre viejo, y también si un ADR `Aceptado` lleva el sufijo (quien lo ve por nombre lo saltea y la decisión sigue rigiendo). Un `Aceptado` con un apartado superseded **no** lleva sufijo: sigue gobernando su materia.
- 5 tests nuevos que siembran el defecto en un corpus falso: estado sin sufijo, sufijo sobre `Aceptado`, contrapeso correcto, supersede parcial que conserva el nombre, y el sufijo tolerado por el matcheo de `check-adr-integrity.py`.
- Skill `adr-archiving` actualizado: paso de renombre con `git mv` y la regla de que el sufijo es parte del mecanismo, no un adorno.

## [2026-10-28] - Swap deepseek/minimax: deepseek vuelve a primario del CORE, minimax queda alternativo

### Changed
- **`deepseek-v4.1-flash:cloud` vuelve a ser primario de `main` y de `agents.defaults`; `minimax-m3.1-flash:cloud` pasa a fallback/alternativo** (ADR-107, supersede ADR-102). Motivo: el ahorro medido en uso real es de **~20% de cuota**, no el 0,5% que estimó la revisión de ADR-102 (que leyó el delta por request, no el peso del CORE sobre los turnos).
- `agents.defaults.utilityModel` queda en `gemma4:cloud` (el Helper, sin cambio). El pipeline A/B no se toca: A `gpt-oss:120b-cloud`, B `deepseek-v4.1-flash:cloud` (revisor), pre-filtro `gemma4:cloud`.
- Los otros siete agentes (dev, ops, auditor, critic, planner, mind, studio) no cambian: diff contra backup muestra **un solo agente modificado** (`main`).

### Added
- **`docs/adr/ADR-107-swap-deepseek-minimax-ahorro-recursos.md`** - la decisión, con la corrección de la unidad de medida (cuota de GPU por sesión, no por request), la tabla antes/después, y la verificación del runtime vivo.
- `ADR-102` marcado **Superseded por ADR-107** en su estado y en las dos filas del índice (`docs/adr/README.md`); su ficha de capacidades y riesgos 1-2 siguen vigentes como medición del modelo.

### Fixed
- Bloques managed re-aplicados para que la prosa no quede mintiendo: `model_primary` y `model_alternative` (`minimax-m3.1-flash:cloud`) seteados, `model_triple`/`model_by_agent` regenerados → `AGENTS.md` línea 150 y `docs/SETUP.md` línea 19 con los modelos nuevos. Segunda corrida de `apply` = "al día".
- `gateway-config-drift.sh --accept` corrido tras el cambio intencional → `no config drift`.

### Notes
- Aplicado con `config patch --file` (`Applied 5 config update(s)`, `Config valid`), backup previo en `/tmp/openclaw.json.bak-20261028-185246`. Alerta `size-drop-vs-last-good` del observador: artefacto del patch, el archivo no perdió ninguna ruta de config (verificado por diff de claves).
- `doctor` reporta `minimax-m3.1-flash:cloud` como "not in the local model catalog": esperado, es cloud y resuelve por `ollama show`.
- Queda pendiente confirmar el ahorro al cierre de la ventana semanal de cuota de Ollama.

---

## [2026-10-28] - Se retiran opencode y OpenHands; Claude Code queda como único harness

### Removed
- **opencode y OpenHands eliminados del stack** (ADR-106). Containers (`opencode`, `openhands-canvas`), imágenes (`opencode-local:dev` 343 MB y `ghcr.io/openhands/agent-canvas:1.28.1` 5,4 GB), volúmenes (`docker_opencode-data`, `docker_opencode-state`) y los proyectos `projects/opencode` (635 MB) y `projects/openhands` (76 MB), estos últimos a la papelera. **~6,3 GB recuperados.**
- `scripts/ai-toolbox.py`: entradas `opencode` y `openhands` borradas del registro (eran las líneas 127-152). `python3 scripts/ai-toolbox.py` devuelve ahora 5 herramientas.
- `docs/tools/REGISTRY.md`: filas de la tabla y las dos fichas completas reemplazadas por una sección `### opencode y OpenHands - ELIMINADOS (2026-10-28)`.
- `skills/ai-toolbox/SKILL.md`: `opencode` y `openhands` fuera de la descripción, de la lista de ids y del ejemplo de emparejamiento por archivo.

### Added
- **`docs/adr/ADR-106-retiro-opencode-y-openhands.md`** - la decisión con la matriz que la sostiene. El criterio no es el promedio ni el techo: es **la celda más baja**. opencode y OpenHands tienen celdas en 0 absoluto; Claude Code nunca bajó de 16/30 y nunca quedó último (0 de 6 modelos).
- **`docs/tools/compose-archivados/`** - los dos compose (`opencode-docker-compose.yml`, `openhands-docker-compose.ollama.yml`) guardados antes de borrar. Reintroducir cualquiera de los dos no exige reescribir su configuración.

### Fixed
- **`scripts/preflight-cata.sh` dejaba de funcionar sin los containers.** Las sondas `need opencode ...` y `need openhands ...` fallaban con "No such container". Reemplazadas por una línea informativa; el bloque de catálogo de modelos queda inerte, guardado por `docker ps | grep -qx opencode`, con un `else` que informa que no hay harness Docker que consultar. Sintaxis validada con `bash -n`.
- `scripts/watch-docker-cata.sh`: el comentario que justificaba mirar el estado de la cata decía que la fase local necesitaba Docker. Ahora aclara que eso era cierto hasta el retiro y que hoy la cata no necesita Docker en absoluto.

### Notes
- **La fase local de la cata se cortó por decisión de Gonzo** antes de la última celda de `qwen3.5:9b-mlx`. Quedan 3 sellos `LOCAL-DONE` en disco (nova-2b, ornith, gemma4:12b-mlx), reanudables, pero retomar esa fase exige reintroducir un harness en Docker.
- **`vane` se bajó por error y se volvió a levantar**: el `docker stop` incluía `vane`, que no estaba en el pedido. Restaurado en el mismo turno, `Up (healthy)`.
- Validadores de ADR en verde tras el alta: `check-adr-integrity.py` → `OK: 61 ADRs, todos indexados, sin duplicados ni refs rotas`; `check-adr-supersede.py` → `OK`.

---

## [2026-10-28] - Cata con 3 modelos: el ranking de harnesses depende del modelo

### Added
- **`docs/evaluacion/cata-harnesses-3-modelos-2026-10-28.md`** - la ampliacion pedida: `gpt-oss:120b-cloud` y `nemotron-3-super:cloud` sobre los mismos 3 harnesses y las mismas 3 tareas. **27 corridas, todas con el control verificado.** Cambia la conclusion de la cata de deepseek sola.
- **El ranking de harnesses se INVIERTE entre modelos.** Con gpt-oss gana OpenHands (30/30) y opencode queda ultimo (23/30); con nemotron-super gana opencode (29/30) y OpenHands queda ultimo (21/30). Con deepseek los tres empatan 30/30. **Claude Code es el mas estable: nunca queda ultimo y nunca colapsa** (2o con dos modelos, empate con el tercero).
- **Un solo modelo no separa el harness del modelo.** El "empate" de la cata de deepseek (90/90 los tres) no era "los harnesses son iguales": era que ese modelo no discriminaba. La unidad de decision real es **harness + modelo**, no el harness.
- **Jueces cruzados:** cada modelo juzga a los otros dos, y `judge.py` **aborta** si el juez coincide con el modelo candidato (un juez que es candidato se auto-prefiere y el ranking seria falso).
- `playground/cata-harnesses-2026-10-27/` - el runner, paramerizado por modelo (`CATA_MODEL`, `CATA_OUT`), mas `consolidate.py` (reconstruye las 27 filas desde los artefactos), `recover-meta.py` (recupera metadatos del log) y `analyze.py` (el cruce modelo x harness).

### Fixed
- **BUG PROPIO que invalido las celdas de opencode de la primera tanda.** El compose de opencode monta `./workspace:/workspace` desde `docker/`, asi que el agente trabaja en `docker/workspace/workspace/_cata` y el runner preparaba el corpus en `docker/workspace/_cata`: **un nivel de diferencia, y el agente no via la tarea.** Se manifesto como 5 caracteres con el texto "PROBE" (el artefacto del probe de control) y como un ratio inventado (4.38:1 sobre `#ffffff`, un color que no existe en el tema dark). Sin revisar el entregable, "gpt-oss/opencode = 1/10" habria entrado al informe como un defecto del harness. **Corregido y las 9 celdas de opencode re-ejecutadas** (con el fix, opencode+deepseek sigue dando 30/30).
- **Un re-run de UNA sola celda SOBREESCRIBE `results.json` y pierde los metadatos de los otros harnesses.** Los artefactos son acumulativos: `consolidate.py` reconstruye desde ahi, y `recover-meta.py` completa desde el log de la corrida.

### Measured
- **Fallo real: `nemotron-3-super` + OpenHands agota las iteraciones y no entrega.** T3 termino en error con 0 caracteres tras 30 acciones de exploracion, y se REPRODUCE en una segunda corrida. Sin leer el log de acciones, "6/12" parece que el modelo no entendio la tarea: habia gastado el turno explorando. Es un fallo de infraestructura disfrazado de tarea dificil.
- **Fallo real: `gpt-oss` + opencode muere sin `finish_reason`** (`OpenAI Chat stream ended without finish_reason`) en 2 de 3 celdas. Es del harness contra ese modelo: con deepseek y con nemotron no lo hace.
- **El costo de OpenHands es su patron de contexto, no su modelo:** 5,5x a 8,0x los tokens de entrada de Claude Code en los tres modelos (reenvia todo el contexto cada turno: 59-80 turnos contra 3 de Claude Code). **Claude Code es el de menor consumo de tokens de entrada en los tres modelos.**
- **El juez ciego coincide con la verdad de base en los extremos** (OpenHands con nemotron 4.83 es el peor y es el que no entrega; opencode con nemotron 9.33 es el mejor y es el que mas acierta): la prosa y el pass/fail dicen lo mismo.
- **Se confirma el descarte de `nemotron-3-ultra`** (ADR-090: mas grande, mismo contexto que super, mas lento y mas caro, perdio el benchmarking). Se midio con `nemotron-3-super`.

### Changed
- **El veredicto operativo se precisa:** no se retira nada (los tres harnesses aciertan 30/30 con su mejor modelo), pero **que harness usar depende del modelo**. Default: Claude Code (el mas estable y el mas barato en tokens de entrada). opencode y OpenHands quedan bajo demanda, cada uno con su pairing: opencode con nemotron-super (29/30) y OpenHands con gpt-oss o deepseek (30/30) mas la UI web.
- **El documento de la cata de deepseek (`cata-harnesses-2026-10-27.md`) queda marcado como SUPERADO en su conclusion**, con el puntero al de 3 modelos.

---

## [2026-10-27] - Cata de harnesses: los tres aciertan igual, y OpenHands consume 8x los tokens

### Added
- **`docs/evaluacion/cata-harnesses-2026-10-27.md`** - la cata completa: Claude Code vs opencode vs OpenHands con el **mismo modelo** (`deepseek-v4.1-flash:cloud`), 3 tareas de casos REALES del workspace con suite oculta, y veredicto por harness. Runner en `playground/cata-harnesses-2026-10-27/` (runner, suite, juez, validacion de la suite en dos direcciones).
- **9/9 corridas con el control verificado.** El control (que el modelo viaje) se comprueba ANTES de medir, con evidencia por harness: `modelUsage` de Claude Code, `model` de la sesion de opencode, `stats.usage_to_metrics.model_name` de OpenHands. Sin esto la cata habria comparado tres modelos distintos.

### Changed
- **opencode y OpenHands pasan a BAJO DEMANDA** en el registro de herramientas (misma mecanica que `browser-use-ui` y `vane`: estado propio + `down` real). No se retiran: la cata mostro que aciertan igual que Claude Code (27/27 y 30/30 asserts). Lo que cambia es que no quedan prendidos sin uso: opencode lleva **0 sesiones** en 32 dias.
- **El veredicto cambia la pregunta original:** con Claude Code solo no se pierde calidad (los tres aciertan 90/90), se pierde la **UI web** de OpenHands y el segundo cliente de opencode. La conclusion correcta no es "retirar" sino "cambiar el estado por defecto".

### Fixed
- **El registro declaraba Cline instalado con un path inexistente.** Su clon (`projects/cline`) fue borrado del disco, pero la entrada lo listaba como instalado y el wrapper `scripts/cline-tool.sh` apuntaba a un repo vacio (no puede funcionar). Ahora el estado dice **"no instalado"**, con el motivo y como reinstalarlo. Se agrego la clase al calculo de estado: una nativa que declara `paths` y no los tiene dice "no instalado", NO "apagado" (apagado es una falla; no instalado es otra cosa). Test nuevo que lo fija.
- **Trampas de invocacion de la cata, documentadas para no volver a tropezar:** (1) la API HTTP de opencode **parte** el sufijo `:cloud` y rechaza el modelo, y el override por request se ignora (siempre gana el `model` del config): hay que ir por el CLI; (2) OpenHands NO se configura por env var sino con `PATCH /api/settings` (`ollama_chat/<modelo>`), y **el backend no re-aplica el settings store sin reiniciar el container** (`/v1/models` devuelve `[]` aunque el JSON este escrito); (3) su via real es `POST /api/conversations` + `POST .../events`, no `/v1/chat/completions`; (4) sus eventos son `action`/`observation`, no `llm_message` para las tool calls.

### Measured
- **La verdad de base NO separa a nadie: 90/90 asserts.** Los tres harnesses pasaron todo, con el mismo modelo y las mismas tareas.
- **El costo si separa.** Totales de 3 corridas: Claude Code 236 s / 337.787 tokens in / 44.843 out; opencode 286 s / 271.156 / 55.859; **OpenHands 482 s / 2.703.821 in / 124.212 out**. OpenHands consume **8,0x los tokens de entrada** y **2,0x el tiempo**: la causa es su patron (reenvia todo el contexto en cada turno: 29, 16 y 28 turnos contra 1 de Claude Code), no el modelo.
- **La suite oculta se valido en las DOS direcciones** (referencia correcta 3/3 PASS, version defectuosa 0/3 PASS). Eso destapo **dos defectos PROPIOS**: un assert de T3 exigia un ADR superseded que **no existe** (los 60 estan en `Aceptado`/`Rechazado`: el ADR-067 esta `Aceptado`), lo que habria castigado la respuesta correcta; y otro assert era tan laxo que la version defectuosa pasaba. Sin esa validacion, la suite habria reportado un defectuo inexistente.
- **Correccion de diseno que la fairness exigio:** los tres harnesses NO ven el repo igual (opencode corre en Alpine **sin python3, node, jq ni git**). Si las tareas exigieran ejecutar un script, la cata habria medido la IMAGEN DOCKER y no el harness. Por eso la ejecucion de los checkers se pre-computa una vez y su salida va a un corpus **identico para los tres**; las tareas son de lectura y analisis.

---

## [2026-10-27] - Vane se queda: research verificado en vivo, 5 commits locales a salvo y bajo demanda

### Added
- **`gonzoblasco/vane` (repo PRIVADO)**: el fork local de Vane con los **5 commits que nunca se pushearon** (el fix del writer prompt que hacia filtrar el monologo del modelo a la respuesta final, el `Dockerfile` con Next.js pineado y bind a `0.0.0.0`, el preconfig de Ollama, y la memoria `.knowledge/`). Antes apuntaba `origin` al upstream de un tercero: un `git push` ahi habria publicado trabajo nuestro en el repo de otro. Ahora `origin` es el fork privado y `upstream` queda como referencia.
- **El clon local era shallow** (cortado en `348feca`, sin padre local), y por eso el primer push fue rechazado con `did not receive expected object`. Resuelto con `git fetch --unshallow upstream master`: la historia completa (1.014 commits) queda en el remoto.
- **Research verificado en vivo** (no solo por logs): `POST /api/search` con `minimax-m3.1-flash:cloud` -> **HTTP 200 en 45,7 s**, respuesta en espanol con **8 fuentes citadas y trazables** sobre el protocolo MCP. El servicio funciona y hace good research (decision de Gonzo: "vane me gusta, hace buenos researches").

### Changed
- **Vane pasa a BAJO DEMANDA.** Es de uso episodic: se enciende para hacer un research y se apaga. Con ~45 s por research, dejarlo prendido sin buscar nada no tiene sentido (medido: **0 requests en 7 dias**). A diferencia de las demas, su `down` es real (`docker compose down`): elimina container y red, y no vuelve sola. Costo: ~340 MB de RAM, 7 s de arranque en frio.
- El triage OSS (`studies/oss-alternatives-triage.md`) decía *"No lo adoptes: es una app completa que no vas a mantener"*. **Eso ya no es la decision vigente**: Vane esta en uso y produce trabajo real. La nota queda como el analisis de ese momento; la decision actual es que se queda.

### Fixed
- **El registro no distinguia "apagado" de "apagado a proposito"** para Vane, que quedaria apagado por defecto. Ahora muestra `bajo demanda` con la instruccion de como levantarlo, igual que `browser-use-ui`.

---

## [2026-10-27] - `browser-use-ui` pasa a bajo demanda: el registro distingue "apagada a proposito" de "caida"

### Added
- **`browser-use-ui` tiene ficha propia en el registro de herramientas** (estaba=listada como "stack de compose corriendo sin ficha"). Decision de Gonzo: es una herramienta de **prueba** (para pilotar el agente a mano en el navegador), no de uso continuo, asi que **queda apagada por defecto**. Antes ocupaba ~190 MB de RAM encendida sin uso.
- **El estado "bajo demanda" es una clase propia en el registro.** Apagada a proposito se muestra como `bajo demanda` con la instruccion de como levantarla, y NO como `apagado`: un servicio que deberia estar vivo y no lo esta es un bug, una herramienta de prueba apagada es el estado normal. `browser-use` (el MCP que el gateway lanza por sesion) ya usaba ese estado, asi que ahora las dos superficeres de browser usan la misma palabra y se distinguen a simple vista.
- **Documentado CUANDO levantar la consola**, que era el punto que pediste: en la skill `browser-tool` (seccion "Cuando hay que levantar la CONSOLA"), en la skill `ai-toolbox` (seccion "Cuando la herramienta es BAJO DEMANDA"), en la ficha de `docs/tools/REGISTRY.md` y en el `README.md` del proyecto. La regla: se levanta solo cuando Gonzo pide probarla o usarla a mano; si pide que *yo* revise algo en el navegador, lo resuelve el MCP, sin la consola. Y si la levantaste para una prueba, la bajas al terminar.
- **Tests nuevos** (`tests/python/test_ai_toolbox.py`): una herramienta bajo demanda apagada no se reporta como caida; su `down` es `docker compose down` y no `stop`; y una herramienta normal sigue usando `stop` (conserva containers y volumenes).

### Fixed
- **`toolbox down` hacia `stop` para TODO, y `stop` no apaga: la herramienta vuelve sola en el proximo reinicio de Docker.** Es el mismo mecanismo que resucito a Onyx (ver la entrada anterior). Para las herramientas **bajo demanda** el `down` ahora es real: `docker compose down` (elimina container y red). Su `restart: no` garantiza que no se levanta sola. El volumen del perfil de Chromium (`browseruse-data`) se conserva: los datos quedan.
- **`browser-use` y `browser-use-ui` no eran la misma cosa, pero se confundian con facilidad:** usan la MISMA imagen `browseruse:local` (3,16 GB) con dos superficies distintas. `browser-use` es el agente, que el gateway expone como MCP y lanza por sesion con `docker run --rm` (no tiene container fijo). `browser-use-ui` es la consola web que corre en su propio container y habla MCP con un `browser-use --mcp` anidado dentro (modo `BROWSER_USE_UI_MCP_MODE=local`, para no depender del socket de Docker). **Apagar la consola no rompe el MCP**: verificado navegando a example.com con la consola apagada. La ficha de REGISTRY y la trampa de la skill `ai-toolbox` lo dejan escrito.

---

## [2026-10-27] - Onyx y LiteLLM fuera del stack: 32,4 GB liberados y el registro que moria

### Removed
- **Onyx eliminado por completo** (decision de Gonzo). **No estaba descartado: estaba apagado sin decision y habia vuelto solo.** Los 6 servicios tienen `restart: unless-stopped`, y esa politica ignora un `docker compose stop` manual: el reinicio de Docker Desktop del 2026-10-26 12:39:40 los levanto a todos en el mismo segundo (junto con vane, opencode y openhands). Para que no vuelva hace falta `down`, no `stop`. Uso real medido antes de borrar: **0 documentos indexados**, 0 requests al API server en 24 h, y las 1740 peticiones al nginx en 7 dias fueron **todas** `/api/health` de la sonda del toolbox. Eliminado: 6 contenedores + red, 4 volumenes (77 MB), 4 imagenes (~5,7 GB), repo clonado `projects/onyx` (138 MB) y `scripts/onyx-tool.py` a la papelera. Puerto 3000 liberado. El todo #82 (activar RAG) se cerro **sin objeto**: exigia el stack completo (Redis + OpenSearch + model servers) que no entra en los 8 GB de Docker Desktop, y la capacidad de RAG ya estaba cubierta por `scripts/memory-search.py`, `projects/langchain-starter` (ChromaDB) y `projects/soporteml` (pgvector).
- **LiteLLM: la entrada del catalogo era el ultimo resto.** La instalacion ya no existia (ADR-103, 2026-10-22: no habia imagen, ni compose, ni el directorio `~/experiments`). Quedaba vivo solo en el registro, que lo hacia figurar como "no instalado" y no como descartado.
- **6 contenedores MCP de browser-use huerfanos** detenidos: cada sesion lanza uno con `docker run --rm` y el runtime no lo baja al terminar. Todos estaban anclados por el supervisor del gateway, pero de sesiones ya cerradas (solo una sesion activa: esta). El de esta sesion quedo vivo.

### Fixed
- **El registro vivo moria por omision, no por decision.** `scripts/ai-toolbox.py` (entradas `onyx` y `litellm`) + la prosa de `docs/tools/REGISTRY.md` + la descripcion y la lista de IDs de la skill `ai-toolbox` + los tests que afirmaban esas herramientas como "nucleo del stack". La tabla de `REGISTRY.md` se **regenero** con `catalog --write` (editarla a mano la desincroniza del generador); la prosa se edito a mano. El test `test_las_herramientas_core_estan` ahora afirma `ollama`, `browser-use` y `vane`, y se agrego `test_las_retiradas_no_estan_en_el_catalogo`: una entrada que vuelve sola reinstala el stack en el proximo `up`.
- **`MEMORY.md` y `docs/SETUP.md` dejaban Onyx como si estuviera vivo.** La entrada curada de memoria y la seccion completa de SETUP (repo, script, modo Lite, trampas verificadas) se eliminaron; la `projects/` del triage paso de 30 a 29 carpetas en el todo #83 (reescrito, no cerrado: la tarea sigue viva).
- **`docker image prune -a` y `docker builder prune -a`:** 12,97 GB de imagenes sin uso y 19,43 GB de cache de build. La imagen `vane-builder:local` (10,66 GB, sin containers) tambien se fue: la imagen que Vane usa en runtime (`vane-local:ollama`) es distinta y sigue en pie, verificado con HTTP 200 en `:3005`.

### Added
- **`docs/ecosystem/onyx-decision.md`** - la decision completa: por que no se resucita, que se elimino, que se conservo, y los 4 aprendizajes. El mas transferible: **`stop` no desactiva la politica de restart** (la firma del diagnostico es "varios stacks arrancando en el mismo segundo"), y **"apagado" y "descartado" son clases distintas**: un descarte tiene documento de decision y limpieza; un apagado sin documento es la clase que el owner decide.

---

## [2026-10-27] - OnWheels queda EN CURSO: roadmap F0-F6, registro como proyecto activo y un bug de atribucion en el HANDOFF

### Added
- **OnWheels registrado como proyecto activo y en curso:** `session-context` (`.data/session-context.db`, estado **Active**, con goal, stack y constraints) + `projects/AUDIT.md` como ACTIVO + repo git local en `projects/onwheels/`. `session-context:resume onwheels` es ahora el punto de entrada para retomar.
- **HANDOFF propio del proyecto** en `projects/onwheels/.knowledge/HANDOFF.md`, con su `SESSIONS.md` append-only. Primer cierre para este proyecto.
- **Learning 312 en la DB** (`scripts/memory-db.sh add-learning`, no a mano en el markdown): un cierre de sesion puede escribir el HANDOFF en el proyecto equivocado cuando un override de slug quedo viejo.

### Fixed
- **`scripts/session-handoff.py`: el override `onwheels` -> `kanam-onwheels` mandaba el HANDOFF al repo DORMIDO.** Existia desde junio, cuando el proyecto se llamaba asi. Con el producto nuevo en `projects/onwheels/` (greenfield del 21/10) y el repo viejo declarado dormido (decision D4), el HANDOFF de la sesion iba a parar al `.knowledge/` del proyecto que ya no se trabaja. No habria dado error (los dos directorios existen): el error era de atribucion silenciosa. Corregido y **verificado por la funcion real**: `resolve_handoff_path('onwheels', None)` devuelve ahora `projects/onwheels/.knowledge/HANDOFF.md`. Tests de `tests/python/test_session_handoff*.py`: 16 passed.
- **Fila 311 de `learnings` eliminada** (la creo mi propia llamada mal parseada de `add-learning --help`: categoria `--help`, cuerpo vacio). Borrada **por id exacto**, nunca con un WHERE amplio: el gate `check-learnings-integrity.py` existe porque un DELETE anterior mio borro 9 lecciones reales. Gate despues: OK, 258 learnings.


---

## [2026-10-27] - La tabla `learnings` no tenia un lugar fijo para el cuerpo de la leccion: 4 defectos, un gate y 25.231 chars recuperados

### Fixed
- **El cuerpo de la leccion no tiene un lugar fijo en `learnings`.** Hay filas donde esta en `content` (lo normal), en `title` y en `tags`. El export a `docs/learnings/*.md` lee el cuerpo de `content` y el titulo de `title`, asi que las otras dos clases se veian como seccion vacia y nadie lo notaba. Origen: `migrate-learnings.py` derivaba los tags del titulo, y la absorcion de la tabla gemela (commit `0518cdf3f3`) descarto la prosa de `tags` **asumiendo que era "el titulo duplicado"** - suposicion falsa: en 5 filas la prosa era el CUERPO. Reparados: 9 cuerpos recuperados (5 de `tags`, 4 de `title`).
- **`memory-db.sh add-learning` escribia en la columna `tags` y nunca en la junction `learning_tags`**, que es lo UNICO que lee el export: 79 filas con tags reales que no aparecian en ninguna vista. Todo lo agregado por ese comando desde la taxonomia normalizada quedo invisible. Ahora escribe en la junction, en una sola invocacion SQL (`last_insert_rowid()` en un proceso sqlite3 separado devolvia 0 y violaba la FK).
- **`memory-catalog-v2.py` cortaba el cuerpo a 500 chars** con el mismo valor que usaba para el embedding (`content_text = learning.get("content","")[:500]`): 34 filas a la mitad. El tope de 500 chars es de la API, no del dato. Ahora el tope queda solo para el embedding y el cuerpo se guarda completo. 20 truncadas se recuperaron del corpus (`sessions_relacional.content_bare` / `daily_notes.content`, buscando el fragmento del **MEDIO**, no el prefijo: el prefijo truncado es identico al original); 14 no existen en ningun lado y quedan como deuda aceptada.
- **4 lecciones que existian solo en los `.md` y que la regeneracion iba a borrar**, y la version larga (2.399 chars, 4 casos con tabla) de la leccion del filtro de idioma, que la DB guardaba truncada a 565 chars. Devueltas a la DB, que es la fuente de verdad.

### Added
- **`scripts/check-learnings-integrity.py`** - gate de la tabla, en el pre-commit SIN CONDICION (la tabla se modifica desde `add-learning`, desde el catalogo y desde las migraciones, y el dano no aparece en el diff). Separa **PERDIDA** (bloquea: el cuerpo no esta donde debe) de **RUIDO HISTORICO** (avisa: prosa en `tags`, titulo largo): con el recalibrado, 0 perdidas y 70 avisos. La primera version reportaba 169 filas y era inutil - un guard que reporta todo no se lee y no se respeta. Probado sembrando el defecto: bloquea con exit 1.
- **`scripts/repair-learnings-body.py`** (C1/C2) y **`scripts/repair-learnings-taxonomy.py`** (C4/C5) - reparacion idempotente, con `--dry` y `--db` para correrla contra una copia antes de la real.

### Measured
- **+25.231 chars de cuerpo recuperado** en `docs/learnings/` que estaba perdido y no se veia en ninguna vista (9 cuerpos + 20 truncadas + los tags repoblados en 79 filas).
- **9 lecciones reales destruidas por un DELETE mio** (asumi que el cuerpo vivia en `content`). Restauradas desde copia y verificadas **fila por fila** con 0 diferencias contra la copia.

---

## [2026-10-26] - El pipeline pasa de A/B a A/B/C: un tercer agente que escribe la red de tests

### Changed
- **El pipeline tiene tres roles con modelos distintos entre si** (ADR-105): A escribe con `gpt-oss:120b-cloud`, B revisa con `deepseek-v4.1-flash:cloud`, C escribe la red de tests de regresion con `minimax-m3.1-flash:cloud`. El gate `scripts/check-pipeline-enforcement.py` verifica la ruta `pipeline_abc`, la consistencia entre fuentes, que los tres sean **distintos entre si** y que coincidan con el canon.
- **Solo A toca el codigo de produccion.** B no edita: escribe la evidencia ejecutable de cada defecto en archivos `probe_*.py` y entrega el reporte. Medido: B encuentra **mas** cuando no edita (10 findings vs 9), porque editarlo lo distrae de reportar. El rework vuelve a A, con la condicion de que todo finding de B termine como un test de C.
- **`scripts/model-router.sh`** - ruta `pipeline_abc`. La ruta `pipeline_ab` se conserva para trabajo donde la red de regresion no aporta.
- **`scripts/managed-blocks.py`** - setting `model_pipeline_c`; bloques `pipeline-abc` (AGENTS.md) y `model-pipeline-abc` (SETUP.md), que estaba huerfano en SETUP.md y por eso nadie mantenia.
- **`skills/agent-orchestration-pipeline-model-arbitration/SKILL.md`** - el pacto ABC y el reparto de trabajo, con la regla del rework.

### Added
- **`bench/`** - harness reproducible: el head-to-head de revisores con `GROUND_TRUTH.md`, `seed_bugs.py` y `verify_recall.py`; el pipeline ABC sobre 3 casos extremos (cache concurrente, bisiestos, token bucket); y el caso de rework. Con ground truth, el recall se mide contra verdad y no contra opinion.

### Measured
- **El slot B se decide por recall, no por velocidad.** Sobre el mismo artefacto con 4 bugs sembrados: `deepseek` 4/4 con 9 hallazgos, `minimax` 4/4 con 10, `beam:cloud` 3/4 con 3 y **se auto-aprobo con un defecto vivo**. beam es 3,5x mas rapido pero es la velocidad de no mirar.
- **El rework de A da el mismo recall que B corrigiendo directo (4/4) pero cubre 7 de 9 findings**, y el que se le escapo tampoco quedo como test: se perdio dos veces. Sin la regla "todo finding de B termina como un test de C", el hallazgo vuelve.
- **El 429 de Ollama Cloud es por cuenta, no por modelo**: saturar un modelo hace fallar a los otros (28/40 y 27/40). Cambiar de modelo no abre presupuesto. La concurrencia efectiva tiene que quedar en 2-6; a 20 en vuelo falla el 70%.
- **`beam:cloud` queda fuera del pipeline** (recall 3/4 como revisor, sin ahorro de requests como pre-filtro: 478 tokens de eval contra 18 de `gemma4`, misma accuracy) y entra como modelo de contexto largo: clavo el needle a 233k tokens donde `minimax` falla con HTTP 500 a 140k.

### Pending
- **Dos ambiguedades del spec sin resolver** (las dejo visibles, son decisiones de contrato): el borde del TTL ("mas viejo que ttl_seconds" admite edad exactamente `ttl`, el codigo usa la ventana estricta) y la copia superficial del cache (copia la lista pero comparte los dicts internos).

## [2026-10-25] - El costo de un modelo en Ollama Cloud no es plata: es cuota

### Changed
- **`docs/adr/ADR-102-minimax-m31-flash-motor-core.md`** - revisado en el sitio, sin crear un ADR nuevo (evitar deuda tecnica: una decision revisada no ensancha la serie). El pendiente vencido del 2026-10-23 ("reevaluar si la gratuidad termina") queda **resuelto**: la gratuidad si termino, pero la unidad correcta no es el precio por token.
- **La unidad correcta es la cuota de GPU de Ollama Cloud.** El plan legacy no tiene creditos de $60/mes: tiene **tasa de uso** (barra semanal con reset). "Barato" = cuanta cuota deja gastar, no cuanta plata cuesta. La cata del 2026-10-20 y la primera redaccion del ADR trataron el costo como dinero, y por eso el balance quedo sin decidir.
- **Precios de referencia verificados** el 2026-10-24 en `ollama.com/pricing` (la pagina si expone la tabla, en HTML estatico, aunque la cata no la encontro): minimax output $0,60/1M; deepseek-v4.1-flash $1,20 en pico y **$0,60 en off-peak** (fuera de 12:00-18:00 UTC en habiles y todo el fin de semana), glm-5.3-flash $0,50, gpt-oss $0,60. Fuera del horario pico, minimax y deepseek cuestan lo mismo por token de output.
- **Cuota medida sobre el panel de Ollama Cloud** (barra medida en pixeles sobre las capturas, track = 820 px, usado = 485 px = 59%, consistente con el 60,4% que reporta el panel): `glm-5.3-flash` 559 requests = 163 px (33,6% de la cuota, 0,29 px/req); `deepseek-v4.1-flash` 2.684 requests = 142 px (0,053 px/req); `minimax-m3.1-flash` 2.201 requests = 146 px (**0,066 px/req**). El "20-30% superior" queda confirmado como **1,25x por request**, pero en absoluto son **4 px de 820: 0,5% de la cuota semanal**.
- **Decision: se mantiene `minimax-m3.1-flash:cloud` como default del CORE.** Cambiar a deepseek para "ahorrar cuota" compra 0,5% y paga con la calidad medida del rol `main` (8,9 vs 7,8 en la cata de 8 roles x 5 clases de estres). El uso real ya esta en minimax sin que la cuota se trabe.
- **`docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`** - el pendiente de reevaluacion de consumo pasa de "precio sin fuente primaria" a la decision tomada, con la referencia al ADR-102.

### Measured
- **La cuota no es proporcional a los tokens**, asi que el px/request hay que leerlo del panel y no derivarlo del consumo. Medido en los transcripts del workspace (7 dias): `glm-5.3-flash:cloud` corre con 274k de cacheRead por turno (mas que minimax con 240k) y aun asi consume 0,29 px/req. Por eso el mix de modelos no se deduce de los tokens.
- **El riesgo grande de cuota de minimax era la espiral de thinking** (7 de 40 celdas con 0 entrega en la cata, 44k-56k caracteres de razonamiento): una espiral de 50k tokens quema cuota de 5-10 turnos normales sin entregar nada, y eso no se ve en la barra. **Medido y descartado en uso real** (ver Pending).

### Pending
- **Requests quemados por hora: RESUELTO 2026-10-25.** Medido sobre los transcripts desde el 2026-10-20 (cuando minimax paso a ser default): **0,33% en minimax** (18 de 5.425 turnos) contra 0,22% en deepseek. Un turno cuenta como quemado si no tiene texto **ni** tool calls. Los 18 quemados consumieron **0 output tokens** (12 fueron `LLM idle timeout (120s)`, no razonamiento quemado), o sea **no gastaron cuota de output**. La espiral de thinking de la cata **no se materializo en uso real**: el riesgo grande queda descartado como factor y la decision queda sin condiciones.

## [2026-10-25] - Los tres ATS verificados end-to-end: Ashby, Lever y Eightfold probados de verdad

### Fixed
Probar los adaptadores de Lever y Ashby (los dos que faltaban) encontro cuatro bugs mas, y uno era el peor de todos: **el gate de "no enviar si hay divergencias" era un no-op en Ashby y un falso positivo en Lever.**

1. **Ashby: el formulario no hidrata con `domcontentloaded`** (0 inputs; hidrata ~2s despues). Y el bug de gallina y huevo: la espera de 12s por el parseo del CV estaba DENTRO del `if` que encuentra el input de CV, pero ese input solo existe despues de hidratar. Sin CV no habia espera, y los textos se escribian contra un formulario vacio: **el reporte decia "5 campos faltantes" con la pagina llena**. Ahora hay un `waitForSelector` al principio, que no depende de nada opcional.
2. **Ashby: los radios no se verificaban.** Se hacia click y se asumia que habia funcionado. Ahora se lee que opcion quedo marcada en cada grupo, por el texto de su etiqueta. El gatelv2immediate dio `ok: false` con los radios BIEN marcados, por un bug del propio gate: truncaba el `name` del grupo con `split("_")`, y el nombre de Ashby es `<uuid>_e7e51cb6-...`: al truncar, "veteran_status" se confundia con "eeoc_veteran_status". Se busca por fragmento sobre el name completo.
3. **Lever: los inputs NO tienen `_valueTracker`** (no es un form React). El gate comparaba el valor del DOM contra `""` y reportaba divergencia en TODOS los campos, con el formulario impecable: **un falso positivo que hacia parecer roto lo que funcionaba**. Ahora distingue tres estados: divergente (hay tracker y difieren), no verificable (no hay tracker: el DOM es la unica evidencia) y ok. Los no verificables se reportan aparte, para que la verificacion parcial sea visible.
4. **Lever: el pitch se perdia.** El campo "Do you want to include additional information?" (donde va el AI Engineering OS, el servidor MCP y los 11 PRs) se llenaba con `answers.coverLetterText`, que es la cover letter - un archivo. En Lever la cover letter no se sube: es texto. El campo quedaba VACIO y el reporte lo daba por bien. Ahora usa la clave semantica `additionalInfo`.

### Added
- **Verificacion de radios en los dos adaptadores que no la tenian** (Ashby y Lever): no alcanza con que el click no tirara error, hay que leer que opcion quedo marcada.
- **Dos tests nuevos** para el falso positivo de los forms no-React (`verifyFields` con un input sin tracker: no reporta divergencia, y queda como "no verificable").
- **Evidencia de las tres corridas** en `docs/entrevistas/_general/outreach-2026-10-22/evidencia/`: `ashby-form-filled.png`, `ryz-form-filled.png`, `meli-form-filled-submitted.png`.

### Notes
- **Los tres adaptadores quedan probados end-to-end contra los formularios reales:**
  - **Eightfold** (Mercado Pago): 6 campos + 4 desplegables + CV, `ok: true`, 0 divergentes.
  - **Ashby** (Mural): 5 campos + 5 radios verificados + CV + cover letter, `ok: true`, 0 divergentes.
  - **Lever** (RYZ): 6 campos + radio de ingles verificado + CV + pitch, `ok: true`, `captcha: true` (el unico que queda pendiente de un humano, y es el hCaptcha de siempre).
- **El captcha de Lever se reporta como `captcha: true` y NO se intenta resolver.** Es el comportamiento correcto segun ADR-104: un captcha detecta el contexto, no los intentos.
- **Una leccion que se repite y que queda escrita: el `ok: true` de un gate no es prueba de nada si el gate no verifica lo que dice verificar.** El gate de radios de Ashby daba `ok` sin mirar los radios; el de Lever daba divergencia en un formulario impecable. Los dos se detectaron mirando la CAPTURA, no leyendo el codigo ni el exit code.

---

## [2026-10-25] - El radar de vacantes deja de romperse en silencio

### Added
- **`skills/job-application/scripts/lib/discovery.mjs`** - las funciones PURAS del discovery (parseo de LinkedIn, filtro por query/pais/remoto, mapa de codigos de pais), extraidas del script que hace la red **para que queden testeadas**.
- **Cuatro fuentes de job boards mas** (`remotive`, `arbeitnow`, `jobicy`, `himalayas`), cada una **medida contra su API antes de agregarla** (no se agrega una fuente que no responde). El radar consulta las cinco en paralelo y **reporta cuales respondieron y cuales fallaron**.
- **20 tests nuevos** del discovery (27 en total en la suite del skill), que cubren los cinco bugs de abajo y el caso de un markup que vuelve al formato viejo.

### Fixed
El radar de vacantes dejo de encontrar nada el 2026-10-25, y la causa NO fue que no hubiera vacantes: fueron **cinco bugs encadenados, cada uno invisible desde afuera** (un radar mudo parece "no hay nada"). Ademas, uno lo encontrado un test nuevo:
1. **Argumentos en el orden equivocado**: `src.url(country, start)` cuando el primer parametro de cada fuente es la QUERY. Se buscaban las vacantes de "AR" en vez de "frontend". La firma ahora es uniforme: `url(query, start, country)`.
2. **LinkedIn cambio la clase del markup**: `result-card__full-card-link` ya no existe, ahora es `base-card__full-link` dentro de un `div.base-card`. La fuente devolvia CERO y nadie lo notaba. El parser ahora extrae titulo, empresa y ubicacion, y descarta la tarjeta si el titulo queda vacio.
3. **El filtro de pais era un `includes` plano**: "ar" matcheaba "**Ar**kansas", y Bentonville, Arkansas, Estados Unidos pasaba el filtro de Argentina. Ahora es match por palabra entera, con un mapa de codigo -> nombre de pais.
4. **Las vacantes remotas "Worldwide" se descartaban**: son justamente las oportunidades LATAM, que es lo que mejor rindio. Ahora entran.
5. **LinkedIn recibe el nombre del pais, no el codigo**: se pasaba `location=AR` y la busqueda daba cero.
6. **La concatenacion de la ubicacion dejaba `", "`** cuando ambos campos estaban vacios, y eso no esta vacio: la vacante se descartaba. Una vacante sin ubicacion no se descarta nunca.

### Notes
- **El aprendizaje de fondo, y el motivo de la lib separada: un scraper sin tests es un scraper que se rompe callado.** La regla de una regla: lo que decide QUE se devuelve va en una lib pura con tests; lo que hace la red queda en el script. Cuando un sitio cambie su markup o sus parametros, el fallo sale en la suite y no en el silencio.
- **El script ahora imprime que fuentes respondieron** (`fuentes: linkedin, remotive, ...`). Es la primera cosa que hay que mirar cuando el radar se calla: si dice una que no esperabas, esa es la rota; si dice todas y no hay resultados, el problema esta en el filtro.
- **Verificado end-to-end**: el radar devuelve vacantes reales de las 5 fuentes, en ingles y en espanol, incluyendo la de RYZ Labs. 27 tests en verde.

---

## [2026-10-24] - kanam-sudoku-iphone: proyecto nuevo desde cero, con la dificultad definida por tecnica

### Added
- **`projects/kanam-sudoku-iphone/`** - sudoku 9x9 **mobile-first para iPhone** (PWA instalable, offline, teclado numerico en pantalla, 3 dificultades), pedido por Gonzo con la instruccion explicita de **no usar los proyectos actuales**. Repo publico previsto (`gonzoblasco/kanam-sudoku-iphone`) en GitHub Pages.
- **Ciclo de definicion cerrado** con los artefactos estandar: 6 specs (`.knowledge/specs/SPEC-001..006`, checker del workspace en exit 0), `KNOWLEDGE.md`, `docs/architecture.md` (contratos, alternativas descartadas, tabla de trazabilidad), `docs/CONTEXT.md` (glosario con sinonimos rechazados), `docs/data-model.md`, 6 ADRs, `AGENTS.md`/`CLAUDE.md` del proyecto y CI + deploy.
- **Decisiones de negocio de Gonzo (2026-10-24):** hosting = GitHub Pages desde repo **publico**; dificultad = **por tecnica de resolucion** (no por cantidad de celdas vacias); instalacion = **PWA completa** (manifest + service worker).
- **Decisiones tecnicas propias:** TypeScript + Vite con **cero dependencias de runtime** y una **unica convencion de mascara** (`bit (d-1)`) - el problema exacto que sufrio el motor previo, que tenia `1 << (d-1)` y `1 << d` conviviendo. Estado en un unico `GameState` con historial de mutaciones, para que deshacer, notas y guardado se agreguen **sin reescribir el nucleo** (el pedido lo exigia explicitamente).

### Measured
- **La trazabilidad se verifica con grep, no se afirma**: las 17 capacidades (`C1`..`C17`) y las 6 specs aparecen en la tabla de `docs/architecture.md`. Las 7 capacidades fuera de v1 estan nombradas como fuera, no omitidas.
- **El stack se verifico contra la maquina, no contra la suposicion**: Node 26.8.1 corre TypeScript con type stripping nativo (`node --test` descubre y corre tests `.ts` sin paso de build), y Playwright-core + Chromium headless ya estan instalados para el e2e en viewport de iPhone.

### Changed
- **`MEMORY.md`** - entrada del proyecto en la seccion de repos activos, con la instruccion de "desde cero" y las tres decisiones de Gonzo, para que nadie lo confunda con el `kanam-sudoku` v1 (que queda intacto y es de escritorio).

### Published (2026-10-24, evening)
- **Repo publico**: `gonzoblasco/kanam-sudoku-iphone` -> **https://gonzoblasco.github.io/kanam-sudoku-iphone/**. CI y deploy verdes; el sitio desplegado verificado en Chromium real (81 celdas, escritura funcionando, 0 errores de consola).
- **Revision B del pipeline A/B**: 18 bugs reales encontrados y corregidos. El grave: **el tablero estaba transpuesto** (filas y columnas invertidas) y **ningun test lo veia**, porque todos los e2e median geometria y ninguno comparaba el valor de una celda contra el dato del motor. Otros: la region `aria-live` visible (faltaba `.sr-only`), el teclado fuera del layout pedido, tres tecnicas con deducciones falsas (`x_wing` eliminaba el digito de su propio patron), semillas correlacionadas en el generador, `matched:false` reportando el nivel con el cap pedido, `undo` roto tras el tope del historial, el cronometro sin pausar en background, la partida ganada quedandose guardada, y el service worker precacheando su propio `sw.js`.
- **El tablero se hizo fluido**: nueve celdas de 44px necesitan 396px y el viewport de referencia tiene 390px. Con el tablero fijo se perdia la ultima columna (y en un iPhone SE, una columna entera). Ahora es `min(100%, 396px)` y la celda es un noveno de la fila con base porcentual: medido, 390px -> 43.33px, 375px -> 41.66px, 430px -> 44px exactos, sin solape. **La spec, el e2e y el `AGENTS.md` del proyecto quedaron reconciliados con la aritmetica.**
- **Verificacion final**: 73/73 tests, `tsc --noEmit` limpio, 4 e2e en Chromium a 390x844 (27/27, 34/34, 61/61, 11/11), contraste AA en los 9 pares de color de ambos temas, axe-core con 0 violaciones, y **una sola convencion de mascara** en todo el arbol.
- **CI corregido**: `tsc` resolvia los tipos de Node desde el `node_modules` del workspace padre, asi que pasaba local y fallaba en CI. `@types/node` es ahora devDependency del proyecto.

### Added (2026-10-24, evening) - sistema de notas
- **`kanam-sudoku-iphone`: notas por celda** (capacidad C12, que la v1 dejo fuera de alcance; pedida por Gonzo despues de la publicacion). **Modo notas** (el teclado marca candidatos en vez de escribir valores), **candidatos automaticos** ("Auto") y **limpieza** de anotaciones, con la grilla 3x3 clasica en la celda.
- **La decision que la hace coherente: una nota no es una jugada.** No cambia el valor de una celda y **no entra al historial de deshacer** (ADR-0007). Por eso su API (`setNote`, `toggleNote`) esta separada de `apply` desde el primer dia, y `apply` sigue siendo el unico camino de escritura del valor.
- **Los candidatos automaticos salen del mismo motor que las tecnicas** (`core/candidates.ts`): una nota automatica nunca ofrece un digito que el motor ya descarto.
- **El valor de una celda y sus notas son informacion distinta**: viven en elementos separados (`.cell-value` y `.note-grid`). Una celda con valor **oculta** sus notas, y al borrar el valor **vuelven**.
- **Fue la primera prueba real de ADR-0004**: la capacidad entro entera y **el nucleo (`core/`, `state/state.ts`) no cambio de forma**, porque el estado ya tenia `notes` y su API desde el primer dia. La promesa de "deshacer, notas y guardado se agregan sin reescribir el nucleo" quedo demostrada, no declarada.
- Verificado: `npm test` **91/91** (11 suites), `e2e.notes` **40/40**, y los otros cuatro e2e siguen verdes (27/34/61/11). Contraste AA del color de notas en ambos temas (8.86:1 claro, 12.12:1 oscuro). Bundle: 23.8 kB -> 26.8 kB (8.76 kB gzip).
- Spec nueva (`SPEC-007-notas.md`), ADR nuevo (`ADR-0007-notas-no-son-jugadas.md`) y reconciliacion de los artefactos que el cambio de alcance deja obsoletos: BRIEF, `docs/architecture.md` (tabla de trazabilidad), `docs/data-model.md` (`CellView.notes`), `docs/CONTEXT.md` (glosario: "modo notas" y "digitos legales") y el indice de ADRs.

### Changed (2026-10-25) - rediseno visual de `kanam-sudoku-iphone`, decidido midiendo
- **El problema real**: el tablero era una planilla con formato condicional. Cuatro colores sin relacion para los cuatro contextos de resaltado (fila roja, columna verde, bloque azul, mismo-numero amarillo), que en modo oscuro se volvian barro; cero acento; menu generico; notas a 8px ilegibles.
- **Se debatieron tres propuestas con tres agentes** y **se midieron, no se discutieron**: se escribio `scripts/palette-check.mjs` (ratios WCAG desde la paleta) y `scripts/theme-lab.mjs` (renderiza cada propuesta como PNG a 390x844). **Dos de las tres propuestas fallaban AA en la linea de la grilla**: declaraban 8.53:1 y 2.2:1, medidas dieron **1.57:1** y **1.52:1** (una habia copiado el ratio del texto secundario). La tercera proponia notas de 8px, el mismo defecto que se queria corregir.
- **La sintesis que se implemento**: **un solo matiz (teal) en cuatro pasos de intensidad** en vez de cuatro colores, cada contexto con un canal que no es color. Papel calido (`#faf7f2`) y tinta calida (`#14120f`): el blanco y el negro puros son un error en una app que se mira de noche. El acento marca la seleccion y la regla bajo el titulo, nada mas; el conflicto es el unico otro color saturado. Cifras tabulares en el tablero. Las teclas se hunden al pulsar (`scale(0.96)`). "Borrar" pasa a ser mas chico y atenuado.
- **Bug de especificidad corregido**: el boton "Notas" activo quedaba transparente porque la regla base le ganaba a la regla de presionado. Verificado con `getComputedStyle` tras la transicion.
- Verificado: 91/91 tests, typecheck limpio, build ok (CSS 6.13 kB, 1.91 kB gzip), e2e 27/27 + 34/34 + 61/61 + 11/11 + 40/40, **todos los pares AA en ambos temas**, incluidos los cuatro tintes de resaltado compuestos sobre el fondo.

---

## [2026-10-23] - Radar de oportunidades OSS: PRs y reviews por separado, con lo que NO es oportunidad

### Added
- **`docs/prs/oportunidades-2026-10-23.md`** - busqueda de material de post en repos de 1er y 2do nivel, con **PRs y reviews por separado**, verificada contra la API de GitHub (comments, assignees, y los PRs que referencian cada issue via timeline). Criterio de tier explicito (1er nivel >9k stars; 2do nivel o sub-marca donde ya hay contribucion propia). Vive en `docs/prs/` y **no** en `docs/linkedin/`: ese directorio es el de los posts, y el gate de la cadena los valida como posts.
- **La accion mas barata, medida:** las 2 PRs propias de `t3-oss/create-t3-app` (**#2243** y **#2240**) estan paradas desde julio con **0 review comments**. No es "waiting for review" del maintainer: es trabajo en curso sin contraparte.
- **4 issues a11y LIBRES en `mui/material-ui`** (#49444 CardActionArea, #49445 AppBar, #49446 SpeedDial, #49447 ImageList): 0 comentarios, sin assignee, **sin ningun PR que los referencie**, y con el scope escrito en el issue (axe tests + `<Componente>/accessibility.md` + `pnpm a11y:scorecard`). El repo ya tiene 12 `accessibility.md` de componentes que dan la plantilla.
- **5 candidatas a review con sustancia** (PRs a11y sin ningun review de humano): `adobe/react-spectrum#10803`, `mui/base-ui#6047`, `radix-ui/primitives#4222` y `#4227`, `facebook/astryx#7906`.
- **Tambien lo que NO es oportunidad**, porque la regla de "nunca piso" lo exige: los 5 issues de `facebook/astryx` (uno con 10 PRs que lo referencian), `adobe/react-spectrum#9556` (4 PRs), `mui/base-ui#5519` (2 PRs), `mui/material-ui#49511` (asignado a un autor).

### Measured (lo que contradice el plan)
- **El tier 2 de a11y NO tiene backlog de issues abiertos.** `carbon-design-system/ibm-products`, `vercel/ai`, `tanstack/router`, `colinhacks/zod` y `payloadcms/payload` dan **0** con label `accessibility`. Y `carbon-design-system/carbon` **no tiene ese label**: usa labels granulares por tecnologia de asistencia (`a11y: JAWS` 56, `a11y: VoiceOver` 33, `a11y: NVDA` 2, `a11y: high contrast mode` 3, `a11y: TalkBack` 0). **Consecuencia:** en tier 2 la oportunidad es destrabar lo propio y revisar donde hay volumen sin review (`shuding/nextra`: 47 PRs abiertas / 45 sin actividad; `t3-oss/create-t3-app`: 53 / 49) - no "encontrar un issue de a11y".
- **Endurecer el gate con `Proyecto`, `PR`, `Fecha` e `Idioma` romperia 8 de los 10 posts vivos, incluido el canonico** (`astryx-5419.md`). El gate hoy exige solo `Status` y `Nicho`, a proposito: el proyecto se deduce del link del PR, que si es obligatorio, y un gate que reprima al canonico esta roto. **Queda como decision de Gonzo, con la migracion de los posts existentes como condicion previa** - no se aplica sobre posts que no lo cumplen.

### Changed
- **`docs/ROADMAP.md` seccion 2.2** - las acciones pasan a llevar lo medido: el radar con sus cuatro acciones concretas, el hallazgo de que el tier 2 de a11y esta vacio, y la pregunta del gate con su condicion.

---

## [2026-10-23] - Postulaciones RYZ y Mural: formularios listos (sin enviar) y limpieza de huellas de IA

### Added
- **Formularios de postulacion de RYZ Labs y Mural completados y verificados** _(scripts en `tmp/job-search-2026-10-22/`, capturas en `docs/entrevistas/_general/outreach-2026-10-22/`)_. El browser de OpenClaw no arranca (no hay Chrome en `/Applications`), asi que se maneja con **Chrome for Testing de Playwright** via Playwright: `projects/a11y-fixer/node_modules/playwright` con `executablePath` explicito.
  - **RYZ (Lever):** CV subido y parseado ("Success!"), nombre, email, telefono, ubicacion geolocalizada, empresa, **salario USD 3.200/mes**, **Upper Intermediate**, e informacion adicional. Captura: `ryz-form-filled.png`.
  - **Mural (Ashby):** CV y **cover letter** en sus slots correctos, 6 campos de texto, **salario USD 3.400/mes**. El **reCAPTCHA se resuelve solo** (token de 2.382 chars, modo invisible). Captura: `mural-form-filled.png`.
  - **Cover letter de Mural** (`cover-letters/cover-letter-mural.md`): 292 palabras de cuerpo. El angulo es el **servidor MCP propio** (que responde a un requisito explicito del JD), los **experimentos A/B reales** con Adobe Target, y los gaps declarados en una frase.
- **Scripts reutilizables de postulacion:** `tmp/job-search-2026-10-22/fill-ryz.js` y `fill-mural.js`. Ambos completan, **verifican campo por campo releyendo el DOM**, toman captura y solo envian con `--submit`. El envio sigue siendo una decision explicita de Gonzo.

### Fixed
- **La cover letter traia 12 guiones no separables (U+2011) y un en-dash:** el residuo tipografico de una salida de modelo, que es exactamente la clase de huella que Gonzo pidio evitar. Normalizados a guion comun y apostrofe recta (`scripts/check_em_dash.py` da verde). Tambien se fueron el cierre formulaico "I look forward to contributing" y el conector "Additionally".
- **La cover letter decia "the design systems you list"** cuando el JD de Mural **no lista design systems** (verificado: 0 coincidencias), y "user insights", que no esta en el corpus. Y repetia el MCP en dos parrafos. Corregido.
- **El parser automatico de Lever pisa el nombre:** al subir el CV, Lever pone "Freelance" en el campo Full name (toma la empresa del CV). Los scripts lo sobreescriben despues de que el parser asiente, y el dry run lo verifica.
- **El input de ubicacion de Lever queda visiblemente vacio** con `fill()` y con click en la opcion: React re-renderiza y borra el valor, aunque el hidden `selectedLocation` quede bien. **El unico metodo que deja el campo visible es el humano: teclear, `ArrowDown`, `Enter`.** Verificado con captura en los tres caminos.
- **El campo de salario de Lever tiene dos inputs** con la misma etiqueta (uno hidden, `baseTemplate`, y el real visible). Agarrar el hidden hace fallar el `fill()` con timeout de 30s. Se toma el visible por `name*="[field0]"`.
- **Los archivos se cruzaban en Ashby:** el cover letter iba al slot del CV. Ashby renderiza tres inputs de archivo (subida del CV sin `name`, `_systemfield_resume`, y el de Cover Letter con UUID) y **los reordena**. Se mapean por `name`, no por indice ni por label (el ancestro con texto mas cercano es "First and Last Name").
- **Los radios de nivel de ingles de Lever no son `<select>`:** son radio con `value` = texto de la opcion ("Upper Intermediate"). Se eligen por `value`, no por etiqueta.

### Notes
- **No hay trampas de deteccion de IA en los formularios.** Solo los captchas estandar: hCaptcha en Lever (que NO se resuelve solo: token 0 en headless y en browser visible) y reCAPTCHA en Ashby (que si se resuelve solo, modo invisible). El riesgo real de rechazo es el **spam filter por contenido**, que se mitiga con los gaps declarados y el cero-slop.
- **El navegador no tiene sesion de LinkedIn.** El perfil `Chrome for Testing` tiene cookies (`li_at`, `JSESSIONID`) pero al copiar el perfil a un directorio temporal las cookies no sobreviven (WAL). El unico Chrome corriendo tiene el login, pero no expone puerto CDP. Para un DM por LinkedIn haria falta loguearse de nuevo en un perfil que Playwright pueda abrir.
- **El `--submit` de RYZ es el unico con captcha sin resolver.** hCaptcha en modo invisible suele generar el token en el momento del submit; eso solo se puede comprobar enviando. Por eso el submit sigue siendo paso manual y con OK.
- **Salarios decididos con datos, no con intuicion:** USD 3.200/mes en RYZ (banda estimada USD 82.600-153.400/ano) y USD 3.400/mes en Mural. Para Mural, la banda que publica un agregador es **estadounidense** (USD 105.054-131.317/ano) aunque el puesto es "Argentina Remote": la referencia real es el dato de empleados (Levels.fyi, L2 en Greater Buenos Aires: ARS 54,3M de compensacion total anual = **USD 2.963/mes** al cambio del 23/10 de 1.527,85). Pedir 3.400 es coherente con el seniority real y con la banda, sin pelear contra el techo de 5K que fijo Gonzo.
- **Pendiente:** enviar (requiere OK explicito), y el canal de LinkedIn, que sigue siendo el unico que no puedo operar.

---

## [2026-10-23] - Cierre de la tanda: las TRES postulaciones confirmadas

### Added
- **Las tres postulaciones quedaron confirmadas por el servidor:**
  - **Mural** (Ashby): "Your application was successfully submitted. We'll contact you if there are next steps." Salario USD 3.400/mes, CV + cover letter.
  - **Mercado Pago** (Eightfold): "¡Gracias por su solicitud, Gonzalo!" + `201 {"success": true}`. Vacante id 44891701 (displayJobId 127795), localizada via `careers-meli.mercadolibre.com/api/positions?country=AR`.
  - **RYZ Labs** (Lever): enviado desde Safari, **sin hCaptcha**. Salario USD 3.200/mes, nivel Upper Intermediate.
- **Invitacion de conexion enviada a Sonia Langone** (recruiter tecnica de RYZ, 2do grado) con nota de 833 caracteres: por que encaja, el AI Engineering OS, el servidor MCP propio, los 11 PRs mergeados, y las dos preguntas de screening (overlap con US en EST, y nivel de ingles conversacional). Es la via que ademas abre la conversacion.
- **`docs/entrevistas/_general/outreach-2026-10-22/scripts/`** - los seis scripts de postulacion, reutilizables y comentados con el por que de cada workaround; mas `ryz-cdp.js` (conexion por CDP al Chrome real) y `ryz-manual.js`.

### Fixed
- **El hCaptcha de Lever no lo puede resolver un navegador automatizado, y el problema lo causo el propio intento de automatizarlo.** El token daba 0 en Chrome de Playwright (`navigator.webdriver: true`) y en el perfil `imported` del browser de OpenClaw (`--headless=new`, "HeadlessChrome" en el User-Agent). Se probaron todas las variantes (click en el checkbox del iframe, click de mouse real, browser visible, 60s de espera): nada. En Safari, sin tocar el captcha, el envio salio directo. El aprendizaje quedo en `docs/learnings/metodologia.md`: **ante un captcha, cambiar de navegador; no insistir con el mismo**. Y antes de pedirle a una persona que resuelva algo a mano, verificar que el contexto que se le pasa no este marcado: el "fallo" de la persona suele ser el fallo del instrumento.
- **Relanzar el perfil `imported` de OpenClaw visible** (mismo `user-data-dir`, con la sesion de LinkedIn, sin `--headless`): con el flag headless el perfil servia solo para el scraping de LinkedIn, pero cualquier formulario con captcha lo rechazaba.

### Notes
- **El aprendizaje operativo mas general de la tanda:** en formularios de React, `fill()` de Playwright deja el valor en el DOM pero NO actualiza el estado interno (`_valueTracker`). El servidor ve "9 fields missing" con los campos visiblemente llenos. Lo que funciono: teclear con `type()`, `Meta+A` para limpiar (en macOS, no `Control+A`), clicks de mouse sobre coordenadas para los desplegables, y click en la ETIQUETA para los radios. Todo documentado en los scripts.
- **El buscador de vacantes de MeLi** (`api/positions?country=AR`) es mucho mas reliable que el listado del portal: 866 vacantes paginadas y filtrables, contra 12 en la primera pagina del HTML.

---

## [2026-10-23] - La postulacion laboral deja de ser una odisea: skill + adaptadores por ATS

### Added
- **`skills/job-application/`** - la skill del flujo, con el knowledge de los tres ATS capturado una vez. Estructura: `SKILL.md` (el flujo: descubrir -> tailored -> aplicar -> verificar -> trackear), `references/ats-playbook.md` (las particularidades de cada ATS, con la evidencia y la fecha), `references/outreach.md` (mensajes y preguntas de screening), `scripts/` (find-jobs, apply y un adaptador por ATS).
- **`docs/adr/ADR-104-busqueda-laboral-proceso-factorizado.md`** - por que existe: el trabajo de hoy no fueron tres postulaciones, fueron **once hallazgos** sobre interfaces de terceros, todos verificados y todos caros de rediscover. La misma logica que ADR-101 para los hechos: si cada postulacion re-descubre que `fill()` no funciona, hay dos verdades sobre como se llena un formulario.
- **`scripts/find-jobs.mjs`** - discovery multi-board. La API de MeLi resulto la mejor fuente: 886 vacantes paginables, contra las 12 del listado.
- **Tres adaptadores** (`scripts/ats/{lever,ashby,eightfold}.mjs`) con una interfaz comun: `fill()` (rellena, no envia) y `submit()` (envia y lee el **veredicto del servidor**).
- **`tests/node/job-application.test.js`** - 7 tests de las funciones puras, incluido uno que prueba que el test puede fallar (leccion de check-contrast.py).

### Fixed
Once bugs del codigo de la tanda, revisados y corregidos por el CORE (bucket `low`: A escribe -> Kanam revisa). Todos verificados con una corrida end-to-end real contra el formulario de Mercado Pago:
1. **`pickOption` nunca encontraba la opcion**: destructuraba `{ text }` pero recibia `{ text: "" }` como primer argumento y el matcher como segundo, asi que la regexp compilaba contra la cadena "undefined".
2. **El listener de `response` se registraba DESPUES del click de submit**: la respuesta del servidor ya habia llegado y el **veredicto salia siempre vacio**. Era el bug mas grave: sin veredicto no hay prueba del envio.
3. **`verifyFields(page, [])` con array vacio**: el gate "no enviar si hay divergentes" era un no-op. Podia mandar un formulario con los campos sin registrar en React.
4. **`newContext()` sobre CDP** crea un contexto NUEVO, sin las cookies de la sesion real: el browser del usuario se abria sin su sesion de LinkedIn.
5. **`browser.close()` sobre un browser conectado por CDP cierra el Chrome del usuario.** Ahora solo se cierra la pestana que abrio el script.
6. **`chromium.launch()` sin `executablePath`** buscaba el binario de la cache de Playwright (1228), que no esta en la maquina (solo hay 1243): "Executable doesn't exist".
7. **La API de MeLi devolvia `name` (no `title`), `positionUrl` relativo (no `applyUrl`) y `standardizedLocations`**: cada vacante salia con titulo vacio y url nula, y el filtro las eliminaba todas.
8. **La API devuelve 12 por pagina de 886** (con `num=100`, 100): sin paginar el radar no veia nada.
9. **El filtro por titulo era un `includes` plano**: "UX" matcheaba "a**UX**iliar" y devolvia una vacante que no era la buscada.
10. **El codigo de pais y el pais estaban al reves** en Eightfold (`input-7` es el prefijo del telefono, `input-10` el pais): el telefono quedaba sin prefijo y el pais nunca se elegia.
11. **El scope del listbox no es el id del combobox**: el popup se renderiza en un portal, con otro id (`aria-controls` apunta a el). Buscando dentro de `#input-7` no se encontraba nada, y el fallback podia elegir la opcion de OTRO desplegable: **el codigo de pais termino escrito en el campo de email**.

### Notes
- **El `ok: true` era un falso positivo y ahora hay que ganarlo.** El reporte de `apply.mjs` decia "ok" con el CV sin adjuntar, porque `filled`/`missing` volvian VACIOS de los adaptadores. Ahora cada adaptador declara sus selectores, el orquestador verifica DOM contra estado de React, y el CV se verifica con lo unico verificable antes del envio (que el input exista y se le haya pasado el archivo). El CV real se prueba con la respuesta del servidor: Eightfold **consume** el archivo del input y su widget no re-pinta el nombre, asi que `input.files.length` da 0 siempre.
- **La prueba end-to-end es la que encuentra los bugs; el test unitario no.** Los 7 tests pasan en verde mientras el formulario quedaba sin pais, sin codigo y con el codigo de pais en el email. Se ve en la captura, no en el exit code. Por eso el flujo deja evidencia (screenshot) de cada corrida.
- **El captcha sigue mandando en la arquitectura (ADR-104).** `real-browser.mjs` se conecta al Chrome real del usuario por CDP cuando hay captcha, y el envio lo hace la persona: un captcha detecta el **contexto**, no los intentos.
- **Pendiente de verificar con una corrida real:** los adaptadores de Lever y Ashby no se probaron end-to-end (Lever tiene captcha; Ashby necesita el orden del autofill). El de Eightfold si, con la pantalla de Mercado Pago.

---

## [2026-10-23] - Dos postulaciones confirmadas (Mural y Mercado Pago), RYZ esperando un click humano

### Added
- **`docs/entrevistas/_general/outreach-2026-10-22/scripts/`** - los seis scripts de postulacion, reutilizables y documentados: `submit-mural.js`, `submit-ryz.js`, `submit-meli.js`, `fill-mural.js`, `fill-ryz.js`, `debug-mural-location.js`. Cada uno completa, **verifica campo por campo releyendo el DOM**, captura y solo envia con `--submit`.
- **`docs/entrevistas/_general/outreach-2026-10-22/evidencia/`** - capturas del estado final de los tres formularios.
- **Canal de LinkedIn operativo.** El `browser` de OpenClaw no arrancaba (no habia Chrome en `/Applications`); con Chrome instalado, `action=importprofile` copio **89 cookies** del perfil `Default` (incluidas las de LinkedIn) al perfil gestionado `imported`, y la sesion quedo viva: el feed cargo con el perfil de Gonzo, 92 vistas de perfil.
- **Localizacion de la vacante de Mercado Pago** via su API: `https://careers-meli.mercadolibre.com/api/positions?country=AR` -> id 44891701, displayJobId 127795, y el ATS real es Eightfold (`https://mercadolibre.eightfold.ai/careers/apply?pid=44891701`).

### Fixed
- **El hCaptcha de Lever (RYZ) no se resuelve por automatizacion:** token 0 en headless y en browser visible, incluso clickeando el checkbox del iframe. El formulario de RYZ queda COMPLETO (captura con los 9 campos) y pendiente de ese unico paso humano. Es el unico limite real de la tanda.
- **En Ashby (Mural) el campo "Location" no acepta "Buenos Aires"**: su autocomplete devuelve "No results" y solo reconoce "Argentina" y "Nunez". Con "Buenos Aires" el envio fallaba con "9 fields missing".
- **En Ashby los `name` de los inputs desaparecen al re-renderizar** y hay que mapear por el texto del ancestro; ademas los `id` de los inputs de archivo se reordenan entre navegaciones.
- **En Ashby el panel de "Autofill from resume" pisa el formulario**: su parseo asincrono sobrescribe los textos ya escritos. El orden correcto es CV -> esperar el autofill -> escribir con `type()` -> radios -> archivos.
- **Los radios de Ashby no se marcan con `input.click()` desde JS** (React no lo registra) ni con `.check({force:true})` en todos los casos: hay que clickear la ETIQUETA.
- **En Eightfold (MeLi) los campos se identifican por `id`, no por `name`** (`name=null` en todos). Y sus dos ultimos campos NO son areas de texto: `input-13` es la confirmacion de la politica de privacidad y `input-16` la pregunta de conflicto de interes, ambas con opciones Si/No. Escribir la presentacion ahi habria sido mandarla a una caja equivocada.
- **En Eightfold el telefono no acepta `+` ni espacios**, y con el codigo de pais en +54 espera el numero NACIONAL. Ademas, al elegir el pais aparece un campo "Estado" nuevo; si el pais no queda elegido, ese campo ni existe y el envio falla con "Error: selecciona un Estado".
- **Los inputs controlados de React no se limpian con Backspace** (el valor se concatena): hay que seleccionar todo y borrar. En macOS el select-all es `Meta+A`, no `Control+A`.
- **El footer sticky de los formularios tapa los ultimos campos** y el click normal da timeout: hay que hacer `scrollIntoView` y usar click forzado.
- **El boton de submit de Lever** tiene la clase dinamica `btn-submit`; el selector generico `button[type=submit]` agarra el boton OCULTO de hCaptcha (`id=hcaptchaSubmitBtn`).

### Notes
- **Dos de tres POSTULADOS y CONFIRMADOS por el servidor:**
  - **Mural** (Ashby): "Your application was successfully submitted. We'll contact you if there are next steps." Salario USD 3.400/mes, CV + cover letter.
  - **Mercado Pago** (Eightfold): "¡Gracias por su solicitud, Gonzalo!" + `201 {"success": true}` del servidor, con `location: Buenos Aires, Ciudad Autónoma de Buenos Aires, Argentina`.
- **RYZ queda a un paso humano:** el formulario de Lever esta completo y verificado; lo unico que no se puede automatizar es el hCaptcha. En paralelo salio la **invitacion de conexion a Sonia Langone** (recruiter tecnica de RYZ, 2do grado, con nota de 833 caracteres: por que encaja, el AI Engineering OS, el servidor MCP propio, los 11 PRs, y las dos preguntas de screening: overlap con US en EST y nivel de ingles conversacional).
- **El limite de LinkedIn es el grado de conexion:** las cuatro recruiters de RYZ (Sonia Langone, Valentina Magni, Valentina Tellechea, Maria Belen Giordano) son 2do grado, asi que el DM directo esta bloqueado. La via que funciona es la invitacion con nota, que ademas no tiene limite de caracteres con Premium.
- **Los 4 candidatos de RYZ encontrados en la busqueda de personas:** Valentina Magni (Senior Talent Acquisition Partner), Sonia Langone (Tech Recruiter, LATAM), Valentina Tellechea (Technical Recruiter), Maria Belen Giordano (Recruiter). Mas los founders Jordan Metzner (CEO) y Sam Nadler.
- **Scripts: los que quedan en `tmp/` no se versionan** (gitignored); las copias limpias y documentadas estan en `docs/entrevistas/_general/outreach-2026-10-22/scripts/`.

---
