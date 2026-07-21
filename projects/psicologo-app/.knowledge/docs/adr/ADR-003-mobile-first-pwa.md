# ADR-003: Mobile-First Web (no app nativa)

**Fecha:** 2026-07-21
**Contexto:** El psicólogo usa la app principalmente desde el celular (entre sesiones, en movimiento). Pero desarrollar app nativa (iOS + Android) duplica el esfuerzo.

**Decisión:** MVP como web mobile-first con PWA (Progressive Web App) para instalación en pantalla de inicio.

**Opciones consideradas:**
- **App nativa (React Native / Flutter):** más costo, más tiempo, más mantenimiento. No justificado para MVP.
- **PWA:** instalable, offline mode básico, notificaciones push. Suficiente para Fase 1.
- **Solo web responsive:** funcional, pero pierde la instalación en home screen y notificaciones push nativas.

**Consecuencias:**
- Positivas: un solo código, despliegue inmediato, sin stores.
- Negativas: PWA en iOS tiene limitaciones (notificaciones push llegaron en iOS 16.4, pero no son tan confiables como en Android). Para el MVP, los recordatorios van por WhatsApp, no por push, así que no es blocker.

**Estado:** Aceptado
