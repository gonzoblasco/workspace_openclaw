---
name: "ficcion-narrativa-prosa"
description: "Escribir ficción (terror, ciencia ficción, thriller psicológico, escuela Highsmith) con el pipeline de dos etapas: un modelo arma el esqueleto, otro redacta, y el texto se verifica con métricas de ritmo, fidelidad y defectos de prosa. Usar cuando el pedido sea un cuento o una escena narrativa, no un análisis."
metadata:
  category: "Escritura"
  tags:
    - ficcion
    - narrativa
    - cuento
    - ritmo
    - prosa
---

# Ficción narrativa: esqueleto, redacción y verificación

## Cuándo usar

Cuando piden un cuento, una escena o un relato de ficción. No cuando piden analizar una obra: eso es `narrative-engineering-analysis`.

## Cuando la historia es de la vida del owner

Si el pedido es narrar un hecho real del owner (un caso judicial, una historia familiar) como thriller o cuento, la fase de acopio va antes que cualquier pipeline y es la que decide si el texto sirve.

1. **Buscar los documentos en el lote de adjuntos del chat, no en el disco.** Lo que el owner manda por la conversación queda en `~/.openclaw/media/inbound/` con sufijo `---<uuid>.<ext>`.
   ```bash
   ls -lt ~/.openclaw/media/inbound/ | grep -iE '\.(pdf|docx?|pages|rtf)$' | head -80
   mkdir -p /tmp/lote && cd ~/.openclaw/media/inbound && n=0
   for f in *.pdf; do n=$((n+1)); pdftotext -layout "$f" "/tmp/lote/$(printf '%02d' $n)-$(echo $f | sed 's/---[0-9a-f-]*\.pdf$//').txt"; done
   ```
   Una carpeta del disco con el mismo nombre del caso puede estar incompleta: contar y decirlo con el número. Si no aparecen, se le dice al owner qué buscó y dónde, en vez de concluir "no tengo el material".
2. **Leer el lote entero antes de escribir una línea.** Ordenar los `.txt` por tamaño, leer los largos primero y el resto en barrido; descartar los que no son del caso (contratos laborales, CVs) por su contenido, no por el nombre del archivo.
3. **Construir primero la cronología real** con fechas, actores y documentos (la de `legal-document-intake`). La fuente de la ficción es esa tabla, no el recuerdo.
4. **Escribir reemplazando solo lo identificatorio:** nombres de personas, ciudades, juzgados, números de expediente. **Cuando la historia es de la vida del owner, cambiar el nombre de la contraparte aunque el owner no lo pida, y aunque el expediente esté en la carpeta privada del caso:** el apellido real de la otra parte en una pieza que circula es un daño que no se deshace. Cambiarlo también en los documentos ya citados, no solo en el cuerpo narrativo. Lo demás —fechas internas, citas de informes, contradicciones, plazos— se conserva, porque los detalles verificables son lo que hace creíble la historia.
4a. **No derivar el material del nombre de una carpeta ni de lo que el agente cree recordar.** Una carpeta del disco puede tener 48 archivos mientras el lote que el owner mandó por el chat tiene 74, y una sesión anterior puede haber dejado un daily con la cronología que hay que leer antes de preguntar. Si el owner dice que ya mandó algo, buscarlo en ese orden: el lote de `~/.openclaw/media/inbound/`, el daily de la fecha que nombra (`memory/YYYY-MM-DD.md`), y solo después el disco. Decirle "no tengo el material" sin haber hecho las tres búsquedas es el error que obliga al owner a repetir el pedido.
4b. **Corregir la cronología con lo que el owner dicta, sin reinterpretarla.** El owner aporta hechos que no están en el lote (cuántas audiencias hubo, qué le dijo el juez, qué pasó antes del corte). Cada corrección se aplica literal: si dice "la última vez que lo vi fue el 25 de enero de 2020", esa es la fecha, y los hitos del relato se reordenan alrededor. No se agrega una escena que el owner no describió para justificar el dato nuevo.
5. **Entregar la lista de qué es real y qué se inventó**, ítem por ítem, y pedir el dato que falte en vez de rellenarlo.

No se escribe de memoria lo que el owner ya documentó: si no se leyó el lote, se dice antes y no después de entregar el texto.

## El pipeline: dos etapas, nunca una

`./scripts/cuento.sh --genero <g> --tema "..." --minimo N --maximo M`

- **Etapa 1 — esqueleto (glm-5.3-flash, `think:"low"`).** Produce premisa, personaje, reloj, escenas, vuelta de tuerca, último objeto e imagen final. GLM tiene la mejor *estructura* y la peor *sintaxis* larga.
- **Etapa 2 — redacción (muse-spark-open, `think:false`).** Sostiene la voz 2.500 palabras sin romperse. Solo, no encuentra un conflicto con consecuencias: describe bien, decide poco.

Un modelo solo para las dos cosas da lo peor de cada uno. Separarlas usa lo mejor.

## Un género nuevo necesita esqueleto propio, no un adjetivo

Cada género tiene su motor y su plantilla en `scripts/templates/`. El wrapper elige la plantilla por `--genero`; forzar una con `--outline-template <ruta>`.

| Género | Motor | Template |
|---|---|---|
| terror | lo inexplicable | `outline-cuento.md` |
| ciencia ficción | lo inexplicable con regla | `outline-cuento.md` |
| thriller psicológico | adversario humano, método repetible, asimetría de información | `outline-thriller-psicologico.md` |
| Highsmith | no hay investigador: el protagonista es el culpable y la tensión es administrativa | `outline-highsmith.md` |

Si el pedido es "otro género", escribir el quinto template antes de correr nada.

## La etapa 1 se trunca y hay que detectarlo antes de la etapa 2

Un esqueleto cortado por presupuesto de tokens produce un cuento sin revelación ni final, y mirando el texto no se nota. `cuento.sh` verifica que el esqueleto tenga las secciones de cierre antes de gastar la etapa 2, y aborta con exit 4 pidiendo subir `num_predict` de la tarea `outline`.

- **Presupuesto del outline: 6.000 tokens.** Con 2.500 un template con sub-viñetas (thriller psicológico, 9 secciones) se cortó a mitad de la escena 1.
- **Un cuento sin final no es un cuento con final flojo.** Si el check de secciones salta, no escribir la etapa 2 "igual" para completar el entregable.

## Entregar el texto completo en el chat, no solo el archivo

Cuando el owner pide una historia, espera leerla. Escribir el `.md` y resumir el resultado fuera del mensaje deja el pedido sin cumplir.

1. Entregar el texto íntegro en el mensaje, con `---` entre escenas, y el archivo como respaldo.
2. Poner después la tabla de real/inventado y las preguntas de datos faltantes.
3. No recortar el texto en el chat "porque está en el archivo": el archivo es para volver, el chat es para leer.

Check: el mensaje contiene todas las palabras del cuento; comparar el conteo del chat con `wc -w` del archivo.

## El ritmo se gobierna con números, no con adjetivos

Pedir "más ritmo" o "dale aire" no funciona. Lo que funciona:

- **Cantidad de párrafos explícita** (52-62 para ~2.400 palabras).
- **Promedio de palabras por párrafo explícito** (42-50).
- **Cuántos párrafos de una línea** (pocos: si hay uno cada tres, ninguno golpea).

Sin la regla, los modelos escriben bloques de 113-155 palabras promedio, uno detrás del otro. Con la regla mal escrita ("nunca dos largos seguidos") producen 96 párrafos de 19 palabras: metralleta. Medir, no estimar.

## La extensión sale de más escenas, no de estirar la prosa

El redactor comprime cada escena a ~200 palabras aunque le pidas 280, y cierra el cuento cuando cree que terminó: tres intentos seguidos dieron 1.817, 1.624 y 1.693 palabras con objetivos de 2.200-2.600. **El arreglo está en el esqueleto: pedir 8-10 escenas × 280 palabras.** Con eso salió 2.083.

## Verificación obligatoria antes de entregar

`scripts/cuento-check.py` avisa (no frena) de:

1. **Ritmo** por género — los umbrales no son universales: un thriller judicial con 26 palabras de promedio está bien, el mismo número en terror es defecto.
2. **Fidelidad** — nombres del esqueleto que no sobrevivieron. Ojo: el redactor *puede* inventar nombres para lo que el esqueleto dejó sin nombrar; eso es correcto. Lo que no puede es renombrar algo ya fijado.
3. **Cabos sueltos** — personas presentadas una sola vez y nunca retomadas. Un detalle plantado que no vuelve es un error, no una ambigüedad.
4. **Fuga de outline** — el metalenguaje del plan en la prosa ("El objeto viajaba en el sobre").
5. **Tell** — etiquetas emocionales ("sintió miedo", "el pánico lo invadió").

## Los defectos que ningún check detecta

Estos salieron de leer los cuentos, no de correr script. Revisarlos a mano siempre:

- **Ruptura de punto de vista.** Un párrafo en primera persona dentro de un cuento en tercera, sin comillas ni raya. Medido: muse lo hizo en Highsmith con un diálogo que se comió las comillas. Si un párrafo empieza con "yo/me/mi" y no tiene raya, es diálogo mal formateado.
- **Palabras inventadas.** `bombe` (por bombilla) apareció tres veces y nadie lo vio: no existe en español. Pasar el texto por un corrector, o buscar palabras que no reconozcas.
- **Detalles que insinúan y no se cobran.** Un "residente joven que no pidió documento" promete una suplantación; si no vuelve, es error.
- **Etiquetas explícitas de la mentira** en estilos donde la mentira se escucha (Highsmith). Si el texto dice "Mentira banal", el redactor está rotulando lo que debía mostrar.

## Regla de oro

**El que lee decide, el check solo avisa.** Un script que distingue "sembrado para volver" de "olvidado" no existe: el check lista candidatos y la lectura decide. Nunca presentar un verde del check como prueba de que el cuento está bien.
