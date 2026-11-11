# ADOPCIÓN — I Built This Interactive 3D Website With AI

**Fecha:** 2026-11-11 · **Curso:** 13:01 · MiladiCode

**Pregunta:** ¿qué hacemos hoy mal en el workspace que este curso arregla?

## Veredicto

**Sí se adopta, con un artefacto:** `contrast-gate.py`, un gate de contraste WCAG AA sobre las variables CSS de un proyecto.

Por qué este y no otro: el único momento del curso donde el método falla **de forma visible** es cuando el ponente descubre que el texto de la hero no se lee encima de la animación y lo resuelve con una sombra (00:06:57). Eso no es un detalle estético del video: es exactamente el error que comete cualquiera que genere una sección con un agente y le ponga texto encima de un asset. En este workspace hay un proyecto con design system en variables CSS (`projects/preflight`), así que hay un caso real donde correrlo.

## Tabla

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| El texto sobre fondo animado no se lee y se parchea con sombra («because of the color of the background, our text is not fully visible», 00:06:57) | Ninguna sección de UI generada con agente pasa por una medición de contraste. `projects/preflight` tiene un design system con tokens y nadie los midió nunca | **`contrast-gate.py`** — resuelve las variables hex de un CSS y falla (exit 1) si un par texto/fondo baja de 4.5:1. Corrido abajo |
| Los tres parámetros del scroll (count de frames, patrón de nombre, ruta del asset) hay que actualizarlos «in the scroll logic section as well» (00:06:15) | No hay hero con frame sequence en ningún proyecto | **Candidato, no escrito.** Cuando exista una animación por frames, el gate es un `grep` que exige que `FRAME_COUNT` salga de una constante y no aparezca hardcodeado en el componente. Hoy no hay a qué aplicarlo |
| Preparar las dos imágenes en el mismo 16:9 antes de generar, en vez de recortar después (00:02:55) | No generamos assets visuales en este workspace con ese flujo | **Sin adopción.** Es una práctica de producción de video, no una regla del repo |

## El artefacto, corrido contra el repo

```bash
$ python3 studies/ai-3d-interactive-website/contrast-gate.py projects/preflight/src/app/globals.css
ok   15.99:1  --text-main          e8e8ea  sobre  --bg-canvas    0b0c0e  (…/globals.css)
ok   14.54:1  --text-main          e8e8ea  sobre  --bg-surface   16181b  (…/globals.css)
ok   13.05:1  --text-main          e8e8ea  sobre  --bg-input     1f2226  (…/globals.css)
ok    6.04:1  --text-muted         8b8f98  sobre  --bg-canvas    0b0c0e  (…/globals.css)
ok    5.49:1  --text-muted         8b8f98  sobre  --bg-surface   16181b  (…/globals.css)
ok    4.93:1  --text-muted         8b8f98  sobre  --bg-input     1f2226  (…/globals.css)
FAIL  1.00:1  --text-on-accent     0b0c0e  sobre  --bg-canvas    0b0c0e  (…/globals.css)
FAIL  1.10:1  --text-on-accent     0b0c0e  sobre  --bg-surface   16181b  (…/globals.css)
FAIL  1.23:1  --text-on-accent     0b0c0e  sobre  --bg-input     1f2226  (…/globals.css)

9 pares verificados, 3 fallas
EXIT=1
```

Las seis que importan —texto normal y texto apagado sobre los tres fondos— pasan, la más ajustada con 4.93:1. Las tres de `--text-on-accent` son un **falso positivo conocido y documentado en el script**: ese token se declara para ir encima de `--accent` (`#f5a524`), donde da 9.59:1. Contra un `--bg-*` oscuro da 1:1 porque es casi el mismo color. El gate mide contraste, no intención de uso; esa pareja va explícita:

```bash
$ python3 studies/ai-3d-interactive-website/contrast-gate.py --pairs "--text-on-accent:--accent" projects/preflight/src/app/globals.css
ok   9.59:1  --text-on-accent     0b0c0e  sobre  --accent       f5a524

1 pares verificados, 0 fallas
```

**Qué prueba esto:** el design system de `preflight` está bien. El gate no encontró un bug; encontró que el token de texto sobre acento tenía que medirse contra *su* fondo y no contra todos. Ese es el uso real del artefacto: obliga a declarar el par, y el par incorrecto salta.

## Lo que el curso no cubre (y por eso el gate es solo contraste)

- **Rendimiento de la animación**: 60 frames de pantalla completa sin comprimir son cientos de MB; el video no dice cuántos frames ni en qué formato. El gate no mide peso de assets.
- **Accesibilidad del scroll-driven**: una animación atada al scroll rompe con `prefers-reduced-motion` salvo que se implemente un fallback; el video no lo menciona. Es el hueco más grande para nosotros, porque es justo lo que `preflight`/`kanam-fixer` atacan.
- **Integración 3D real**: el video integra el GLB con el agente y no muestra el componente ni el manejo de carga. No hay nada que copiar; hay que escribirlo.
- **Los prompts**: están en un Notion externo. La clase enseña el método y la secuencia, no los textos.

## Candidato a futuro (no escrito)

Si algún día se hace una landing o hero con frames en el workspace, el artefacto es un **checklist previo al prompt de animación**: contar frames reales del directorio, verificar que el patrón del nombre exista en el componente y en la lógica, y exigir un `prefers-reduced-motion` con imagen estática. Hoy no hay caso.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
