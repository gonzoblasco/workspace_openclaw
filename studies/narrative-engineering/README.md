# Ingeniería Narrativa - Estudio

**Inicio:** 2026-09-26
**Estado:** abierto — 9 casos, 5 ejes, 6 perfiles de voz medidos (2026-11-17)

---

## Objetivo

Construir un **modelo mental operable** de cómo funcionan los arquitectos de historias
(guionistas, escritores), para que Kanam pueda acompañar a Gonzo cuando crea sus propias
historias: no resumir peliculas, sino **conocer la maquinaria** y poder decir "aca este
autor haria X" y por que.

**El pedido textual de Gonzo (2026-09-26):**

> "estoy intentando crear un estado mental en el que conozcamos el modelo y como funciona
> su metodologia para asi ayudarme a mi cuando estoy intentando crear historias... me
> ayudaria que ya seas una experta en estos temas para que me puedas ir mostrando este
> camino y enseñando como crearlo"

**Regla de oro del estudio:** *conocer lo que se busca antes de buscarlo.*
Nada de "mapas de influencia" ni listas de recomendaciones. Primero diseccionamos autores,
despues sabremos que buscar. (Negativo explicito de Gonzo al mapa de influencia.)

---

## Metodo de analisis: los 4 ejes

Cada obra se disecciona por estos cuatro ejes, siempre en el mismo orden. Los ejes salieron
del primer caso (Dark City) y se confirmaron en el segundo (Batman Begins).

1. **Premisa y Regla de Hierro** - el High Concept. Una contradiccion violenta + una regla
   que no se rompe nunca. El escenario es la fuente del conflicto.
2. **Gestion de la Informacion (Asimetria)** - que sabe el heroe, que sabe el villano, que
   sabe el publico. El conflicto vive en la brecha entre esas tres columnas.
3. **World-building Funcional** - Escenario -> Regla -> Herramienta. El mundo como obstaculo
   y como herramienta, nunca como decorado.
4. **Arco de Identidad** - el vacio emocional que el personaje debe llenar. El motor interno.
5. **Voz y Prosa** - *(desde el caso 04, 2026-11-16)* como suena el texto, con cifras medidas:
   ritmo de frase, densidad de dialogo, atribuciones, punto de vista y pensamiento interno, y
   sobre todo **lo que el autor nunca hace**. Es el eje que permite escribir en ese estilo; los
   otros cuatro explican como esta armada la historia.

## Los cinco perfiles medidos (narracion)

| Perfil | Mediana | <=6 | 7-15 | 16-30 | 31+ | Estrategia |
|---|---|---|---|---|---|---|
| Card | 9 | 35% | 47% | 16% | 1% | golpes cortos |
| Katzenbach | 12 | 24% | 41% | 27% | 8% | medio, dialogo dominante |
| Rowling | 16,5 | 14% | 35% | 38% | 12% | medio-alto parejo |
| Echeverria | 20,5 | 14% | 25% | 30% | 31% | alto con picos |
| Garcia Marquez | 21 | 8% | 28% | 38% | 26% | alto **sin picos**, sin frases cortas |

Verificados con `scripts/prose-metrics.py --perfil <nombre>`; cada uno se auto-valida a +-0,4%
sobre su propio texto fuente. **Seis autores, tres idiomas de origen, cuatro siglos, seis géneros:
ninguna distribucion se repite.** La tabla no dice quien escribe mejor, dice que eligio cada uno.

**Cervantes cambia la escala de la tabla.** Con mediana 41 y 82% de frases de más de 30 palabras,
no está un escalón arriba de García Márquez: está en otra física. Antes del siglo XX la unidad de
respiración era el párrafo, no la frase.

**Criterio de "modelo confirmado":** si los 4 ejes aparecen con la misma mecanica en un
material original y en uno adaptado, deja de ser casualidad: es la firma del autor.

**Nota critica (2026-11-16):** este criterio es debil como validacion - si buscas el patron, lo
encontras. El Eje 5 es el que pone el estudio a prueba de verdad, porque sus afirmaciones se
pueden medir y refutar con cifras.

---

## Casos

| # | Obra | Autor foco | Tipo de material | Estado |
|---|------|-----------|------------------|--------|
| 01 | Dark City (1998) | David S. Goyer (co-guion) | Idea **original** | 5/5 (Eje 5 no medible: guion) |
| 02 | Batman Begins (2005) | David S. Goyer | **Adaptacion** (comic DC) | 5/5 (Eje 5 no medible: guion) |
| 03 | Mamma Mia! (musical y película) | Catherine Johnson | **Adaptación** (musical y película) | 5/5 (Eje 5 no medible: libreto) |
| 04 | Ender's Game (1985) | Orson Scott Card | Idea **original** | 5/5 ejes (**muestra parcial**: Ch. 1) |
| 05 | Harry Potter y el prisionero de Azkaban (1999) | J. K. Rowling | **Continuacion de serie** | 5/5 ejes (extracto oficial, Ch. 1) |
| 06 | La sombra / The Shadow Man (1995) | John Katzenbach | Idea **original** (thriller) | 5/5 ejes (fragmento oficial, es) |
| 07 | El matadero (1838-40, pub. 1871) | Esteban Echeverria | Idea **original** (cuento fundacional) | 5/5 ejes + peso (dominio publico, completo) |
| 08 | Cronica de una muerte anunciada (1981) | Gabriel Garcia Marquez | Idea **original** (hecho real) | 5/5 ejes (edicion oficial, cap. 1) |
| 09 | Don Quijote I-1 (1605) | Miguel de Cervantes Saavedra | Idea **original** (parodia) | 5/5 ejes (dominio publico, completo) |

---

## Archivos

- `metodo.md` - el enfoque, los 5 ejes, cómo se registra cada caso y la regla de separar hecho de lectura.
- `caso-01-dark-city.md` - el caso que fundó el método. Reescrito con los 5 ejes el 2026-11-17.
- `caso-02-batman-begins.md` - adaptación y sistema de adquisición. Reescrito con los 5 ejes el 2026-11-17.
- `modelos.md` - **qué modelos hay, con qué evidencia y qué falta para cerrar el resto.** El mapa completo por autor.
- `modelo-goyer.md` - síntesis acumulativa. **Límite corregido el 2026-11-17:** los 4 ejes son estructura, no firma; sin Eje 5 no se puede hablar de autoría.
- `caso-04-enders-game.md` - primer caso con **Eje 5 (Voz y Prosa)** medido sobre texto real.
  Su traduccion ejecutable vive en `docs/stories/las_tres_sabanas/PLANTILLA-voz-enders-game.md`.
- `caso-05-harry-potter-azkaban.md` - segundo perfil de voz, **opuesto** al 04 y sobre el mismo
  eje: demuestra que el Eje 5 mide una eleccion, no una jerarquia de calidad.
- `caso-06-la-sombra-katzenbach.md` - tercer perfil, y el primer caso que **no** es sobre voz sino
  sobre **peso**: como un objeto carga sin convertirse en simbolo. Su formula vive en
  `docs/stories/las_tres_sabanas/PLANTILLA-peso-katzenbach.md`.
- `caso-07-el-matadero-echeverria.md` - cuarto perfil y el primero **fuera del ingles**: espanol
  rioplatense de 1838. Prueba que el metodo aguanta. Agrega una tercera direccion de asimetria
  (el narrador fiscal) y el peso por **funcion** en vez de por historia.
- `caso-09-quijote.md` - el extremo de la tabla: mediana 41, cero frases cortas, 0% de diálogo.
  Es el caso que muestra que la tabla de perfiles era, sin saberlo, una tabla del siglo XX.
- `caso-08-cronica-muerte-anunciada.md` - quinto perfil, el cierre del arco metodologico. Agrega
  la cuarta direccion de asimetria (comunitaria y retrospectiva) y la tercera forma de peso (el
  testimonio). Con cinco autores queda demostrado que **no hay una prosa buena: hay cinco
  decisiones**.

---

## Pendientes

- [x] Cerrar Batman Begins: eje 3 (World-building) y eje 4 (Arco de Identidad).
- [x] Consolidar `modelo-goyer.md` al cerrar el caso 2.
- [x] Elegir tercer caso (camino de reinterpretacion, otro material ya existente).
- [ ] Cerrar el caso 04 con el texto completo (sala de batalla y cierre): hoy los ejes 1-4 se
  sostienen sobre el Ch. 1 mas estructura publica conocida.
- [x] Validar `PLANTILLA-voz-enders-game.md` escribiendo una escena de Las Tres Sabanas y
  midiendola con el mismo script. (Superada: la novela entera se escribió con el perfil `casa`,
  que es un perfil propio derivado de los cinco autores.)
- [ ] **Eje 5 de los casos 01, 02 y 03:** imposible mientras el material sea guion. Si aparece
  prosa narrativa de Goyer o de Johnson en edición estable, se mide y se cierra.
- [ ] **Segundo caso de Rowling** (*The Casual Vacancy*): es el único autor del estudio donde el
  segundo caso responde una pregunta abierta —cuánto de su voz es la serie y cuánto es ella—, y
  ya hay un perfil medido contra el que comparar. Ver `modelos.md`.
- [ ] Revisar si el "criterio de modelo confirmado" (4 ejes en original y adaptación) sigue
  sirviendo para algo: hoy el estudio lo considera superado por el Eje 5.
- [x] Decidir si el caso 03 prueba a un autor **distinto** de Goyer para saber si el modelo es una forma de escribir o la firma de un hombre.

---

## Notas de contexto

- El autor foco lo eligio Gonzo desde IMDb: `https://www.imdb.com/es/name/nm0275286/`
- Dato corregido: Goyer **si** es co-autor del guion de Dark City (con Alex Proyas y
  Lem Dobbs; historia de Proyas). Gonzo lo corrigio y la fuente lo confirma.
- Esto NO es portfolio: es material personal de estudio, en espanol, no va a GitHub publico.
