# Reinos de la Frontera — Documento de arranque

**Fecha:** 2026-11-11
**Proyecto:** nuevo, desde cero. Sin código previo, sin assets previos, sin base heredada.
**Destino:** RTS medieval isométrico en Godot 4.7.2, macOS 27 Apple Silicon (Mac mini M4, 24 GB).
**Nombre:** provisional. Se confirma en la fase 0.

**Regla de este documento:** si dice "verificado", hay fuente y se chequeó. Si dice "sin verificar", no se usa como base de decisión. Si dice "estimación", es criterio, no dato.

---

## 0. Resumen

Un RTS medieval isométrico para un jugador contra la IA. Economía de cuatro recursos, cuatro edades, aldeanos que recolectan, ejércitos con counters legibles, niebla de guerra y un mapa donde los recursos se pelean.

**Inspirado en Age of Empires II. No es un remake.** Se toman las mecánicas del género —que no son copyrighteables— y se descarta toda la expresión: arte, textos, nombres, música y estructura de campañas son originales.

El arte se produce en **3D low-poly con cámara ortográfica**, no en sprites 2D. La razón no es estética: es la única ruta donde existen assets libres animados y verificados. Está desarrollado en §4.

El marco histórico es **Iberia, 1085-1260**: la frontera entre los reinos cristianos y Al-Andalus. Es un período con identidad visual propia, asimetría militar real y documentación abundante — y el género lo trató poco.

---

## 1. La referencia: qué se toma y qué no

Age of Empires II se siente como se siente por **la economía**, no por la historia ni por los gráficos. Un RTS donde el aldeano no es la unidad más importante del juego no se parece a AoE.

### 1.1 Lo que se toma

| Pilar | Traducción a sistemas |
|---|---|
| **Cuatro recursos con depósitos físicos** | Madera, comida, oro, piedra. El aldeano carga y descarga en el centro urbano, molino o campamento. La distancia al depósito es una decisión de diseño. |
| **El aldeano es la economía** | Única unidad que recolecta y construye. Perder aldeanos es perder la partida. Atacar la economía es una estrategia legítima. |
| **Población gateada por casas** | Cada casa sube el límite. El límite inicial obliga a expandirse. |
| **Cuatro edades con costo creciente** | Cada edad desbloquea edificios, unidades y tecnologías. Subir es una inversión que se paga o se pierde. |
| **Counters legibles** | Infantería > caballería > arqueros > infantería. El jugador tiene que leer el ejército enemigo y responder. |
| **Recursos disputados** | El mapa es el tablero. Quien controla el oro, controla la partida. |
| **Información imperfecta** | Niebla y exploración. Sin scouting no hay RTS. |

### 1.2 Lo que no se toma

- Nombres de unidades, edificios, eras, campañas y escenarios de AoE.
- Textos, voces, música y arte de Microsoft.
- La estructura exacta de sus campañas.
- Sus números de balance. Se calibran jugando.

### 1.3 Booming, rushing y castling no se implementan

Son **estrategias emergentes**, no features. No existe un "sistema de rushing": existen costos, tiempos de entrenamiento, tiempos de edad y distancias que hacen que rushear sea rentable en ciertas condiciones. Si se codifica una estrategia, el juego deja de ser un RTS y pasa a ser un tutorial.

Lo que se implementa es la tabla de costos y tiempos, la curva de las edades y una IA que juega. El balance se ajusta en la fase de tuning, con partidas, no en la de arquitectura.

---

## 2. El juego

### 2.1 Bucle de una partida

| Minuto | Qué pasa |
|---|---|
| 0-5 | Explorar, recolectar, construir casas, llegar a la primera edad. |
| 5-15 | Expandir la economía, asegurar el segundo recurso, elegir build order. |
| 15-25 | Subir a la segunda edad, primer ejército, primer choque. |
| 25-40 | Disputa por el oro y la piedra, castillos, presión territorial. |
| 40+ | Cierre: asedio al centro urbano enemigo o rendición. |

**Victoria:** destruir el centro urbano enemigo. **Derrota:** perder el propio.

### 2.2 Las cuatro edades

Nombres propios, no los de AoE:

| Edad | Nombre | Desbloquea |
|---|---|---|
| I | **Aldea** | Casa, granja, molino, campamento maderero, cuartel, peón, lancero, arquero |
| II | **Villa** | Campamento minero, galería de tiro, establo, herrería, hondero, jinete |
| III | **Señorío** | Torre, muralla, ballestero, caballero, mejoras de herrería |
| IV | **Reino** | Mejoras finales, unidades de élite, producción acelerada |

### 2.3 Economía

- **Madera:** casas, edificios, arcos, ballestas.
- **Comida:** aldeanos, infantería, caballería, granjas.
- **Oro:** unidades avanzadas, tecnologías, edificios de élite.
- **Piedra:** torres, murallas, castillos.

Reglas duras: el aldeano carga 10 unidades, descarga en el depósito más cercano, las granjas se agotan y se pueden resembrar, los árboles y minas son finitos.

### 2.4 Unidades (8 en el MVP)

| Unidad | Rol | Counter |
|---|---|---|
| Aldeano | Economía | — |
| Peón | Infantería barata | Arqueros, en masa |
| Lancero | Anticaballería | Caballería |
| Arquero | Rango | Infantería lenta |
| Hondero | Rango barato, móvil | Arqueros |
| Ballestero | Rango pesado | Infantería, caballería |
| Jinete | Caballería ligera, hostigamiento | Arqueros, aldeanos |
| Caballero | Caballería pesada | Arqueros, infantería ligera |

Triángulo principal: **lancero > caballería > arqueros > infantería > lancero**. El hondero y el ballestero agregan matices sin romperlo.

### 2.5 Edificios (12 en el MVP)

Centro urbano, casa, granja, molino, campamento maderero, campamento minero, cuartel, galería de tiro, establo, herrería, torre, muralla.

### 2.6 Civilizaciones

MVP: **dos**, una jugable y una como IA.

- **Castilla** — caballería pesada, infantería de mesnada, órdenes militares. Bonus: caballeros más baratos en la tercera edad.
- **Almohades** — caballería ligera, infantería bereber, fortificación rápida. Bonus: jinetes más rápidos y torres más baratas.

La asimetría es de bonificaciones y roster, no de sistemas distintos. Dos civs que comparten motor pero se juegan distinto.

---

## 3. Marco histórico

### 3.1 Por qué Iberia

- **Identidad visual distinta:** alcázar, arco de herradura, azulejo, yesería, frente a castillo románico y muralla de sillar. Un RTS de la frontera se reconoce en una captura.
- **Asimetría militar real:** caballería pesada cristiana contra caballería ligera y infantería bereber. No hay que inventar el contraste.
- **Documentación:** crónicas de la época en dominio público y bibliografía académica abundante.
- **Poco explotado:** el género cubre Europa del norte y Japón; Iberia aparece de refilón.

### 3.2 Cronología de diseño

| Año | Hecho | Uso |
|---|---|---|
| 1085 | Toledo cae ante Alfonso VI | Escenario inicial |
| 1086 | Sagrajas / Zallaqa | Primera gran derrota cristiana |
| 1147 | Lisboa | Expansión portuguesa |
| 1212 | Las Navas de Tolosa | Punto de inflexión |
| 1229-1231 | Mallorca | Campaña naval/mediterránea |
| 1236 | Córdoba | Caída del califato |
| 1248 | Sevilla | Cierre del período |

### 3.3 Campaña

5-6 escenarios originales, con narración propia, sobre un personaje ficticio que atraviesa la frontera. Los hechos históricos son el marco; el protagonista y los diálogos son del proyecto.

**Nada de nombres de campaña, textos ni personajes de AoE.** Los hechos son de dominio público; la narración concreta de Microsoft, no.

### 3.4 Fuentes históricas

Crónicas (dominio público): *Historia Roderici*, *Crónica Najerense*, *Primera Crónica General de España*.

Bibliografía moderna: *La España musulmana* (Levi-Provençal), *The Ornament of the World* (Menocal), *Las Navas de Tolosa* (Vara Thorbeck), los volúmenes de la *Historia de España* de Menéndez Pidal.

**Wikipedia no es fuente de diseño.** Se usa para orientarse, no para fijar un dato.

---

## 4. Arte y pipeline gráfico

La sección que decide el proyecto. Un RTS con 200 unidades en pantalla es, antes que nada, un problema de producción de arte.

### 4.1 Los tres caminos

**A. 2D isométrico pre-renderizado.**
Modelos 3D en Blender, cámara ortográfica, render de cada dirección y cada frame a spritesheets. Es el look de 1999. Costo de producción alto, costo de runtime casi cero.

**B. 3D low-poly en tiempo real.**
Modelos glTF con esqueleto, animados en el motor, cámara ortográfica isométrica. Costo de producción bajo, runtime medio. El look es moderno, no pixel art.

**C. Híbrido.**
Mundo 3D en tiempo real, UI y retratos en 2D.

### 4.2 Comparación

| Criterio | A. 2D pre-render | B. 3D runtime |
|---|---|---|
| Fidelidad al look clásico | **Alta** | Media |
| Costo de una unidad nueva | 3-5 h (modelo + 8 dirs × frames + atlas) | 1-2 h (modelo + rig + clips) |
| Costo de una animación nueva | Alto (re-render completo) | **Bajo** (un clip más) |
| Consistencia entre unidades | Depende del render | **Alta** (mismo rig, misma paleta) |
| 200 unidades en M4 | Trivial | Viable |
| Iteración de arte | Lenta (render offline) | **Inmediata** |
| Dependencia de assets libres | Alta: no hay sprites animados CC0 | **Baja: hay modelos animados** |
| Curva para agentes | Alta: cada iteración es un render | **Baja: se edita y se ve** |

### 4.3 Decisión: 3D runtime (B)

Razones, en orden de peso:

1. **Existe el arte.** Quaternius *Ultimate Fantasy RTS*: 128 modelos animados y texturados, tag Medieval/Isometric, glTF. KayKit *Adventurers*: 5 personajes riggeados y animados, CC0, con pack de animaciones aparte. Es exactamente lo que no existe en 2D.
2. **Elimina el cuello de botella.** Agregar una animación es agregar un clip. Agregar una unidad es un modelo y un rig, no 160 sprites.
3. **La cámara ortográfica conserva el look.** Un RTS isométrico en 3D con cámara ortográfica a 30° se lee como isométrico. Se pierde el pixel art, no la identidad del género.
4. **Iteración real.** Un agente puede cambiar un material y ver el resultado en segundos. En el camino A, cada cambio es un render de 8 direcciones por N frames.

**Costo aceptado:** el juego no va a verse como AoE II. Va a verse como un RTS isométrico moderno y limpio. Si en el futuro se quiere el look original, el camino A sigue disponible: los modelos ya estarían hechos y solo faltaría el render.

### 4.4 La cámara isométrica, con números

La isometría no es un ángulo arbitrario: es geometría.

- **Proyección ortográfica**, no perspectiva. Sin esto, los edificios se deforman al alejar y el look se rompe.
- **Pitch 30°, yaw 45°, roll 0.**
- Un tile de 1×1 proyectado a 30° da un rombo de **2:1** exacto (alto = ancho × sin 30° = ancho / 2). El borde del rombo queda a 26,57° — el número que suele citarse como "ángulo isométrico", que es el del dibujo, no el de la cámara.
- **1 tile = 1 unidad de mundo = 1 metro.** Personaje: 1,8 m. Puerta: 1,2 m. Edificio: 3-5 tiles de huella.
- `Camera3D.projection = PROJECTION_ORTHOGONAL`, `size = 14` (tiles visibles en vertical), `near = 0.1`, `far = 200`.
- Zoom entre 8 y 30. Rotación fija en el MVP; cuatro orientaciones a 90° después.

**Consecuencias técnicas:**

- **Sin Y-sort.** El depth buffer resuelve el orden. Solo hay que ordenar lo transparente (partículas, billboards).
- **Anillo de selección:** malla plana en el plano del suelo (rotada -90° en X), nunca billboard.
- **Barras de vida:** `Sprite3D` con billboard y `no_depth_test`, o una capa 2D proyectada. Para 200 unidades, la capa 2D es más barata.
- **Sombras:** una sola `DirectionalLight3D` con `directional_shadow_max_distance = 40`. Sombras por unidad con luces puntuales son inviables a 200.
- **Niebla de guerra:** shader sobre el plano del terreno con una máscara de textura, no un TileMap. Se actualiza por chunks.

### 4.5 Inventario de assets — verificado el 2026-11-11

| Fuente | Contenido | Licencia | Comercial | Formato | Uso |
|---|---|---|---|---|---|
| **Quaternius — Ultimate Fantasy RTS** | 128 modelos animados y texturados, estética medieval isométrica | **QAL v1.0** (no CC0) | Sí, sin atribución; no se redistribuye el pack | FBX/OBJ/Blend/glTF | **Base del juego** |
| **Quaternius — Medieval Village MegaKit** | Entorno modular medieval | QAL v1.0 | Ídem | FBX/glTF | Edificios y props |
| **Quaternius — Universal Base Characters + Universal Animation Library** | Rigs humanoides retargeteables y librería de animaciones | QAL v1.0 | Ídem | FBX/glTF | Unidades propias |
| **KayKit — Adventurers** | 5 personajes riggeados y animados, 25+ accesorios | **CC0** | Sí, sin atribución | FBX/glTF | Unidades jugables |
| **KayKit — Character Animations** | Animaciones para los rigs KayKit | **CC0** | Sí | FBX/glTF | Ciclos walk/attack/die |
| **Kenney — Medieval RTS** | 120 archivos 2D | **CC0** | Sí | PNG | Referencia de layout y escala; no mezclar con 3D |
| **ambientCG / Poly Haven** | Texturas PBR, HDRIs | **CC0** | Sí | JPG/EXR | Terreno y materiales |
| **0 A.D. (Wildfire Games)** | Arquitectura y unidades históricas | **CC-BY-SA 3.0** | Sí, con atribución y copyleft | Varios | Referencia visual únicamente |

**Advertencia sobre Quaternius:** la QAL permite usar los assets en un producto comercial, pero **prohíbe redistribuirlos como pack**. Consecuencia práctica: si el repo se publica, los binarios de Quaternius no van commiteados — se descargan con un script y se listan en `.gitignore`. Un clon del repo no debe poder extraer los modelos.

**Advertencia sobre 0 A.D.:** CC-BY-SA es copyleft. Se lee como referencia, no se importa al juego.

**Regla operativa:** cada asset que entra se registra en `assets/CREDITS.md` con autor, URL de origen, licencia y fecha de verificación. Sin ficha, no entra.

### 4.6 SDXL: para qué sirve y para qué no

**Sirve** para retratos de unidad, iconos de tecnología, ilustraciones de campaña, pantallas de menú, texturas de UI y concept art que dirija el modelado.

**No sirve** para sprites isométricos animados en 8 direcciones. El modelo no mantiene identidad entre vistas. Se compensa con ControlNet, IP-Adapter y reference-only, y aun así requiere corrección manual frame por frame. Para una unidad completa (8 direcciones × ~12 frames), corregir cuesta más que modelar en 3D.

**Regla:** SDXL entra donde el output es una imagen única y estilizada. No entra donde el output es un set consistente.

**LoRAs:** antes de adoptar uno, verificar en su página (a) licencia comercial, (b) modelo base permitido, (c) si permite derivados. "Gratis" no es "usable". La licencia del modelo base (OpenRAIL-M para SDXL) permite uso comercial con restricciones de uso aceptable.

### 4.7 Reglas de consistencia visual

La consistencia no se logra eligiendo bien los packs: se logra imponiendo reglas.

1. **Una sola familia de assets.** Quaternius como base; KayKit solo si un personaje puntual lo justifica, ajustando material.
2. **Una paleta de 12-16 colores.** Un `ShaderMaterial` de terreno y edificio que la respete. Sin esto, el juego se ve como un collage.
3. **Una escala.** 1 tile = 1 m. Lo que no la respete se reescala en el import, no en la escena.
4. **Una luz.** Una direccional, un color de ambiente, una hora del día.
5. **Contorno opcional.** Un outline de 1-2 px unifica siluetas dispares y acerca el resultado al look de RTS clásico.

### 4.8 Presupuesto de performance en M4 (estimación)

| Elemento | Objetivo | Nota |
|---|---|---|
| Unidades visibles | 200 | `AnimationTree` por unidad; 200 es cómodo, 1000 no |
| Draw calls | < 400 | Un material por familia |
| Triángulos por unidad | 1.000-3.000 | Los packs low-poly están en ese rango |
| Sombra | 1 direccional, 40 m | Sin sombras por unidad |
| Simulación | 30 Hz fijo | El render corre a 60-120 |
| Animación lejana | 15 Hz o pausa | Fuera de cámara o zoom mínimo |

**`MultiMeshInstance3D` no anima esqueletos.** Sirve para props estáticos (árboles, rocas, cultivos), donde rinde muchísimo. Para unidades animadas, nodos normales.

### 4.9 El spike, en cinco días

1. **Día 1:** importar Quaternius, montar la cámara con los números de §4.4, ver un modelo a escala. *Criterio: se lee como isométrico y el personaje mide 1,8 m contra un tile de 1 m.*
2. **Día 2:** terreno con textura y grid, 200 copias del mismo personaje caminando. Medir FPS. *Criterio: 60 fps estables a zoom medio.*
3. **Día 3:** un edificio, un recurso, una orden de movimiento, un ataque. *Criterio: el bucle mínimo se entiende sin explicación.*
4. **Día 4:** selección, barras de vida, niebla, minimapa. *Criterio: 200 unidades con toda la parafernalia a 60 fps.*
5. **Día 5:** segunda pasada de arte: paleta, outline, sombras. *Criterio: una captura se reconoce como RTS medieval.*

Si el día 1 o el 2 fallan, se cae al camino A sin haber perdido más que una semana.

---

## 5. Arquitectura desde cero

### 5.1 Regla de oro: simulación y render separados

- `sim/` es datos puros. No toca nodos, `Input`, `AudioServer` ni el árbol de escena. Se instancia y simula en `--headless`.
- `view/` lee el estado y dibuja. No decide nada.
- El input escribe comandos en una cola. La simulación los consume en el tick.
- La UI lee el estado.

Esto permite tests headless, permite cambiar el render sin tocar la lógica y es la única forma sana de sostener determinismo.

### 5.2 Tick

- Timestep fijo, **30 Hz**. El render interpola.
- RNG con semilla explícita, una por partida. Nunca `randi()` global.
- Orden de iteración estable: arrays, no diccionarios con orden arbitrario.
- El determinismo se respeta desde el día uno aunque el multijugador no esté en el MVP: es lo que permite agregarlo después sin reescribir.

### 5.3 Estructura del proyecto

```
project.godot
main.tscn                    # raíz mínima
sim/
  sim_state.gd               # estado completo, sin nodos
  commands.gd                # cola de comandos
  economy.gd                 # recolección, depósitos, población
  combat.gd                  # daño, counters, proyectiles
  ages.gd                    # edades y requisitos
  pathfind.gd                # A* sobre grid + cache
  ai.gd                      # controlador de la IA
  rng.gd                     # RNG determinista
data/
  units.json
  buildings.json
  techs.json
  civs.json
view/
  world.gd                   # construye el mundo 3D desde el estado
  unit_view.gd
  building_view.gd
  camera_rig.gd
  selection.gd
  fog.gd
  healthbars.gd
ui/
  hud.gd
  minimap.gd
  menus.gd
tests/
  headless_test.gd
  sim_economy.gd
  sim_combat.gd
assets/
  CREDITS.md
```

### 5.4 Datos

**JSON como fuente de verdad** para unidades, edificios, tecnologías y costos. Se edita sin abrir el editor, se diffea, y es la base del modding.

Un cargador tipado convierte JSON en objetos al arrancar. Validación con errores claros: un ID inexistente en una receta rompe el arranque, no la partida.

`Resource` (`.tres`) solo para lo que se edita a mano en el editor y no necesita modding (tema de UI, configuración de cámara). **No** `.tres` para balance: no se diffea bien y no sirve para mods.

Esquema de una unidad:

```json
{
  "id": "spearman",
  "name": "Lancero",
  "age": 1,
  "cost": { "food": 35, "wood": 25 },
  "train_time": 22,
  "hp": 45,
  "attack": 3,
  "armor": { "melee": 0, "pierce": 0 },
  "speed": 1.0,
  "counters": { "cavalry": 2.0 },
  "requires": ["barracks"]
}
```

### 5.5 Pathfinding y formaciones

- **A\* en grid** (`AStarGrid2D`) para rutas individuales. Un mapa de 96×96 es barato.
- **Flow field** solo cuando la medición lo pida. A 200 unidades no es necesario; es la optimización para 1000+.
- **Formaciones:** offsets relativos a un ancla, no una ruta por unidad. El líder calcula, el resto sigue con separación.
- **Evitación local:** separación simple entre agentes (radio + empuje). No usar `NavigationAgent3D` para 200 unidades: cada uno es un nodo con su propio costo.
- **Cache de rutas** por tick, no por frame.

Referencias conceptuales: openage (GPL-3), 0 A.D. (GPL), OpenRA (GPL). **Se leen las ideas, no el código.**

### 5.6 Presentación

- **Selección:** caja en espacio de pantalla → raycast contra un `Plane` del suelo, no contra cada unidad.
- **Cola de órdenes** con Shift.
- **Niebla:** máscara de visibilidad en textura de baja resolución (1 texel = 2 tiles), actualizada por chunks. El shader del terreno la multiplica.
- **Minimapa:** se dibuja el `SimState` a una `Image`. No una segunda cámara.
- **Guardado:** serializar el estado a JSON con versión de esquema. Determinista y reproducible.

### 5.7 Multijugador

Fuera del MVP, por decisión. Cuando entre: **lockstep determinista** — ticks fijos, solo comandos por red, checksum por tick para detectar desync. El state-sync de Godot (`MultiplayerSynchronizer`) no sirve para RTS.

Diseñar para esto ahora cuesta cero (RNG con semilla, tick fijo, comandos en cola). Implementarlo ahora cuesta meses.

---

## 6. Legal

**No se puede usar:**

- La marca "Age of Empires", sus logos e íconos.
- Arte, música, sonidos, textos, nombres de campaña o de escenario de Microsoft.
- Los nombres de unidad que AoE acuñó como identidad propia. Los términos históricos genéricos sí; conviene elegir nombres propios.
- Los nombres de las eras de AoE como conjunto (Oscura, Feudal, Castillos, Imperial). Por separado son genéricos; juntos son la firma del juego.

**Sí se puede usar:**

- Mecánicas del género: recolección, construcción, edades, tecnología, combate, niebla. Las mecánicas no son copyrighteables.
- Hechos históricos, batallas, personajes y cronologías.
- Assets CC0, QAL y CC-BY, cada uno con su condición.

---

## 7. Alcance y etapas

### 7.1 MVP

- 2 civilizaciones (1 jugable, 1 IA).
- 4 edades, 8 unidades, 12 edificios.
- 1 mapa de 96×96 con recursos disputados.
- IA con tres dificultades.
- Niebla, minimapa, guardado y carga.
- Audio: música de ambiente y SFX.
- **Sin multijugador, sin campaña, sin editor de mapas.**

Criterio de terminado: una partida completa de principio a fin, sin placeholders, sin crashes, a 60 fps con 200 unidades, y el jugador entiende qué hacer sin leer un manual.

### 7.2 Etapas

| Etapa | Entregable | Criterio de aceptación |
|---|---|---|
| **E0** | Spike gráfico (§4.9) | 200 unidades a 60 fps, cámara ortográfica, captura reconocible |
| **E1** | Esqueleto de simulación | Tick 30 Hz, comandos, dos unidades moviéndose, test headless |
| **E2** | Economía | 4 recursos, aldeano, depósitos, casas, 4 edades |
| **E3** | Combate | 8 unidades, counters, proyectiles, muerte, victoria |
| **E4** | IA | 3 dificultades, build order, oleadas, cierre de partida |
| **E5** | Presentación | UI completa, audio, minimapa, niebla, menús |
| **E6** | Cierre | Guardado, balance, export `.app`, sin crashes |

Cada etapa termina con tests verdes y una captura. Sin captura no hay etapa cerrada.

### 7.3 Estimación

| Etapa | Horas (estimación) |
|---|---|
| E0 Spike | 20-30 |
| E1 Simulación | 60-80 |
| E2 Economía | 50-70 |
| E3 Combate | 50-70 |
| E4 IA | 50-70 |
| E5 Presentación | 70-90 |
| E6 Cierre | 50-70 |
| **Total** | **350-480** |

Orden de magnitud, no compromiso. Es un proyecto de varias sesiones, no de una.

### 7.4 Fuera de alcance (lista cerrada)

Campaña, multijugador, editor de mapas, tercera civ, unidades navales, asedio con mecánicas propias, mods, localización. Lo que no está acá no entra sin una decisión explícita.

---

## 8. Riesgos

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| El look 3D no convence y se extraña el pixel art | Media | Spike de 5 días antes de comprometerse; el camino A queda abierto |
| Los assets no cubren la Iberia medieval | Media | Auditar el pack completo el día 1; modelar solo lo faltante |
| 200 unidades no llegan a 60 fps | Baja | Medir el día 2, antes de construir encima |
| El alcance crece | **Alta** | §7.4 es una lista cerrada |
| Licencias mal registradas | Media | `assets/CREDITS.md` obligatorio |
| La IA no cierra partidas | Media | Criterio de aceptación en E4: una partida termina sola |
| El proyecto se estanca en el arte | Media | El arte es una capa: primero el bucle, después la belleza |

---

## 9. Fuentes y correcciones a la investigación

**Verificadas el 2026-11-11:**

- `godotengine.org/download/macos` — builds Apple Silicon. Versión local: `4.7.2.stable.official.ed1daf0bf`.
- `kenney.nl/assets/medieval-rts` — 120 archivos, 2D, CC0.
- `kaylousberg.itch.io/kaykit-adventurers` — 5 personajes riggeados y animados, CC0, FBX/glTF.
- `quaternius.com/license.html` — QAL v1.0, 2026-08-28.
- `quaternius.com/packs/ultimatefantasyrts.html` — 128 modelos animados y texturados.
- `quaternius.com` — catálogo medieval: Village MegaKit, Universal Base Characters, Universal Animation Library.

**Correcciones a la investigación previa:**

- Los links de assets eran mirrors (`assethoard`, `assetsdownload`), no las fuentes.
- `OpenDungeons` es un clon de Dungeon Keeper: no pertenece al género.
- "Las campañas van desde el 8000 a.C." es falso: AoE II cubre ~400-1600 d.C.
- "Alta Edad Media 1000-1300" es Plena Edad Media.
- Hastings, Manzikert y la Tercera Cruzada son escenarios de AoE II: no sirven como "contenido original".
- Quaternius **ya no es CC0**: es QAL v1.0 desde el 28/08/2026.

**Referencias conceptuales (no código):**

- `github.com/SFTtech/openage` — GPL-3.0. Reimplementación del motor de AoE II.
- 0 A.D. / Wildfire Games — RTS histórico open source; arte CC-BY-SA 3.0.
- OpenRA — RTS open source; pathfinding en grid y formaciones.

**Descartadas:** mirrors de assets; Wikipedia, Fandom, Instagram, Medium y YouTube como fuente técnica; listas de LoRAs sin licencia verificada en la página del autor.

---

## 10. Decisiones abiertas

| # | Decisión | Recomendación |
|---|---|---|
| 1 | Nombre definitivo | "Reinos de la Frontera" es provisional; verificar que no colisione si se publica |
| 2 | ¿Proyecto personal o publicable? | Define licencias y esfuerzo de arte; no bloquea el arranque |
| 3 | ¿Una o dos civs en el MVP? | **Dos** (una jugable, una IA): prueba que el sistema soporta más de una |
| 4 | ¿Rotación de cámara? | **No** en el MVP; cuatro orientaciones después |
| 5 | ¿Campaña en algún momento? | Fuera del MVP; el marco histórico la deja lista |
| 6 | ¿Se publica el repo? | Si sí, Quaternius va por script y `.gitignore` |

---

## 11. Prompt de apertura de sesión

_Listo para pegar en una sesión nueva. Diseñado para lanzar la construcción con varios agentes._

```
iniciar sesión. Proyecto NUEVO desde cero: "Reinos de la Frontera", RTS medieval
isométrico en Godot 4.7.2 nativo en macOS Apple Silicon (Mac mini M4, 24 GB).

Leé completo docs/reinos-de-la-frontera-documento-de-arranque.md antes de
responder. Manda sobre cualquier conversación previa.

NO HAY CÓDIGO PREVIO. No hay assets previos. No se reutiliza nada de otro
proyecto del workspace, ni código, ni arte, ni datos, ni narrativa. El repo se
crea de cero en projects/reinos-de-la-frontera/.

REGLAS QUE NO SE NEGOCIAN
- Godot 4.7.2.stable.official.ed1daf0bf, ya instalado.
- Nada de Microsoft: ni arte, ni textos, ni nombres, ni música.
- No se copia código de openage (GPL-3), 0 A.D. (GPL) ni OpenRA (GPL). Se leen
  las ideas, no el código.
- Cada asset que entra se registra en assets/CREDITS.md con autor, URL, licencia
  y fecha. Sin ficha no entra.
- Textos de UI en español. Código, identificadores y commits en inglés.
- El proyecto vive en projects/reinos-de-la-frontera/, con repo propio y
  .knowledge/ propio.

CÓMO SE TRABAJA ESTO
Es un programa multi-sesión. Antes de ejecutar, llamá al Planner (kanam-planner)
para que produzca el plan por etapas con dependencias y criterios de aceptación.
La implementación va por el pipeline A/B: un agente escribe, otro revisa, y el
CORE verifica el repo antes de dar nada por hecho. El CORE no implementa.

FASE 0 — ARRANQUE (esta sesión)
1. Crear el repo y el esqueleto de carpetas de la sección 5.3, vacío, sin lógica.
2. Verificar Godot y dejar el proyecto abriendo en una escena mínima.
3. Confirmar o corregir las seis decisiones abiertas de la sección 10.
4. Entregar el plan del spike (E0) con tareas, responsables y criterios medibles.

FASE 1 — SPIKE GRÁFICO (la siguiente sesión)
Los cinco días de la sección 4.9: cámara ortográfica a 30 grados, un modelo a
escala, 200 unidades caminando, FPS medidos en la M4, una captura por día.
Ese spike decide si el camino es 3D runtime o 2D pre-render. No se construye
nada encima hasta que el spike pase.

FASE 2 — SIMULACIÓN
Recién con el spike aprobado: tick fijo a 30 Hz, estado sin nodos, comandos en
cola y tests headless. Ese es el esqueleto sobre el que entra todo lo demás.

QUÉ QUIERO DE ESTA SESIÓN
1. El repo creado y abriendo, con la estructura vacía y un README honesto.
2. Las decisiones de la sección 10 confirmadas o corregidas, con motivo.
3. El plan de E0 y E1, con criterios de aceptación testeables.

No empezar por el arte ni por la UI. Se empieza por lo que puede matar el
proyecto: el spike de render y el esqueleto de simulación.
```

---

*Documento de arranque. Se actualiza cuando una decisión de §10 se cierra.*
