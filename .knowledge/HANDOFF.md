# HANDOFF - workspace

**Fecha:** 2026-10-27 16:36 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-27). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-27.md`.

---

## Que se hizo en esta sesion

Sesion de cierre: evaluacion y descarte de Moderno Diffusion, y auditoria de la tabla learnings de memory.db. (1) Moderno Diffusion (repo publico de Jose): se evaluo, se instalo y se depuro la app Electron en Apple Silicon, y se descarto. Se corrigieron 3 bugs reales en un branch local (fix/macos-arm64-stability, 3 commits, NUNCA pusheado): tensorflow==2.10.0 no tiene ruedas arm64 (pin a >=2.13.0,<2.14.0), PIL.Image.ANTIALIAS eliminado en Pillow 10 (a Image.Resampling.LANCZOS), y el img2img derivaba la resolucion del tamaño nativo de la foto (3264x4912) y mataba el backend por OOM sin traza (guard de 512x768 + 7 tests). Se midio con datos el comportamiento de las imagenes como base: SIN mascara, input_image_strength es suma cero (strength 0.35-0.40 cambia la ropa Y regenera la cara; 0.45-0.75 conserva la cara y el prompt no aplica); CON mascara la identidad se conserva de forma absoluta (face_diff = 0.29 sobre 255 en 7 corridas, pixel a pixel). La mascara tiene polaridad INVERTIDA (blanco = se repinta) y se reescala con la imagen (sin force_use_given_size deja de coincidir). Gonzo decidio descartar el proyecto y BORRAR TODO: repo clonado, carpetas temporales, scripts, logs, ~/.modernodiffusion (5,4 GB con modelos y la foto personal) y los datos de Electron, dejando solo las enseñanzas. Los 3 commits del branch se perdieron con el repo (nunca se publicaron). (2) Auditoria de la tabla learnings: un DELETE mio borro 9 lecciones REALES porque asumi que el cuerpo vivia en la columna content, cuando la tabla lo guarda en title (y en tags en otras filas). Se restauraron 9 desde copia, verificadas fila por fila. La auditoria encontro 4 defectos estructurales, no un error: (a) el cuerpo no tiene lugar fijo (content/title/tags) y el export solo lee content, asi que esas lecciones se veian como seccion vacia; (b) add-learning escribia en la columna tags y nunca en la junction learning_tags, que es lo UNICO que lee el export: 79 filas con tags invisibles; (c) memory-catalog-v2.py cortaba el cuerpo a 500 chars con el mismo valor del embedding: 34 filas a la mitad, 20 recuperables del corpus (buscando el fragmento del MEDIO, no el prefijo); (d) el truncado no era bug sino decision: un tope de la API no es un tope del dato. Se recuperaron 9 cuerpos, 20 truncadas y se repoblaron 79 junctions: +25.231 chars de cuerpo que estaba perdido y no se veia en ninguna vista. Causas raiz corregidas: add-learning escribe en la junction (una sola invocacion SQL, porque last_insert_rowid() en un proceso sqlite3 separado devolvia 0 y violaba la FK) y el catalogo ya no trunca el cuerpo. Gate nuevo scripts/check-learnings-integrity.py en el pre-commit, RECALIBRADO: la primera version reportaba 169 filas y era inutil, asi que separa PERDIDA (bloquea) de RUIDO HISTORICO (avisa): 0 perdidas, 70 avisos. Probado sembrando el defecto: bloquea con exit 1. Ademas se recuperaron 4 lecciones que existian solo en los .md y la regeneracion iba a borrar, y se devolvio a la DB la version larga (2399 chars, 4 casos con tabla) de la leccion del filtro de idioma, que la DB guardaba truncada a 565. El commit fue bloqueado por otro guard (rutas rotas) porque una leccion citaba scripts/verify-schema.sh sin calificar: la propia leccion decia como arreglarlo y la ruta real era projects/kanam-onwheels/scripts/verify-schema.sh. Tres lecciones nuevas en memory.db (301, 302, 308) y 2 commits (635770b3a0, 4f1d78e1ea).

## Estado actual

Moderno Diffusion evaluado y descartado; todo borrado del disco (5,4 GB liberados), solo quedan 2 lecciones en docs/learnings. Tabla learnings auditada y reparada: 0 perdidas, 70 avisos historicos, gate en el pre-commit. El branch fix/macos-arm64-stability con los 3 commits se perdio al borrar el repo (nunca se pusheo, no habia OK para publicar).

## Proximos pasos

1. Nada pendiente de esta sesion: el proyecto se descarto por decision de Gonzo y la limpieza esta completa. Lo unico abierto es de fondo: 14 lecciones siguen truncadas a 500 chars y NO son recuperables (no existen en la DB, ni en el corpus de sesiones, ni en la historia de los .md); reconstruirla requiere volver a la sesion original. Tambien 51 filas conservan prosa en la columna tags (es el fragmento del titulo, ruido historico, no perdida) y 8 tienen titulo desproporcionado pero cuerpo correcto.

## Decisiones y contexto que no debe perderse

- DECISION DE GONZO (27/10): Moderno Diffusion no se va a usar; borrar TODO (repo, temporales, datos de la app con la foto personal y los modelos) y conservar solo las enseñanzas y conclusiones. Lo que se le transmite a Jose: el repo publico NO es el producto (el motor nativo arm64 esta en .gitignore, el repo solo tiene el fallback por CPU) y las limitaciones al usar imagenes como base (sin mascara es regeneracion, con mascara la identidad se conserva pero el prompt solo manda sobre la textura, no sobre el color; la mascara tiene polaridad invertida). El gate de integridad de learnings separa perdida de ruido porque un guard que reporta 169 filas no se lee ni se respeta.

## Archivos tocados

```
docs/CHANGELOG.md
docs/entrevistas/_general/job-search-tracker.md
docs/entrevistas/eit-htc-disney/Gonzalo_Blasco_Lead_Digital_Accessibility_Resume.docx
docs/entrevistas/eit-htc-disney/Gonzalo_Blasco_Lead_Digital_Accessibility_Resume.pdf
docs/entrevistas/eit-htc-disney/Gonzalo_Blasco_Lead_Software_Engineer_Digital_Accessibility.docx
docs/entrevistas/eit-htc-disney/Gonzalo_Blasco_Lead_Software_Engineer_Digital_Accessibility.pdf
docs/entrevistas/eit-htc-disney/eit-cv-gonzalo-blasco-a11y.md
docs/entrevistas/mercadopago-ux-expert/Gonzalo_Blasco_UX_Expert_Software_MercadoPago.docx
docs/entrevistas/mercadopago-ux-expert/Gonzalo_Blasco_UX_Expert_Software_MercadoPago.pdf
docs/entrevistas/mercadopago-ux-expert/cv-ux-expert-mercadopago.md
docs/entrevistas/mural-growth-senior-swe/Gonzalo_Blasco_Senior_SWE_Growth_Mural.docx
docs/entrevistas/mural-growth-senior-swe/Gonzalo_Blasco_Senior_SWE_Growth_Mural.pdf
docs/entrevistas/mural-growth-senior-swe/cv-senior-swe-growth-mural.md
docs/entrevistas/ryz-labs-ai-first-frontend/Gonzalo_Blasco_AI_First_Frontend_Engineer_RYZ.docx
docs/entrevistas/ryz-labs-ai-first-frontend/Gonzalo_Blasco_AI_First_Frontend_Engineer_RYZ.pdf
docs/entrevistas/ryz-labs-ai-first-frontend/cv-ai-first-frontend-ryz.md
docs/entrevistas/sol-senior-fullstack/Gonzalo_Blasco_Senior_Full_Stack_AI_Native.docx
docs/entrevistas/sol-senior-fullstack/Gonzalo_Blasco_Senior_Full_Stack_AI_Native.pdf
docs/entrevistas/sol-senior-fullstack/cv-senior-fullstack-ai-native-gonzalo-blasco.md
docs/entrevistas/sol-senior-fullstack/sol-seguimiento.md
docs/entrevistas/team-international-tempo/README.md
docs/entrevistas/team-international-tempo/cv-senior-frontend-growth-gonzalo-blasco.md
docs/entrevistas/team-international-tempo/cv-senior-frontend-growth-gonzalo-blasco.pdf
memory/career-facts.md
scripts/check-cv-facts.py
studies/english/README.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-27.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
