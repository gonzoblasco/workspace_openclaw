# Pipeline de sprites isométricos con Blender

**Fecha:** 2026-11-12
**Origen:** proyecto `abya-yala` (Godot, RTS isométrico), archivado el 2026-11-12
tras 46 commits. Este documento salva la técnica, no el código del juego.
**Alcance:** conocimiento transferible. Si se reabre un proyecto isométrico, se
reimplementa desde acá en horas, no en semanas.

> El juego no convenció. La fábrica de sprites sí: es lo único de ese repo que
> vale la pena reconstruir en el próximo proyecto.

---

## 1. La matemática isométrica, resuelta

La cámara que produce un diamante 2:1 exacto — el mismo ratio que cualquier tile
isométrico estándar:

```
Cámara ortográfica, azimut 45°, elevación 30°.
Para un cuadrado horizontal, altura/anchura proyectada = sin(elevación).
sin(30°) = 0.5  →  ratio 2:1  ← el diamante del tile.

1 unidad Blender = 1 tile.
ortho_scale = 5.657   (= 8·√2, elegido para que 1 tile mida 128 px
                       en el render final)
Render 1024 → downscale al tamaño de juego.
```

**Verificado contra dos proyectos hermanos** (`caesar3-clone`,
`edad-de-los-reinos`) que llegaron a los mismos números por separado. No es una
receta inventada.

### El corolario que sorprende

Un tile de 129 px de **ancho** mide solo **64.6 px de alto**. Cualquier cálculo
que cruce ancho con alto explota por un factor de 2. Los edificios y las
unidades deben escalar **ancho contra ancho**, o alto contra alto. Mezclar
dimensiones produjo en este proyecto un sprite de guerrero 2.6× más grande que
la casa al lado de la cual debía caminar, y el bug pasó dos revisiones porque el
test medía la cosa equivocada.

---

## 2. Reglas del render que costaron iteraciones

### 2.1 La elevación depende del sujeto

| Sujeto | Elevación | Por qué |
|---|---|---|
| Edificios | **30°** | se leen bien y muestran la fachada |
| Personajes | **18°** | a 30° mirás la coronilla y la cara desaparece |

Sin cara no hay dirección de mirada, y sin dirección de mirada un personaje
quieto parece un adorno.

### 2.2 Las cuatro direcciones son cuatro cámaras, no cuatro rotaciones

Rotar el modelo arrastra la iluminación con él: una unidad caminando al norte
quedaría iluminada distinto que una caminando al este. **Se rota la cámara, la
luz queda fija al mundo.**

```python
FACINGS = {
    "s": 45.0,   # de frente (la vista única de siempre)
    "e": 135.0,  # hacia la derecha de la pantalla
    "n": 225.0,  # de espaldas
    "w": 315.0,  # hacia la izquierda
}
```

### 2.3 La escala es del modelo, no de la vista

Un guerrero de perfil ocupa menos píxeles de ancho que el mismo guerrero de
frente (0.457 vs 0.506 tiles en la medición real). Si la escala se deriva del
ancho de cada vista, **el personaje crece al doblar la esquina**.

Regla: el ancho del manifest se toma como el **máximo de las cuatro vistas**, y
ese único valor se aplica a todas. La silueta cambia; el tamaño, no.

### 2.4 El ancla la calcula la cámara, nunca el ojo

`world_to_camera_view` proyecta el origen del suelo (0,0,0) y ese punto va al
`manifest.json` como `anchor_px`. Un offset medido a mano (`-alto * 0.5 + 8`)
fue la causa de un bug de anillo de selección que se persiguió durante días. Un
ancla proyectada elimina la clase entera de error.

Y ojo: el ancla se recalcula **después del recorte**, no antes. Recortar y
conservar el ancla del frame original desplaza todo sprite por lo que se cortó
de arriba.

### 2.5 Detalle a resolución alta, entrega a resolución de juego

Renderizar a 1024 y bajar a 129 px da margen para antialiasing y perfilado que
un sprite pintado a tamaño final no tiene. La silueta queda limpia.

---

## 3. Anatomía de un personaje legible

Lo que hizo que las unidades se leyeran a 74 px:

| Rasgo | Regla |
|---|---|
| Proporción | cabeza ≈ 1/7 de la altura total. Es la señal de "persona" más fuerte |
| Hombros | más anchos que la cintura; sin esto la figura es un rectángulo |
| Piernas | separadas, con hueco visible. Pegadas se leen como pollera |
| Brazos | despegados del cuerpo, si no la silueta es una losa |
| Casco | **cúpula baja**, nunca esfera completa: la esfera se traga la cara |
| Rol | el pose tiene que llevar la información de juego |

Los cuatro roles del proyecto, y qué los distinguía:

- **Aldeano** — sin armas, cesta en la cadera
- **Guerrero** — escudo redondo con umbo, maza en alto
- **Arquero** — arco tensado, el único con un elemento horizontal
- **Jefe** — manto, capa, estandarte en asta

El **único elemento horizontal** como firma del arquero es un truco reusable:
en una multitud de siluetas verticales, la que rompe el eje se encuentra sola.

---

## 4. La fábrica: estructura del pipeline

```
tools/blender/render_*.py     → Blender headless, escribe .preview/blender_*/
                                 (PNG 1024 transparente + meta.json con
                                  ángulo, resolución y anchor_px proyectado)
tools/blender/postprocess_*.py → recorta, escala, hornea sombra, aplana a RGBA
                                 y escribe assets/sprites/*/manifest.json
```

Decisiones que conviene conservar:

- **`meta.json` lo escribe el render; `manifest.json` lo escribe el post-proceso.**
  Son dos etapas y dos archivos. Confundirlos produjo un bug real: 48 sprites
  renderizados que el juego nunca levantó porque el manifest seguía viejo.
- **La sombra se hornea en post-proceso**, con tamaño derivado de la huella, no
  dibujada en la escena. Sale más barata y más consistente.
- **Blender no entra al runtime.** Es una fábrica offline: si el resultado no
  combina, se descarta y los sprites viejos quedan. Riesgo cero.
- **Los PNG se versionan.** La difusión y el render no son bit-reproducibles
  entre GPUs; el repo es la garantía, no la seed.

---

## 5. El error de método que más caro salió

> **Verificar la magnitud derivada, no la fuente.**

El test de "escala estable entre direcciones" hacía lo correcto: llamaba a
`unit_scale()` —la escala que el juego aplica de verdad— y comparaba la vista
frontal con la de perfil. Falló en rojo apenas el bug existió, y fue lo que
atrapó que el personaje crecía al girar.

El error fue mío, no del test: **miré el manifest en vez de la salida del test.**
Al ver que `art_tiles_w` no se movía (porque se mide antes del resize) concluí
que el arreglo no había funcionado, cuando el arreglo estaba bien y el número
que yo vigilaba no era el que importaba.

La lección general: la pregunta correcta es **"¿qué valor ve el juego?"**, nunca
**"¿qué dice el archivo intermedio?"**. Cuando un número no se mueve después de
un cambio que debería moverlo, la primera sospecha tiene que ser que se está
midiendo el lugar equivocado.

---

## 6. Qué sobrevive de abya-yala

Útil si se reabre algo parecido:

- La matemática de §1, ya resuelta y verificada contra dos proyectos
- Las reglas de render de §2, cada una con su bug detrás
- La anatomía de personaje de §3
- La separación render/post-proceso de §4
- **El criterio de escala:** ancho contra ancho, alto contra alto, jamás cruzado

Lo que **no** vale la pena arrastrar: el diseño de civs, el mapa, el modelo de
juego, la deuda técnica del `game.gd` monolítico. El proyecto se archiva entero.

---

## 7. Si se retoma: por dónde empezar

1. **La cámara primero.** §1 en 20 líneas de Python. Sin esto resuelto, todo lo
   demás se rehace.
2. **Un edificio y un personaje**, no un set completo. Ajustar elevación (30° vs
   18°) sobre esos dos.
3. **El ancla proyectada** antes de poner un solo sprite en el juego.
4. **Las cuatro direcciones** desde el inicio. Agregarlas después obliga a
   re-renderizar todo y a migrar el manifest.
5. **Los tests, contra la magnitud final.** Ver §5 antes de escribir el primero.

---

_Registrado al archivar `abya-yala`, 2026-11-12. Si el proyecto se borra, esto
queda._
