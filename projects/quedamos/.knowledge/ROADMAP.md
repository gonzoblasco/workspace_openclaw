# ROADMAP.md — Quedamos

> Plan de ataque para el MVP. Output de Fase 0.2.

## Estimación: 3-4 semanas (desarrollo enfocado)

Dependiendo de cuántas personas se sumen al equipo y cuánto tiempo puedan dedicarle.

---

## Sprint 1: Fundación (Semana 1)

### Setup del proyecto
- [ ] Inicializar Next.js 15 con App Router + Tailwind + shadcn/ui
- [ ] Configurar Biome (lint + format)
- [ ] Configurar Supabase project (auth, DB, edge functions)
- [ ] Configurar PWA (next-pwa, manifest, service worker)
- [ ] Configurar GitHub repo + CI (type-check, lint, test)
- [ ] Configurar deploy en Vercel

### Auth + Onboarding
- [ ] Auth con email + Google OAuth (Supabase)
- [ ] Página de registro/login
- [ ] Flujo de onboarding: elegir apodo
- [ ] Test de personalidad Big Five (~20 preguntas)
- [ ] Selección de actividades favoritas
- [ ] Guardar perfil en DB

### DB Schema
- [ ] Migraciones: users, salidas, participantes, feedback, user_activity_history, weekly_suggestions, trust_scores, reportes
- [ ] RLS policies básicas
- [ ] Función PostgreSQL: calcular_compatibilidad

**Entregable:** Usuario puede registrarse, completar onboarding, y tiene perfil en DB.

---

## Sprint 2: Core de Salidas (Semana 2)

### Feed de salidas
- [ ] Página de feed con salidas abiertas (próximos 7 días)
- [ ] Filtros por actividad, fecha
- [ ] SalidaCard component (actividad, lugar, fecha, cupo, asistentes)
- [ ] Vista detalle de salida con lista de participantes

### Crear salida (solo administradores)
- [ ] Panel de administración protegido
- [ ] Formulario: seleccionar lugar, actividad, fecha, hora, cupo
- [ ] El cupo se valida contra la capacidad del lugar (20 comida, 40 cine, etc.)
- [ ] Publicar salida → aparece en feed y sugerencias

### Unirse a salida
- [ ] Botón "Unirse" en detalle de salida
- [ ] Validación de cupo
- [ ] Confirmación visual

### Compatibility score
- [ ] Edge Function: matching-engine (distancia coseno + ajustes)
- [ ] Mostrar compatibility score en detalle de salida (por participante)
- [ ] Badge visual (0-100%)

**Entregable:** Usuario puede ver feed de salidas programadas, unirse, y ver compatibilidad con otros asistentes.

---

## Sprint 3: Experiencia Semanal + Feedback (Semana 3)

### Sugerencias semanales
- [ ] Edge Function: weekly-suggester
  - [ ] Obtener perfil + historial del usuario
  - [ ] Filtrar salidas activas de la semana
  - [ ] Calcular compatibility score para cada salida
  - [ ] Rankear top 5 con diversidad
  - [ ] Almacenar en weekly_suggestions
- [ ] Sección "Tus sugerencias de esta semana" en feed
- [ ] Badge de "sugerido para vos" en SalidaCard

### Notificaciones push
- [ ] Configurar Web Push API (vapid keys)
- [ ] Service Worker: suscripción push
- [ ] Edge Function: notifications (scheduling)
- [ ] Notificación 24h antes de salida
- [ ] Notificación cuando alguien se une a tu salida

### Feedback post-salida
- [ ] Modal de feedback (24h después de la salida)
- [ ] Rating de compatibilidad con cada asistente (1-10)
- [ ] Edge Function: feedback-processor (actualiza pesos)
- [ ] Feedback anónimo (el otro usuario no ve quién puntuó)

### Perfil
- [ ] Perfil público (apodo, bio, actividades, historial de salidas)
- [ ] Editar perfil (bio, actividades)
- [ ] Trust score visible (asistencia rate)

**Entregable:** Experiencia semanal completa con sugerencias, notificaciones y feedback loop.

---

## Sprint 4: Polish + Launch (Semana 4)

### Sistema de confianza
- [ ] Reportes (motivo, descripción)
- [ ] Bloqueos individuales (no ver salidas, no ser emparejado)
- [ ] Trust scores automáticos (no-shows reducen score)
- [ ] Umbrales: si trust_score < 0.3, restricciones temporales

### UI/UX
- [ ] Diseño responsive (mobile-first)
- [ ] Animaciones y transiciones suaves
- [ ] Estados vacíos (no hay salidas, no hay sugerencias)
- [ ] Loading states y skeletons
- [ ] Error handling (toast notifications)

### Testing
- [ ] Tests de integración (flujos críticos)
- [ ] Tests de RLS policies
- [ ] Tests de matching engine
- [ ] QA manual en mobile (iOS + Android)

### Launch
- [ ] Landing page pública
- [ ] PWA instalable
- [ ] Deploy a producción
- [ ] Invitar a los amigos que se sumaron

**Entregable:** MVP listo para usar con amigos.

---

## Post-MVP (Fase 2+)

- Chat grupal temporario (48h post-salida)
- Fotos opcionales
- Mapa de salidas cercanas
- Promociones en locales asociados
- Múltiples ciudades
- Eventos especiales

## Dependencias

```
Sprint 1 ──→ Sprint 2 ──→ Sprint 3 ──→ Sprint 4
   │              │              │
   └── Setup      └── Core       └── Experiencia
   └── Auth       └── Salidas    └── Feedback
   └── DB         └── Matching   └── Notificaciones
```

## Riesgos del Plan

| Riesgo | Impacto | Acción |
|---|---|---|
| iOS push notifications no funcionan bien | Retraso en notificaciones | Fallback a email; considerar React Native post-MVP |
| Cold start del matching (pocos usuarios) | Sugerencias pobres | Matching inicial por Big Five + actividades; feedback loop arregla con el tiempo |
| Baja participación en feedback | Algoritmo no mejora | Gamificación: "tu feedback ayuda a encontrar mejores matches" |
| No-shows frecuentes | Mala experiencia | Trust scores desde el día 1; límite de no-shows antes de restricciones |
