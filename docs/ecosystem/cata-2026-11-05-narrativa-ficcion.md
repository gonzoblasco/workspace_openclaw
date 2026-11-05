# Cata 2026-11-05 (3): narrativa de ficción - quién escribe bien CF, thriller y terror

**Estado:** medido. Hay un ganador por criterio, no un ganador único.
**Origen:** decisión de Gonzo (2026-11-05): *"quiero probar esto, buscar el mejor para narrativa de ficción.. me gusta la ciencia ficción, los thrillers y el terror"*
**Precedente:** la cata de §3 de `cata-2026-11-05-auditoria-camino-y-gemma4.md` mostró que `muse-spark-open` inventa un mundo coherente con contexto parcial ("Kimi Antonelli en Mercedes"). De ahí la pregunta: **si inventa mundos, ¿los inventa bien?**
**Harness:** `/tmp/cata_narrativa2.py` (temporal; los tres prompts van copiados acá)

> **⚠️ CORREGIDO EN §5 (2026-11-05, mismo día).** Las secciones 1-4 se corrieron con `think=false`.
> Repetida la cata con `think="low"`, **dos veredictos se dan vuelta**: `glm-5.3-flash` **sí escribe**
> (con `false` planificaba) y `gpt-oss:120b` **no se cuelga en terror** (era presupuesto de tokens).
> Y `deepseek` **se hunde**: 19,75 tok/palabra y un vacío cada tres prompts. Leer §5 antes de usar
> cualquier conclusión de abajo. Las secciones 1-4 quedan como registro del error, no como veredicto.

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

---

## 5. `think=low`: la corrección que invierte dos veredictos

La cata de arriba se corrió con `think=false`. Gonzo pidió repetirla **con `think="low"` en los
siete modelos**, y el resultado no confirma la primera: **dos veredictos se dan vuelta y uno se
hunde.**

Mismos tres prompts, `num_predict=6000`, `temperature=0.75`.

| Modelo | out (off) | out (low) | s (off) | s (low) | Vacíos | tok/palabra |
|---|---|---|---|---|---|---|
| `gemma4` | — | **1.542** | — | **9,6** | 0 | **1,40** |
| `gpt-oss:120b` | 7.402 | **2.502** | 30 | **12,0** | 0 | **1,44** |
| `minimax-m3.1-flash` | 7.855 | 14.005 | 184 | 88,8 | 0 | 1,51 |
| `glm-5.3-flash` | **12.000** | **2.141** | 114,5 | **21,0** | 0 | 1,58 |
| `muse-spark-open` | 4.100 | **3.318** | 60,1 | 56,4 | 0 | 2,32 |
| `deepseek-v4.1-flash` | 2.021 | **15.881** | 13,1 | 59,2 | **1** | **19,75** |
| `nemotron-3-super` | — | 18.000 | — | 125,5 | **3** | ∞ (0 palabras) |

### 5.1 `glm-5.3-flash` no estaba roto: estaba mal invocado

La sección anterior lo descartó con "planifica en vez de escribir" (9/9 salidas eran el plan en
inglés). **Con `think="low"` escribe.** Verificado tres veces en el mismo prompt, con los tres
ajustes:

| `think` | Palabras de cuento | `thinking` | Segundos | Resultado |
|---|---|---|---|---|
| `false` | **0** (1.762 de plan en inglés) | 0 | 31,0 | plan, no cuento |
| `"low"` | **309** | 41 caracteres | **8,0** | prosa limpia, `done_reason: stop` |
| `"medium"` | 330 | 8.948 caracteres | 31,6 | prosa, pero 200× más pensamiento |

Con `think:false` glm no piensa *y* no escribe: el modelo usa el stream de salida para razonar.
Con `"low"` piensa 41 caracteres y escribe. **Un modelo descartado por un parámetro de invocación,
no por su capacidad.** Es exactamente el error que la regla de §2 del AGENTS.md prohíbe: verificar
contra el repo antes de afirmar, y acá el "repo" era el parámetro.

Y escribe bien. Su terror cierra así:

> *A las 4:15, cuando pasó de nuevo, la silla estaba frente a la pared de la habitación. Ferrari
> sentado, mirando la pared nueva. Los sensores intactos.*
>
> *Nadie lo había levantado.*

Giro limpio, sin adjetivos, sin explicar. Su thriller cierra con una voz que contesta desde el
living y un cadáver que "supuestamente" está en Bariloche: **el giro que el prompt pedía** (cambia
lo que el lector cree saber). glm con `low` no es el último: es candidato.

### 5.2 `deepseek` se hunde con `think=low`, y es el hallazgo incómodo

Con `think:false` era el segundo mejor (1,63 tok/palabra, 13 s en tres prompts, 9/9 limpio).
Con `think="low"`:

- **49.789 caracteres de razonamiento** en los tres prompts (17.139 + 12.408 + 20.242).
- **15.881 tokens de salida** para 804 palabras: **19,75 tok/palabra, 12× más que con thinking off.**
- **Un prompt vacío**: terror con 20.242 caracteres de pensamiento y cero palabras de cuento.
- **59 s** contra 13 s.

**"Low" no es bajo en deepseek.** El nivel `low` abre el razonamiento y lo deja correr; el único
ajuste que lo apaga es `false`. Un slot con `think="low"` en deepseek gasta **ocho veces** lo que
gasta con `false`, y una de cada tres veces no entrega.

Y explica la observación de Gonzo sobre el panel: **26 requests de muse pesan menos que 134 de
deepseek.** No es que muse sea más barato por token; es que **deepseek gasta tokens en pensar lo
que no escribe**, y el panel lo cobra igual.

### 5.3 Lo que `think=low` NO arregla

- **`muse` es estable en los dos modos** (4.100 → 3.318 tokens, 0 vacíos, 2,32 tok/palabra): su
  pensamiento es corto y proporcional (5.616 caracteres en tres prompts, contra 49.789 de deepseek).
  Sigue siendo el mejor en calidad de prosa y el que menos varía.
- **`gpt-oss` mejora en todo y es el más económico de los buenos** (1,44 tok/palabra, 12 s, 0 vacíos).
  **Corrección a la sección anterior: no "se cuelga en terror"** — con `low` entrega 640 palabras.
  Con `num_predict=4000` y `think:false` gastó el presupuesto pensando. Era el harness, otra vez.
  Lo que sí tiene: **2 tell de emoción explícita** ("sintió una corriente de aire frío", "la sombra
  se alargó... el silencio lo había protegido"), y su cierre explica el misterio en vez de dejarlo.
- **`gemma4` escribe bien y barato** (1,40 tok/palabra, 9,6 s, la mejor economía del cuadro) pero
  **es el que más dice en vez de mostrar**: 3 tell de emoción, incluido *"el pánico comenzó a
  filtrarse en su mente"* — que es literalmente lo que el prompt prohibía. Barato y explícito.
- **`minimax` sigue roto**: 23 viñetas en el terror, 3 marcas de contaminación, 6.000 tokens gastados
  y 4.528 palabras que no son un cuento. Y con `low` pensó 6.385 caracteres igual.
- **`nemotron-3-super` está muerto para esto**: 66.929 caracteres de razonamiento, **cero palabras
  en los tres prompts**. Es el mismo patrón que lo descartó en auditoría de camino: piensa sin parar
  y no entrega el artefacto.

### 5.4 Veredicto corregido

| Uso | Modelo | `think` | Por qué |
|---|---|---|---|
| **Narrativa de ficción** | **`muse-spark-open`** | `false` o `"low"` (estable) | mejor prosa, el único que no explica el miedo, 0 vacíos en 6 corridas |
| **Alternativa de calidad** | **`glm-5.3-flash`** | **`"low"` obligatorio** | con `false` planifica; con `low` escribe prosa limpia en 8 s y con giros que cumplen |
| **Borradores rápidos / volumen** | `gpt-oss:120b` | `"low"` | 1,44 tok/palabra, 4 s por escena, el más barato de los que escriben bien |
| **Económico pero explícito** | `gemma4` | `false` | 1,40 tok/palabra y 3 s, pero *dice* la emoción en vez de mostrarla |
| **Nunca** | `deepseek` con `"low"` · `minimax` · `nemotron` | — | 19,75 tok/palabra con un vacío cada tres · se traba · no entrega nada |

**La lección que vale más que el slot:** en la primera cata descarté dos modelos por rendimiento
cuando el problema era **el parámetro de invocación**. `glm` no planifica porque no sepa escribir:
planifica cuando nadie le deja pensar. Y `gpt-oss` no se cuelga en terror: se cuelga cuando el
presupuesto de tokens es menor que lo que necesita para pensar. **Antes de descartar un modelo por
su salida, se revisa la invocación.**
