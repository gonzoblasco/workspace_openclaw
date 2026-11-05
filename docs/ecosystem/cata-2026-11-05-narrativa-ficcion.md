# Cata 2026-11-05 (3): narrativa de ficción - quién escribe bien CF, thriller y terror

**Estado:** medido. Hay un ganador por criterio, no un ganador único.
**Origen:** decisión de Gonzo (2026-11-05): *"quiero probar esto, buscar el mejor para narrativa de ficción.. me gusta la ciencia ficción, los thrillers y el terror"*
**Precedente:** la cata de §3 de `cata-2026-11-05-auditoria-camino-y-gemma4.md` mostró que `muse-spark-open` inventa un mundo coherente con contexto parcial ("Kimi Antonelli en Mercedes"). De ahí la pregunta: **si inventa mundos, ¿los inventa bien?**
**Harness:** `/tmp/cata_narrativa2.py` (temporal; los tres prompts van copiados acá)

---

## Método, y su primera lección

5 modelos × 3 géneros, `temperature=0.75`, `top_p=0.9`, `num_predict=4000`, `think=false`.

**La primera corrida falló entera, y por una razón que no era del modelo:** con `num_predict=1600`,
cuatro de los cinco modelos gastaron los 1.600 tokens **pensando** y devolvieron `content` vacío
(glm: 7.012 caracteres en `thinking`, cero en `content`). Las respuestas "vacías" eran presupuesto
de tokens mal asignado, no incapacidad.

Y con `think:false`, **el thinking no se apaga en todos**: `minimax` pensó 16.522 caracteres y
`gpt-oss` 13.408 en el probe de terror, con `think:false` en el payload. Es la misma propiedad que
ADR-102 documentó de minimax: *always-on*, `think:false` no lo apaga. **Se ve en la cuenta.**

## Resultados

| Modelo | CF-1 | TH-1 | TE-1 | Formato limpio | Prosa real |
|---|---|---|---|---|---|
| `muse-spark-open` | 499 p | 434 p | 484 p | **9/9** | **9/9** |
| `deepseek-v4.1-flash` | 475 p | 371 p | 392 p | **9/9** | **9/9** |
| `gpt-oss:120b` | 443 p | 514 p | **0 p** | 5/6 | 5/9 |
| `minimax-m3.1-flash` | 619 p | 1.111 p | **96 p** | 6/9 | 3/9 |
| `glm-5.3-flash` | 2.137 p | 2.711 p | 2.785 p | **0/9** | 0/9 |

**"Formato limpio"** = sin viñetas ni numerales en el texto final. **"Prosa real"** = sin
contaminación con el razonamiento (frases como *"The user wants..."*, *"Let me write..."*,
*"Final text:"* pegadas dentro del cuento).

### Los dos que pierden, y por qué

- **`glm-5.3-flash` no escribe: planifica.** Las nueve salidas son el plan en inglés
  (*"The user wants the first 400 words..."*), con hasta **28 viñetas**, 2.100-2.800 palabras de
  instrucciones y **cero párrafos de cuento**. Contaminación: 21, 12 y 28 marcas por pieza. No es
  un problema de calidad literaria: no produce el artefacto.
- **`minimax-m3.1-flash` mezcla idiomas y se traba.** Su CF arranca *"once años粘连 al cinturón"*
  y sigue con *"lasExpansion Thermal"*, *"una respiración Tartamuda"*, *"la法国"* y un `</mm:think>`
  incrustado. En terror: 16.522 caracteres de razonamiento y **96 palabras de output**. Pensó más de
  dos minutos y entregó un fragmento.
- **`gpt-oss:120b` escribe bien dos de tres y desaparece en el tercero.** CF y thriller son prosa
  sólida, limpia, sin contaminación. Terror: 13.408 caracteres de thinking y **cero palabras**.
  Un modelo de narrativa que se cuelga en un género no sirve para un slot.

### Los dos que quedan

**`muse-spark-open`** - 9/9 limpio, sin pensamiento visible, la única pieza que cumplió el
requisito de la última línea de una sola frase seca:

> *La cama estaba hecha y alguien dormía en ella.*

…que además es el giro que el prompt pedía (cambia lo que el lector cree saber sin explicarlo).
En CF abrió con *"un pitido que no correspondía a ninguna de las balizas registradas... tres notas
ascendentes y una pausa larga que vibraba en los dientes"*: la señal se describe por su efecto en el
cuerpo, no por su explicación. En thriller resolvió el giro con el monitor grabándolo de espaldas -
y cerró con *"La puerta del baño del despacho se abrió detrás de él."*

**`deepseek-v4.1-flash`** - 9/9 limpio, el más rápido de los dos (3,7-5 s contra 12-26 s), y el
único que respetó **todas** las restricciones prohibidas del thriller: cero apariciones de
"tensión", "nervioso", "miedo" y "silencio", que `glm` y `minimax` usaron a mansalva. Su terror:

> *Pero el yeso frente al que él miraba tenía una mancha de humedad con forma de hombro, y Lucía
> pensó, sin permitirse pensarlo del todo, que la mancha estaba a la altura exacta de una espalda
> apoyada.*

Y la última línea: *"Fue a buscar la silla."* -seca, sin adjetivos, como se pidió- que obliga a
preguntarse qué va a encontrar.

## La distinción que decide el slot

**Las dos piezas de deepseek usan el género correcto pero el método de siempre: el informe.** La
enfermera *"hizo el cálculo"*, *"revisó mentalmente la logística"*, el perito piensa en
procedimientos. Y está bien, porque el prompt del thriller **pedía pensar en procedimientos**. Pero
en terror se le filtró: deepseek explica *por qué* da miedo (la mancha, la barandilla, el freno)
antes de que el lector lo sienta. Muse no explica: **pone al personaje a mirar y deja el miedo al
lector.**

**Esa es la diferencia que importa para narrativa de ficción** -y no es "creatividad", que es una
palabra que no se puede medir. Es **si el texto le explica al lector o le deja sentir**. Deepseek
narra como documenta; muse narra como alguien que ve la escena.

## Decisión

| Uso | Modelo | Por qué |
|---|---|---|
| **Narrativa de ficción** (CF, thriller, terror) | **`muse-spark-open`** | 9/9 limpio, pensamiento invisible, el único que cumplió el requisito de la última línea seca, y no explica el miedo |
| **Borradores narrativos / iteración rápida** | `deepseek-v4.1-flash` | 9/9 limpio, 4 s por escena, respeta prohibiciones de vocabulario al pie de la letra |
| Redacción con voz (no ficción: LinkedIn, cartas) | `muse-spark-open` | ya en ADR-109 §3, mismo criterio: produce prosa que se sostiene sola |
| **Nunca** para narrativa | `glm-5.3-flash` (planifica), `minimax-m3.1-flash` (se traba), `gpt-oss:120b` (se cuelga en terror) | no producen el artefacto |

**Muse queda en tres slots:** auditoría de camino, redacción con voz y narrativa. Es mucho para un
solo modelo, y el riesgo ya está escrito en ADR-109: si alguna vez muse audita un texto que muse
escribió, ese caso necesita un tercero. Con narrativa se agrega la misma condición: **narrativa de
muse no se audita con muse.**

## Límites de la evidencia

- **Una corrida por modelo y género.** Temperature 0.75 sin repeticiones: esto es direccional, no
  una cata con varianza. El veredicto de "glm planifica" es sólido (9/9 salidas son el plan); el de
  "muse > deepseek" es una diferencia de calidad que **una sola lectura humana puede discutir**.
  Gonzo tiene que leer las seis piezas y decir si coincide.
- **400 palabras no es un cuento.** No mide estructura larga, voz sostenida en 5.000 palabras, ni
  capacidad de resolver un final en el punto correcto. El próximo paso real es pedir un cuento de
  2.000-3.000 palabras a los dos finalistas y comparar.
- **`think:false` en el payload no apaga el thinking de minimax ni de gpt-oss.** Cualquier slot de
  narrativa tiene que verificar `thinking` en la respuesta, no confiar en el parámetro.
- **No se midió con `num_predict=1600`**: ese presupuesto hace que casi todos devuelvan vacío. El
  slot de narrativa necesita presupuesto alto declarado, igual que el de auditoría.
