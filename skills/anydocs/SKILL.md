---
name: "anydocs"
description: "Indexa y busca documentación técnica localmente desde sitemaps"
---

# anydocs

## Descripción
Indexa cualquier sitio de documentación a partir de un sitemap URL, construye un índice de búsqueda local, y permite queries keyword, hybrid, o regex. Soporta múltiples perfiles de documentación con cache local.

## Cuándo usarlo
- Para buscar en documentación de APIs sin salir de la terminal
- Para indexar documentación de nuestro stack (Supabase, Next.js, shadcn/ui, Biome)
- Para construir agents que referencien documentación on-demand
- Para consultar múltiples sitios de documentación desde una herramienta

## Workflow
1. Identificar el sitemap URL de la documentación a indexar
2. Ejecutar anydocs con la URL del sitemap
3. Esperar a que se construya el índice local
4. Realizar queries sobre la documentación indexada
5. Cambiar de perfil para consultar otra documentación

## Notas
- La indexación inicial puede ser lenta para docs grandes, pero es one-time
- El cache local acelera consultas subsecuentes
- No requiere API keys externas
