# DEFINITION — Psicólogo App

## MVP Scope (Fase 1)

### Feature Set

#### 1. Gestión de Pacientes (CRUD)
- [ ] Alta de paciente: nombre, teléfono, email, motivo de consulta, obra social (opcional)
- [ ] Editar / eliminar paciente
- [ ] Lista de pacientes con búsqueda
- [ ] Perfil de paciente: datos + historial de sesiones

#### 2. Agenda de Sesiones
- [ ] Calendario semanal con slots configurables (duración de sesión, días y horarios de atención)
- [ ] Agendar sesión: seleccionar paciente, fecha, hora, duración
- [ ] Cancelar / reprogramar sesión
- [ ] Vista del día: lista de sesiones ordenadas
- [ ] Confirmación de asistencia (check-in manual)

#### 3. Recordatorios Automáticos
- [ ] Recordatorio 24h antes vía WhatsApp
- [ ] Recordatorio 2h antes vía WhatsApp
- [ ] Si no confirma → re-recordatorio 1h antes
- [ ] Configuración: activar/desactivar recordatorios por paciente

#### 4. Registro de Sesión (mínimo)
- [ ] Notas de sesión: campo de texto libre
- [ ] Fecha y paciente asociados automáticamente
- [ ] Historial de notas por paciente (ordenado cronológicamente)

#### 5. Dashboard
- [ ] Próximas sesiones del día
- [ ] Pacientes que no confirmaron
- [ ] Sesiones del mes (contador rápido)

### No incluye en MVP
- ❌ Facturación / obra social
- ❌ Seguimiento entre sesiones (ejercicios diarios)
- ❌ Transcripción voz a texto
- ❌ Detección de patrones
- ❌ Portal del paciente
- ❌ App nativa (PWA sí)
- ❌ Multi-profesional (un solo psicólogo)

## User Personas

### Persona 1: Martín (el psicólogo)
- **Edad:** 38
- **Pacientes/semana:** 15-20
- **Dolor principal:** "Se me olvida avisar a los pacientes y después se olvidan ellos. Pierdo 2-3 sesiones por mes."
- **Tech level:** usa WhatsApp, Instagram, Google. No es power user pero tampoco analfabeto digital.
- **Objetivo:** "Quiero algo simple que me avise a mí y a los pacientes, y que no tenga que pensar."

### Persona 2: Paciente tipo
- **Edad:** 25-45
- **Relación con la tecnología:** usa WhatsApp todo el día. No va a instalar otra app.
- **Comportamiento:** olvida sesiones, agradece el recordatorio, a veces cancela a último momento.

## User Flow (sesión típica)

1. Martín abre la app → ve el dashboard con sesiones de hoy
2. Toca "Agendar nueva sesión" → selecciona paciente, fecha, hora
3. El sistema agenda y programa recordatorios automáticos
4. 24h antes → paciente recibe WhatsApp: "Recordatorio: tenés sesión mañana a las 15:00. Confirmá con 👍"
5. 2h antes → si no confirmó, otro WhatsApp
6. Martín llega a la sesión → toca "Iniciar sesión" → escribe notas
7. Al cerrar, las notas quedan guardadas en el historial del paciente

## Métricas de éxito (MVP)
- **Adopción:** Martín usa la app para agendar TODAS sus sesiones en la primera semana
- **Reducción de ausencias:** pasar de 2-3 ausencias/mes a 0-1
- **Tiempo ahorrado:** Martín reporta ahorro de al menos 30 min/semana en gestión administrativa
- **NPS:** Martín recomendaría la app a un colega (score 8+)

## Posicionamiento
> "La agenda de tu consultorio que no te hace pensar. Pacientes que no se olvidan, sesiones que no se pierden."
