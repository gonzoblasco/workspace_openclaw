# EVALUATION — Psicólogo App

## Mercado
- **Tamaño:** ~60.000 psicólogos en Argentina (aprox). Segmento consultorio propio: ~40%.
- **Crecimiento:** estable, la demanda de salud mental crece post-pandemia.
- **Competidores directos:**
  - **TurnosApp / DoctorPlus:** apps generalistas de turnos médicos. No específicas para psicología.
  - **PsyTools / Terapify:** plataformas de terapia online. No apuntan a gestión de consultorio.
  - **Excel / Google Calendar:** lo que usan hoy. Gratis pero desorganizado.
  - **WhatsApp:** el "CRM" del psicólogo argentino.
- **Diferenciación:** ninguna app existente combina agenda + recordatorios + seguimiento entre sesiones + registro clínico en un solo producto pensado para el psicólogo clínico argentino.

## Competidores indirectos
- **Notion / Airtable:** usados por psicólogos tech-savvy. Curva de aprendizaje alta.
- **Sistemas de obras sociales:** horribles, nadie los quiere usar.

## Viabilidad técnica
- **Stack:** Next.js 15 + Supabase es ideal para este tipo de app CRUD con necesidades de auth y tiempo real.
- **WhatsApp API:** Meta Business API requiere aprobación. Alternativa: WhatsApp Cloud API (gratis para envío de plantillas) o usar un servicio como Twilio.
- **Riesgo técnico bajo:** es una app CRUD con notificaciones. No hay ML ni procesamiento complejo en el MVP.
- **Tiempo estimado MVP:** 2-3 semanas (una persona fullstack).

## Riesgos
- **Regulación:** datos de salud en Argentina. Supabase en US puede ser issue legal. Alternativa: hostear en Argentina o usar Supabase con DPA firmado.
- **Adopción:** el target no es tech-savvy. La UI tiene que ser ridículamente simple.
- **WhatsApp API:** puede tener costos o restricciones. Validar antes de comprometer la arquitectura.

## Fit estratégico
- **Para Gonzo:** proyecto chico, rápido, concreto. Bueno para portfolio y para validar el workflow de product discovery.
- **Para el psicólogo:** resuelve un dolor real sin sobredimensionar.
- **Riesgo:** que no pase de MVP si el psicólogo no lo adopta. Pero como ejercicio de discovery vale la pena.

## Conclusión
✅ Construir. MVP acotado, 2-3 semanas, partnership con el psicólogo como early adopter y validador.
