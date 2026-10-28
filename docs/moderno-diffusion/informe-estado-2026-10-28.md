# Informe de estado - Moderno Diffusion (`Breacorp/Moderno-Diffusion`)

**Fecha:** 2026-10-28
**Alcance:** auditoría técnica, legal-licenciamiento y de producto sobre `main` (`b5a16e8`, tag `v2.5.1`)
**Método:** clonado del repo, diff contra el upstream de origen, build real del renderer, lint, verificación de artefactos publicados (Hugging Face) y lectura de código.
**Autor del informe:** colaborador del repositorio (revisión independiente)
**Revisión:** verificado de forma independiente el 2026-10-28 - se recomputaron el solapamiento con el upstream, el lint, el conteo de assets, el estado del lockfile y los pesos del modelo publicado. Las cifras de este documento son las verificadas; ver nota al pie.

---

## 1. Resumen ejecutivo

El proyecto **no es un producto en estado de entrega**: es un **rebranding avanzado y funcional de un proyecto de terceros (DiffusionBee, AGPL-3.0)**, con documentación y marketing escritos como si fuera un desarrollo propio terminado.

Tres conclusiones:

1. **El código es 76 % idéntico al upstream** (139 de 182 archivos, byte a byte). El resto son cambios de marca, configuración de build y parches de resolución de rutas. No hay módulo de inferencia propio.
2. **Hay un problema de licenciamiento de severidad alta**: se conserva el `LICENSE` AGPL-3.0 del upstream, pero el README y el diálogo *Acerca de* declaran software propietario ("Todos los derechos reservados"), sin atribución al autor original, y se distribuye un binario nativo (`core/moderno_backend`) cuyo código fuente no está en el repositorio.
3. **El build es reproducible en parte**: el renderer compila (`npm install` + `npm run build` → `dist/` OK), pero el empaquetado del `.app` depende de un directorio `core/` que está *gitignoreado* y de una ruta absoluta hardcodeada a la máquina de un desarrollador. Desde un clon limpio, la app **no se puede reconstruir tal como se distribuye**.

Adicionalmente: el modelo "Moderno Diffusion Fast 0.1" está publicado con claims de destilación/poda que **no tienen artefacto reproducible**, y el propio archivo `WEIGHTS_LICENSE` heredado afirma lo contrario ("los pesos no fueron modificados, solo reformateados").

**Veredicto:** presentable como *demo interna / prototipo con marca*, **no** como release público ni como producto con claims de rendimiento y privacidad.

---

## 2. Evidencia: es un fork de DiffusionBee

Comparación de árboles de trabajo contra `divamgupta/diffusionbee-stable-diffusion-ui` (`daf82f8`):

| Métrica | Valor |
|---|---|
| Archivos en el upstream | 183 |
| Archivos en Moderno Diffusion | 220 |
| Archivos en común | 182 |
| **Idénticos byte a byte** | **139 (76,0 %)** |
| Modificados | 43 |
| Borrados del upstream | 1 (`diffusionbee_backend.py`) |
| Nuevos | 38 |

El "backend reescrito" es en realidad un **rename con 10 líneas de diferencia** (una de ellas, `sys.path.insert`):

```
diffusionbee_backend.py → backend.py
- projects_root_path = os.path.join(home_path, ".diffusionbee")
+ projects_root_path = os.path.join(home_path, ".modernodiffusion")
- def diffusion_bee_main():
+ def moderno_diffusion_main():
+     sys.path.insert(0, dir_path)
  (y un comentario de ejemplo de invocación reescrito)
```

Lo mismo en el resto de los "feats" de mayor peso:

| Commit | Cambio real |
|---|---|
| `refactor(bridge): rename binary search candidate to moderno_backend` | 6 líneas en `bridge.js` |
| `feat(models): set Moderno Diffusion Fast 0.1 as default model` | 2 líneas en `sd_options_adv.json` |
| `feat(ui): add visual style presets … multi-LoRA` | 32 PNG + `styles_data.json` + 51 líneas en `BasicSDApplet.vue` |
| `feat: initial commit - rebranding to Moderno Diffusion` | 186 archivos, 51.286 líneas (historia *squasheada*: sin trazabilidad de origen) |

El primer commit se llama literalmente *"initial commit - rebranding to Moderno Diffusion"*: **no hay historia previa que acredite el origen**, lo que además inutiliza `git blame` y cualquier auditoría de procedencia. El repositorio tiene 26 commits en total, y 5 de ellos son actualizaciones del log de sesión (`memory/`).

---

## 3. Estado técnico

### 3.1 Verificado - funciona

- `npm install` en `electron_app/`: **OK** (1.948 paquetes).
- `npm run build`: **OK** - `dist/` generado en 4,6 s (app.js 3,6 MB / 1,4 MB gzip, `chunk-vendors` 917 KB). Compila y sirve.
- Integridad del modelo: el MD5 declarado en `BasicSDApplet.vue` (`aabb73c2fd2de59edd70cf117e464677`) **coincide con el archivo publicado** en Hugging Face (2.440.763.520 bytes verificados). El sistema de verificación de descargas no está roto.
- Los 31 estilos visuales existen (`styles_data.json`, 31 entradas) y la inyección de prompt en `StableDiffusion.vue:207` está implementada.
- `electron_app/package-lock.json` **está commiteado** (850.289 bytes, blob `bdee174`, presente desde el commit inicial).

### 3.2 Defectos verificados

| # | Severidad | Hallazgo | Evidencia |
|---|---|---|---|
| 1 | **Crítica** | Ruta absoluta hardcodeada a la máquina del dev, como último candidato de resolución del intérprete | `electron_app/src/bridge.js:41` → `/Users/joseluis/proyectos/SDifussion/diffusion-stable-diffusion-ui-master/.venv/bin/python` |
| 2 | **Crítica** | El motor nativo (`core/moderno_backend`, `realesrgan_ncnn_macos`) **no está en el repo** (`core/` está en `.gitignore`) → el `.app` distribuido no se puede reconstruir desde el código | `.gitignore:7`, `bridge.js:47-56`, `native_functions.js:450-458` |
| 3 | **Media** | Reproducibilidad nominal, no exigida: el `package-lock.json` de la app **sí existe y está versionado**, pero en la raíz hay un stub de 95 bytes (`"packages": {}`), el flujo documentado usa `npm install` en vez de `npm ci`, y no hay CI que valide ninguno de los dos | `git ls-tree HEAD`; `package-lock.json` raíz |
| 4 | **Alta** | `"main": "background.js"` apunta a un archivo inexistente (el real es `src/background.js`). Solo funciona porque `vue-cli-plugin-electron-builder` lo parchea al empaquetar; `electron .` falla | `electron_app/package.json:20` |
| 5 | **Alta** | **0 tests, 0 CI**. No hay `.github/`, ningún archivo de test. Todo el flujo de inferencia (IPC, bridge, forms) está sin red de seguridad | repo completo |
| 6 | **Media** | Lint en rojo: **23 errores** (`no-unused-vars` ×16, `no-empty` ×3, `vue/valid-template-root` ×2, `no-redeclare` ×1, `no-mixed-spaces-and-tabs` ×1) | `./node_modules/.bin/vue-cli-service lint --no-fix` |
| 7 | **Media** | Endpoint heredado de terceros: el botón *Compartir* sigue publicando en **arthub.ai**, y el upload va a `https://studio.moderno.com.ar/api/upload`. El commit `be4318c` dice "remove competitor discord link" pero dejó el competidor en el flujo de share, incluido en `History.vue` | `electron_app/src/utils.js:132,147,156`; `pages/History.vue:232` |
| 8 | **Media** | Asset externo hardcodeado en la UI: una foto de perro del CDN de Hearst (`hips.hearstapps.com`) como `img src` de un selector | `components_bare/inputform/BetterSelector.vue:9` |
| 9 | **Media** | Sin migración de datos de usuario: el cambio `.diffusionbee` → `.modernodiffusion` abandona historial y modelos importados de la versión anterior. No hay código de migración | `backend.py`, `native_functions.js:350-609` |
| 10 | **Media** | Versión inconsistente: tag `v2.5.1` vs `package.json` `2.3.0` vs `docs/CHANGELOG.md` `2.3.0-moderno`. El changelog tiene una única entrada | `git tag`, `package.json:3`, `docs/CHANGELOG.md:5` |
| 11 | **Media** | Stack EOL: Electron 13 (sin soporte desde 2022), Vue 2 (EOL dic-2023), `bootstrap-vue`, `vue-analytics`, `babel-eslint`, `request`, `electron-notarize@1` | `electron_app/package.json` |
| 12 | **Baja** | `el repositorio auditado` filtra rutas locales del autor (5 ocurrencias de `/Users/joseluis/...`) y los próximos pasos ya están todos marcados en `memory/` | `el repositorio auditado` |
| 13 | **Baja** | Docs inconsistentes: `DOCUMENTATION.md` está **mezclado** - arranca en español, pasa a inglés desde *"Generating images"* y sigue así el resto -, referencia imágenes de la cuenta del autor original (`user-images.githubusercontent.com/105890749`, 7 imágenes), y describe un *"Sharing"* que sube a arthub.ai y que ya no coincide con el flujo real | `docs/DOCUMENTATION.md:9,73-76` |
| 14 | **Baja** | 77 `console.log` en el código de UI; bundle único sin code splitting (3,6 MB) | `electron_app/src` |
| 15 | **Baja** | Assets binarios (**12 MB**, 58 PNG) commiteados sin LFS; `.git` pesa 26 MB | repo |
| 16 | **Baja** | Riesgo de estado: la inyección de estilo **muta** `prompt_params` (el objeto del formulario) dentro del handler de generación → el prompt negativo del estilo se acumula entre generaciones sucesivas. Requiere confirmación en runtime | `StableDiffusion.vue:207-219` |

### 3.3 No verificable en esta revisión (declarado, no asumido)

- Inferencia real y los benchmarks de velocidad: requiere TensorFlow 2.10 + pesos de 2,4 GB; no se ejecutó generación.
- Empaquetado y firma del `.app` (216 MB, arm64) publicado en `diffusion.moderno.com.ar`.
- Soporte Windows/Intel: el README lo anuncia; `vue.config.js` **sí declara un target `win` (NSIS)**, pero `arch` se deriva de `process.arch`, así que un build hecho en Mac no produce artefactos de Windows. No hay build ni CI para esas plataformas.
- Funcionamiento efectivo de LoRA multi-slot y ControlNet en runtime (el cableado frontend→backend existe y es plausible: `BasicSDApplet.vue:131` → `SDRun.lora_tdict_paths`).

---

## 4. Licenciamiento - el riesgo más serio

### 4.1 Contradicción directa

| Fuente | Declara |
|---|---|
| `LICENSE` (idéntico al upstream, sin tocar) | **GNU AGPL v3** |
| `README.md:75` | "se distribuye bajo términos de licencia **autorizados por Moderno Tech**" |
| `background.js:168` (diálogo *Acerca de*) | "Copyright © 2026 Moderno Tech. **Todos los derechos reservados**" |

AGPL-3.0 **no es compatible** con "todos los derechos reservados". Al ser un trabajo derivado distribuido (repo público + `.app` descargable), la licencia del upstream se mantiene y obliga a:

- **(§5a)** conservar avisos de copyright del autor original y **avisar prominentemente que el trabajo fue modificado**;
- **(§4/§6)** entregar el **código fuente correspondiente completo** de lo que se distribuye binariamente - incluye el `core/moderno_backend` y los binarios ESRGAN, hoy **ausentes del repositorio**;
- **(§13)** no imponer restricciones adicionales sobre el código derivado.

Hoy **no se cumple ninguno de los tres**: no hay una sola mención a DiffusionBee ni a su autor en README, docs, historia de git ni UI (0 coincidencias), no existe archivo `NOTICE`, y el binario del motor no tiene fuente publicada. Las 12 referencias a `divamgupta` que quedan en el código son **URLs de descarga de pesos en Hugging Face**, no atribución.

Agrava el punto que el repo es **público**: cualquiera puede verificar el fork y la ausencia de atribución. El riesgo no es solo legal, es reputacional para Moderno Tech.

### 4.2 El modelo "Moderno Diffusion Fast 0.1"

Evidencia recolectada:

- Tamaño del tensor file: **2.440.763.520 bytes**, exactamente el mismo que el `sd-v1-5_fp16.tdict` del upstream.
- El encabezado con el mapa de tensores (nombres, `start`/`end`, `shape`, `dtype`) es **idéntico** al del SD 1.5 fp16 de `divamgupta/stable_diffusion_mps`.
- Los bloques de datos **sí difieren**: en 12 muestras de 1 KB distribuidas a lo largo del archivo, **1 coincidió y 11 no** (~92 % de bytes distintos). → **no es una copia byte a byte**; es otro juego de pesos con el mismo layout.

Conclusión honesta: **no puedo afirmar que sea SD 1.5 renombrado ni que sea un modelo destilado.** Lo que sí puedo afirmar:

- La model card afirma *"destilación latente y poda estructurada"* y las tags incluyen `distilled`.
- El `WEIGHTS_LICENSE` heredado en el repo dice literalmente: *"The weights content has not been modified as part of this reimplementation (**only reformatted**)"*. **Contradicción directa con la model card.**
- El benchmark publicado atribuye la mejora "45-55 % más rápido" a la arquitectura, pero su propia tabla compara **25 steps vs 20 steps**: la mayor parte de la ganancia se explica por generar con menos pasos, no por destilación.
- No hay receta de conversión, script de entrenamiento, dataset, ni `model-index`. El repo `ModernoTech/moderno-diffusion-fast-0.1` tiene 0 descargas y 0 likes.

Riesgo: un claim de "modelo propio destilado" sin evidencia reproducible es el tipo de afirmación que se desarma en una demo técnica frente a un cliente o un inversor.

### 4.3 Privacidad

El README titula **"Privacidad Integral Zero-Cloud"**, pero el flujo de *Compartir* sube imágenes a `studio.moderno.com.ar/api/upload` y luego abre `arthub.ai`. Es defendible (es opt-in, por acción del usuario, igual que el upstream), pero **la formulación "zero-cloud" es falsa tal como está escrita** y no hay política de privacidad enlazada en el repo.

### 4.4 Contenido de terceros sin trazabilidad

- `electron_app/src/assets/styles_data.json` - los 31 estilos (prompts + negative prompts) coinciden con las listas de estilos ampliamente difundidas del ecosistema SDXL/Fooocus. **Verificar procedencia y licencia antes de distribuir.**
- 7 imágenes de documentación servidas desde la cuenta del autor original.
- La foto del CDN de Hearst embebida en la UI.

---

## 5. Claims vs. implementación

| Claim (README / memory log) | Estado real |
|---|---|
| "Suite Profesional de Generación de Imágenes" | Fork rebrandeado; 76 % del código es del upstream |
| "Modelo destilado propio, 45-55 % más rápido" | Sin artefacto reproducible; contradicho por `WEIGHTS_LICENSE`; la ganancia se explica por 20 vs 25 steps |
| "Corrección integral del backend Python" | Rename + 10 líneas |
| "Integración de motor nativo Mach-O arm64" | El binario no está en el repo; ruta de fallback hardcodeada |
| "Blindaje absoluto de identidad de marca" | Quedan `divamgupta` (12 refs), `arthub.ai`, imágenes de doc del autor original, foto de Hearst |
| "Eliminación total de endpoints externos" | Falso: upload a `studio.moderno.com.ar` y share a `arthub.ai` siguen activos |
| "Recibe actualizaciones periódicas" | No hay auto-updater ni canal de release en el código |
| "Multi-LoRA hasta 3" | Cableado plausible, sin tests ni verificación runtime |
| "31 estilos visuales" | ✔ Implementado (hay 32 PNG: `craft clay1` duplicado) |
| "Integridad MD5 del modelo" | ✔ Verificado, el hash coincide |
| Soporte Windows / Intel | Target `win` declarado, pero `arch` sale de `process.arch`; no hay build ni CI para esas plataformas |

---

## 6. Lo que está bien (y conviene preservar)

- **Compila**: el renderer se construye limpio y rápido. La base del upstream es sólida.
- **La resolución de rutas del bridge está mejorada** respecto del upstream: el upstream asumía `../backends/...` y un `BIN_PATH` obligatorio; acá hay búsqueda por candidatos con `fs.existsSync` (bien, salvo la línea 41).
- **Verificación de integridad de descargas** funcionando (MD5 correcto contra el archivo real).
- **Empaquetado condicional** en `vue.config.js` (solo incluye `core/` si existe) - es una buena decisión de robustez.
- **Documentación de sesión** (`memory/`) valiosa como bitácora, aunque hoy funciona más como changelog interno que como documentación de producto.
- La UI de estilos y el modo avanzado están integrados de forma coherente con el formulario declarativo existente.

---

## 7. Recomendaciones priorizadas

### P0 - Antes de cualquier distribución o comunicación pública

1. **Resolver licenciamiento (bloqueante).**
   - Mantener AGPL-3.0 y **corregir** el README y el diálogo *Acerca de*: quitar "todos los derechos reservados", declarar AGPL-3.0 y agregar `NOTICE` con autoría original (Divam Gupta / DiffusionBee), link al repo upstream y fecha de las modificaciones (§5a).
   - Publicar el **fuente del `core/`** (backend nativo + script de build de ESRGAN) o dejar de distribuir el binario.
   - Actualizar `WEIGHTS_LICENSE` o la model card para que digan lo mismo.
   - Esfuerzo: 1-2 días (legal + 1 PR).
2. **Hacer reproducible el build distribuido.**
   - Borrar `bridge.js:41`; documentar `BACKEND_BUILD_PATH`, `BIN_PATH`, `PY_SCRIPT`.
   - Eliminar el stub de `package-lock.json` raíz y pasar el flujo documentado a `npm ci`.
   - Corregir `"main"` a `src/background.js` (o quitarlo y dejar que el plugin lo genere).
   - Añadir CI mínima: `npm ci && npm run build && npm run lint` en cada PR.
   - Esfuerzo: 1 día.
3. **Enmendar los claims del modelo.** Publicar cómo se generó el `.tdict` (script + checkpoint de origen + pasos) o bajar el tono de la model card a lo verificable. Citar benchmarks con hardware, steps y metodología, o eliminarlos.
   - Esfuerzo: 2 h + decisión de producto.
4. **Corregir la política de privacidad.** Cambiar "Zero-Cloud" por "procesamiento local; las imágenes solo salen de tu equipo si vos las compartís", y enlazar una política.
   - Esfuerzo: 2 h.

### P1 - Antes de una beta con usuarios

5. **Tests mínimos**: smoke del `bridge` (resolución de rutas con fixtures), parseo/serialización del formulario declarativo (`sd_options_adv.json` ↔ `SDRun`), e inyección de estilos. Objetivo realista: cubrir los 3 caminos que más se rompen.
6. **Lint en verde** (23 errores → 0) y `no-unused-vars` como error bloqueante en CI.
7. **Limpiar la herencia**: eliminar `arthub.ai` del flujo de share (o hacerlo explícito y configurable), sacar la imagen de Hearst, unificar `DOCUMENTATION.md` en un solo idioma con capturas propias y borrar las referencias a `user-images.githubusercontent.com/105890749`.
8. **Migración de datos** `.diffusionbee` → `.modernodiffusion` (copiar/avisar), para no romper a quien venga de la versión anterior.
9. **Versionado coherente**: alinear tag ↔ `package.json` ↔ CHANGELOG; mover `memory/` fuera del repo (o a `docs/logs/`).
10. **Verificar en runtime** LoRA multi-slot, ControlNet y el bug de acumulación de estilo en `StableDiffusion.vue:207`.

### P2 - Deuda estructural

11. Plan de upgrade de stack: Electron 13 → 30+, Vue 2 → 3 (o congelar versión y asumir EOL documentado). Es el ítem más caro del repo; hoy nadie lo está mirando.
12. Code splitting en el renderer (3,6 MB en un solo `app.js`).
13. Git LFS para los 58 PNG / 12 MB de assets.
14. Reemplazar `console.log` por un logger con niveles.

---

## 8. Criterios de aceptación sugeridos para la próxima entrega

- [ ] `git clone` limpio + `npm ci` + `npm run build` + `npm run electron:build` produce un `.app` equivalente al distribuido, **sin rutas absolutas ni pasos manuales no documentados**.
- [ ] `LICENSE` + `NOTICE` + README coherentes; atribución al upstream visible en README y en *Acerca de*.
- [ ] Fuente del motor nativo publicada, o binario eliminado del release.
- [ ] `npm run lint` con 0 errores y CI corriendo en cada PR.
- [ ] Model card del modelo con metodología reproducible y sin claims que el repo contradiga.
- [ ] `DOCUMENTATION.md` en un solo idioma, con capturas del producto actual, sin assets de terceros.
- [ ] Ningún endpoint de terceros ajeno al ecosistema Moderno Tech en el código.

---

## 9. Anexo - cómo reproducir esta auditoría

```bash
git clone https://github.com/Breacorp/Moderno-Diffusion.git && cd Moderno-Diffusion
git clone --depth 1 https://github.com/divamgupta/diffusionbee-stable-diffusion-ui.git /tmp/upstream

# 1) solapamiento con el upstream
python3 - <<'EOF'
import os,hashlib
s=lambda r:{os.path.relpath(os.path.join(d,f),r):hashlib.sha256(open(os.path.join(d,f),'rb').read()).hexdigest()
            for d,_,fs in os.walk(r) if '.git' not in d and 'node_modules' not in d for f in fs}
m,u=s('.'),s('/tmp/upstream'); c=set(m)&set(u)
print(len(u),len(m),len(c),sum(m[f]==u[f] for f in c))
EOF

# 2) build del renderer y lint
cd electron_app && npm ci && npm run build && ./node_modules/.bin/vue-cli-service lint --no-fix

# 3) integridad del modelo publicado
curl -sIL "https://huggingface.co/ModernoTech/moderno-diffusion-fast-0.1/resolve/main/moderno-fast-0.1.tdict" | grep x-linked-size

# 4) el modelo publicado vs SD 1.5 fp16: header y muestras de datos
curl -sL -r 0-511 "https://huggingface.co/divamgupta/stable_diffusion_mps/resolve/main/sd-v1-5_fp16.tdict" | xxd | head -6
# repetir con -r <offset>-<offset+1023> en varios offsets para comparar bloques de datos
```

---

**Nota final:** este informe se apoya en inspección estática, diff contra el upstream, build real y verificación de artefactos publicados. No incluye pruebas de inferencia ni de empaquetado firmado, que quedan explícitamente fuera de alcance (ver §3.3).

**Nota de verificación independiente (2026-10-28):** las cifras de este documento fueron recomputadas desde un clon limpio. Coinciden con las del informe original en el solapamiento con el upstream (183/220/182/139 → 76,0 %), el desglose del lint (16+3+2+1+1 = 23), los 77 `console.log`, los 31 estilos con 32 PNG y el duplicado `craft clay1`, las 7 imágenes del autor original, las 0 menciones a DiffusionBee, el tamaño del modelo (2.440.763.520 bytes), los 0 descargas / 0 likes y el estado del `LICENSE` frente a README y *Acerca de*. Se corrigieron cinco afirmaciones respecto de la versión original: el lockfile de la app sí está commiteado (hallazgo #3 reformulado a severidad Media), los assets pesan 12 MB y no 16, el rename del backend son 10 líneas y no 5, `DOCUMENTATION.md` está en idioma mixto y no solo en inglés, `vue.config.js` sí declara target de Windows, y el conteo de archivos nuevos es 38 (220 − 182). Se agregó además la medición por muestreo de bloques de pesos del modelo publicado.
