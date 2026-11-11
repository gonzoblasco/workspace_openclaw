# Caesar III Clone — Investigación Consolidada

**Fecha:** 2026-11-10
**Destino:** clon de Caesar III en Godot 4.7.2, macOS Apple Silicon (Mac mini M4, 24 GB)
**Estado:** documento de entrada. Consolida dos informes previos y corrige sus errores.

---

## 0. Cómo leer este documento

Los dos informes originales (uno generado por Vane con el prompt de Gonzo, otro con el prompt corregido) tenían datos correctos mezclados con afirmaciones falsas. Este documento **solo conserva lo verificado contra fuente**, marca explícitamente lo que quedó en duda, y agrega lo que ninguno de los dos tenía: constantes reales del motor, extraídas de ingeniería inversa documentada y del manual oficial.

**Regla de este documento:** si dice "verificado", hay fuente. Si dice "sin verificar", no se usa como base de decisión.

---

## 1. Datos básicos del juego — VERIFICADO

| Dato | Valor | Fuente |
|---|---|---|
| Desarrollador | Impressions Games | Manual oficial |
| Publisher original | Sierra On-Line | Manual oficial |
| Lanzamiento | 30 de septiembre de 1998 | Consenso de fuentes |
| Diseñador principal | David Lester | Wikipedia/MobyGames |
| Composer | Robert Euvino | Manual oficial |
| Motor | Propio (2D isométrico, pre-renderizado) | Manual + análisis técnico |
| Steam app ID | 517790, publicado por Activision, USD 5.99 | Ficha de Steam, verificada 2026-11-10 |
| Plataformas originales | Windows, Mac OS | MobyGames |

**Corrección al informe original:** el informe de Vane decía que no había podido verificar la reedición de Steam. Sí existe: es una re-edición de Activision, se vende a USD 5.99, y está empaquetada dentro del "Activision Collection" (52 juegos, USD 774.38). Corresponde al juego original sin cambios de mecánicas.

**Corrección al informe de Kanam:** yo afirmé que Godot 4.7 no existía. Gonzo lo corre: **Godot v4.7.2.stable.official [ed1daf0bf]**. Es la versión objetivo.

---

## 2. El bucle de simulación — VERIFICADO (ingeniería inversa documentada)

Fuente primaria: dalerank, "Reverse-engineering Caesar III: the game loop (Part 6)", 2014. Es la referencia técnica más valiosa encontrada y **ninguno de los dos informes la tenía**.

### 2.1 Estructura temporal

```
gameLoop():
  while game.run:
    gametime.ticks++
    switch(gametime.ticks): ejecuta UN sistema por tick (case 1..49)
    if ticks >= 50:
      ticks = 0
      doGameDayTick()
    renderCity()
```

**Constantes clave:**
- **50 ticks = 1 día de juego.**
- **16 días = 1 mes de juego.**
- **12 meses = 1 año.**

Esto significa que **cada día de juego ejecuta ~50 pasos de sistemas, uno por tick**. No todos los sistemas corren todos los días: se distribuyen por número de tick.

### 2.2 Orden de sistemas por tick (los documentados)

| Tick | Sistema |
|---|---|
| 1 | Felicidad de los dioses |
| 4 | Parámetros de invasión de César |
| 5 | Formaciones militares |
| 6 | Tierra de nativos |
| 7 | IDs de red de caminos |
| 8 | Info de almacenamiento de graneros |
| 12 | Decaimiento de edificios en casas cubiertas |
| 16 | Recálculo de stock de recursos |
| 17 | Advisor de comida + trigo para Roma |
| 18 | Materias primas en talleres |
| 19 | Acceso de agua a muelles |
| 20 | Producción industrial |
| 21 | Acceso de pathing a Roma |
| 22 | Población en casas |
| 24 | Desalojo de casas superpobladas |
| 25 | Cálculo de trabajadores por categoría, desempleo, % de trabajadores por edificio |
| 27 | Acceso a reservorios y fuentes |
| 28 | Acceso de agua a casas |
| 31 | **Generación de walkers por edificio** |
| 32 | Generación de comerciantes |
| 33 | Conteo de tipos de edificio + cobertura cultural |
| 34 | Distribución de tesoro en foros y senados |
| 35 | Decaimiento de servicios culturales |
| 36 | **Servicios de vivienda para evolución** |
| 37 | Deseabilidad de edificios y terreno |
| 38 | Deseabilidad de edificio |
| 39 | **Evolución/devolución de casas** |
| 43 | Estado de ruinas ardientes |
| 44 | Daño por crimen y fuego |
| 45 | Generación de criminales |
| 49 | Info de entretenimiento |

### 2.3 Ciclo diario (`doGameDayTick`)

```
totalDays++; day++;
if day > 15:
    day = 0
    newcomersThisMonth = 0
    monthsSinceFestival++
    monthHandle()
    month++
    if month <= 11: updateRatings(0)
    else: startNewYear()
    recordMonthlyPopulation()
    holdFestival()
if day == 0 or day == 8:
    calculateCityHappinessAndCrime()
```

### 2.4 Ciclo mensual (`monthHandle`)

```
calculateHealthRate()
handleRandomEvents()        <- acá viven los desastres
collectMonthlyTaxes()
payMonthlyWages()
payMonthlyInterest()
payMonthlySalary()
housesConsumeMonthlyFood()
handleDistantBattleEvent()
handleInvasionEvent()
checkRequestsEvent()        <- pedidos de César
checkDemandChangesEvent()
checkPriceChangesEvent()
tickMonth_updateLegionMorale()
determineGraphicIdsForRoads()
determineGraphicIdsForWater()
calculateOpenGroundCitizen()
sortAndCompactPlayerMessages()
```

### 2.5 Ciclo anual (`startNewYear`)

```
month = 0
handleExpandEmpireEvent()
year++
gametick_requestBirthsDeaths_calculateHousingTypes()
[guardar historial financiero del año]
calculateAndPayTribute()
resetTradeAmounts()
tick_updateFireSpreadDirection()   <- dirección de propagación del fuego
updateRatings(1)
blessingNeptuneDoubleTradeActive = 0
```

### 2.6 Implicancia para el clon en Godot

**No usar `_process` para cada sistema.** El modelo correcto es:
- Un `SimulationTick` de 50/segundo lógico (o desacoplado del frame).
- Un dispatcher por número de tick.
- El render es independiente del tick lógico.
- Esto permite simular rápido (fast-forward) sin romper lógica.

---

## 3. Sistema de walkers — VERIFICADO (experimental + código)

Dos fuentes independientes, coincidentes:

**A. Experimento de comunidad (kaluhiok, 1998):** midió distancias reales en el juego.
**B. Código de Julius:** `bvschaik/julius`, C, **licencia AGPL-3.0**.

### 3.1 Distancias de caminata (tiles)

| Walker | Tiles |
|---|---|
| Niño de escuela | 22 |
| Barbero, baños, doctor, librero, mercado, reclutador, sacerdote, cirujano, profesor | 35 |
| Prefecto | 52 |
| Actor, ingeniero, gladiador, domador de leones, recaudador (foro/senado) | 156 (o 52 si la dirección deseada no está disponible) |

### 3.2 Algoritmo de walker (no-destino)

1. Al emplearse la plaza, el walker intenta caminar **paralelo al camino principal**, en la misma dirección que los inmigrantes.
2. Cada tipo de edificio tiene un **camino preferido de salida** — incluso en una intersección, el prefecto siempre sale por el mismo lado. Esto tiene implicancia de diseño: **hay zonas que un walker nunca cubre** según de qué lado salga.
3. El walker cambia de dirección solo por dos motivos:
   - No puede seguir (sin camino/vía de agua).
   - Cumplió su cuota de tiles.
4. El cambio de dirección es de **90 grados**, y es aleatorio.
5. Al terminar la cuota, vuelve por el **camino más corto** a su oficina.

### 3.3 Walkers con destino (warehouse, granero, granjero, comprador de mercado)

- Caminan lo que necesiten.
- El destino se elige por **distancia euclidiana** (verificado: no Manhattan).
- **No conocen el camino más corto al destino** — usan el mismo algoritmo de walking. Consecuencia: pueden rodear media ciudad para llegar a algo que estaba al lado. Es un artefacto del original y hay que decidir si se replica o se corrige.

### 3.4 Frecuencias de spawn

- Actor: uno cada 13 tiles, incluso sin colonia de actores (las colonias aceleran).
- Gladiador: uno cada 13 tiles desde el Coliseo o escuela de gladiadores.
- Domador de leones: cada 20 tiles, siempre desde la fosa de leones.
- Niños de escuela: **4 a la vez en cada dirección**, desaparecen al terminar.

### 3.5 Implicancia para el clon

El walking system **es** el juego. Si el clon implementa A* con destino directo para todos, el resultado no es Caesar III: es otro juego. La decisión de diseño tiene que ser explícita: replicar el algoritmo original (incluidos sus artefactos) o mejorarlo. **Replicar es lo que hace creíble al clon.**

---

## 4. Vivienda y evolución — VERIFICADO (tabla completa)

Fuente: tabla del handbook de Caesar 3 Augustus (mmxl.wz.cz/c3a/housing.html), coincidente con el manual.

### 4.1 Niveles (20 + lote vacío)

| # | Nivel | Tamaño | Población | Requisitos |
|---|---|---|---|---|
| 0 | Lote vacío | 1x1 | 0 | Acceso a camino |
| — | **Plebeians: ciudadanos trabajadores** | | | |
| 1 | Small Tent | 1x1 / 2x2 | 5 / 20 | Inmigrantes |
| 2 | Large Tent | 1x1 / 2x2 | 7 / 28 | Pozo o fuente |
| 3 | Small Shack | 1x1 / 2x2 | 9 / 36 | 1 tipo de comida |
| 4 | Large Shack | 1x1 / 2x2 | 11 / 44 | 1 dios |
| 5 | Small Hovel | 1x1 / 2x2 | 13 / 52 | Fuente |
| 6 | Large Hovel | 1x1 / 2x2 | 15 / 60 | 1 entretenimiento |
| 7 | Small Casa | 1x1 / 2x2 | 17 / 68 | Escuela o biblioteca |
| 8 | Large Casa | 1x1 / 2x2 | 19 / 76 | Baños, cerámica |
| 9 | Small Insulae | 1x1 / 2x2 | 19 / 76 | 2 entretenimientos |
| 10 | Medium Insulae | 1x1 / 2x2 | 20 / 80 | Doctor u hospital, muebles |
| 11 | Large Insulae | 2x2 | 84 | Escuela y biblioteca, barbero, aceite |
| 12 | Grand Insulae | 2x2 | 84 | 2 tipos de comida, 3 entretenimientos |
| — | **Patricians: ciudadanos que pagan** | | | |
| 13 | Small Villa | 2x2 | 40 | 2 dioses, vino |
| 14 | Medium Villa | 2x2 | 42 | Doctor y hospital |
| 15 | Large Villa | 3x3 | 90 | Academia |
| 16 | Grand Villa | 3x3 | 100 | 3 tipos de comida, 3 dioses |
| 17 | Small Palace | 3x3 | 106 | 2 tipos de vino |
| 18 | Medium Palace | 3x3 | 112 | 4 dioses |
| 19 | Large Palace | 4x4 | 190 | Hipódromo |
| 20 | Luxury Palace | 4x4 | 200 | Todo |

**Nota crítica de diseño:** la vivienda **se expande** de 1x1 a 2x2 a 3x3 a 4x4, y en la expansión **puede comerse jardines y estatuas**. Si después pierde el requisito, devoluciona y los jardines ya no están. Es un sistema con memoria espacial, no un simple "cambio de sprite".

### 4.2 Entretenimiento (fórmula verificada)

- Cada casa tiene rating de entretenimiento 0–100.
- **Hasta 80 puntos** de walkers que pasaron (teatro, anfiteatro, coliseo, hipódromo).
- **Hasta 20 puntos** de cobertura citywide.
- Los puntos **decaen con el tiempo**.
- Anfiteatro/coliseo con 2 shows valen más.
- **Un solo** walker (gladiador o domador) alcanza si hay 2 shows activos.

Esto es relevante porque **el rating no es booleano**: es un valor que decae y hay que modelar el decaimiento, no solo la visita.

---

## 5. Favor del emperador — VERIFICADO

Fuente: handbook oficial de Caesar 3 Augustus (caesar3augustus.com/book/gameratings/favor).

### 5.1 Mecánica

- **Arranca en 50** en cada misión.
- **Sube por:**
  - Progreso hacia objetivos.
  - Cumplir pedidos de César (bienes, dinero, ejército) — a tiempo vale más.
  - Regalos desde ahorros personales (pequeño/mediano/grande).
- **Baja por:**
  - Mal progreso.
  - Ignorar pedidos.
  - Mala gestión del dinero — **"la forma más fácil de enojar a César"**.
  - **No aparecer en el radar** en un año: baja un poco por ausencia.
  - Pagarte un salario mayor a tu rango.

### 5.2 La invasión de César

- **Favor 10 o menos** → César te destituye.
- Envía un ejército que **acampara junto a tu ciudad hasta un año**.
- Si en ese tiempo subís el favor a **40**, el ejército vuelve a Roma.
- Si no, entra a la ciudad y te arresta. **Pelearle no es opción.**
- Los regalos tienen **rendimientos decrecientes**: varios regalos seguidos pierden efecto; hay que esperar un año para recuperar el efecto completo.
- Excepción práctica documentada: **2-3 regalos grandes en secuencia** sí alcanzan para frenar una invasión en curso.

### 5.3 Fórmula de ganancia por ejército prestado

- Ganar una batalla con legiones prestadas: **hasta +25 puntos de favor**, más un Arco Triunfal para construir.

---

## 6. Desastres — VERIFICADO

**Corrección al informe de Vane:** decía que no había podido documentar desastres. Están en el manual y en el código (`handleRandomEvents`, tick 44 `updateCrimeFireDamage`, tick 43 `updateBurningRuin`, anual `tick_updateFireSpreadDirection`).

| Desastre | Causa | Mitigación | Detalle técnico |
|---|---|---|---|
| **Fuego** | Espontáneo o por criminales | Prefectura (prefectos) | Se propaga en una dirección que se recalcula al inicio de cada año (`tick_updateFireSpreadDirection`). Edificios adyacentes a fuego se dañan (tick 28 del daily loop) |
| **Colapso** | Falta de mantenimiento | Ingenieros (engineer, walk de 156 tiles) | Daño por "crimen y fuego" en tick 44 |
| **Invasión** | Favor bajo, o escenario hostil, o evento aleatorio | Ejército, muros, torres | `handleInvasionEvent` en ciclo mensual |
| **Terremoto** | Evento aleatorio | Ninguna | `handleRandomEvents` |
| **Criminalidad** | Sentimiento bajo, desempleo, dioses enojados | Prefectura, foro/senado, templos | Tick 45 `generateCriminal` |

### 6.1 Maldiciones de dioses (del código real)

Cada dios tiene maldición pequeña y grande:

- **Neptune:** hunde barcos (destruye comercio marítimo).
- **Mercury:** remueve bienes del almacén.
- **Mars:** levantamiento local (revuelta armada).
- **Venus:** sube crimen y baja salud.
- **Ceres:** marchita las cosechas.

La felicidad de cada dios se calcula con un sistema de bolts (`numBoltsGod`) y meses desde el último festival. **Esto es mecánica, no color.**

---

## 7. Assets y licencias — RESUELTO (personal)

### 7.1 Lo que existe CC0 / libre

| Fuente | Contenido | Licencia | Sirve para |
|---|---|---|---|
| **Kenney** | Isométrico, romano básico | CC0 | Prototipado |
| **Quaternius** | Modelos 3D low-poly | CC0 | Base 3D |
| **Poly Haven** | Texturas, HDRIs | CC0 | Ambiente |
| **ambientCG** | Texturas PBR | CC0 | Ambiente |
| **OpenGameArt** | Variable item por item | Mixta — **verificar cada uno** | Sueltos |

### 7.2 0 A.D. — VERIFICADO

- Desarrollado por **Wildfire Games**.
- Arte bajo **CC-BY-SA 3.0** (confirmado en `svn.wildfiregames.com/public/ps/trunk/binaries/data/mods/public/art/LICENSE.txt`).
- Código bajo GPL.
- **Implicancia concreta:** podés usar, modificar y distribuir. **Pero** CC-BY-SA es *copyleft*: si incorporás el arte a tu juego, tu juego (o al menos el derivado de esas piezas) debe distribuirse bajo la misma licencia. Para un clon **publicable**, esto contamina la obra. Para un clon **personal**, es irrelevante.
- Hay que **atribuir a Wildfire Games**.

### 7.3 Julius / Augustus — CRÍTICO

- Julius: **AGPL-3.0**.
- **AGPL es la licencia más contagiosa del ecosistema.** Si linkeás código AGPL o derivás de él, tu proyecto completo debe ser AGPL — incluso como servicio en red.
- **Para un clon comercial: no se puede reutilizar código de Julius ni de Augustus.** Se puede **leer** como referencia de comportamiento y reimplementar la lógica desde cero en Godot. Eso es limpio.
- Los assets originales **no** se redistribuyen: Julius los extrae de la instalación local en runtime. Si querés esos assets, tenés que tener Caesar III comprado y extraerlos para uso personal. **Redistribuirlos es violación de copyright de Activision.**

### 7.4 DECISIÓN TOMADA — Clon personal, sin assets del original

**Decidido 2026-11-10:** el clon es **personal** (uso propio, no se publica ni se vende), **y no hay copia de Caesar III disponible** (Gonzo no posee el juego y no hay presupuesto para comprarlo).

**Corrección importante:** Julius y Augustus son reimplementaciones del **motor**, no traen assets. Sin una instalación real de Caesar III, no arrancan. Por lo tanto **los assets del original no son una opción**. Hay que usar arte de reemplazo.

### 7.5 Estrategia de arte — reemplazo CC0

**Principio rector: el arte es una capa, no el proyecto.** La simulación es independiente de los sprites. Se construye primero con primitivas y se cambia el arte después.

**Fase 1 — Prototipo (primitivas):**
- Rectángulos de colores por tipo de edificio, con el tamaño correcto en tiles.
- Caminos como líneas.
- Walkers como puntos que se mueven.
- **Objetivo:** que el walking system y el game loop funcionen. Nada más.

**Fase 2 — Arte de reemplazo:**

| Fuente | Contenido | Licencia | Uso |
|---|---|---|---|
| **Kenney** | Isométrico genérico: terreno, caminos, agua | CC0 | Base del terreno |
| **Quaternius** | Modelos 3D low-poly | CC0 | Renderizar a sprites isométricos |
| **0 A.D.** (Wildfire) | Arquitectura y unidades romanas | **CC-BY-SA 3.0** | Lo más cercano al look original. Para uso personal no obliga a nada; si se muestra, requiere atribución |
| **OpenGameArt** | Tilesets romanos sueltos | Mixta | Revisar item por item |
| **ambientCG / Poly Haven** | Texturas, materiales | CC0 | Detalle de superficies |

**Nota sobre 0 A.D.:** es la mejor opción visual para un look romano. CC-BY-SA no impide usarlo en un proyecto personal; solo pide atribución a Wildfire Games si se distribuye o muestra. Poner el crédito en el juego cuesta cero.

**Fase 3 — Si el proyecto crece:** generar arte propio con el pipeline 3D → render (Blender + script). Solo si hace falta.

**Ventaja de esta secuencia:** no se invierte un minuto en arte hasta que la mecánica esté probada. Para entonces ya se sabe exactamente qué se necesita.

### 7.5 Pipeline recomendado (2D isométrico pre-renderizado)

El original es 2D isométrico pre-renderizado: modelos 3D renderizados a sprites desde ángulos fijos (8 direcciones típicamente).

Pipeline para el clon:
1. Modelar en **Blender**.
2. Script de render por dirección (8 o 16 frames por animación).
3. Exportar spritesheets.
4. Importar en Godot con `AtlasTexture` + `Sprite2D` o `AnimatedSprite2D`.

**Ventaja:** look idéntico al original, rendimiento liviano, corre en cualquier lado.
**Desventaja:** pesa en producción de arte, no se puede re-iluminar dinámicamente.

---

## 8. Arquitectura para Godot 4.7.2 — sin verificar contra docs 4.7

**Aviso:** la búsqueda no devolvió documentación específica de Godot 4.7 (el número es muy reciente y la mayoría del contenido es 4.3–4.5). Lo siguiente es extrapolación de 4.x; **hay que validar cada punto contra la doc instalada de 4.7.2**.

### 8.1 Render isométrico

- **`TileMapLayer`** (reemplaza al `TileMap` monolítico desde 4.3).
- Múltiples `TileMapLayer`: terreno, caminos, agua, decoración, edificios.
- **Y-sorting** para el problema del pintor. `y_sort_enabled = true` en los nodos.
- Para edificios multi-tile con altura, `TileMapLayer` solo no alcanza: conviene **`Sprite2D`/`Node2D` individuales con `y_sort`**, no tiles.

### 8.2 Pathfinding

- El A* de Godot (`AStarGrid2D`) **no sirve directamente** para el walking system de Caesar III, porque el original no busca destino para la mayoría de walkers. Sirve sí para walkers con destino (mercado → granero).
- El walking system necesita un **grafo de caminos propio** con el algoritmo descrito en §3.2.

### 8.3 Simulación

**Recomendación fuerte:** la simulación **no** vive en nodos de Godot. Vive en datos planos (arrays/structs en GDScript, o GDExtension en C++/Rust si hace falta rendimiento).

- 10.000+ walkers en nodos = muerte por frame.
- `MultiMeshInstance2D` para dibujar miles de sprites iguales en un frame call.
- O usar `RenderingServer` directo.

### 8.4 Mac Apple Silicon

- Godot 4.x corre nativo ARM64 en macOS.
- Motor de render: `Forward+` o `Mobile` funcionan. Para 2D isométrico, `Mobile` o `Compatibility` alcanzan y vuelan.
- 24 GB RAM en M4 es **equipo de sobra**. El límite no es hardware, es arquitectura de simulación.

---

## 9. Lo que hay que construir (y lo que no existe)

### 9.1 No existe — hay que crear

- **Pack de assets de Caesar III CC0.** No existe. Punto.
- **Un clon completo en Godot.** No existe públicamente (hay prototipos, nada serio).
- **Port oficial a Apple Silicon.** No existe.

### 9.2 Existe pero con restricciones

- **Código de referencia:** Julius (AGPL) y Augustus (AGPL). Leer sí, copiar no.
- **Arte romano:** 0 A.D. (CC-BY-SA), Kenney (CC0), Quaternius (CC0).
- **Documentación técnica:** dalerank (artículos de ingeniería inversa), manual de Sierra, wiki de heavengames.

### 9.3 Lo que hay que construir sí o sí

1. Motor de simulación (game loop por ticks).
2. Sistema de walkers (algoritmo propio).
3. Sistema de vivienda y evolución (20 niveles, expansión espacial).
4. Cadena económica (producción, almacenamiento, distribución).
5. Labor pool y empleo.
6. Sistema de agua (pozos, fuentes, reservorios, acueductos).
7. Desastres y mitigación.
8. Favor del emperador e invasiones.
9. Sistema de dioses (5 dioses, festivales, maldiciones).
10. Combate (formaciones, legiones, muros).
11. Render isométrico con Y-sort.
12. UI (advisors, overlays, mensajes).
13. Save/load.
14. Escenarios/misiones.

---

## 10. Decisiones abiertas

| # | Decisión | Impacto | Estado |
|---|---|---|---|
| 1 | **¿Clon personal o publicable?** | Define licencias y esfuerzo de arte | **RESUELTO: PERSONAL** |
| 1b | **¿Assets del original?** | Requiere copia de Caesar III | **RESUELTO: NO HAY COPIA. Arte de reemplazo CC0** |
| 2 | ¿Replicar el walking system original (con artefactos) o mejorarlo? | Define fidelidad vs. calidad de vida | Recomiendo **replicar** — es lo que hace el clon creíble |
| 3 | ¿2D pre-renderizado o 3D real? | Con arte CC0, el camino es renderizar 3D a sprites 2D | Recomiendo **3D→sprite isométrico** |
| 4 | ¿Alcance del MVP? | Qué se construye primero | **A definir en la sesión de planificación** |
| 5 | ¿GDScript o GDExtension para la simulación? | Depende de cuántos agentes simultáneos | Empezar GDScript, medir, migrar solo si hace falta |

**Nota sobre #2:** los "artefactos" del original (walkers que no cubren ciertas zonas, compradores que dan vueltas) son parte de lo que hace al juego reconocible. Un clon que los "arregla" se siente distinto. Recomiendo replicarlos primero y hacerlos configurables después.

---

## 11. Fuentes (verificadas 2026-11-10)

**Primarias / técnicas:**
- dalerank, *Reverse-engineering Caesar III: the game loop (Part 6)*, 2014 — `dalerank.github.io/en/articles/caesar3-part6.html`
- `bvschaik/julius` — github.com/bvschaik/julius (AGPL-3.0)
- `Keriew/augustus` — fork de Julius con extensiones (AGPL-3.0)
- Manual oficial de Caesar III — `sierragamers.com/wp-content/uploads/2019/12/Caesar_3_Manual.pdf`

**Handbook y referencias:**
- Caesar 3 Augustus Handbook — `caesar3augustus.com/book/` (favor, housing, entertainment)
- Tabla de housing levels — `mmxl.wz.cz/c3a/housing.html`
- Caesar 3 Heaven (heavengames) — FAQs, foros, investigación experimental de walkers
- Experimento de walkers de kaluhiok (1998) — `caesar3.heavengames.com/...fn=10&tn=608`

**Producto:**
- Steam app 517790 — verificada directamente, USD 5.99, Activision

**Licencias:**
- 0 A.D. — `svn.wildfiregames.com/public/ps/trunk/binaries/data/mods/public/art/LICENSE.txt` (CC-BY-SA 3.0)
- Kenney, Quaternius, Poly Haven, ambientCG — CC0

**Descartadas del informe original (no usar):**
- Grokipedia (espejo generado por IA)
- Posts de Instagram
- TurboSquid / free3d / cults3d (licencias comerciales, no CC0)
- "No se encontró información verificada sobre X" como sustituto de búsqueda

---

## 12. Próximo paso

Con las decisiones de §10 resueltas, este documento pasa a ser la entrada de la sesión de planificación, que produce:
1. Alcance del MVP.
2. Arquitectura técnica en Godot 4.7.2.
3. Specs por sistema, empezando por el walking system.

---

## 13. Prompt de apertura de sesión

_Listo para pegar en una sesión nueva._

```
iniciar sesión. Proyecto nuevo: clon personal de Caesar III en Godot 4.7.2, macOS Apple Silicon (Mac mini M4, 24 GB).

Adjunto la investigación consolidada. Leela completa antes de responder.

CONTEXTO QUE MANDA:
- Es un proyecto PERSONAL. No se publica, no se vende.
- NO hay copia de Caesar III disponible y no hay presupuesto para comprarla. Julius y Augustus son reimplementaciones del motor, no traen assets: los assets del original NO son una opción.
- El arte es de reemplazo. La estrategia es: primero se construye la simulación con primitivas (rectángulos de color por tipo de edificio, walkers como puntos), y el arte se agrega después con assets CC0 (Kenney, Quaternius) o CC-BY-SA (0 A.D., con atribución).
- Godot 4.7.2.stable.official [ed1daf0bf], ya instalado y funcionando.
- El clon busca replicar la simulación del original, no "mejorarla". Los artefactos del walking system son parte del juego.
- El objetivo de la primera versión es que se SIENTA como Caesar III. Que se VEA como Caesar III viene después.

LO QUE QUIERO DE ESTA SESIÓN:

1. Alcance del MVP: qué sistemas entran en la primera versión jugable y cuáles quedan afuera. Sé concreto y defendé la decisión.

2. Arquitectura técnica: cómo se organiza el proyecto en Godot 4.7.2. Específicamente:
   - La simulación NO vive en nodos. Definí cómo se estructuran los datos (walkers, edificios, casas, caminos) y cómo se renderiza encima.
   - El game loop por ticks (50/día, 16 días/mes, 12 meses/año) — cómo se despacha.
   - Qué va en GDScript y qué, si algo, iría en GDExtension.
   - Cómo está pensada la capa de arte para que se pueda empezar con primitivas y cambiar los sprites después sin tocar la lógica.

3. El walking system como primera spec completa. Es el corazón del juego y el riesgo técnico más grande. Necesito:
   - Grafo de caminos.
   - Algoritmo de walker no-destino (cuota de tiles, cambios de 90°, dirección de salida fija por edificio).
   - Walkers con destino (euclidiano, no Manhattan).
   - Cómo se registra el servicio que un walker entrega a una casa.

Empezá por (1) y (2). No escribas código todavía: quiero la arquitectura acordada primero.
```
