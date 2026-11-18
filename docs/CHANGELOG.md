# CHANGELOG.md

Registro de cambios estructurales del workspace. Contiene las entradas de los **últimos 14 días** (corte: 2026-11-04). Lo anterior está archivado en [`./docs/archive/CHANGELOG-archive.md`](./docs/archive/CHANGELOG-archive.md). No incluye actividad diaria (ver `memory/`).

> **Política de rotación:** la mantiene `scripts/changelog-rotate.py` (pre-commit `--check` + cierre de sesión). Al superar la ventana, el bloque viejo se mueve al archivo. Reconstruir el activo desde cero cuando arrastre hipótesis refutadas.

---

## [2026-11-18]
- **ADR-114 (supersede ADR-042): pagos sin proveedor obligatorio.** `AGENTS.md` deja de fijar Stripe como único: cada proyecto elige proveedor (Stripe, Mercado Pago u otro) con criterio explícito y lo registra en su propio ADR. `memory/career-facts.md` actualizado.

## [2026-11-17] - Caso 09: el Quijote, y la tabla que era del siglo XX

### Added
- **`studies/narrative-engineering/caso-09-quijote.md`** — Parte I, capítulo I, completo (1.887 palabras), edición de 1905 en Wikisource. Cinco ejes, el primero medido en un texto anterior a 1830.
- **Perfil `cervantes` en `prose-metrics.py`**: mediana 41, bandas 0/3/15/82. Se auto-valida a ±0,4% sobre su propio texto.

### Notes
- **El hallazgo:** Cervantes no está un escalón arriba de García Márquez, está en otra física. **Cero frases de seis palabras o menos**, 82% de frases de más de treinta, párrafos de 156 palabras de mediana, 27 puntos y coma y 0% de diálogo con turnos. La tabla de perfiles del estudio era, sin saberlo, una tabla del siglo XX: antes, la unidad de respiración era el párrafo, no la frase.
- **Límite declarado:** 34 frases de muestra. La mediana es robusta; las bandas, gruesas. Con 34 frases, mover una cambia el porcentaje en tres puntos.
- **El "diálogo 0%" es artefacto de la puntuación:** hay discurso citado entre « », pero no turnos con raya; el script lo cuenta como narración y así queda dicho en el caso.
- El caso mide lo que el de Rowling no pudo: fuente entera, de dominio público, sin depender de comprar nada.

---

## [2026-11-17] - `modelos.md`: por qué hay un solo modelo y ocho casos

### Added
- **`studies/narrative-engineering/modelos.md`** — el índice que faltaba: por autor, cuántos casos, qué ejes están documentados, si la voz está medida y cuál es el artefacto ejecutable. Incluye la regla (un modelo exige dos obras; una obra es un caso), la inversión que el estudio tenía escondida y qué falta para cerrar cada modelo, con prioridad sugerida.

### Notes
- **La inversión:** el único archivo llamado `modelo` (Goyer) es el que no tiene voz medida, y los cinco autores con voz medida no tienen `modelo-*`. No es una falta: es que cada uno tiene un solo caso. Pero el nombre pesaba más que la evidencia, y el índice lo deja visible.
- **Prioridad propuesta:** el segundo caso de Rowling (*The Casual Vacancy*), porque es el único donde el segundo caso responde una pregunta abierta —cuánto de su voz es la serie y cuánto es ella— y ya existe un perfil medido contra el que comparar.
- `metodo.md` ahora distingue caso de modelo y apunta a `modelos.md`.

---

## [2026-11-17] - Los casos 01-03 del estudio, reescritos con el método vigente

### Changed
- **`caso-01-dark-city.md`, `caso-02-batman-begins.md`, `caso-03-mamma-mia.md` reescritos** con los cinco ejes, la misma estructura que los casos 04-08, la separación hecho/lectura y una sección de límites. Eran del 2026-10-01, tenían cuatro ejes y tres formatos distintos entre sí.
- **Eje 5 declarado no medible en los tres**, con el motivo: son guiones y libretos, no prosa; las cifras de `prose-metrics.py` describirían otro objeto. Se agrega lo que sí se puede decir por lectura, marcado como impresión.
- **`metodo.md` reescrito:** cinco ejes, la regla de separar hecho de lectura, cuándo no aplica el Eje 5, la plantilla de caso y la regla de densidad por escena.
- **`modelo-goyer.md`: límite corregido.** Se retiran "firma de autor" y "forma universal": los cuatro ejes son estructura —cualquier guionista competente los produce— y la confirmación era circular. Queda en pie el hallazgo central (heredar el mecanismo) y las reglas operativas.

### Notes
- **Las carpetas de `scripts/` no generan casos.** El único script es `prose-metrics.py`, que mide prosa y no redacta. Los casos son escritura, no salida de programa: lo que sí es reproducible es la medición del Eje 5.
- Lo que un guion puede aportar al estudio es estructura; la voz de un autor de guiones no se puede analizar hasta que haya prosa suya en edición estable.

---

## [2026-11-17] - Un flujo con nombre para pasar texto a voz

### Added
- **`skills/text-to-speech/SKILL.md`** — el flujo completo: voz vigente (es-AR-TomasNeural, -10% de ritmo, -2Hz), cómo se invoca, qué le hace al markdown, qué límites tiene y cuándo no usarlo.
- **`scripts/tts-render.py`** — toma un archivo markdown y devuelve un `.m4a`: saca encabezados y marcas, convierte la raya de diálogo en pausa, corta en párrafos enteros, renderiza por tramos con edge-tts y concatena con ffmpeg. Idempotente por hash: si el texto no cambió, no re-renderiza.
- **`docs/stories/las_tres_sabanas/audio/capitulo-1.m4a`** — el capítulo 1 leído entero con Tomás: 7:05, tres tramos.

### Notes
- **Por qué no el TTS del gateway:** el tool `tts` responde *"no provider registered; openai, xai, openrouter: not configured"*. Se resolvió con edge-tts en un venv dentro del workspace (`.venvs/tts`, gitignored) y voces neurales argentinas, que es lo que pedía el material. El primer intento con `say` de macOS sonó a robot y se descartó.
- **Decisión de archivo:** el audio no se versiona. Se versiona el texto y el comando; el `.m4a` se regenera. Los audios viven en `<carpeta>/audio/` con un `.json` al lado que guarda voz, ritmo y hash del texto.
- **Cambiar de voz en el futuro es un flag**, no una migración: `--voice`, `--rate`, `--pitch`, o los tres defaults en el script.
- **Ritmo ajustado a -4%** (era -10%) por pedido de Gonzo: el capítulo 1 pasó de 7:05 a 6:38. El script ahora también re-renderiza si cambia el ritmo, no solo si cambia el texto.
- **`scripts/tts-dramatize.py`**: una voz por personaje, turno por turno, repartiendo por atribución y alternando cuando no hay. Prueba sobre la escena de la cocina del capítulo 14: 26 turnos, tres voces, 1:19. La ironía sigue sin resolverse: eso no es del reparto, es del proveedor.
- **La atribución ya no la dice el personaje.** "— No —dijo ella—. Se lo digo ahora." se parte en tres: Vera dice "No", el narrador dice "dijo ella", Vera dice "Se lo digo ahora". Antes la frase entera salía con la voz del personaje, que es como leer un guion con los ojos cerrados.
- **Voz profunda adoptada (2026-11-17):** Chatterbox con `--deep` — dos semitonos abajo moviendo formantes, 3 dB en 180 Hz, −1,5 dB en 3,2 kHz. Gonzo eligió ese ajuste sobre el de tres semitonos: la voz base del motor le resultaba juvenil. Queda como perfil del pipeline (`scripts/tts-chatterbox.py --deep`).
- **Motor local instalado (2026-11-17):** Chatterbox multilingual en `.venvs/chatterbox` (Python 3.12, torch 2.6, MPS). Español andando: 4,6 s de audio en 29 s de proceso, o sea 6,3 veces más lento que el tiempo real. La emoción se controla con `exaggeration`; el watermarker neural de Perth no importa en este entorno y se reemplaza por el dummy (el watermark es de procedencia, no de calidad).

---

## [2026-11-17] - Las Tres Sabanas: el sistema funcionando

### Added
- **Capítulo 4, primera escena: el tanque.** Una semana antes de la reunión, la casa se queda sin agua, el plomero no viene, y los tres la arreglan: Néstor arriba con la bomba, Adán abajo con la escalera, Vera al costado con la linterna. Funciona. Después se sientan con una cerveza y durante veinte minutos no hablan de la casa. Es lo que el Acto I no tenía: una escena donde el sistema hace lo que el sistema sabe hacer, para que después se pueda perder. La POV es Vera, y el pensamiento es de dos líneas: *"Esto. Esto es lo que se va a vender."*
- **El auto de la casa** queda establecido ahí (un gris viejo en el fondo del terreno, de los tres), que es el que Adán maneja en el Acto III.

### Notes
- **Acto I: 9.884 palabras** (era 9.163). Perfil: mediana 9,0 y bandas 33,9/44,9/19,0/2,2, las cuatro dentro.
- **Libro: 26.854 palabras.** Los tres actos quedan parejos: 9.884, 7.103 y 9.867.
- El capítulo 4 pasa de 1.600 a 2.515 palabras y de una escena a dos.
- **Pasada de lectura en voz alta:** se arreglaron las tres frases que no se pueden decir de corrido. La de Adán en el capítulo 3 ("yo estuve treinta años en esta casa...") ahora respira con comas; en el 7 se agregó una coma en la descripción de la planilla; y en el 15 se partió en dos la frase de Vera mirando a Adán, que tenía treinta y tres palabras sin pausa.

---

## [2026-11-17] - Las Tres Sabanas: el Acto I arranca

### Changed
- **Capítulo 2, de tres viñetas a dos.** Se cortó la de Néstor (650 palabras): era la tercera versión del mismo silencio, después del capítulo 1 y antes de la carta del 3. Quedan la espalda de Adán y la llamada que Vera no hizo, que son las dos que pagan más adelante. El capítulo pasa de 1.942 a 1.305 palabras y abre con "La espalda le avisó el lunes".
- **Lo que traía la viñeta cortada se movió al capítulo 3:** la llamada de la madre ("vos siempre estás viendo") cae entre el escribano y la cara de Adán, y la planilla con la línea del banco queda plantada cinco capítulos antes de que aparezca el préstamo.

### Notes
- **Acto I: 9.163 palabras** (era 9.689). Perfil: mediana 9,0 y bandas 33,5/46,3/18,0/2,2, las cuatro dentro.
- **Libro: 26.133 palabras.** Mediana 9, bandas 36,3/43,1/18,5/2,2. Cero frases repetidas.
- Se resuelve el último defecto de relato que la lectura de corrido había dejado abierto.

---

## [2026-11-17] - Las Tres Sabanas: borrador 2, de los siete datos a las ocho decisiones

### Changed
- **El plazo de doce días ahora dispara.** En el capítulo 6 el escribano llama a Néstor: el inventario quedó firme, el expediente pasa a venta, la tasación de Vera sirve para fijar el precio y cualquiera de los tres puede traer un comprador. El reloj del Acto I enciende el Acto II, y esa última frase es la que después habilita a Basterra.
- **Vera trae a Basterra.** En el capítulo 10 le pregunta a la inmobiliaria si hay quién compre para demoler y le dan el nombre. No lo dice. En el 13 vuelve el "es lo mismo" y en el 15 se entera de que el hombre con el que Adán firmó es el que ella trajo. Deja de tener razón en todo.
- **Néstor ya no dice su tesis.** La frase "lo único que me toca es juntarlos" pasa a la boca de Adán, como acusación.
- **Adán es empleado municipal desde hace treinta y un años.** Explica las llamadas y las firmas, lo ata al pueblo y hace el final más duro: conserva el sueldo y pierde la casa.
- **El socio** pasa a ser el chico que le da una mano. **Los cuatro y medio de Vera** pasan a ser "para la seña del departamento".

### Fixed
- **La densidad de pensamiento no era un defecto del libro sino de la plantilla.** Medida por escena, la voz `casa` va de 0,59 en diálogo a 1,77 en una escena sola; el 0,65 de promedio era el resultado de promediar escenas que hacen cosas distintas. `PLANTILLA-voz-casa.md` §4 ahora registra la distribución y la regla: se sube cuando una escena pide cabeza, no para llegar a un número. Se agregaron tres pensamientos en el capítulo 16.

### Notes
- **26.659 palabras** (9.689 + 7.103 + 9.867), +497 sobre el borrador 1. Los tres actos dentro de perfil: I 9,0 · 34,6/45,3/18,1/2,0 · II 8,0 · 38,5/39,3/19,5/2,7 · III 8,0 · 38,0/42,1/18,2/1,8. Libro: mediana 9, bandas 36,6/42,8/18,5/2,1.
- Cero frases repetidas, cero punto y coma, cero adverbios en `-mente`.
- **Queda un solo defecto de relato:** el Acto I todavía tarda en arrancar, porque las escenas 2 y 3 siguen demasiado cerca la una de la otra.

---

## [2026-11-17] - Las Tres Sabanas: la lectura de corrido destapó siete cosas

### Fixed
- **La casa estaba en dos calles.** Acto I: calle Salta. Acto III: Sarmiento al 400, en cuatro lugares. Unificado en Salta; la pieza que alquila Adán pasó a calle Urquiza para no quedar en la calle de la casa demolida.
- **Adán tenía dos apellidos.** Vergara en el Acto I, Quiroga en el capítulo 12. Corregido: Vergara (Adán), Quiroga (Néstor), Salas (Vera), cada uno de su rama.
- **La sábana que se rompe no estaba donde decía.** Vera se lleva la de Adán en el capítulo 1 y la sábana reaparece colgada en el 5 y en el 7 sin que nadie la devuelva. Ahora el 5 la muestra ausente, el 7 registra la devolución de agosto, y el 14 y el 16 dejan claro que es la sábana de Adán, no "de Elvira". También se corrigió que se rompía "en mis manos" cuando la rompe Vera.
- **La cuenta del dinero no cerraba.** El capítulo 13 repartía trece y cuarto "para dos" sin que la aritmética lo sostuviera. Ahora los tres actos cuentan lo mismo: cuarenta y dos de tasación, doce de deuda, doce y ocho por cabeza, ochocientos mil para Néstor. La renuncia deja de ser un gesto y pasa a ser un cálculo mal hecho.
- **La escritura se firmaba una semana después del boleto.** El capítulo 16 pasa a "el nueve de enero".
- **Dos frases repetidas en todo el libro** (capítulos 1/6 y 3/10). Barrido final: cero.
- **Vera fumaba y no fumaba** entre el capítulo 2 y el 15.

### Added
- **`docs/stories/las_tres_sabanas/EVALUACION-contenido-3-actos.md`** — la primera lectura del manuscrito como relato, con los siete errores corregidos, las cinco cosas que quedan abiertas (el plazo de doce días que nunca vence, el socio que desaparece, el oficio de Adán, la seña del departamento, el pensamiento del POV a la mitad del perfil) y los tres defectos de relato que no se tocan sin decidir antes.

### Notes
- **Regla que faltaba:** compilar un acto no es haberlo leído. La medición verifica la voz; no ve que un personaje firme una seña con plata que consigue un día después, ni que una sábana esté en dos casas. Las siete correcciones salieron de leer, no de medir.
- **Los tres actos siguen dentro de perfil** después de las correcciones: I 9,0 · 34,9/45,3/17,8/2,1 · II 8,0 · 38,4/39,0/19,8/2,8 · III 8,0 · 38,4/41,4/18,4/1,8. Libro completo: 26.162 palabras, mediana 9, bandas 36,9/42,4/18,5/2,1.

---

## [2026-11-17] - Las Tres Sabanas: el primer borrador completo

### Added
- **Acto III escrito y compilado** (`docs/stories/las_tres_sabanas/manuscript/acto_3.md`): capítulos 12 a 17, 9.664 palabras. Con el Acto I (9.430) y el II (6.968) la novela queda en **26.062 palabras** y las 17 escenas del outline están escritas.
- **Capítulos sueltos** `capitulo_12.md` a `capitulo_17.md`, uno por escena, con POV declarado: 12 Adán, 13 Vera, 14 los tres, 15 Adán, 16 Vera, 17 Néstor.

### Changed
- **README del proyecto**: secciones faltantes del Acto I y del Acto III, con tablas de escena/POV/palabras, y el estado actualizado a "primer borrador completo".
- **Acto I**: 9.430 palabras, mediana 9,0 exacta. Compilado y corregido en el commit anterior del mismo día (`318a35c4dc`).

### Notes
- **Perfil `casa` en los tres actos**: I 9,0 · 34,9/45,1/17,9/2,0 · II 8,0 · 38,5/39,5/19,2/2,8 · III 8,0 · 38,5/41,8/17,9/1,8. Las cuatro bandas dentro de tolerancia en los tres.
- **Diálogo en alza por acto**: 53% de párrafos en el I, 66% en el II, 63% en el III. Se acepta y se documenta: del 12 al 15 la novela es una serie de conversaciones donde nadie puede moverse sin romper algo.
- **La deuda oculta** (préstamo de 12 millones con garantía sobre el tercio de Néstor, con vencimiento anticipado disparado el mismo día de la renuncia) es el hueco sobre el que se sostiene el acto. Sin villano: el banco cumple su contrato.
- Cero punto y coma, cero adverbios en `-mente`, cero frases repetidas dentro del acto y cero repetidas contra los actos anteriores.

---

## [2026-11-17] - La skill del vault quedó con dos cuerpos y nada lo dijo

### Fixed
- **`memory-wiki-vault` tenía el cuerpo nuevo Y el viejo pegados: 87 líneas, dos `## Decision rules` y dos `## Related`.** El rewrite automático del skill review insertó el procedimiento nuevo arriba y dejó el viejo abajo, sin cerrar. Un agente que la leyera recibía dos procedimientos contradictorios a la vez: uno con el repo como default y otro que mandaba a habilitar el plugin y ingestar. Quedó en 49 líneas, un solo cuerpo.
- **Referencia muerta en `Related`.** Decía `memory-wiki-workflow` "en el workspace"; esa skill vive en `agents/kanam-mind/skills/` desde la reorganización por rol. Ahora el path es explícito y avisa que si la skill da el vault por activo sigue siendo deuda.
- **La regla del paso 9 estaba al revés.** Decía "dejar la deuda visible como claim" sin distinguir el caso del valor duplicado, que es exactamente el que el 2026-11-17 demostró al revés: alinear tres claves las mantiene vivas y el siguiente `set` las vuelve a desincronizar. Ahora separa **contradicción** (decisión pendiente, se reporta al owner) de **duplicado** (defecto, se retira la copia). Misma distinción agregada a `Decision rules`.
- **`agents/kanam-mind/skills/memory-wiki-workflow`** alineada: el vault pasa a ser fallback documentado y el camino default apunta a `docs/claims/`. La descripción dejó de prometer el plugin como capa analítica vigente.

### Added
- **`scripts/check-skill-integrity.py`** — el gate que habría cazado esto. Verifica frontmatter único y cerrado, `name:` igual al directorio, `description:` presente, y **headings de nivel 2 duplicados** (la firma de dos cuerpos pegados). Ignora `.archive/`, donde cada versión vive en una carpeta con timestamp y comparar `name:` contra el directorio es ruido puro (425 falsos positivos el primer intento). Cableado al pre-commit como **aviso, no bloqueo**: una skill es documentación, y un gate que bloquea por prosa enseña `--no-verify`. Verificado en negativo con dos sondas (cuerpo duplicado y frontmatter sin `name:`) — las dos fallaron con el número de línea.

### Notes
- 87 skills revisadas en los árboles de agente: 0 findings, 0 warnings tras el arreglo.
- El gate anterior (`check-claims.py`) no podía ver este defecto: valida datos, no la integridad del documento que los prescribe.

---

## [2026-11-17] - Una sola clave para la asignacion de modelos

### Removed
- **`settings.model_triple` y `settings.model.triple` borradas de la DB.** Eran copias de `model_by_agent`: ningún bloque managed ni script las lee. Alinearlas (2026-11-16) dejaba el duplicado vivo; un dato, un dueño. Queda solo `model_by_agent`, la clave que lee el bloque `model-operativo` de `AGENTS.md`. La DB pasó de 12 a 10 claves; los seis bloques siguen rindiendo sin drift.

### Changed
- **`managed-blocks.py set` escribe UNA sola clave.** Antes replicaba el valor en cada alias "para que ninguna quedara vieja", y eso era seguir manteniendo el duplicado: el gate de alias fallaba justo por la red de seguridad. Ahora acepta un alias como *nombre de entrada* (lo resuelve al canónico y avisa) pero nunca lo usa como destino.
- **`managed-blocks.py retire-aliases [--force]`** — borra las copias y **se frena si un alias difiere del canónico**: un valor distinto es una decisión que alguien perdió, no basura. Dry-run por default.
- **`seed` nunca crea un alias.** Una clave que ningún bloque lee no es un default: `DEFAULTS` no la define, así que `seed` no puede reintroducirla.

### Fixed
- **`check-settings-aliases.py` invierte su regla.** Antes exigía que las tres claves coincidieran; ahora exige que **no exista** ninguna copia, nombra la que reaparezca y dice si difiere. También compara el `ALIASES` del gate contra el de `managed-blocks.py` y avisa si se desincronizan, en vez de confiar en una de las dos listas.
- **ADR-090 §1 actualizado en el lugar** (sin ADR nuevo, mismo criterio que la corrección del 2026-11-04): se documenta la decisión, el mecanismo y la verificación en negativo. La advertencia sobre las tres claves queda como historia resuelta, no como riesgo abierto.

### Notes
- Verificado en negativo: sembrar un `model.triple` a mano hace fallar el gate con el nombre y el valor; `retire-aliases` lo limpia; un `set` posterior deja la DB en 10 claves y el gate en verde. Backup de la DB tomado antes de borrar.
- Los claims pasan a 25: `workspace.model-keys-aligned` ahora afirma la ausencia de copias y `workspace.settings-write-path-is-single` cubre el mecanismo.

---

## [2026-11-17] - Caesar III Clone (caravana con carga real)

### Fixed
- La caravana **carga en el almacén** y entrega en el puesto comercial; la venta se contabiliza recién al llegar.
- `TradeSystem.month` ya no vende por teletransporte: solo informa si la ruta está abierta.
- Un viaje abortado devuelve la carga al almacén.
- `home_tile` del puesto ya no se usa como waypoint (causaba la muerte de la caravana al salir).

### Added
- `sim/walkers/caravan_market.gd` (selección de almacén/puesto, entrega y venta).
- `tests/test_caravan_cargo.gd`; gate **40 tests**.

### Verified
- Gate EXIT 0: 40 tests + smoke + pureza.
- `./scripts/demo.sh` EXIT 0.

---

## [2026-11-17] - Caesar III Clone (rutas e importaciones)

### Added
- Panel `F6` de rutas: exportar cerámica/muebles, importar vino/aceite.
- La caravana vuelve con la importación y el warehouse la recibe.
- `sim.trade_route_open`, `export_good` e `import_good` persistidos en save/load.

### Verified
- Gate **40 tests** + pureza; `Caravan cargo test passed`.

---

## [2026-11-17] - Caesar III Clone (auditorías profundas)

### Added
- `test_deep_integration`: 2 seeds, 10 casas, walkers, save/load con hash y continuación.
- `test_fuzz_placement`: 80 operaciones deterministas de placement/removal.
- `test_asset_integrity`: manifests base/Blender, 27 edificios, 96 frames, 9 terrain y 23 iconos.

### Verified
- Gate **39 tests** + smoke + pureza.
- `resume.mjs caesar3-clone` reconstruye HANDOFF/DB sin el transcript.
- Stress 7,83 ms/tick (2k walkers).

---

## [2026-11-16] - La capa de claims sale del vault y entra al repo

### Added
- **`docs/claims/`** — la idea de `memory-wiki` (ADR-064) sin el plugin: un claim es un hecho con `id`, `status`, `confidence`, `updatedAt` y `evidence[]` que apunta a un artefacto real (una clave de `settings`, un archivo, un bloque managed, un ADR). Tres archivos de arranque: `models.md` (10 claims, todos los roles de ADR-090 + thinking), `pipeline.md` (6 claims: A, B, C, pre-filtro, el principio de asimetría y el gate), `workspace.md` (7 claims: fuente de verdad, frontera de roles, una máquina, el formato, el estado del vault y la deuda de `model.triple`).
- **`scripts/check-claims.py`** — el gate. Resuelve la evidencia contra disco y DB, valida vigencia de `updatedAt`, umbrales de confianza, `contested` sin decidir y contradicciones entre claims del mismo tema y sujeto. `--negative` siembra un claim roto, verifica que **cada** detector dispare, lo borra y confirma que vuelve a cero; sin eso un detector ausente y uno limpio se ven iguales.

### Removed
- **`memory-wiki` desactivado como capa analítica del workspace.** No fue un fallo del plugin: al retirarlo el vault tenía 86 fuentes ingestadas, **una** entity con 4 claims, y todos los reports en cero. Los detectores se verificaron en negativo otra vez el 2026-11-16 (sonda sembrada, cada report nombró su defecto, se limpió sola) — funcionaban, lo que faltaba era sustrato. Escribir un claim a mano era el paso caro, y nadie lo paga para un vault que vive fuera de git (`~/.openclaw/wiki/main`, 716K, sin versionado). El vault queda en disco como archivo histórico; no se borró nada.

### Fixed
- **`settings.model.triple` alineada: doce dias de drift entre tres claves que son el mismo dato.** `model_by_agent` y `model_triple` decían `main/defaults deepseek-v4.1-flash:cloud` (ADR-107) mientras `model.triple` conservaba `main/defaults minimax-m3.1-flash:cloud`, el valor superseded. ADR-090 lo documenta como trampa recurrente ("corregir solo las conocidas deja una copia viva del valor viejo"); pasó dos veces el 2026-11-04 y volvió a quedar así. Corregido en el lugar, con backup previo de la DB.
- **`scripts/check-settings-aliases.py`** — el gate que hace visible esa copia. Declara el grupo de alias (`model_by_agent` = `model_triple` = `model.triple`), reporta qué clave derivó y con qué valor, y `--fix` copia el canónico (`model_by_agent`, la clave que lee el bloque de `AGENTS.md`). También lista claves de modelo huérfanas: ninguna hoy. Verificado en negativo sembrando el drift a propósito y confirmando que falla, y limpiándolo con `--fix`. Cableado al pre-commit sin condición, porque la DB no se versiona y ningún pathspec vería el cambio.

### Notes
- **Deuda detectada, no corregida:** el esquema de `settings` conserva la misma definición bajo tres claves (`model_by_agent`, `model_triple`, `model.triple`). Hoy las tres coinciden y el gate las vigila, pero la copia sigue existiendo: borrar dos claves y dejar solo `model_by_agent` toca el esquema y los bloques que las referencian, así que queda como decisión aparte. Los claims `workspace.model-triple-key-was-stale` (retracted) y `workspace.model-keys-aligned` (activo) registran el antes y el después.

### Fixed
- **`scripts/check-refs.py` bloqueaba commits por una ruta declarada propuesta.** `docs/pipeline/roadmap-ingresos-a11y-2026-11.md:146` dice "Script propuesto `scripts/watch-devto-trends.sh` (a crear)" y el gate lo leía como ruta rota, así que cualquier commit fallaba por un archivo de otra sesión. Ahora una ruta cuya misma línea o la anterior la declara `propuesto`, `a crear`, `planned` o equivalente queda fuera de la verificación, con match por palabra completa y ventana de dos líneas: no es una promesa de que el archivo existe, es un plan. Verificado en las dos direcciones (propuesto no reporta, ruta muerta sin declaración sigue fallando) y el corpus real quedó en 742 rutas citadas, todas existentes.

---

## [2026-11-16] - Cata extendida a nueve modelos

### Added
- **`bench/cata-2026-11-16-extended/`** — segunda corrida del fixture con cuatro candidatos más (`minimax-m3.1-flash`, `glm-5.3-flash`, `gemma4:12b-mlx` local, `gemma4:cloud`): 54 celdas, `REPORT.md` con diez secciones. Resultado: `glm-5.3-flash` es el más barato (122 eval promedio, 1.1 s) y empata en contenido; `gemma4:12b-mlx` falla T3 en las dos tandas (135.74); `gemma4:cloud` entrega lo mismo con 5x menos tokens al apagar el razonamiento; `minimax` ignora `think:false`.

### Fixed
- **Assert T3 del fixture** — el regex exigía la redacción de la referencia (`fila 4`, `fila 7`) y rechazaba equivalentes correctas (`id 4`, `fuera del rango`). Corregido, re-validado en las dos direcciones y las celdas re-evaluadas desde el `content` guardado, sin re-correr la cata.

### Changed
- **`skills/model-comparison-cata/SKILL.md`** — tres reglas nuevas: 4-bis (corregir un assert se paga re-evaluando desde el `content` guardado, no re-corriendo), 5-bis (una tanda `off` con `thinking` no vacío no es evidencia de nada), y la auditoría obligatoria del ciego: ninguna frase se acredita sin abrir el archivo citado, y ninguna se descarta sin abrirlo — el padre descartó con un grep mal hecho un hallazgo real.

---

## [2026-11-16] - Kit reproducible de catas de modelos

### Added
- **`skills/model-comparison-cata/`** — la metodología de la cata 2026-11-16 hecha reusable: fixture con suite oculta validada en las dos direcciones, tandas `low` y razonamiento apagado, evaluador ciego de CONTENT vs CLEANLINESS, y `REPORT.md` de nueve secciones. Incluye plantillas (`tasks.json`, `evaluate.py` con suite de ejemplo funcionando, referencia, defectuosa, brief del evaluador ciego).
- **`scripts/cata-kit.py`** — CLI `init` / `check` / `run` / `analyze`. El runner trae lo que costó caro: nonce anti-caché por celda, auto-escalado de `num_predict` con content vacío, nombres de artefacto seguros y warm-up separado.
- **`SKILLS-INDEX.md`** — alta en la sección Core (34 → 35).

### Changed
- **`harness-model-comparison`** (skill aprendida) — el "qué/cómo se mide" queda ahí como doctrina; el kit ejecutable vive en el workspace y se referencia desde `Related`.

---

## [2026-11-16] - Nueva categoría `docs/propuestas/`

### Added
- **`docs/propuestas/reservas-avion-compartido/brief-socios.md`** — brief de una página para que los dos socios de una aeronave compartida aprueben un sistema de reservas. `docs/` no tenía categoría para propuestas a clientes (las existentes son linkedin, entrevistas, prs, pipeline, feedback); esta es la primera pieza.

---

## [2026-11-12] - Tests negativos en tres gates que no los tenían

### Added
- **`tests/python/test_check_single_source.py`** — 7 tests. El gate corre en cada commit y no tenía ni uno: si dejara de detectar una segunda copia, nada lo diría. Cubre duplicado detectado, líneas distintas, título repetido (ALLOW), línea corta, tag de modelo a mano, tag dentro de MANAGED, y `exit 3` sin archivos normativos.
- **`tests/python/test_check_skill_overlap.py`** — 9 tests: pares, vectores vacíos, equivalencia con `cosine()` legacy, truncado de `text_key` igual que `embed()`, caché de otro modelo descartado, y `exit 3` sin catálogo.
- **`tests/python/test_check_handoff_merge.py`** — 5 tests: pendiente perdido falla, declarado en CERRADOS pasa, `--closed` pasa, HANDOFF que agrega no falla, sin archivos no es verde.

### Changed
- **`scripts/gate-base-rate.py`** — el detector de tests no encontraba `test_check_single_source.py` (buscaba `test_single_source`) ni contaba los `returncode == 3` como caso negativo. Corregido: **de 11/18 a 14/18 gates con al menos un test negativo**.

### Gotcha encontrado escribiendo los tests
`check-handoff-merge.py` matchea el título de sección por substring ya lowercased: **"Próximos pasos" con tilde no contiene `"proximo"`**, así que la sección se saltea en silencio. Un HANDOFF con títulos acentuados puede quedar fuera del chequeo de pendientes. Documentado en el docstring del test; el gate no se tocó (arreglarlo es otro trabajo).

### Status
14 de 18 gates con test negativo. Quedan cuatro: `agent-skill-boundary`, `design-tokens`, `learnings-integrity`, `roadmaps`.

---

## [2026-11-12] - skill-overlap: de 9,65 s a 1,49 s

### Changed
- **`scripts/check-skill-overlap.py`** — dos arreglos, ninguno cambia el resultado:
  - **Caché de embeddings** en `.git/skill-overlap-cache.json` (no se commitea), clave `sha256(nombre + descripción[:500])` — exactamente el texto que `embed()` embebe. Con caché caliente: **0 llamadas a Ollama** contra 176.
  - **Normas calculadas una vez por vector**, no por par. La versión anterior recalculaba la norma de cada vector en cada uno de los 15.400 pares (176 skills): 47,4 M de `sum()` y 2,5 s de los 3,5 s.
  - **`--no-cache`** para forzar el re-embed, **`SKILL_OVERLAP_STATS=1`** para ver embebidos/reusados.
- **Salida idéntica**, verificada con `diff` contra la versión de `HEAD`.

### Added
- **`exit 3`** cuando el catálogo no carga o tiene <2 skills: antes devolvía `0` y el pre-commit no distinguía "el runtime no respondió" de "no hay solapamiento".
- **`tests/python/test_check_skill_overlap.py`** — 9 tests: pares, vectores vacíos, equivalencia con `cosine()` legacy, `text_key` truncada igual que `embed()`, caché de otro modelo, y los dos casos de `no corrible`.

### Why
**Medido:** de los 10,44 s del pre-commit, 9,65 s eran este check. Ahora el pre-commit entero tarda **2,26 s**. Un gate que se paga en cada commit y tarda 10 s se apaga en dos semanas; éste ya no.

### Status
10 de 25 gates con `exit 3`; pre-commit de 10,44 s a 2,26 s.

---

## [2026-11-12] - Honestidad de los gates: exit 3 y tests negativos

### Added
- **`scripts/check-gate-honesty.py`** — verifica que cada `check-*.py` (a) declare `exit 3` ("no se pudo correr"), (b) resuelva la raíz sin depender del `cwd`, (c) reporte un veredicto legible. Sale 1 si hay violaciones. Medido hoy: **21 de 25 sin `exit 3`**.
- **`scripts/gate-base-rate.py`** — mide cuántos gates del pre-commit tienen al menos un test con caso negativo. Hoy **11 de 18**. No es bloqueante y lo declara: su fórmula no convierte "cuántos casos" en una sensibilidad calibrada.
- **`tests/python/test_check_gate_honesty.py`** — 6 tests.
- **`docs/learnings/GATES-Y-TASA-BASE.md`** — el cruce Módulo 1 / Módulo 3 / Módulo 5 con el sustrato de verificación.

### Changed
- **`scripts/check-bootstrap-budget.py`** — si ningún archivo de bootstrap existe, devuelve `3` en vez de `0`.
- **`scripts/check-single-source.py`** — si no hay archivos normativos, devuelve `3`.

### Why
`skills/verification-gates` fija desde 2026-09-28 que «cero casos corridos no es verde», y ningún gate la aplicaba a los gates. Un check que no encuentra su archivo de entrada devuelve `0` con un "OK": verde sin haber mirado. Es la misma forma que el curso enseñó tres veces (heurística no admisible, tasa base, overfitting): **una medición que no puede fallar no mide nada**.

### Status
21 de 25 gates sin `exit 3`; 7 de 18 sin test negativo; `check-skill-overlap` se lleva 9,65 s de los 10,44 s del pre-commit. Deuda medida, no prometida.

---

## [2026-11-12] - Gate de citas de las clases de studies/

### Added
- **`scripts/check-study-citations.py`** — gate promovido desde `studies/cs50-ai-python/heldout.py` tras siete usos reales en un día (los siete módulos del curso CS50 AI). Verifica que cada cita `"texto" (h:mm:ss)` de una clase exista literalmente en su `transcripcion.md` y que el timestamp sea el del bloque que la contiene. Modos: archivo+d transcript, directorio de clase, `--all`, `--fix`. Códigos 0/1/3 según `verification-gates`: un archivo que no puede verificar NO es verde.
- **Pre-commit**: bloque propio con disparador en `studies/<slug>/*.md`; verifica sólo los archivos staged con `transcripcion.md` al lado.
- **`tests/python/test_check_study_citations.py`** — 8 tests que cubren cita correcta, paráfrasis, timestamp corrido, cita que cruza bloques, `--fix`, y los dos casos de `no corrible`.

### Changed
- **`studies/ai-engineer-full-course/outline.md`** — 41 timestamps corridos ~14 s, corregidos con `--fix`.
- **`studies/sql-full-course/outline.md`** — 3 timestamps corregidos; una cita con puntos suspensivos reemplazada por el literal del transcript.
- **`studies/n8n-ai-automations/outline.md`** — 13 citas que eran paráfrasis con comillas reemplazadas por literales del transcript (el ASR transcribe "n8n" como "NAT" y "NAN").
- **`studies/cs50-ai-python/ADOPCION.md`** — la promoción documentada con los tres bugs que el gate encontró al generalizarse.

### Why
El gate existía como script de una sola clase. Siete usos reales en un día (101 citas, tres fallos distintos) cumplieron la condición que `ADOPCION.md` había fijado: sobrevivió a un uso real, repetido y con fallos distintos. Al generalizarlo se rompió en tres formas que el script original no veía; los tests las cubren.

### Status
`--all`: 37 archivos, 407 citas, 407 verificadas, 0 fallidas, 22 no corribles. Próximo: las 22 clases sin citas con timestamp son la lista de trabajo del gate, no un agujero.

---

## [2026-11-11] - Reinos de la Frontera (proyecto nuevo)

### Added
- **`projects/reinos-de-la-frontera/`** — RTS medieval isométrico para un jugador contra IA, desde cero, en Godot 4.7.2 sobre macOS Apple Silicon. Repo propio, branch `main`, sin remoto (uso 100 % personal). Fase 0 cerrada: estructura §5.3, `project.godot` válido para Godot 4, `main.tscn` con cámara ortográfica real (`projection=1`, size 14, pitch −30/yaw 45), cubo de 1 m y cápsula de 1,8 m como referencias de escala, 21 stubs sin lógica, tests `scaffold_test.gd` y `headless_test.gd`, captura 1600×900 en `docs/captures/fase0.png`.
- **Programa del Planner** `reinos-de-la-frontera` (24 pasos, E0–E6) en `agents/kanam-planner/.knowledge/programs/`.
- **Documento de arranque** en `docs/reinos-de-la-frontera-documento-de-arranque.md`.

### Why
El proyecto se juega en el spike gráfico, no en el arte: primero hay que demostrar 200 unidades a 60 fps con cámara ortográfica en la M4, y recién después construir simulación. Fase 0 deja el repo abriendo y el riesgo identificado.

### Status
Fase 0 cerrada. Próximo: E0 Día 1 (importar Quaternius, validar escala, captura).

---

## [2026-11-11] - Caesar III Clone (capa de sprites)

### Added
- **`tools/gen_sprites.py`** — generador determinista (Pillow + geometría isométrica) de 13 edificios (5 niveles de casa + well/fountain/farm/granary/market/temple/prefect/engineer), 20 walkers (5 tipos × 4 direcciones) y árbol/roca. Sin assets de Caesar III ni de terceros.
- **`assets/sprites/`** — 35 PNG + `manifest.json` con archivo, ancla y tamaño; README con el contrato de ancla y regeneración.
- **`view/sprite_theme.gd`** — carga y cachea el catálogo; `CityView` dibuja sprites cuando existen y cae a las primitivas si falta una entrada, ordenando edificios/walkers/props por la casilla frontal (`x+y`).
- **`tests/test_sprite_theme.gd`** — valida las 13+20+2 entradas, texturas, anclas/tamaños y fallback de tipos desconocidos; gate actualizado a 24 tests.

### Why
El MVP ya era legible con primitivas, pero los bloques no comunicaban la ciudad. La capa de sprites demuestra el contrato `VisualTheme` sin tocar `sim/`: arte propio, reemplazable, con anclas verificables y fallback.

### Verified
- `python3 tools/gen_sprites.py` dos veces → `shasum` idéntico (determinista).
- `bash scripts/gate.sh` → EXIT 0: smoke + main input + 24 tests + pureza, sin leaks.
- `./scripts/demo.sh` → EXIT 0; captura 1600×900 `tmp/shot-sprites-final.png`.

### Status
Capa de sprites prototipo: estática, 4 direcciones, sin animación; agua/caminos/terreno siguen primitivos. Próximo: texturas de terreno/agua, animación y UI.

---

## [2026-11-11] - Caesar III Clone (terreno, animación y UI)

### Added
- **`tools/gen_sprites.py`** — completa el set: 3 variantes de pasto, camino de piedra, 3 frames de agua, 40 frames de walker (5 tipos × 4 direcciones × 2 zancadas) y 5 skins de UI. Sigue sin assets de Caesar III ni de terceros.
- **`view/sprite_theme.gd`** — APIs `grass(variant)`, `road()`, `water(frame)` y `walker(type, dir, frame)`; todo cacheado desde el manifiesto.
- **`view/city_view.gd`** — terreno por tile con textura, agua animada, camino texturado y zancada de walker por tiempo/fase; fallback a color plano y líneas.
- **`main.gd`** — `StyleBoxTexture` 9-patch para panel y estados normal/hover/pressed/disabled de los botones; fallback a `StyleBoxFlat`.
- **`tests/test_sprite_theme.gd`** — cubre 13 edificios, 40 frames, 9 tiles/props, las 5 skins de UI, tamaños/anclas y frames distintos.

### Verified
- `python3 tools/gen_sprites.py` dos veces → `shasum` idéntico (determinista).
- `bash scripts/gate.sh` → EXIT 0: smoke + main input + 24 tests + pureza, sin leaks.
- `./scripts/demo.sh` → EXIT 0; captura 1600×900 `tmp/shot-art2-final.png`.

### Status
Terreno/agua/caminos y UI ya tienen assets propios; walkers animan 2 frames. Sigue sin 8 direcciones, animación de edificios ni arte final. Próximo: fidelidad visual (Blender/SDXL/CC0/CC-BY-SA) e iconos/retratos.

---

## [2026-11-11] - Caesar III Clone (overrides 3D de Blender)

### Added
- **`tools/blender/render_buildings.py`** — set 3D procedural de 13 edificios + árbol/roca. Blender 5.3 headless, cámara ortográfica compartida, fondo transparente y EEVEE. Sin modelos, texturas, HDRI ni assets del original.
- **`tools/blender/render_temple.py`** — templo hero y helpers compartidos (escena, cámara, luces, primitivas).
- **`tools/blender/postprocess.py`** — 1024→512, sombra suave y manifest con ancla derivada de `world_to_camera_view`.
- **`assets/sprites/blender/`** — 15 PNG + `manifest.json`; `SpriteTheme` los fusiona sobre el manifiesto vector y mantiene el fallback.
- **`tests/test_sprite_theme.gd`** — verifica que el override del templo sea 512×512 cuando el manifiesto Blender existe.

### Why
El set 2D ya era legible, pero seguía plano. Blender permite volumen, luz y detalle sin comprar assets ni usar el original. La capa de override permite comparar el set 3D con el vector sin tocar `sim/` ni romper el fallback.

### Verified
- Blender 5.3 headless verificado; 15 renders EEVEE + postproceso.
- `bash scripts/gate.sh` → EXIT 0: smoke + main input + 24 tests + pureza, sin leaks.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-blender-full3.png` a 1600×900.

### Status
Override 3D activo y visible en el juego. Es low-poly/prototipo; falta decidir 3D vs vector, animar edificios/walkers y agregar detalle. El siguiente paso es dirección de arte y contenido visual, no más pipeline.

---

## [2026-11-11] - Caesar III Clone (fix override 3D)

### Fixed
- **`view/sprite_theme.gd`** — el merge guardaba `file` relativo a `assets/sprites/blender/`, pero `_entry` lo resolvía contra `assets/sprites/`: el metadata 3D era correcto y la textura cargada seguía siendo el PNG vector base. Ahora el merge prefija `blender/` y el test exige que el templo cargue una textura real de 512×512, no solo metadata.
- **Walkers 3D** — 40 frames (5 tipos × 4 direcciones × 2 zancadas) renderizados y probados; se descartaron del override porque a tamaño de juego se leían como peones. Los walkers vectoriales siguen activos.

### Verified
- `bash scripts/gate.sh` → EXIT 0: smoke + main input + 24 tests + pureza, sin leaks.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-real3d-final.png`.

### Status
Set 3D de edificios activo y visible; walkers 2D. El siguiente paso es detalle/animación 3D y decidir si vale un walker 3D de mayor calidad.

---

## [2026-11-11] - Caesar III Clone (alineación 2:1)

### Fixed
- **Cámara Blender** — el set 3D usaba una elevación de ~28° y `ortho_scale=5.2`; Godot usa tiles 2:1 (128×64). Ahora la cámara está a 45° de azimut y 30° de elevación, `ortho_scale=5.657`, para que un cuadrado de 1×1 proyecte exactamente un rombo de 128×64.
- **15 renders 3D regenerados**; ancla proyectada en `(256, 361.81)`; se validó con overlays de footprints 1×1, 2×2 y 3×3.

### Verified
- `bash scripts/gate.sh` → EXIT 0: smoke + main input + 24 tests + pureza.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-aligned.png`.

### Status
El set 3D de edificios queda activo y alineado; walkers 2D. El siguiente paso es detalle/animación 3D, no más calibración de cámara.

---

## [2026-11-11] - Caesar III Clone (centrado de footprints)

### Fixed
- **`view/city_view.gd`** — el sprite de un edificio se centraba en `origin + size * 0.5`. Para un footprint de 1×1 eso es la esquina entre cuatro tiles, no el centro: todo el set quedaba media celda hacia adelante y las bases pisaban los caminos.
- **`view/iso.gd`** — nuevo `footprint_center(origin, size) = origin + (size - 1) * 0.5`: 1×1 usa el centro del tile, 2×2 el punto entre sus cuatro tiles y 3×3 el tile medio.
- **`tests/test_iso.gd`** — cubre los tres tamaños para que la regresión no vuelva.

### Verified
- `bash scripts/gate.sh` → EXIT 0: smoke + main input + 24 tests + pureza.
- Debug de footprints 1×1/2×2/3×3: las bases quedan dentro del rombo y no invaden caminos.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-footprint-final.png`.

### Status
Cámara 2:1 y centrado de footprints resueltos. El set 3D de edificios queda activo y alineado; walkers 2D.

---

## [2026-11-11] - Caesar III Clone (vida ambiente)

### Added
- **Chimeneas 3D** en las cinco casas, con cap; el sprite de cada nivel se regeneró desde Blender.
- **`assets/sprites/fx_smoke.png`** + `tools/gen_fx.py`: puff suave determinista para humo.
- **`view/city_view.gd`**: humo de chimeneas/templo y spray de fuente; se dibuja después del sprite del edificio para que el depth sorting siga correcto. El fallback de primitivas también usa `footprint_center`.

### Verified
- `bash scripts/gate.sh` → EXIT 0: smoke + main input + 24 tests + pureza.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-life-final.png`.

### Status
El set 3D queda alineado, centrado y con vida ambiente; walkers 2D. Siguiente: detalle de mercado/granja/templo y banderas.

---

## [2026-11-11] - Caesar III Clone (detalle 3D)

### Added
- **Mercado**: awnings a rayas con valance, barriles con flejes y canastas.
- **Granero**: dock de carga, sacos, aparejo de carga (postes/beam/rope).
- **Templo**: braseros con llama, medallones de frieze y ánforas de ofrenda.
- **Granja**: espantapájaros, gavillas atadas y canastas de cosecha.

### Decision
- **Texturas se postergan** hasta congelar geometría/cámara/UV. A 100–150 px por edificio el detalle fino se pierde y el set todavía cambia; primero se cierra silueta/detalle y después se hornea un atlas procedural (estuco, terracota, piedra, madera) sin assets externos.

### Verified
- Render Blender: 15/15 assets; sin geometría flotante tras quitar las ventilas del granero.
- `bash scripts/gate.sh` → EXIT 0: smoke + main input + 24 tests + pureza.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-details4.png`.

---

## [2026-11-11] - Caesar III Clone (banderas)

### Added
- **Banderas animadas** de prefecto (azul) e ingeniero (naranja): el sprite 3D conserva el poste y `CityView` dibuja la tela con onda; sin estado nuevo en `sim/`.

### Verified
- Render Blender 15/15; `bash scripts/gate.sh` → EXIT 0 (24 tests + smoke + pureza).
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-flags.png`.

---

## [2026-11-11] - Caesar III Clone (iconos de UI)

### Added
- **10 iconos 24×24** para la barra de construcción, generados por `tools/gen_ui_icons.py` y asignados a los botones en `main.gd`.
- Caminos, casa, pozo, fuente, granja, granero, mercado, templo, prefecto e ingeniero.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-ui-icons.png`.

---

## [2026-11-11] - Caesar III Clone (blending de tiles + techo de granja)

### Fixed
- **Techo del cobertizo de la granja**: `hip_roof()` ahora acepta centro (`cx, cy`) y el roof queda sobre el shed de la esquina, no flotando en el centro del campo.

### Added
- **Blending por capas** en `CityView`: base de terreno → agua → camino → bordes. Rellenos expandidos 1 px para tapar antialias y fringes por vecino: pasto sobre camino, arena sobre agua.
- `tools/gen_tile_edges.py`: 8 máscaras de borde; assets de vista directos, fuera del manifest.
- Tiles de camino/agua sin borde propio para evitar costuras internas.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-layers.png`.

---

## [2026-11-11] - Caesar III Clone (HUD con iconos)

### Added
- **HUD por segmentos** icono+valor para fondos, felicidad, población, trabajo, deuda, fecha y herramienta actual.
- 6 iconos 24×24 generados por `tools/gen_ui_icons.py`.
- Smoke test actualizado para validar `_hud_labels` (7 etiquetas) y el contador de deuda.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-hud-icons.png`.

---

## [2026-11-11] - Caesar III Clone (overlays de cobertura/riesgo)

### Added
- **F3 cicla overlays**: agua, comida, trabajo, riesgo de fuego y riesgo estructural.
- `CityView._draw_overlay` tiñe tiles/edificios después de los objetos; `main.gd` muestra la leyenda `Overlay: … · F3`.
- Smoke test valida el ciclo completo (Agua → … → Sin overlay).

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.
- `./scripts/demo.sh --overlay=Agua` → EXIT 0; captura `tmp/city-overlay.png`.

---

## [2026-11-11] - Caesar III Clone (leyenda de overlays)

### Added
- **Leyenda F3** con swatches: pozo/fuente, con/sin comida, con/sin acceso, y semáforo verde/amarillo/rojo para fuego/estructura.
- `CityView.overlay_legend()` expone pares color/etiqueta; `main.gd` los renderiza en el panel.
- Smoke test valida leyenda de agua (2 entradas) y leyenda vacía en “Sin overlay”.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.
- `./scripts/demo.sh --overlay=Agua` → EXIT 0; captura `tmp/city-overlay-legend.png`.

---

## [2026-11-11] - Caesar III Clone (entretenimiento)

### Added
- **Teatro 2×2** (coste 400, 4 trabajadores) y **actor** que recorre caminos y da cobertura mensual a casas.
- `ServiceResolver` service_type 4; `House.entertainment`; felicidad hasta +10 por cobertura.
- Overlay F3 “Entretenimiento”, leyenda y arte propio (2D, 3D Blender, icono y 8 frames de actor).
- Test de servicio, edificio, hotkey T, HUD con 11 botones y felicidad base 42.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.
- Demo con teatro/actor; capturas `tmp/shot-theater-final.png` y `tmp/shot-theater-overlay.png`.

---

## [2026-11-11] - Caesar III Clone (inspector de edificios)

### Added
- **Modo inspección `I`**: click sobre casa/edificio abre panel con estado vivo; `Esc`/Cerrar lo ocultan.
- Inspector muestra nivel, población, agua, comida, entretenimiento, dios, camino, fuego; para edificios, trabajadores, stock, producción, riesgo y daño.
- Test de input: abre/cierra inspector y verifica el título de una casa.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.
- Captura `tmp/city-inspector.png`.

---

## [2026-11-11] - Caesar III Clone (educación y salud)

### Added
- **Escuela** (350, maestro) y **clínica** (400, doctor), ambos 2×2, con cobertura mensual.
- `education_until_month`/`health_until_month`; felicidad +5 por cada servicio.
- Overlays F3 “Educación” y “Salud”, inspector con ambas coberturas y hotkeys `E`/`H`.
- Arte propio: 2D, 3D Blender, iconos y 16 frames de teacher/doctor; build bar de 13 botones.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.
- Demo con teacher/doctor; capturas `tmp/shot-ed-final2.png` y `tmp/shot-ed-overlay2.png`.

---

## [2026-11-11] - Caesar III Clone (inspector de servicios)

### Fixed
- El inspector explica por qué falta comida/salud: `falta granero/mercado`, `mercado sin trabajadores`, `sin cobertura`, `clínica sin trabajadores` o `sin clínica`.
- Clic derecho inspecciona; Shift+clic derecho demuele.

### Verified
- Gate **36 tests**; juego reiniciado.

---

## [2026-11-11] - Caesar III Clone (zoom trackpad)

### Fixed
- La cámara ahora soporta `InputEventPanGesture` y `InputEventMagnifyGesture` (trackpad macOS), además de la rueda.

### Verified
- `Camera zoom test passed`; gate **36 tests**.
- Juego relanzado y usable en la Mac Mini.

---

## [2026-11-11] - Caesar III Clone (auditoría de ingeniería)

### Fixed
- **P1:** `CityBuilder.remove` ahora elimina `DestinationTarget` de cualquier edificio, no solo granary; evita caravanas apuntando a warehouses borrados.
- **P2:** `Housing.try_merge` devuelve la `large_house`; `CityBuilder.place` ya no retorna una casa removida.

### Added
- `test_remove_cleanup`, `test_invariants` multi-seed y `test_catalog`; gate **34 tests**.
- Informe `.knowledge/AUDIT-2026-11-11.md` con hallazgos P1/P2/P3 y evidencia.

### Verified
- Gate EXIT 0: 34 tests + smoke + pureza.
- Stress: 2.000 walkers × 10.000 ticks = 78.280 ms / **7,83 ms/tick**.

---

## [2026-11-11] - Caesar III Clone (caravana de comercio)

### Added
- **Caravana** del puesto comercial al warehouse y de vuelta; `target_mode=DESTINATION`, 8 frames y slot propio.
- El warehouse crea un `DestinationTarget` kind `warehouse`; test real de spawn en tick 31.
- Gate **31 tests**; la venta mensual determinista no cambia.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 31 tests + smoke + pureza; `Caravan test passed`.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-caravan.png`.

---

## [2026-11-11] - Caesar III Clone (comercio/exportación)

### Added
- **Trade post 2×2** y ruta fija mensual: exporta hasta 20 cerámicas (8) y 20 muebles (12) desde un warehouse activo.
- Evento `trade` con mensaje en UI; build bar de 23 botones en 12 columnas; arte 3D e icono propios.
- Test `test_trade.gd`; gate actualizado a **30 tests**.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 30 tests + smoke + pureza; `Trade test passed`.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-trade.png`.
- Reviewer PASS sobre `90bf4d3`.

---

## [2026-11-11] - Caesar III Clone (save/load y tiempo)

### Added
- **Snapshot binario completo** (`scripts/save_load.gd`): clock, RNG, grid, stats, edificios, casas, targets, destinos, walkers, slots, mapas y festivales.
- **3 slots** en `user://`, menú compacto de **Pausa/1x/2x/4x** y `F5`/`F9`/`Space`.
- Test `test_save_load.gd` con hash round-trip y continuación determinista; gate **29 tests**.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 29 tests + smoke + pureza.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-save-final.png`.
- Reviewer PASS sobre `3076ebd`.

---

## [2026-11-11] - Caesar III Clone (cinco dioses)

### Added
- **Ceres, Neptuno, Mercurio, Marte y Venus** con templos dedicados 2×2.
- `god_maps` por dios + unión legacy; `House.gods` e inspector; festivales por dios con costo/duración/cooldown.
- Build bar de 22 botones en 11 columnas; 4 templos 3D e iconos propios; 28 tests.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 28 tests + smoke + pureza; `Five‑god test passed`.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-gods.png`.
- Reviewer PASS sobre `080e326`.

---

## [2026-11-11] - Caesar III Clone (unificación 3D)

### Fixed
- Baño, talleres, almacén, casa grande y parque dejaron el estilo 2D vectorial y ahora usan **renders 3D de Blender**, igual que el resto de las estructuras.
- `blender/manifest.json` cubre **22 edificios** + árbol/roca (24 renders); los sprites 2D quedan solo como fallback.

### Verified
- `tools/blender/render_buildings.py` → 24 renders; `postprocess.py` → 22 edificios + 2 props.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-merge-3d.png`.
- Gate 27 verde.

---

## [2026-11-11] - Caesar III Clone (casas 2×2, merging y deseabilidad)

### Added
- **Large house 2×2** generada por merging automático de cuatro casas 1×1; capacidad duplicada y población preservada.
- **Park 1×1** de deseabilidad (radio 3, valor 10), cálculo por tile, overlay F3 **Deseabilidad** e inspector.
- Arte 2D de casa grande/parque e icono de parque; build bar de 18 botones en dos filas.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 27 tests + smoke + pureza; `Houses merge test passed`.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-merge.png`.
- Reviewer PASS sobre `1f39d83`.

---

## [2026-11-11] - Caesar III Clone (cerámica, muebles y almacén)

### Added
- **Talleres de cerámica y muebles** 2×2 y **almacén** 3×3 con stock por bien.
- `GoodsSystem` (tick 21), carros `pottery_cart`/`furniture_cart` (`service_type 8/9`), consumo de casas y +2.5 felicidad por bien.
- Overlay F3 **Bienes**, inspector con stock, build bar de 17 botones en dos filas y arte 2D/iconos.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 26 tests + smoke + pureza; `Ceramics test passed`.
- `./scripts/demo.sh` → EXIT 0; captura `tmp/shot-goods2.png`.
- Reviewer PASS sobre `9e157ac`.

---

## [2026-11-11] - Caesar III Clone (baños e higiene)

### Added
- **Bathhouse 2×2** (350, 3 trabajadores) con walker **bather** (`service_type 7`), cobertura mensual y +5 felicidad.
- Overlay F3 **Higiene**, línea **Higiene** en el inspector, hotkey `B`, icono y arte 2D con pileta/vapor.
- `tests/test_bathroom.gd` (NUEVO) y gate actualizado a 25 tests.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 25 tests + smoke + pureza.
- `./scripts/demo.sh` → bather activo (`state=1`); captura `tmp/shot-baths.png`.
- Reviewer PASS sobre repo limpio (commit `2da5e48`).

---

## [2026-11-11] - Caesar III Clone (religión/festivales)

### Added
- **Festival `F4`** con templo activo: 200 denarios, +15 felicidad por 2 meses y cooldown de 6.
- `ReligionSystem` puro; estado `festival_until_month`/`festival_cooldown_until_month`; overlay F3 “Religión”.
- Test de templo cubre costo, duración y cooldown; capture `tmp/shot-religion.png`.

### Verified
- `bash scripts/gate.sh` → EXIT 0: 24 tests + smoke + pureza.

---

## [2026-11-10] - Caesar III Clone (proyecto nuevo)

### Added
- **`projects/caesar3-clone/`** — clon personal de Caesar III en Godot 4.7.2, desde cero y basado en el original. Documentos iniciales: `BRIEF.md`, `ARCHITECTURE.md`, `WALKING-SYSTEM.md`, `DECISIONS.md`, `STATUS.md`. Sin código todavía.
- **Registro del proyecto** en `session-context` (Active), `projects/AUDIT.md` y `MEMORY.md`.

### Why
El proyecto necesita una base de diseño antes de escribir código: alcance del MVP, arquitectura de simulación fuera de nodos, y una spec completa del walking system, que es el corazón y el mayor riesgo técnico. La meta final es un clon completo; el MVP es la primera porción.

### Status
Diseño. Próximo: revisión de la spec y esqueleto Godot fase 0.

---

## [2026-11-10] - El bind del gateway deja de degradarse en silencio

### Added
- **`scripts/gateway-bind-check.sh`** — compara `gateway.bind` del config contra lo que el proceso realmente escucha, y falla explicitamente cuando no coinciden.
- **Hook en `scripts/gateway-audit.sh`** — seccion "Bind" antes de Jobs, asi el audit periodico lo reporta sin depender de que alguien lo recuerde.

### Why
Con `bind: tailnet`, el gateway necesita la IPv4 del tailnet **en el arranque**. Si el LaunchAgent gana la carrera contra Tailscale, cae a loopback y se queda ahi: el archivo sigue diciendo `tailnet`, el proceso escucha en `127.0.0.1`, y la unica senal es que un cliente remoto no conecta. Paso el 2026-11-09 19:34 y no lo detectamos en el momento.

Ese desvio de runtime se convirtio en un cambio de config el 2026-11-10 12:28: la Control UI emitio `config.patch` con el estado que veia correr (`loopback` + `tailscale.mode: serve`) y se llevo puestos `bind`, `tailscale.mode` y `allowedOrigins`. La leccion queda escrita: **el estado del proceso es lo que la UI refleja**, asi que un bind degradado se propaga al archivo.

### Changed
- Los cambios de gateway se aplican con `openclaw config patch` (escritura validada), no editando `openclaw.json` a mano.

---

## [2026-11-09] - Edad de los Reinos (proyecto nuevo)

### Added
- **`projects/edad-de-los-reinos/`** — RTS medieval 1v1 en Godot 4.7, independiente de ABYA YALA. Mapa isométrico 80×80, economía de 4 recursos, 11 edificios, 3 edades, 7 unidades, combate con counters, IA con 3 dificultades, niebla, minimapa, audio sintetizado, menú/pausa/victoria y tests headless/UI.
- **`play.command`** — lanzador local con `godot --path .`; F11 alterna pantalla completa.

### Verified
- 24 asserts headless, UI de construcción/entrenamiento/edad, selección por mouse/caja/rally y menú → partida.
- Simulación de 20 minutos: la IA alcanza la Edad Feudal al minuto 3 y ataca entre los minutos 10 y 13.

## [2026-11-09] - Metodología HANDOFF y cursos

### Added
- Soporte para `--course <slug>` en `scripts/session-handoff.py`, creando `studies/<slug>/HANDOFF.md` con título `# HANDOFF - Curso <slug>` y tomando el repo del workspace.
- Implementación de fusión del HANDOFF general (alias de workspace) que preserva y deduplica entradas:
  * Cabecera (Fecha, Branch, Repo) del nuevo.
  * `## Que se hizo en esta sesion` mantiene máximo 5 entradas con timestamps (`### YYYY-MM-DD HH:MM`).
  * `## Estado actual`, `## Proximos pasos`, `## Decisiones y contexto que no debe perderse`, `## Cerrados en esta sesion` se unen, con deduplicación y numeración conservada en próximos pasos.
  * `## Archivos tocados` combina los bloques de código.
  * Se conservan secciones desconocidas del documento anterior.
- Añadido flag `--course` a `skills/session-lifecycle/scripts/session-end.sh` y ajuste del label de guardado diario a `studies/<slug>`.
- Nuevo test `scripts/test-handoff-merge.py` con seis casos, incluido el merge de workspace, validación de slug de curso y comportamiento de proyecto sin merge.
- Actualización de la documentación de `skills/session-lifecycle/SKILL.md` (sección de cierre) para describir HANDOFF general y por curso.

## [2026-11-07] - Skill-router: del 20% al 100% del catalogo

### Added
- **skill-router lee el catalogo del runtime, no un directorio.** `scripts/skill-router.py` consume `openclaw skills list --agent <id> --json` (171 skills) con fallback al walk de disco. `load_skills()` extrae a la funcion `suggest()` para reuso sin duplicar logica. `--list` ahora anota el `source`.
- **Regresion medible del router (`scripts/test-skill-router.py`):** 10 casos con expectation en top-3; reporta rango y falla (exit 1) si alguno sale del top-3.
- **Gate de solapamiento (`scripts/check-skill-overlap.py`):** modo aviso, umbral 0.87, 20 pares detectados en el primer barrido. Cableado al pre-commit con disparador propio (`BOUNDARY_RELEVANT`), solo `--staged`, advisory.
- **Skill `capability-index`:** procedimiento de cuatro estados (existe / existe en rol Y / no existe + alternativa / ambiguo) con verificacion de ruta (`test -e`) antes de citar. No inventa skills.

### Changed
- **Fuente unica del pipeline:** ADR-049 marcado `Superseded` (archivado); skills `agent-orchestration-pipeline` y `-model-arbitration` eliminadas (trash) por duplicar la fuente (`model-router.sh` + managed block). `check-pipeline-enforcement.py` deja de exigir a la skill borrada.
- **SKILLS-INDEX.md:** count Core de 34 a 35; fila `capability-index`.
- **AGENTS.md:** la lista de workflows clave paso de `agent-orchestration-pipeline` a `planner-delegation`.
- **Memoria dedicada al subsistema:** `memory/skill-router/STATE.md` y `LEARNINGS.md` para iteracion paso a paso.

### Decision
- No se crea ADR nuevo de scope del router: managed block en AGENTS + SETUP + este ChangeLog son la fuente unica. Editar, no agregar.

---

## [2026-11-06] - El Planner deja de ser un agente que hay que abrir a mano

### Added
- **Pre-flight de OPS antes de tocar el sustrato (E3.3).** El CORE ya no aplica cambios de config, canales, plugins, automatizaciones ni credenciales: delega a `kanam-ops` y pide veredicto (APLICA / NO APLICA / APLICA CON CAMBIOS) con valor actual, valor resultante, qué más toca el patch y el backup que crearía, antes de escribir. Si es APLICA, OPS aplica con backup y al humano se le trae la evidencia real. Restart, borrado y cambio de producción siguen requiriendo OK explícito. Procedimiento: `docs/OPS-DISPATCH.md` §6-bis.
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
- **Regla de verificación del Planner (caso Preflight, 2026-11-06).** Un plan afirmó que Chromium corría con `--no-sandbox` sin leer `src/lib/scan.ts:69`; era falso. Ahora `program-orchestration` y `planner-delegation` exigen que cada afirmación de estado cite `archivo:línea` y el commit/snapshot leído, o se marque como supuesto, con un paso 0 de verificación si no se pudo comprobar. El review del CORE señaló quota y cap de concurrencia ausentes; era correcto en el snapshot pre-fix, y el commit `289cb19` los agregó después. La lección es citar commit + archivo:línea, no solo el archivo actual.
- **Compatibilidad de programas legacy.** `program_plan.py` normaliza `write_path` singular y campos faltantes de `abya-yala-05.json`; el programa ya pasa `plan_lint` y produce contrato de ejecución.
- **Review semanal sin pasos inventados.** El primer run de `planner-weekly-review` (17:30) inventó los pasos #2 y #3 de Abya Yala porque el prompt usaba `board`/`status`, que no listan todos los pasos. Se agregó `program_plan.py show` y `status --json.steps`; el prompt del review ahora usa `show` y prohíbe inventar pasos. El run se repitió.

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
