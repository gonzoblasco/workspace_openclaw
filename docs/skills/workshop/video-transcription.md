---
name: video-transcription
description: "puedes ver este video?', 'te dejo un mp4', transcribir la narración de un video compartido: extraer audio con ffmpeg, transcribir con whisper.cpp local y ofrecer persistirlo."
---
# Transcribir un video con el pipeline local (ffmpeg + whisper.cpp)

Gonzo comparte un mp4 (local o grabado por una plataforma) y pide "puedes verlo" / transcribir la narración: extraer el audio con ffmpeg, transcribir con whisper-cli en la Mac mini, y entregar resumen + transcripción.

## 0. Silencio largo: recortar antes de transcribir
Una grabacion de espera (el owner llega antes de que lo atiendan) tiene la mitad del audio en silencio y ruido de fondo. Sobre ese tramo los modelos alucinan: `ggml-base` inventa dialogo plausible y `ggml-small` repite una misma frase durante todo el archivo. Localizar donde empieza la voz y transcribir solo desde ahi.
```bash
ffmpeg -i audio16.wav -af "silencedetect=noise=-35dB:d=1.5" -f null - 2>&1 | grep silence_end | tail -5
ffmpeg -y -ss <segundo_donde_termina_el_ultimo_silencio> -i audio16.wav -ar 16000 -ac 1 -c:a pcm_s16le /tmp/video-tx/hablado.wav
```
Check: la duracion del recorte coincide con lo que el owner dijo que duraba la conversacion util; si el recorte es casi todo el archivo, el umbral de silencio esta alto.

**Corroborar la duracion con el owner antes de recortar, y medir el archivo con `ffprobe` antes de creer una duracion de memoria.** Un `.m4a` de 2 MB con bitrate ~66 kbps dura cuatro minutos; el owner puede describirlo como "apenas 4" cuando el habla empieza en el segundo 100 y lo que recuerda son los ultimos 143 s. Medir primero, y decir el numero medido en vez de repetir el estimado.
```bash
ffprobe -v error -show_entries format=duration,bit_rate -of default=noprint_wrappers=1 <audio>
```
Check: la duracion que se reporta sale de `ffprobe`, no de lo que dijo el owner ni del tamano del archivo.

**Un recorte mal ubicado devuelve una transcripcion vacia o en bucle, y no es fallo del modelo.** Si `grep silence_end` muestra el ultimo silencio antes del final del archivo, el umbral `-35dB` esta por debajo del ruido de fondo y todo el archivo parece hablado; probar `-30dB` o mirar el `silence_start` mas largo en vez del ultimo `silence_end`.
Check: el recorte tiene voz audible cuando se reproduce con `afplay` o el conteo de palabras sube respecto de la corrida completa.

## 1. Extraer el audio a WAV mono 16 kHz
whisper requiere WAV mono 16 kHz; los mp4 traen audio comprimido.
```bash
mkdir -p /tmp/video-tx
ffmpeg -i "<video.mp4>" -vn -ac 1 -ar 16000 /tmp/video-tx/audio16.wav -y
```
Check: la salida imprime `audio:<KiB>` con `time=` mayor a 0 y `/tmp/video-tx/audio16.wav` existe.

## 2. Instalar lo que falte, una vez por máquina
`ffmpeg` y `whisper-cli` no vienen preinstalados en la Mac mini: `brew install ffmpeg whisper-cpp` (ffmpeg-full no es necesario).
Check: `which ffmpeg whisper-cli` devuelve ambos paths.



## 3. Conseguir el modelo
`whisper-cli` no trae modelo utilizable: `/opt/homebrew/share/whisper-cpp/` solo tiene `for-tests-ggml-tiny.bin`, que no transcribe bien voz real. Guardar el modelo en una carpeta fija para no volver a bajar 150 MB en cada corrida:
```bash
mkdir -p ~/.openclaw/models/whisper
curl -sSL --max-time 240 -o ~/.openclaw/models/whisper/ggml-base.bin \
  "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin"
```
Check: `ls -la ~/.openclaw/models/whisper/ggml-base.bin` muestra ~141 MB.

Elegir el modelo por la dificultad del audio, no por tamano a ojo: `base` alcanza una conversacion a dos voces cuando el tramo hablado esta recortado. `small` (466 MB) sobre el mismo audio recortado entra en bucle y repite una frase fija; `medium` (1,4 GB) transcribe el tramo recortado con suficiente fidelidad para citar, a costa de ~170 ms por run de encode. Probar `small` y `medium` SOLO despues de recortar el silencio, y quedarse con la salida que se pueda citar sin adivinar.

## 4. Transcribir
```bash
cd /tmp/video-tx
whisper-cli -m ggml-base.bin -f audio16.wav -l en -otxt -of <salida> --no-timestamps
```
Ajustar `-l` al idioma real del audio; con `-l en` sobre audio en espanol la salida sale plausible pero inventada.
Check: `<salida>.txt` existe, tiene mas de 200 palabras y la `decode time` en las timings es de segundos, no minutos (si tarda minutos, el modelo elegido es grande para la maquina).

## 5. Frames si la narración no alcanza
Si el video puede tener slides o pantallas que la narración no cubre, extraer frames para verlos como imágenes:
```bash
ffmpeg -i "<video.mp4>" -vf fps=1/30 /tmp/video-tx/frame_%03d.png
```
Mirarlos con view_image antes de afirmar que la transcripción cubre todo el contenido.

## Entrega
- Ofrecer persistir transcripción + resumen en Markdown en la carpeta de docs del proyecto (p.ej. `docs/entrevistas/<proyecto>/orientacion-transcripcion.md`) en vez de dejar todo en `/tmp`.
- Preguntar si hay contenido visual que la narración no menciona antes de dar la transcripción por entregable completo.