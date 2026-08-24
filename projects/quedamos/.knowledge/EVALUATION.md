# EVALUATION.md — Quedamos

## Mercado

### Tamaño
- Timeleft: 3M+ usuarios, 200+ ciudades, 52 países. Fundado 2020.
- Meetup: ~60M usuarios global. Propiedad de Bending Spoons desde 2024.
- Soledad post-pandemia: crisis global de salud pública (OMS, US Surgeon General).
- Demanda creciente de "third places" y conexiones IRL.

### Tendencia
- Cansancio de apps de citas (Tinder, Bumble reportan caída de usuarios jóvenes)
- Auge de "amistad intencional" (Bumble BFF, Timeleft, Friender)
- Preferencia por experiencias presenciales post-pandemia
- Interés en plataformas transparentes y éticas (contra-algoritmo)

## Competidores Directos

### Timeleft
- **Fortalezas:** Marca establecida, algoritmo probado, presencia global, experiencia curada
- **Debilidades:** Pago por evento, solo miércoles, solo cenas, matching opaco, no sabés con quién vas hasta último momento
- **Precio:** ~$12-15 USD por cena

### Meetup
- **Fortalezas:** Gran base de usuarios, cualquier actividad, grupos por interés
- **Debilidades:** Experiencia fría, sin matching, calidad variable, interfaz anticuada
- **Precio:** Gratis para asistentes, pago para organizadores

### Bumble BFF
- **Fortalezas:** Base de usuarios enorme, matching 1:1, foto + bio
- **Debilidades:** Esencialmente Tinder para amigos, presión de "cita", no grupal
- **Precio:** Gratis con premium

### "Are We Friends?"
- **Fortalezas:** Matching profundo (IPIP-NEO-120), transparente
- **Debilidades:** Proyecto chico, sin tracción, solo web
- **Precio:** Gratis

## Diferenciación de Quedamos

| Factor | Quedamos | Timeleft | Meetup | Bumble BFF |
|---|---|---|---|---|
| Matching | Semi-automático, score visible | Automático, opaco | Sin matching | 1:1, swipe |
| Precio | Gratis | $12-15/evento | Gratis (org. paga) | Gratis + premium |
| Actividades | Cualquiera | Solo cenas | Cualquiera | Citas de amistad |
| Transparencia | Algoritmo visible | Caja negra | N/A | Caja negra |
| Formato | Grupal (4-6) | Grupal (6) | Grupal (variable) | 1:1 |
| Código | Visible | Cerrado | Cerrado | Cerrado |

## Viabilidad Técnica

### Stack
- **Next.js 15 + PWA:** ✅ Conocés el stack, PWA es viable para MVP
- **Supabase:** ✅ Lo usás, cubre auth, DB, realtime, edge functions
- **Matching engine:** 🟡 Algoritmo Big Five + feedback loop no es trivial pero es abordable
- **Notificaciones push PWA:** 🟡 iOS limita push en PWA (solo con service worker + Web Push API, Safari lo soporta desde 2023 pero con restricciones)

### Riesgos Técnicos
1. **Notificaciones push en iOS:** Safari soporta Web Push desde iOS 16.4+, pero la UX de instalación PWA en iOS sigue siendo pobre. Posible blocker para usuarios Apple.
2. **Algoritmo de matching:** El feedback loop necesita datos para funcionar bien. Al principio los matches van a ser medio pelo hasta que haya feedback acumulado.
3. **Moderación:** Gente desconocida encontrándose = riesgo de malas experiencias. Sin moderación desde el día 1, la app puede morir.

### Tiempo Estimado (MVP)
- **Setup + Auth + Test personalidad:** 3-4 días
- **Feed + Crear/Unirse a salidas:** 4-5 días
- **Compatibility score + Matching engine:** 4-5 días
- **Notificaciones push:** 2-3 días
- **Feedback post-salida:** 2-3 días
- **Perfiles + UI/UX general:** 3-4 días
- **Testing + polish:** 3-4 días

**Total estimado:** ~3-4 semanas de desarrollo enfocado

## Go/No-Go Assessment

### ✅ Puntos a favor
- Problema real y validado (Timeleft 3M users)
- Diferenciación clara vs competidores
- Stack que ya conocés
- MVP factible en 3-4 semanas
- Sin presión de monetización inmediata
- Portfolio piece sólido

### ⚠️ Puntos de atención
- iOS PWA push notifications son limitadas
- El matching necesita datos para ser bueno (cold start problem)
- Moderación es trabajo no técnico (gente real)
- Retención es el riesgo más grande

### 🟢 Veredicto
**Go.** Es un proyecto con propósito real, stack conocido, MVP acotado, y diferenciación clara. El riesgo más grande (retención) se mitiga con buen matching + notificaciones + variedad de actividades.
