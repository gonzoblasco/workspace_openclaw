# Veredicto SHARP - `blog-publishing-skill`

**Fecha:** 2026-11-18 · **Sujeto:** `skills/blog-publishing/SKILL.md` (198 lineas)
**Emisor:** `ollama/deepseek-v4.1-flash:cloud` (Critic). F8 sigue abierta: el rol declara `gpt-oss:120b-cloud`.
**Rubrica:** `.knowledge/SHARP.md` · **Total:** 19/25 -> **Aprobado** (19-23)

## Snapshot

| Pieza | Ubicacion |
|---|---|
| La skill evaluada | `skills/blog-publishing/SKILL.md:1` |
| Estandar de voz que cita | `projects/a11y-portfolio/content/writing/the-quieter-announcement.md:1` |
| Build del sitio que invoca | `projects/a11y-portfolio/scripts/build.ts:1` |
| Mapa editorial que declara | `projects/a11y-portfolio/.knowledge/CONTENT-MAP.md:1` |
| Brief de diseno | `projects/a11y-portfolio/.knowledge/DESIGN-BRIEF.md:1` |
| Hechos de carrera | `memory/career-facts.md:1` |

## Evidencia mecanica (corrida real, 2026-11-18)

### 1. Las siete fuentes que la skill declara existen todas

```
projects/a11y-portfolio                                               OK
projects/a11y-portfolio/content/writing/the-quieter-announcement.md    OK
projects/a11y-portfolio/scripts/build.ts                               OK
projects/a11y-portfolio/.knowledge/CONTENT-MAP.md                      OK
projects/a11y-portfolio/.knowledge/DESIGN-BRIEF.md                     OK
memory/career-facts.md                                                 OK
docs/linkedin                                                          OK
```

Es el primer skill auditado en el que **cada ruta citada resuelve**. La mayoria de los
skills del arbol citan archivos que no existen; este no.

### 2. El estandar que invoca tiene el largo que dice

```
$ wc -w projects/a11y-portfolio/content/writing/the-quieter-announcement.md
    1103
```

La skill lo llama "1.000 palabras" (`skills/blog-publishing/SKILL.md:23`) y pide 800-1.200
para un articulo nuevo (`skills/blog-publishing/SKILL.md:74`). 1.103 cae dentro del rango: el
estandar es real, no una referencia decorativa.

### 3. Las cuatro categorias existen en el build, no en la prosa

```
projects/a11y-portfolio/scripts/build.ts:42   "field-notes": {
projects/a11y-portfolio/scripts/build.ts:215  if (!(meta.category as string in CATEGORIES)) {
```

La tabla de categorias de la skill (`skills/blog-publishing/SKILL.md:40-46`) coincide con
`CATEGORIES` del generador: si alguien inventa una categoria, el build falla. La skill no
declara una taxonomia propia y paralela.

### 4. La skill cumple la regla de guiones que exige a los articulos

```
$ python3 scripts/check_em_dash.py skills/blog-publishing/SKILL.md
Sin guiones largos.
$ ./scripts/frontmatter_validator.sh
Front-matter validation completed.
```

Una skill que exige "nada de em dashes" y despues los usa en su propio texto seria un
chiste. No es el caso.

## Los 5 ejes

| Eje | Puntaje | Causa con ubicacion |
|---|---|---|
| **S - Sharpness** | **4** | La anatomia de siete partes (`skills/blog-publishing/SKILL.md:59-72`) y la tabla de fuente de verdad (`SKILL.md:27-36`) son quirurgicas: cada dato tiene un dueno declarado. Se pierde el 5 porque el mecanismo central contra la invencion, la **ficha de hechos** (`SKILL.md:100-110`), es una tabla manual de 5-10 lineas sin ninguna verificacion: el mismo hueco que el resto del workspace paga (una regla sin guarda se viola sola). |
| **H - Horizon** | **4** | La sindicacion a dev.to esta declarada como bloqueada por API key (`SKILL.md:169-172`) en vez de fingida, y las categorias ya cubren el crecimiento fuera de a11y (`SKILL.md:44-46`). No hay mecanismo para que el mapa editorial crezca solo, pero la etapa siguiente esta nombrada. |
| **A - Asymmetry** | **4** | Convierte un PR o un post en una pieza publicada con gates explicitos (build, axe, contraste, overflow, `SKILL.md:150-160`) a cambio de 198 lineas de proceso. Palanca alta: la salida es publica y verificable, el costo es texto. No llega a 5 porque el proceso no tiene un solo script propio: todo el trabajo lo hace quien lo lee. |
| **R - Resistance** | **4** | Es la skill mejor anclada del arbol: siete rutas citadas, todas existen; categorias validadas por el build; frontmatter valido; cero guiones largos en su propio texto. Se pierde el 5 por dos huecos concretos: la ficha de hechos no tiene gate (F25) y la skill **no esta registrada** en `SKILLS-INDEX.md` ni en `.knowledge/skills-catalog.tsv` (F24), asi que no es descubrible por el catalogo. |
| **P - Parsimony** | **3** | Hay solape real: la anatomia (`SKILL.md:59-72`), los anti-patrones (`SKILL.md:174-189`) y el checklist de cierre (`SKILL.md:191-198`) dicen tres veces lo mismo con distinto formato. Ademas repite la regla de guiones que ya tiene dueno en `scripts/check_em_dash.py`, y la regla de no inventar metricas que ya vive en el corpus de hechos (`memory/career-facts.md`). |

## Veredicto

**19/25 -> Aprobado.** Es una skill de oficio bien escrita y, por primera vez en este
arbol, **verificable en sus referencias**: cada fuente que declara existe y el build valida
la taxonomia. Aprueba con tres anotaciones: falta el registro en el catalogo, el corazon
anti-invencion (la ficha de hechos) no tiene guarda, y el proceso se dice tres veces.

## Fricciones de mejora (no bloquean, tienen dueno)

| # | Eje | Causa | Ubicacion | Ajuste concreto |
|---|---|---|---|---|
| **F24** | Resistance | La skill no esta en `SKILLS-INDEX.md` ni en `.knowledge/skills-catalog.tsv`: existe en disco pero no es descubrible | `skills/blog-publishing/SKILL.md:1`, `SKILLS-INDEX.md:1`, `.knowledge/skills-catalog.tsv:1` | Registrarla con `state=keep` y `layer=core-workflow`, igual que se hizo con `evidence-hunter` y `sharp-adversarial-review` |
| **F25** | Sharpness | La ficha de hechos es el unico mecanismo contra inventar metricas y es 100% manual: ninguna corrida comprueba que cada numero del articulo este en la tabla | `skills/blog-publishing/SKILL.md:100-110` | Un script que cruce el `.md` del articulo contra la ficha y falle si aparece un numero o un `#PR` que no este en la tabla. El criterio ya esta escrito; falta que lo verifique algo |
| **F26** | Parsimony | Anatomia, anti-patrones y checklist repiten las mismas reglas; la regla de guiones y la de no inventar metricas ya tienen dueno en otro archivo | `skills/blog-publishing/SKILL.md:59-72`, `SKILL.md:174-189`, `SKILL.md:191-198` | Dejar la anatomia como unica fuente del orden y convertir el checklist en las verificaciones mecanicas (build, axe, ficha de hechos), sin repetir prosa |

## Como se verifica este veredicto

```bash
cd /Users/gonzoblasco/.openclaw/workspace
python3 agents/kanam-critic/bin/verify-verdict.py --artifact blog-publishing-skill
python3 agents/kanam-critic/bin/query_verdicts.py
python3 scripts/check_em_dash.py skills/blog-publishing/SKILL.md
```

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
