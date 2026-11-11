# HANDOFF — SQL Full Course (Data with Baraa, 30 h)

**Fecha:** 2026-11-11
**Estado:** clase montada (transcript + outline + banco de preguntas). Sin ejercicios desglosados por módulo todavía.
**Fuente:** https://www.youtube.com/watch?v=SSKVgrwhzus

## Qué hay

| Archivo | Qué es |
|---|---|
| `outline.md` | La clase: tesis, resultados esperados, mapa temporal de los 41 capítulos, 22 módulos, citas verificadas y banco de 18 preguntas. |
| `transcripcion.md` | Subtítulos automáticos `en-orig` normalizados: 48.358 cues, ~364.000 palabras, formato `[hh:mm:ss] texto`. |
| `video-meta.json` | Metadatos de la fuente (título, canal, fecha, capítulos, description). |

## Leer en este orden

1. `outline.md` — todo el contenido de la clase.
2. `outline.md` §"Mapa temporal" — para ubicar un tema por timestamp y saltar directo en `transcripcion.md`.
3. `transcripcion.md` — solo el tramo que interese (grep por `[hh:`).

## Decisiones tomadas

- **Transcript por subtítulos automáticos, no ASR local.** Un video de 30 h con `whisper-cli medium` a ~170 ms de encode por run no era viable en esta sesión; YouTube ya tenía `en-orig` con timestamps reales y cobertura completa del audio. La deduplicación bajó 96.716 eventos a 48.358 cues.
- **Sin ejercicios por módulo todavía.** El formato de las otras clases (`ai-engineer-full-course`, `rag-mcp-fundamentals`) incluye ejercicios por módulo; acá se hizo primero la estructura completa porque el curso tiene 22 módulos y 30 h.

## Gotchas

- `yt-dlp` de `pip --user` (2025.10.14) funciona para metadata y captions, **no** para bajar audio: todos los formatos de video dan `HTTP 403`, con o sin `player_client` alternativo. Para bajar audio de este video hay que usar otro camino (cookies, otro cliente, o el archivo del curso).
- La extracción de metadata es intermitente: `"The page needs to be reloaded"` aparece en ~3 de cada 5 intentos. Un loop de 5-6 reintentos con `sleep` resuelve.
- Los subtítulos se bajan de la URL en `automatic_captions["en-orig"]` (`fmt=json3`), directo con `curl`: 37 MB en un request.
- El curso es **SQL Server**, no agnóstico. Cualquier ejercicio portable tiene que traducirse.

## Próximo paso sugerido

Si Gonzo quiere que esto sea una clase como las otras: agregar ejercicios ejecutables por módulo (los "Beginner" y los de ventanas son los más ejercitables), y decidir si se monta un Postgres local para correrlos o se quedan como SQL Server en papel.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

## Cómo se montó (2026-11-11)

```bash
# metadata + chapters (con reintentos por "page needs to be reloaded")
python3 -c "import yt_dlp,json; ..."   # skip_download=True → video-meta.json
# captions: URL de automatic_captions["en-orig"] con ext=json3
curl -sL -o en.json3 "<url>"
# normalizar: events[].segs[].utf8 → [hh:mm:ss] texto, dedupe de líneas consecutivas
```
