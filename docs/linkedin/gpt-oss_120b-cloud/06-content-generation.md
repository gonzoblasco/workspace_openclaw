# Kanam OS: Generación de contenido visual y auditivo

**Hook**
> "Una imagen vale más que mil palabras, y un video aún más. Deja que los agentes de STUDIO creen el material de marketing por ti."

## Herramientas del agente STUDIO
- `image_generate` - crea imágenes a partir de prompts.
- `music_generate` - produce jingles o música de fondo.
- `video_generate` - genera videos breves con imágenes o clips.
- `show_widget` - inserta el arte en el dashboard para revisión.

## Flujo de creación de un post de LinkedIn
1. **CORE** envía un mensaje a **STUDIO** con `sessions_send` solicitando una portada para el artículo.
2. **STUDIO** usa `image_generate` con prompt específico (p. ej. “Kanam OS multi-agent diagram”).
3. Cuando la imagen está lista, **STUDIO** la adjunta al markdown del artículo (`docs/linkedin/...`).
4. Opcional: generar una pista musical corta (`music_generate`) y añadirla como comentario de voz en la publicación.
5. **DEV** revisa el markdown y los assets antes de la publicación.

## Buenas prácticas
- **Consistencia visual**: usar la misma paleta (teal/green) y estilo minimalista.
- **Tamaño**: imágenes 1024×768 px para LinkedIn, videos ≤ 30 s, 720p.
- **Revisión humana**: antes de publicar, el borrador debe pasar por `sessions_send` a `DEV` con `thinking:high` para que el agente solicite confirmación.

---
**CTA**: En el próximo post veremos cómo proteger nuestras credenciales y secretos con la herramienta `secrets`.
