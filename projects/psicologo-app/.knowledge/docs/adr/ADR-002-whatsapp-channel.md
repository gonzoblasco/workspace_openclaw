# ADR-002: WhatsApp como Canal Principal de Comunicación

**Fecha:** 2026-07-21
**Contexto:** El canal de comunicación con pacientes debe ser el que ya usan. En Argentina, WhatsApp es ubicuo.

**Decisión:** Usar WhatsApp Cloud API (Meta) como canal principal para recordatorios y comunicación con pacientes.

**Opciones consideradas:**
- **Email:** baja tasa de apertura en Argentina para este perfil de usuario.
- **SMS:** caro, sin rich media, sin confirmación de lectura.
- **Notificaciones push (PWA):** requiere que el paciente instale/abra la PWA. Fricción alta.
- **WhatsApp API:** el paciente ya vive ahí. Confirmación de lectura, botones de respuesta rápida, alta tasa de apertura.

**Riesgos:**
- Meta Business API requiere aprobación y configuración inicial.
- Costo: gratuito para primeros 1,000 chats/mes, después ~$0.005/chat. Para 15-20 pacientes/semana, está dentro de lo gratuito.
- Política de Meta: no se puede usar para spam. Los recordatorios son transaccionales (esperados por el usuario), debería estar bien.

**Alternativa temporal:** Si la aprobación de Meta demora, arrancar con un placeholder que registre "recordatorio enviado" sin enviar realmente, o usar un webhook de prueba.

**Estado:** Aceptado
