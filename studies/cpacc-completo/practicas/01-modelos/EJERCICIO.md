# Práctica 01 — Los siete modelos aplicados a un caso real

**Caso:** `facebook/astryx` #5419 — un HoverCard con label se expone como `dialog popup` en
vez de descripción. El usuario de lector de pantalla cree que se abrió un diálogo y busca un
botón de cerrar que no existe.

Fuente del caso: `docs/OSS-TRACKER.md` (PR propio mergeado, 24/08).

**Herramienta:** [`modelos.py`](./modelos.py) — `python3 modelos.py "<caso>"`.
**Tests:** [`test_modelos.py`](./test_modelos.py) — 11/11 OK.

---

## Lo que el script no puede hacer

`modelos.py` imprime la **lente** de cada modelo, pero no razona sobre tu caso: eso lo hacés vos.
El script es el andamio. Acá está el entregable de verdad, escrito a mano.

## Los siete modelos sobre el HoverCard

### 1. Médico
*"El lector de pantalla no anuncia bien."*
**Lectura:** describe el defecto como limitación de la tecnología asistiva.
**Por qué está mal acá:** el lector no tiene ningún problema. VoiceOver anuncia exactamente lo que
el DOM le dice: `role=dialog`. La falla es del markup.
**Para qué sirve igual:** para recordar que el AT es el canal y que cambia entre NVDA, JAWS y
VoiceOver — el bug se reprodujo con VoiceOver y no con los otros.

### 2. Social
*"Construimos un contrato de roles incorrecto y le pedimos al usuario que lo decodifique."*
**Lectura:** la barrera la pusimos nosotros. Un `role=dialog` es una promesa: "hay un diálogo, hay
un botón de cerrar, el foco está atrapado". Ninguna de las tres es cierta.
**Es el modelo central del fix.** La corrección (`aria-haspopup=dialog` gateado en `open`,
`aria-controls`, `aria-expanded` sincronizado) no cambia al usuario: cambia lo que el componente
promete.

### 3. Biopsicosocial
**Lectura:** el costo no es solo el anuncio. Hay un costo psicológico real: el usuario cree que
abrió un modal y se queda **buscando cómo salir**. Ansiedad de quedar atrapado, que es un miedo
aprendido y documentado en usuarios de AT.
**Uso práctico:** es el argumento que convence a un PM. "Se pierde" suena a métrica; "el usuario
queda encerrado" suena a persona.

### 4. Económico
**Lectura:** el componente es de un design system usado por varios productos. Un `role` mal puesto
se multiplica por cada consumidor y no aparece en ningún ticket.
**Uso práctico:** el costo de no arreglarlo en la librería es N veces el de arreglarlo en una app.
Ese es el argumento de priorización de un maintainer.

### 5. Soluciones funcionales
**Lectura:** es el lente del fix. Reemplazar el `aria-describedby` ciego por un par
`aria-haspopup=dialog` + `aria-controls` gateado en el estado abierto, y sincronizar
`aria-expanded`. Sin label, mantener `aria-describedby` con `role=group`.
**Y su debilidad se aplicó de verdad:** la primera versión probablemente arreglaba el anuncio y
rompía el caso sin label. El fix terminó gateado por estado por ese motivo.

### 6. Identidad social / afiliación cultural
**Lectura:** un lector de pantalla no es solo una herramienta, es la forma en que alguien participa
del mundo. Un anuncio que lo trata como si estuviera confundido es una microagresión a su
competencia: él no se equivocó, el componente mintió.
**Uso práctico:** el tono del changelog y del issue importa. "Corregido" y no "simplificado para
lectores de pantalla".

### 7. Caridad
**Lectura:** la solución caritativa habría sido "documentar en el README que los usuarios de
VoiceOver pueden ignorar el anuncio de diálogo".
**Por qué es la trampa:** es ayuda que mantiene el defecto y le pasa la carga al usuario. Es
exactamente lo que el fix evitó.

---

## Lo que saqué de hacer este ejercicio

1. **El lente médico es el default del lenguaje técnico.** "El AT no lo anuncia bien" aparece solo.
   Detectarlo es el 50% del trabajo de revisar un issue.
2. **Los siete no se excluyen.** Este caso se explicó con social + biopsicosocial + funcional, y
   se dejó fuera médico y caridad. El BoK lo dice: «No model is comprehensive».
3. **El examen pregunta fortalezas y debilidades.** Escribir la debilidad de cada modelo sobre un
   caso propio es la forma más rápida de fijarlas.
4. **La práctica convirtió el ejercicio en herramienta.** `modelos.py` ya es usable en un review
   real: pegás la descripción del bug y ves por qué lentes se puede leer antes de decidir el fix.

## Qué sigue

Este script es el molde: catálogo de datos + CLI + tests + un caso real aplicado. El de la Unidad 1
(las 8 categorías) y el de POUR (Unidad 2) van a tener la misma forma, y ahí se puede empezar a
pensar en un `practicas/` con un runner común.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
