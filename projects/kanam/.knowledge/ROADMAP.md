# Kanam — Roadmap

**Versión:** 0.1
**Fecha:** 2026-07-26

---

## Semana 1: Fundación

### Día 1-2: Scaffold + Supabase
- [ ] Crear proyecto Next.js con `create-next-app`
- [ ] Configurar Tailwind + shadcn/ui
- [ ] Configurar PWA (manifest + service worker básico)
- [ ] Crear proyecto Supabase
- [ ] Configurar auth (magic link)
- [ ] Schema inicial: `entries` table
- [ ] Edge Function de prueba (ping)

### Día 3-4: Timeline + Entradas
- [ ] Página principal con timeline cronológico inverso
- [ ] Crear entrada (modal o página separada)
- [ ] Soporte para: nota rápida (texto)
- [ ] Soporte para: check-in (ánimo, energía)
- [ ] Subida de fotos a Supabase Storage

### Día 5: Pulir
- [ ] Editar/eliminar entrada
- [ ] Loading states
- [ ] Error handling
- [ ] Despliegue en Vercel

## Semana 2: IA + Calidad

### Día 6-7: IA
- [ ] Edge Function que consume Ollama Cloud
- [ ] Prompt para resumen diario
- [ ] Botón "Resumir hoy" en la app
- [ ] Guardar resúmenes en tabla `summaries`

### Día 8-9: UX
- [ ] Tags en entradas
- [ ] Filtro por tipo de entrada
- [ ] Búsqueda simple
- [ ] Vista calendario (mini)

### Día 10: Polish
- [ ] Offline support (service worker cache)
- [ ] PWA install prompt
- [ ] Testing en iOS (Safari + home screen)
- [ ] Fix de bugs

## Post-MVP

Dependiendo del uso real, evaluar:
- Writing tracker
- Notificaciones push
- Multi-tenant (invitaciones)
- Dashboard de proyectos
