---
name: text-to-speech
description: Convert any markdown file —a chapter, a note, an essay— into a voice file, with a fixed voice profile you can change with one flag. Use when someone asks to hear a text out loud, to "leerlo en voz alta", or to turn generated content into audio.
---

# Texto a voz

**La regla:** el audio de un texto es **reproducible, no un archivo que se guarda**. Se versiona el texto y
el comando; el `.m4a` se regenera cuando cambia la fuente. Por eso los audios viven en `<carpeta>/audio/` y
están gitignored, con un `.json` al lado que dice con qué voz y con qué hash se generaron.

## Voz vigente (2026-11-17)

| Parámetro | Valor | Por qué |
|---|---|---|
| Voz | **es-AR-TomasNeural** | masculina, grave, argentina. Elegida por Gonzo después de escuchar Elena y Tomás sobre el capítulo 1 de *Las Tres Sabanas* |
| Ritmo | **-10%** | la lectura por defecto va apurada para narrativa |
| Tono | **-2Hz** | un poco más abajo, menos luminoso |
| Motor | **edge-tts** (neural, sin API key) | el TTS del gateway no tiene proveedor configurado; `say` de macOS suena a robot |
| Formato | `.m4a` AAC 64k | se adjunta en cualquier chat sin pesar |

**Cambiar de voz es cambiar `VOICE`, `RATE` y `PITCH` en `scripts/tts-render.py`**, o pasar los flags.
No hay migración que hacer: los audios se regeneran.

## Cómo se usa

```bash
# un archivo entero
python3 scripts/tts-render.py docs/stories/las_tres_sabanas/manuscript/capitulo_1-definitivo.md \
    --out docs/stories/las_tres_sabanas/audio/capitulo-1.m4a

# una muestra corta, para elegir voz o ritmo
python3 scripts/tts-render.py archivo.md --limit-chars 1800 --out /tmp/muestra.m4a --force

# otra voz, sin tocar el default
python3 scripts/tts-render.py archivo.md --voice es-AR-ElenaNeural --rate=-15% --out /tmp/x.m4a --force

# qué voces en español hay
python3 scripts/tts-render.py --voices
```

Después de renderizar, el audio se adjunta con `MEDIA:<ruta>` — una línea, sin texto alrededor.

## Qué hace con el texto

- **Saca el markdown:** encabezados, `---`, `**`, backticks.
- **Lee el pensamiento del POV** (las cursivas) como texto normal: al oído es la voz del personaje.
- **Convierte la raya de diálogo** en pausa: `—Hola —dijo.` → `, Hola, dijo.` Sin esto, la raya se lee
  como un tartamudeo.
- **Corta en párrafos enteros** de hasta 2.200 caracteres y concatena con ffmpeg. Nunca parte una frase.

## Límites conocidos

- **No interpreta.** Lee bien y parejo; no hace voces distintas por personaje ni subraya la ironía. Para
  un relato, alcanza; para una obra de radio, no.
- **La raya desaparece.** Un diálogo sin atribución suena igual que la narración. En prosa que depende del
  ritmo del diálogo, eso se nota; es el precio de escucharlo.
- **Necesita red.** edge-tts habla con el endpoint de Microsoft; sin conexión no hay audio.
- **Sin proveedor en el gateway.** `tts` falla con *"no provider registered"*. Si algún día se configura
  uno (OpenAI, ElevenLabs), esta skill pasa a usarlo y el script queda como fallback.

## Instalación (una vez, ya hecha)

```bash
python3 -m venv .venvs/tts
.venvs/tts/bin/pip install edge-tts
```

`.venvs/` está gitignored. `ffmpeg` tiene que estar en el PATH (está, por Homebrew).

## Dónde van los archivos

```
docs/stories/<proyecto>/audio/
    capitulo-1.m4a          # gitignored, regenerable
    capitulo-1.m4a.json     # voz, ritmo, hash del texto, duración
```

Para contenido que no es de un proyecto —una nota, un ensayo—, `audio/` al lado del archivo fuente.

## Cuándo NO usarla

- Cuando alguien pide **texto**: un audio no reemplaza una respuesta escrita.
- Para contenido confidencial que no debería salir a un servicio externo.
- Para un archivo de una línea: no hay nada que escuchar.
