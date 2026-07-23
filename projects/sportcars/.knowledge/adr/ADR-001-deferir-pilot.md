# ADR-001 — Deferir integración automática con Pilot CRM al Post-MVP

## Estado
Aceptado

## Contexto
Sport Cars ya usa Pilot CRM internamente. La hermana de Gonzo trabaja como vendedora pero no tiene acceso admin al módulo de configuración de Pilot. Para integrar el sitio con Pilot se necesitan:
- `app_token` (visible en pantalla inicial del módulo Admin)
- `sub_origen` (código en Admin > Origen de Datos)
- `company_code` para autenticación JWT
- Posiblemente acceso al webhook `/pilot/leadcreation/webhook`

Sin un contacto con permisos admin, no podemos garantizar que consigamos estas credenciales en el timeline del MVP.

## Decisión
No bloquear el MVP por la integración con Pilot. El sitio captura leads en Supabase y notifica al vendedor. La sincronización automática con Pilot se implementa en una release posterior cuando se consigan credenciales.

## Consecuencias

### Positivas
- El MVP puede lanzarse en semanas, no en meses.
- Se demuestra valor comercial rápidamente.
- La arquitectura está preparada para agregar Pilot luego.

### Negativas
- Doble trabajo temporal: leads en Supabase + carga manual en Pilot.
- Riesgo de que el vendedor no cargue los leads puntualmente.
- Menos "wow" técnico en la demo inicial.

## Mitigaciones
- Panel simple de leads para que el vendedor vea y copie datos fácilmente.
- Notificación inmediata por WhatsApp/email con todos los datos del lead.
- Exportación a CSV para carga masiva en Pilot.

## Alternativas consideradas
1. **Esperar a conseguir credenciales antes de lanzar:** rechazada porque retrasa indefinidamente el MVP.
2. **Pedir acceso admin a la hermana:** rechazada porque no lo tiene y podría generar fricción interna.
3. **Usar Cliengo como puente:** rechazada porque Gonzo quiere chatbot custom y Cliengo es un SaaS extra.

## Notas
- Esta ADR se revisa cuando se obtengan credenciales de Pilot.