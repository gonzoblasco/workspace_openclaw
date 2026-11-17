# Capítulo 1 — las cinco versiones, medidas

*2026-11-17. Los manuscritos anteriores se borraron (recuperables del historial de git). Este
documento es el registro de las cinco reescrituras de E1, una por perfil.*

---

## Los números

| Versión | Mediana | ≤6 | 7-15 | 16-30 | 31+ | Bandas OK |
|---|---|---|---|---|---|---|
| **Card** | 8 (-1) | 39,5% OK | 39,5% bajo | 20,9% OK | 0% OK | **3/4** |
| **Rowling** | 16,5 (**0**) | 19,2% OK | 28,2% OK | 41,0% OK | 11,5% OK | **4/4** |
| **Katzenbach** | 9,5 (-2,5) | 32,8% alto | 45,3% OK | 20,3% OK | 1,6% OK | **3/4** |
| **Echeverría** | 34,5 (+14) | 16,7% OK | 11,1% bajo | 19,4% bajo | 52,8% alto | **1/4** |
| **García Márquez** | 33 (+12) | 15,4% alto | 20,5% bajo | 10,3% bajo | 53,8% alto | **0/4** |

**Solo Rowling entró completa**, y no por mérito mío: es la plantilla que ya había fallado una vez
y de la que había aprendido. Las otras cuatro las escribí desde cero y las cuatro se fueron para
algún lado.

## El patrón de mis errores

Tres de las cuatro fallas tienen **la misma forma**: el tramo 16-30 se infla y los extremos se
vacían o se llenan.

| Versión | Qué hice mal |
|---|---|
| Card | Escribí frases cortas: el 7-15 quedó bajo. **Reduje el extremo y no llené el medio.** |
| Katzenbach | Corté de menos: 32,8% de frases de ≤6 palabras. |
| **Echeverría** | **Rompe el texto dos veces.** Un script de split cortó oraciones a la mitad ("un problema que nadie de la familia se había tomado el") y el archivo quedó roto aunque los números dieran bien. Reescribí a mano y quedó en mediana 34,5: párrafo-río. |
| García Márquez | Igual: mediana 33 y 54% de frases de 31+. Mi banda es 16-30 y desde ahí no salgo. |

**Diagnóstico honesto: escribo en la banda 16-30 y desde ahí no me muevo.** Cuando intento otra
voz, lo hago *alrededor* de mi banda, no en lugar de ella. Es lo mismo que pasó con la primera
versión de Rowling.

## Lo que esto enseña, y vale más que las cinco versiones

**1. Imitar una voz no es escribir distinto: es escribir con otra distribución.** Los cinco
perfiles tienen medianas de 9 a 21, pero el dato que los separa de verdad son las bandas. Y yo
tiendo a mi banda.

**2. La regla 10 se confirmó con mi propio fracaso.** En Echeverría corté, uní, corté otra vez, y
cada corrección me alejó más. Optimizar por número deforma. Lo dejé en 0/4 y **eso también es un
resultado**: dice que mi mano no llega ahí, no que el perfil esté mal.

**3. Las plantillas sirven, pero no son suficiente.** Tengo las cinco reglas escritas y aun así
fallé cuatro de cinco. La diferencia entre saber la regla y aplicarla es la práctica, y eso no lo
resuelve ningún script.

## Qué hacer con esto

- **Rowling** es la única que se puede usar como está.
- **Card y Katzenbach** están a un ajuste: falta llenar el tramo 7-15.
- **García Márquez** necesita que baje la banda media, y eso ya es reescribir, no corregir.
- **Echeverría y García Márquez** quedaron en mediana 34 y 33, lejos de 20,5 y 21. Intenté
  corregirlas con scripts de split y **rompí el texto dos veces**: corté oraciones a la mitad y los
  números seguían dando bien, así que el error era invisible en la medición. Las reescribí a mano y
  quedaron legibles pero fuera de perfil.

**La lección más dura de la sesión:** corregir prosa con un script de regex no funciona. El
medidor sirve para leer, no para editar. Y el hecho de que los números mejoraran mientras el texto
se rompía demuestra que **la medición por sí sola no garantiza nada**.

**Lo que falta, y es lo único que importa:** que las leas. Los números dicen dónde está cada una
respecto del autor; no dicen cuál sirve para tu novela.
