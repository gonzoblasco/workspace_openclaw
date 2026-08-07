# Kanam (PWA) - Archivado

**Fecha:** 2026-08-06
**Motivo:** Decisión de Gonzo - el proyecto kanam PWA se elimina (local + repo GitHub). La idea "sistema operativo personal con IA" queda documentada por si se retoma.

## Qué se conserva acá

- `BRIEF.md` - brief original del proyecto
- `ROADMAP.md` - roadmap planificado
- `README.md` - descripción y stack

## Qué se eliminó

- Carpeta local `projects/kanam/` (con `.env` de credenciales Supabase/Ollama)
- Repo remoto `github.com/gonzoblasco/kanam` (si no pude borrarlo por permisos, el historial git del proyecto sigue existiendo ahí)

## Para retomar

Si Gonzo quiere retomar la idea, el punto de partida es este `BRIEF.md` + `ROADMAP.md`. El stack era Next.js + Tailwind + shadcn/ui + Supabase + Edge Functions (Ollama Cloud) + Vercel.

## Nota

El workspace antes trackeaba `.env.example`, `.knowledge/BRIEF.md`, `.knowledge/ROADMAP.md` y `README.md` de `projects/kanam`. Esos archivos trackeados se quitan del índice del workspace al borrar el proyecto.
