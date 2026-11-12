# HANDOFF - Curso dsa-mega-course

- **Modulo actual:** Modulo 1 (Big O) cerrado: leccion `modulo-01-big-o.md` + practica medida en `practica/m1/`.
- **Ejercicios hechos:** Modulo 1 completo (8.1 tabla, 8.2 cinco bloques, 8.3 benchmark, 8.4 entrevista) con mediciones reales en `practica/m1/RESULTADOS.md`. 1 de 20 bloques.
- **Preguntas abiertas:** ¿se sigue el orden del video (1→20) o el tramo propuesto (A: Fundamentos + Arrays, ~2,8 h)? ¿Se resuelven en Java, que es el lenguaje del curso, o en el lenguaje del proyecto donde se vaya a aplicar?
- **Proximo bloque:** Modulo 2 (Arrays, 0:50:21-3:29:02) con los 10 problemas del outline; practica en `practica/m2/`.

## Estado actual

- Modulo 1 cerrado con practica: `modulo-01-big-o.md` (leccion) + `practica/m1/` (4 ejercicios, benchmarks medidos en `RESULTADOS.md`). JDK 27.0.1 instalado con brew; el `java` de macOS era un stub.
- Clase completa en `studies/dsa-mega-course/`: `transcripcion.md` (9.850 bloques con `[h:mm:ss]`, 2,8 MB) y `outline.md` (21 módulos, mapa temporal oficial de 29 capítulos, ~150 problemas con timestamp).
- Gate de citas corrido: 22 citas con timestamp, `BAD: 0`; sin citas no literales.
- Registrada en `studies/README.md`.

## Proximos pasos

1. Decidir el orden (video completo vs. tramos) y el lenguaje de los ejercicios.
2. Empezar por el Módulo 1 y cerrarlo con los tres ejercicios de Big O.
3. Al terminar cada bloque, tildar en el checklist y anotar el problema que costo mas.

## Decisiones

- Se uso `youtube-transcript-api` en vez de `timedtext` porque la URL del HTML devolvio 0 bytes en todos los `fmt` probados (srv3, json3, vtt).
- Los bloques se agrupan a ~300 caracteres / 18 s para que las citas sean citables; la marca es la del primer cue del bloque.
- Los problemas sin nombre explicito en la transcripcion se marcan como «(problema de X)» en vez de inventarles el titulo; el enlace al repo de soluciones cubre el hueco.

## Archivos tocados

- `studies/dsa-mega-course/transcripcion.md`
- `studies/dsa-mega-course/outline.md`
- `studies/dsa-mega-course/HANDOFF.md`
- `studies/README.md`

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
