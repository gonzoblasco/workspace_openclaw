# Kanam — BRIEF

**Versión:** 0.1
**Fecha:** 2026-07-26
**Estado:** Discovery

---

## 1. Propósito

Kanam es un PWA personal que funciona como un sistema operativo de vida digital. Comienza como un diario personal inteligente para Gonzo, y evoluciona para ser un espacio seguro donde su círculo de confianza pueda tener su propio dashboard con asistencia IA.

No es una app más. Es **la** interfaz de tu vida digital.

## 2. Visión a largo plazo

- **Fase 1 (ahora):** Uso personal. Diario + asistente IA.
- **Fase 2 (próximo):** Multi-tenant con invitaciones. Cada usuario tiene su espacio aislado.
- **Fase 3 (futuro):** Producto comercial. Dashboard de sitios/aplicaciones del usuario con soluciones de valor agregado.

## 3. Stack

| Capa | Tecnología |
|---|---|
| Frontend | Next.js + Tailwind + TypeScript |
| PWA | next-pwa o similar (service worker + manifest) |
| Backend | Supabase (auth, DB, storage, realtime) |
| IA | Edge Functions → Ollama Cloud (DeepSeek V4 Flash / Gemma 4) |
| Hosting | Vercel |

Sin builds nativos. Sin Xcode. Funciona en cualquier browser, instalable en iOS como PWA.

## 4. Autenticación

Supabase Auth con magic link. En Fase 1 solo Gonzo. En Fase 2, invitaciones con código.

## 5. MVP: "El Diario"

Una sola pantalla principal con timeline cronológico inverso. Cada entrada puede ser:

- **📝 Nota rápida** — texto libre
- **📸 Foto** — imagen con caption
- **📊 Check-in** — ánimo, energía, sueño (sliders/emojis)
- **✍️ Writing** — palabras escritas hoy
- **💡 Idea** — pensamiento fugaz con tags

Al final del día, la IA genera un resumen automático.

### Lo que NO entra en el MVP

- Dashboard de proyectos
- Gestión de sitios web
- Chat conversacional con IA
- Multi-tenant

## 6. Principios de diseño

- **Offline-first:** La app debe funcionar sin internet (lectura de entradas cacheadas)
- **Privacidad por defecto:** Los datos son del usuario, no nuestros
- **IA aumentativa, no reemplazo:** La IA sugiere, no decide
- **Paso a paso:** Cada feature se justifica antes de implementarse
- **Sin vendor lock-in:** Stack portable, datos exportables

## 7. Riesgos identificados

- **Dependencia de Ollama Cloud:** Si el servicio cambia precios/condiciones, migrar a otro provider
- **PWA en iOS:** Limitaciones de Safari (notificaciones, background sync, almacenamiento)
- **Adopción personal:** Si Gonzo no usa la app a diario, el proyecto muere
