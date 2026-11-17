# Plantilla de voz - Perfil García Márquez (*Crónica de una muerte anunciada*, 1981)

> **Que es esto:** la traducción ejecutable del Eje 5 del caso 08.
> **Fuente:** `studies/narrative-engineering/caso-08-cronica-muerte-anunciada.md`.
> **Estado:** v1, **sin validar**.

---

## 1. La trampa principal

García Márquez tiene la mediana más alta de los cinco (21) y **la frase más larga más corta de los
tres altos** (56, contra 60 de Rowling y 102 de Echeverría).

**La firma no es "frases largas": es "períodos largos parejos, casi sin frases cortas".**

| Banda | Objetivo |
|---|---|
| ≤6 palabras | **8%** ← el mínimo de los cinco |
| 7-15 | 28% |
| 16-30 | **38%** |
| 31+ | 26% |

**Regla dura #1:** si el texto tiene más del 15% de frases de 6 palabras o menos, no es esta voz.
No hay picos: no hay frases de 90 que compensen las de tres palabras.

## 2. Ritmo (medido)

| Métrica | Objetivo | Tolerancia |
|---|---|---|
| Mediana | **21** | 18-24 |
| Media | 22,2 | 19-26 |
| Frases ≤6 | **8%** | 4-14% |
| Frases 7-15 | 28% | 21-35% |
| Frases 16-30 | 38% | 31-45% |
| Frases 31+ | 26% | 19-33% |
| Frase más larga | 56 | hasta 70 |

**Cómo se arma el período de García Márquez:**
- **Por coordinación con matiz**, no por subordinación profunda. Encadena con `y`, `pero`, `porque`,
  sin anidar.
- **Por la cifra exacta dentro de la frase:** *"se levantó a las 5.30 de la mañana"*, *"veintisiete
  años después"*. La precisión numérica es ritmo y es verosimilitud a la vez.
- **Por la contradicción interna:** *"Muchos sabían que lo iban a matar, y no lo creían"*. Dos
  verdades opuestas en una oración.

## 3. Diálogo

- **Casi no hay diálogo escenificado: 6% de las palabras.**
- **El diálogo va citado dentro del reporte**, con comillas angulares («»): *«Le recordé que era
  lunes», me dijo.*
- **El narrador siempre atribuye:** *me dijo*, *me contó*, *recordaba*, *aseguró*. Es periodismo.
- **Nunca dos personas hablando solas.** Siempre hay un narrador que recolecta.

## 4. Punto de vista

- **Primera persona testigo** que reconstruye: "yo", "me dijo", "mi madre".
- **Nunca entra en la cabeza de nadie:** no hay pensamiento de personajes, hay **declaraciones**.
- **El pensamiento del narrador es duda, no emoción:** "nunca supe", "no logré saber", "me pareció".
- **El arco es del narrador, no del protagonista.** Quien cambia es el que cuenta.

## 5. Lo que García Márquez hace y otras voces no

1. **Adelanta el final y lo usa como motor**, no como spoiler. Saber no quita tensión.
2. **Acumula versiones contradictorias y no las resuelve.** El misterio no está en el hecho: está
   en la imposibilidad de saber.
3. **La cifra exacta como verosimilitud:** horas, distancias, años.
4. **El detalle doméstico dentro del horror:** el olor a rosas, la lluvia, el olor a amoníaco.
5. **El adjetivo sensorial, nunca emocional:** tibia, amarga, perfumada. Nunca "triste".

## 6. Lo que García Márquez **nunca** hace

| Nunca | Por qué |
|---|---|
| Frase corta como golpe | 8% de ≤6 palabras |
| Diálogo como escena | Todo va citado dentro del reporte |
| Entrar en la cabeza de otro | Solo cita |
| Resolver una contradicción | La deja |
| Adjetivar la emoción del narrador | Sensorial, no emocional |

## 7. Trasplante a Las Tres Sábanas: qué SÍ y qué NO

**SÍ — y esto es lo más valioso del caso para tu novela:**
- **La acumulación de versiones contradictorias.** Los tres primos recuerdan distinto **por canon**
  (`historia_familiar`: "cuando la ruptura pasó, Adán ya entendía y Vera era una nena. Por eso cada
  uno recuerda una familia distinta"). **Ese es exactamente el mecanismo de García Márquez**, y tu
  canon ya lo tiene sin usarlo.
- **La cifra exacta:** cuántos metros tiene la casa, qué año, cuántos años vivió Adán ahí.
- **El detalle doméstico dentro del dolor:** el olor a humedad, la lluvia sobre la chapa.
- **El arco del narrador:** si la novela la cuenta alguien, ese alguien puede ser el que cambia.

**NO:**
- **La primera persona testigo.** Las Tres Sábanas es tercera limitada con POV rotativo (regla de
  `STYLE.md`). Cambiar a primera persona es otra novela.
- **El 6% de diálogo.** En tres primos encerrados, el habla es el material.
- **La distancia del reporte.** Acá el drama es presente y duele; el reporte retrospectivo lo
  enfría.
- **La ausencia de pensamiento.** Los primos calculan.

## 8. Validación (pendiente)

Criterio: escena escrita con estas reglas desde el principio.
- mediana **18-24**
- frases ≤6 **4-14%**
- frases 16-30 **31-45%**
- frase más larga **≤70**

Y un criterio que el script no mide: **si el texto se lee como crónica y no como escena, se pasó.**
