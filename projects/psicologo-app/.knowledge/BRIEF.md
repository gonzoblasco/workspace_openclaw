# BRIEF — Psicólogo App

## Problema
Un psicólogo clínico con consultorio propio maneja toda su gestión de forma manual: agenda en papel o mental, recordatorios uno por uno por WhatsApp, fichas de pacientes en carpetas físicas, seguimiento entre sesiones inexistente. Esto le genera:
- Pacientes que olvidan sesiones (pérdida de ingresos)
- Tiempo administrativo que podría dedicar a pacientes
- Sin datos objetivos del progreso del paciente entre sesiones
- Dependencia total de su memoria para seguimiento

## Solución propuesta
App web (mobile-first) que centralice la gestión del consultorio: agenda, recordatorios, fichas de pacientes, y seguimiento entre sesiones.

## Usuario target
- Psicólogos clínicos en Argentina
- Consultorio propio
- 10-30 pacientes semanales
- Baja o nula adopción digital
- Presupuesto limitado (no son grandes clínicas)

## Stack propuesto
- **Frontend:** Next.js 15 (App Router), Tailwind, shadcn/ui
- **Backend/Database:** Supabase (Postgres + Auth + Edge Functions)
- **Mensajería:** WhatsApp API (Meta) o alternativa
- **Hosting:** Vercel + Supabase

## Restricciones
- MVP debe ser usable en 2-3 semanas de desarrollo
- Sin app nativa por ahora (PWA o web mobile-first)
- Cumplimiento mínimo de datos sensibles (Ley de Salud Mental Argentina)
- Presupuesto: partnership / precio amigo
