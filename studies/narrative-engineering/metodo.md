# Método de análisis

> **Vigente desde 2026-11-17.** Reemplaza la versión de 2026-10-01, que tenía cuatro ejes y no
> distinguía dato de lectura. Los casos 01 a 08 están escritos con este método.

---

## Enfoque

No es crítica de cine ni resumen. Es **lectura de planos**: tratamos la obra como el manual de
una máquina que funciona y buscamos los engranajes.

Pregunta central de cada caso: **¿cómo está construido esto para que funcione?**

Dos reglas que mandan sobre todo lo demás:

1. **Separar hecho de lectura.** Año, autoría, formato y trama son dato verificable. Lo que
   interpretamos es nuestro, y va dicho como tal.
2. **Conocer lo que se busca antes de buscarlo.** Nada de mapas de influencia ni listas de
   recomendaciones.

---

## Los cinco ejes (orden fijo)

### Eje 1 — Premisa y Regla de Hierro

- **High Concept:** una frase que ya contiene el conflicto y la curiosidad.
- **Contradicción violenta:** el contraste que genera claustrofobia o deseo.
- **Regla de Hierro:** una regla que no se rompe jamás. Una vez establecida, la trama se vuelve
  ajedrez: todo lo que sigue es consecuencia.
- Clave: el escenario mismo es la fuente del conflicto, no el fondo.

### Eje 2 — Gestión de la información

Tres columnas siempre vivas:

- **Héroe:** ceguera → revelación.
- **Público:** intuición → certeza (ironía dramática).
- **Villano:** control → vulnerabilidad.

El ritmo de la revelación *es* el ritmo de la tensión. Regla: **jamás dar una respuesta sin
haber plantado antes la pregunta**.

Direcciones de asimetría encontradas hasta hoy: contra el villano (01, 02), entre todos los que
protegen a alguien (03), fiscal contra el lector (07), comunitaria y retrospectiva (08).

### Eje 3 — World-building funcional

Fórmula: **escenario → regla → herramienta**.

1. El escenario crea una limitación.
2. La regla explica por qué existe esa limitación.
3. La herramienta permite superarla usando la propia lógica del mundo.

Si el escenario no estorba, es decorado. Si estorba, es historia.

### Eje 4 — Arco de identidad

- **Identidad como rompecabezas:** dar un vacío que el personaje necesite llenar.
- **Ancla emocional:** un recuerdo significativo que convierte lo abstracto en sentimiento.
- **Evolución:** víctima → observador → operador → creador.

### Eje 5 — Voz y prosa *(desde 2026-11-16)*

El único eje **medible**, y por eso el único que puede refutar el modelo. Se corre
`scripts/prose-metrics.py` sobre texto narrativo real y se registra:

- mediana de palabras por frase y distribución en bandas (≤6, 7-15, 16-30, 31+);
- porcentaje de párrafos y de palabras en diálogo;
- atribuciones por mil palabras de diálogo;
- punto de vista y densidad de pensamiento interno;
- **lo que el autor nunca hace** (punto y coma, adverbios en -mente, repeticiones, marcas).

Un perfil no dice quién escribe mejor: dice **qué eligió**. Con cinco perfiles medidos (Card,
Katzenbach, Rowling, Echeverría, García Márquez) queda demostrado que no hay una prosa buena,
hay decisiones distintas.

**Cuándo no aplica:** cuando el material es guion, libreto o letra, no hay prosa que medir. En
los casos 01, 02 y 03 el Eje 5 queda **no medido**, y se dice por qué. Inventar cifras sobre un
guion sería medir otro objeto.

**Regla de densidad por escena:** la densidad de pensamiento se mide por escena, no por libro.
Una novela con mucho diálogo promedia bajo aunque cada escena esté en su punto.

---

## Cómo se registra cada caso

1. **Ficha:** año, autor foco, tipo de material, acreditación exacta y estado del análisis.
2. **Ejes 1 a 4:** mecánica detectada + lección aplicable.
3. **Eje 5:** perfil medido, o la razón por la que no se puede medir.
4. **Síntesis:** tabla de mecánicas y qué produce el conjunto.
5. **Comparativa** contra el caso anterior.
6. **Límites del caso:** qué no prueba. Todo caso tiene alguno, y decirlo es parte del método.

---

## Caso y modelo no son lo mismo

Un **caso** es una obra. Un **modelo** es un autor, y exige **dos obras o más** cruzadas: qué se
repite, qué no hace nunca, cuál es su procedimiento. Con una sola obra se describe una mecánica,
no una firma.

El mapa de quién tiene qué, y qué falta para cerrar cada modelo, vive en `modelos.md`.

---

## Reglas de escritura del estudio

- **Fuentes citadas** cuando se afirma un dato externo (acreditaciones, fechas, ediciones).
- **Hecho verificado separado de lectura.** Si no se puede verificar, se dice "lectura nuestra".
- **Un caso no prueba el método.** Tres casos elegidos por quien definió el modelo lo confirman
  por construcción. Lo que lo pone a prueba es el Eje 5, porque sus afirmaciones se pueden
  refutar con cifras.
