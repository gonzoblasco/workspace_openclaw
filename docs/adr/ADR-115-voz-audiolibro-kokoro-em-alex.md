# ADR-115: La voz del audiolibro es Kokoro em_alex con post-proceso fijo

**Status:** Accepted (2026-11-18)
**Supersedes:** —
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-11-18
**Origen:** instruccion directa de Gonzo tras escuchar la muestra ("esa sera nuestra voz SIEMPRE... es genial alex-jazz-10")

---

## Contexto

*Las Tres Sabanas* tiene 26.087 palabras en 17 capitulos y necesita audio. Se probaron tres
caminos en una sola noche, y la decision no salio de una preferencia estetica: salio de medir.

**1. Voz del sistema (Paulina).** Descartada de entrada por robotica. Sin numeros: el oido alcanzo.

**2. Chatterbox multilingual (local, GPU).** Elegida primero por el `exaggeration`, la unica perilla
de emocion disponible en local. Se renderizaron los capitulos 1 y 14. Funciona, pero:

- 268 s para 620 caracteres. El capitulo 14 (2.232 palabras) tardo **67 minutos**.
- **Genera cola alucinada.** El capitulo 1 tenia 7,6 s de basura al final: respiraciones,
  chasquidos, un murmullo que Gonzo describio como "se metio un demonio en mi IA".
- **Genera siseos en el medio.** A 1,88-2,12 s del render de prueba, un bloque de -41 dB con
  zero-crossing en 0,24 (diez veces el de una voz humana): ruido de banda ancha sin fundamental.
- La causa raiz es estructural: es un TTS autoregresivo. Genera token por token y **no tiene
  concepto de silencio**; el silencio tambien hay que generarlo, y a veces lo genera mal.

**3. Kokoro-82M (local, no autoregresivo).** Elegida. Mismo texto, misma frase, medido:

| | Chatterbox | Kokoro |
|---|---|---|
| Tiempo por muestra (620 car.) | 268 s | **11 s** |
| Cola de basura | 7,6 s | **0,40 s** |
| Siseo a 1,88 s | si, -41 dB | **no existe** |
| Chasquido a 3,58 s | si | **no existe** |
| Silencios | 2, uno roto | **9, todos reales** |

Kokoro no puede alucinar cola porque no genera token por token: renderiza el audio completo de una
vez. El precio es menos emocion por frase; el beneficio es que un audiolibro de 17 capitulos no
necesita cirugia de audio en cada tramo.

## Decision

**La voz del audiolibro de *Las Tres Sabanas* es Kokoro-82M, voz `em_alex`, con esta cadena fija:**

```
voz        em_alex
velocidad  1.075
semitono   -3
grano      0.25
aire       +1 dB
```

Son los **defaults** de `scripts/tts-kokoro.py`: `python3 scripts/tts-kokoro.py capitulo.md --out salida.m4a`
produce directamente esta voz, sin parametros. Cambiarla exige tocar el default, no pasar flags.

### Por que esos numeros y no otros

- **Velocidad 1.075, no 0.92.** La velocidad de Kokoro **no se traduce 1:1 en duracion total**: las
  pausas entre parrafos no se escalan, solo el habla. Medido: 0,92 -> 39,0 s; 1,06 -> 35,6 s;
  1,10 -> 34,8 s. Para bajar 10% del total hay que subir ~17% la velocidad del habla. 1.075 da
  35,3 s sobre los 39,0 originales: el 10% que se pidio, calibrado y no calculado.
- **-3 semitonos.** Es el limite donde el timbre deja de sonar grave y empieza a sonar procesado.
  Probado a -2, -3, -4 y -5; a -5 el baritono se vuelve artificial.
- **Grano 0.25.** No es `chorus`: **ese filtro de ffmpeg rompe a 24 kHz** (el delay es mas corto que
  su buffer interno y devuelve error 234). El desdoble se arma con `asplit` + `adelay 28 ms` + `amix`.

### Limite conocido

Kokoro tiene un componente estocastico: dos renders del mismo texto **no son identicos bit a bit**.
Se observo la misma frase con y sin un silencio de 5,03 s. La duracion y la estructura de pausas se
mantienen; la respiracion no. Consecuencia operativa: **se escucha antes de publicar**, no se asume
que una corrida salio igual a la anterior.

## Consecuencias

- Los capitulos 1 y 14, renderizados con Chatterbox, quedan **obsoletos** como audio de referencia.
  Rehacerlos con Kokoro es trabajo pendiente, no urgente: el 14 esta roto en los 59 tramos.
- `.venvs/chatterbox` y `scripts/tts-chatterbox.py` **no se borran**: Chatterbox sigue siendo la
  unica opcion local con perilla de emocion, y si algun dia un texto pide actuacion, es ahi donde se
  mira. Pero no es la voz del proyecto.
- `scripts/voz-jazz-test.py` queda como el banco de pruebas de la escalera de tonos, sin uso diario.
- El pipeline A/B no aplica: esto no es codigo, es audio generado con un comando reproducible.
