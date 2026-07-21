# STATUS — Psicólogo App

**Estado:** MVP funcional ✅
**Fase actual:** Fase 1 completa — MVP listo para testear
**Última actualización:** 2026-07-21

## Lo que está hecho
- [x] Product discovery completo
- [x] ADRs: stack, WhatsApp channel, mobile-first PWA
- [x] Scaffold del proyecto (Next.js 15 + Supabase + shadcn/ui)
- [x] Supabase conectado (URL, anon key, service key)
- [x] Schema aplicado (pacientes, sesiones, config, recordatorios con RLS)
- [x] Auth configurado (email/password, login page, middleware)
- [x] **Dashboard con datos reales** (stats + sesiones del día)
- [x] **CRUD de pacientes real** (listado, detalle, alta funcional)
- [x] **Agenda semanal con datos reales**
- [x] Build exitoso ✅

## Próximo paso
- [ ] Agendar sesiones desde la UI
- [ ] Recordatorios WhatsApp
- [ ] Testing con Martín (early adopter)

## Cómo probar
1. `cd projects/psicologo-app`
2. `npm run dev`
3. Ir a http://localhost:3000
4. Login con gonzoblasco@icloud.com
5. Agregar pacientes, ver dashboard, explorar agenda
