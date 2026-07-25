# DEFINITION.md — Quedamos

> Definición de producto completa. Output de Fase 0.1 (Brainstorming).

## 1. Visión

Un mundo donde hacer amigos de adulto sea tan natural como cuando éramos chicos. **Quedamos** es la plataforma que conecta personas a través de salidas reales en lugares asociados, con matching inteligente pero transparente, sin paywalls ni algoritmos opacos.

## 2. Propuesta de Valor

**Para el usuario:** Conocé gente afín sin el peso de las apps de citas ni el frío de Meetup. Salí a hacer lo que ya te gusta, con personas que probablemente te caigan bien. Sin pagar por el privilegio de socializar.

**Para el comercio:** Recibí grupos de personas con ganas de socializar en tu local. Ofrecé un descuento (ej: 15%) a cambio de visibilidad en la app. El usuario no paga, el comercio sí.

## 3. User Personas

### Primaria: Gonzo (basado en experiencia real)
- **Edad:** 43
- **Ubicación:** CABA
- **Ocupación:** Profesional, actualmente sin trabajo formal
- **Dolor:** Usó Timeleft en 2024. El matching le funcionó — conoció un grupo copado con el que empezó a salir todos los sábados. Pero:
  - Pagaba ~$15 USD + ~$50 USD de cena = **~$65 USD por salida**. Impagable sin laburo.
  - El grupo de WhatsApp derivado se volvió tóxico (admin con poder, echadas, juicios).
  - Lo echaron del grupo. Necesitó un descanso de la app.
- **Necesidad real:** Una plataforma gratuita que conecte gente afín, sin jerarquías de poder, con salidas programadas de calidad. La app es el catalizador, no el dueño de la vida social.
- **Comportamiento:** Prefiere salidas variadas (cine, teatro, almuerzo, reuniones informales). Gasta ~$40 USD por salida cuando arma por su cuenta.

### Secundaria: Santiago
- **Edad:** 25-45
- **Ubicación:** CABA
- **Ocupación:** Profesional remoto/híbrido
- **Dolor:** Llegó hace años, su círculo se achicó. Quiere conocer gente pero no sabe cómo.
- **Comportamiento:** Sale 1-2 veces por semana. Usa apps pero está harto de Tinder. Prefiere actividades con propósito (cine, café, caminar) antes que "quedar en verse".
- **Motivación:** Hacer amigos post-30 sin que sea raro.

### Terciaria: Martina
- **Edad:** 20-40
- **Ubicación:** CABA / GBA
- **Ocupación:** Estudiante / freelancer
- **Dolor:** Sus amigues se fueron del país o están en otra. Quiere expandir su círculo.
- **Comportamiento:** Activa, le gusta bailar, ir a bares, probar cosas nuevas.
- **Motivación:** Encontrar gente con quien compartir hobbies sin presión de "cita".

## 4. Principios de Diseño (lecciones de la experiencia real)

1. **Sin admins con poder absoluto.** Nadie puede echar a otro de la plataforma. A lo sumo, bloqueos individuales. No hay "dueños" de la comunidad.
2. **Los grupos son efímeros por diseño.** La app conecta, después la gente se va a WhatsApp/Telegram si quiere. No intentamos retenerlos en un chat interno.
3. **Costo cero siempre.** No es "gratis por ahora y después cobramos". Es gratis porque el objetivo no es monetizar usuarios, es conectar gente.
4. **La salida es el producto, no el usuario.** No hay algoritmo de engagement, no hay métricas de retención oscuras. La app cumple su propósito cuando la gente sale y después no la necesita más.
5. **Transparencia radical.** El algoritmo de matching es visible y explicable. No hay caja negra.
6. **Calidad sobre cantidad.** Las salidas son programadas por la plataforma en lugares asociados, no creadas por usuarios. Esto garantiza experiencia consistente y viabilidad del modelo de descuentos.

## 5. User Journey (MVP)

### Onboarding
1. Instala PWA (o abre web)
2. Registro con email o Google
3. Elige apodo (único, visible para otros)
4. Completa test de personalidad (~20 preguntas, 3 min)
5. Selecciona actividades favoritas (cine, bares, café, baile, almuerzo, etc.)
6. ¡Bienvenide! → Recibe **5 sugerencias semanales** de salidas

### Experiencia semanal (core loop)
1. **Lunes/Martes:** Recibís 5 salidas sugeridas para la semana
   - Cada sugerencia incluye: actividad, lugar, fecha, hora, cupos disponibles, participantes con compatibility score
   - Las sugerencias se basan en: tu perfil de personalidad + historial de actividades que te gustaron + compatibilidad con los asistentes
2. **Elegís:** Te sumás a 1, 2 o todas las que te copen (ocupás un cupo)
3. **24h antes:** Notificación push con recordatorio
4. **La salida:** Vas, conocés gente, la pasás bien
5. **Post-salida:** Feedback anónimo de compatibilidad con cada asistente
6. **El algoritmo aprende:** Próximas sugerencias mejoran

### Los usuarios NO crean salidas
Solo la plataforma (y eventualmente los comercios asociados) pueden programar salidas. El usuario elige a cuál sumarse. Esto permite:
- Control de calidad de las experiencias
- Gestión de cupos por lugar (20 para comida, 40 para cine, etc.)
- Modelo de monetización con comercios (pagan por visibilidad + descuentos)
- Evitar salidas fantasma o mal organizadas

## 6. Features por Fase

### MVP (Fase 1)
- Auth + apodo + test de personalidad (Big Five reducido)
- **5 sugerencias semanales** generadas por algoritmo (personalidad + historial + compatibilidad)
- Feed completo de salidas programadas (para explorar más allá de las sugeridas)
- Compatibility score visible en cada salida
- Unirse a salida (ocupa un cupo)
- Notificaciones push (24h antes)
- Feedback post-salida (anónimo, alimenta algoritmo)
- Perfil básico (apodo, bio, actividades favoritas, historial de salidas)
- Historial de actividades del usuario (para que el algoritmo aprenda preferencias)
- **Panel de administración** para programar salidas (lugares, fechas, cupos)

### Fase 2
- Sistema de confianza (reportes, bloqueos, historial de asistencias)
- Fotos opcionales (verificadas o no)
- Chat grupal temporario (expira 48h post-salida)
- Moderación mínima (reportes automáticos, sin admins humanos con poder)
- Algoritmo de recomendación de salidas mejorado (feedback loop maduro)
- Más tipos de actividad y lugares

### Fase 3
- **Promociones y descuentos en locales asociados** (15% off, 2x1, etc.)
- Locales pueden crear salidas como "anfitriones" (pagan por visibilidad)
- Mapa de salidas cercanas
- Categorías de salidas más ricas (etiquetas, vibes, rangos de precio)

### Fase 4
- Múltiples ciudades
- Eventos especiales (Quedamos Nights, salidas masivas)
- API pública para integraciones

## 7. Arquitectura Conceptual

```
[PWA - Next.js 15]
       ↕
[Supabase]
  ├── Auth (email/Google)
  ├── PostgreSQL (usuarios, salidas, lugares, feedback, matching data)
  ├── Realtime (notificaciones, actualizaciones en vivo)
  └── Edge Functions
       ├── weekly-suggester (genera 5 sugerencias por usuario/semana)
       ├── matching-engine (algoritmo de compatibilidad)
       ├── feedback-processor (actualiza perfiles post-feedback)
       └── notifications (push scheduling)
```

## 8. Modelo de Datos (Conceptual)

### users
- id, apodo (único), email, bio, actividades_fav[], big_five_vector, created_at

### lugares
- id, nombre, direccion, tipo (restaurante, cine, bar, etc.), capacidad_comida, capacidad_cine, etc., activo

### salidas
- id, lugar_id, actividad, fecha, hora, cupo_max, asistentes_actuales, descripcion, etiquetas[], estado (abierta/cerrada/cancelada/completada)

### participantes
- id, salida_id, user_id, estado (confirmado/no_show), joined_at

### feedback
- id, salida_id, de_user_id, para_user_id, compatibility_score, created_at

### user_activity_history
- id, user_id, actividad, salida_id, rating, created_at

### weekly_suggestions
- id, user_id, semana (ISO), salida_ids[], generada_en, estado (pendiente/vista)

### trust_scores (futuro)
- user_id, asistencia_rate, reportes_recibidos, reportes_hechos

## 9. El Algoritmo (Conceptual)

### Matching de compatibilidad (entre personas)
- **Base:** Vector Big Five (5 dimensiones: apertura, responsabilidad, extraversión, amabilidad, neuroticismo)
- **Cálculo:** Distancia coseno entre vectores → score 0-100%
- **Ajuste por feedback:** Cada feedback post-salida ajusta el peso de cada dimensión para ese usuario
- **Ajuste por actividades:** Gente con actividades favoritas similares tiene bonus de compatibilidad

### Sugerencia semanal (5 salidas)
- **Filtro 1:** Salidas activas en la próxima semana, con cupo disponible
- **Filtro 2:** Compatibilidad promedio del grupo > umbral (ej: >60%)
- **Filtro 3:** Actividad alineada con historial del usuario
- **Ranking:** Las 5 con mejor score compuesto (compatibilidad + afinidad de actividad + novedad)
- **Diversidad:** No sugerir 5 actividades iguales si hay variedad disponible

## 10. Monetización (Fase 3+)

- **No se cobra al usuario. Nunca.**
- **Modelo:** Los comercios (bares, restaurantes, cines) pagan por:
  - Estar listados como "lugar recomendado"
  - Ofrecer descuentos/promos a grupos de Quedamos (ej: 15% off)
  - Ser destacados en sugerencias semanales
- **Tipo Groupon inverso:** El comercio paga por visibilidad, el usuario recibe el descuento.
- **Precio estimado:** Módico. No busca ser negocio, busca cubrir costos de infraestructura.

## 11. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Gente que no se presenta | Alta | Medio | Sistema de confianza, límite de no-shows |
| Salidas incómodas/aburridas | Media | Medio | Matching mejora con feedback, apodo + sin foto reduce presión |
| Moderación (reportes, acoso) | Media | Alto | Reportes desde el día 1, bloqueos, sin admins con poder absoluto |
| Baja retención | Alta | Alto | Sugerencias semanales + notificaciones + variedad de actividades |
| iOS PWA notificaciones | Media | Bajo | Fallback a email, o migrar a React Native si es blocker |
| Cold start del algoritmo | Alta | Medio | Matching inicial por Big Five + actividades; feedback loop arranca después |
| Poca variedad de salidas (al inicio) | Alta | Alto | Programar salidas variadas manualmente hasta que el sistema tenga tracción |
| Competencia (Timeleft, Meetup) | Baja | Medio | Diferenciación clara: gratis, transparente, matching visible, cualquier actividad |

## 12. Posicionamiento

**Quedamos** nace de una experiencia real: Timeleft funcionó para conocer gente, pero el costo y la dinámica de poder la arruinaron. Quedamos es la alternativa gratuita, transparente y sin jerarquías. No es una app de citas, no es un calendario de eventos. Es una plataforma social donde el matching inteligente te ayuda a encontrar personas afines para salir, sin pagar, sin que nadie te eche, sin algoritmos opacos.

**Tono de la app:** Cálido, directo, argentino. Nada corporativo. "Quedamos" es una invitación, no un servicio.

## 13. Validación Gate 0.1 ✅

- [x] Problema definido en una frase
- [x] Público objetivo identificado (con persona real basada en experiencia)
- [x] Principios de diseño derivados de experiencia real
- [x] Features core listadas (con sugerencias semanales como feature estrella)
- [x] Algoritmo conceptual definido
- [x] Métricas de éxito definidas
- [x] Stack asumido y restricciones técnicas documentadas
- [x] Preguntas abiertas para el arquitecto
