# DEFINITION — Cábala

## Product Vision

Una app mobile que te invita a capturar 3 momentos de tu día, sin presión, sin nube, sin ruido. Tu bitácora visual personal.

## Core Loop

1. **Notificación** — la app te avisa (hasta 3 veces por día, en ventanas configurables)
2. **Captura** — sacás una foto con la cámara. Se comprime automáticamente. Nada de galería.
3. **Contexto** — agregás título, texto, tags, nota de voz. La ubicación se guarda automáticamente.
4. **Archivo** — queda en tu timeline: calendario, mapa, lista.
5. **Revisión** — "Un día como hoy" y modo Cábala te invitan a mirar atrás.

## User Personas

### Gonzo (primary)
- Fotógrafo casual, quiere registro visual de su vida
- No quiere suscripciones ni nube
- Valora simplicidad y ausencia de presión
- Le gusta la idea de "cábala" — replicar fotos del pasado

### Viajero frecuente
- Quiere recordar dónde estuvo y cuándo
- Usa el mapa como navegador de recuerdos
- No quiere apps pesadas en el celu

### Persona creativa
- Usa los desafíos como excusa para fotografiar
- Le gusta compartir resultados en redes

## MVP Features (priorizadas)

### P0 — Core
- [ ] Sacar foto (solo cámara, nada de galería) con compresión automática
- [ ] Título + texto descriptivo (opcional)
- [ ] Tags libres (uno o varios)
- [ ] Geolocalización automática
- [ ] Nota de voz (opcional)
- [ ] 3 notificaciones diarias configurables por ventanas de tiempo
- [ ] Timeline: vista calendario
- [ ] Timeline: vista lista
- [ ] Timeline: vista mapa
- [ ] Búsqueda/filtro por tags, fecha, ubicación
- [ ] SQLite local, sin cuenta

### P1 — Valor agregado
- [ ] Modo Cábala: "hace X tiempo sacaste esta foto acá, ¿querés replicarla?"
- [ ] "Un día como hoy": 1 semana, 1 mes, 6 meses, 12 meses
- [ ] Compartir entrada como card/imagen
- [ ] Export zip con fotos + metadata JSON
- [ ] Widget foto del día
- [ ] Modo incógnito (sin ubicación en entrada puntual)

### P2 — Diferenciación
- [ ] Desafíos de fotografía (ej: "30 días en B/N", "7 días de texturas")
- [ ] Modo paseo: detectar lugares nuevos, sugerir foto
- [ ] Estadísticas: fotos por mes, tags más usados, rachas
- [ ] Backup cifrado opcional a iCloud / Google Drive

### P3 — Pulido
- [ ] Modo oscuro
- [ ] Animaciones suaves en transiciones
- [ ] Onboarding interactivo (3 pantallas)
- [ ] Soporte múltiples idiomas (ES/EN)

## User Flow (MVP)

```
App abierta → Timeline (vista por defecto)
  ├── Calendario (mes actual, días con fotos marcados)
  ├── Mapa (pins con fotos)
  └── Lista (scroll cronológico inverso)

Tap "+" → Cámara
  ├── Sacar foto → Preview → Aceptar/Repetir
  ├── Agregar título (opcional)
  ├── Agregar texto (opcional)
  ├── Agregar tags (opcional)
  ├── Grabar nota de voz (opcional)
  ├── Modo incógnito toggle (opcional)
  └── Guardar → vuelve a Timeline

Tap entrada → Detalle
  ├── Foto grande
  ├── Título, texto, tags
  ├── Nota de voz (reproducir)
  ├── Ubicación en mapa chico
  ├── Compartir
  └── Modo Cábala (si aplica)

Settings
  ├── Notificaciones: cantidad (default 3), ventanas de horario
  ├── Calidad de foto (default: comprimida)
  ├── Respaldo (iCloud / Google Drive)
  └── Exportar datos
```

## Métricas de éxito (MVP)

- **Retención D7:** >40% (vuelven a usar la app después de una semana)
- **Fotos por usuario por semana:** >10 (al menos 1 por día)
- **NPS interno:** Gonzo la usa por más de 2 semanas
