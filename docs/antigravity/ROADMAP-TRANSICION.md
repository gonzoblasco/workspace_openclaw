# Roadmap de Transición y Retiro Ordenado de OpenClaw
## *De la Coexistencia Temporal a la Autonomía Total en Antigravity*

**Fecha de creación:** 2026-11-18  
**Autor:** Kanam (CORE)  
**Contexto:** Gonzo recurrió a OpenClaw por agotamiento de cuota en Antigravity durante la semana del 15 al 18 de noviembre. Este documento traza el camino para eliminar esa dependencia paso a paso sin quedar varado en ningún momento.

---

## 1. El Diagnóstico de la Realidad

No podemos ni debemos apagar OpenClaw "a la fuerza" hoy porque todavía cumple dos roles de rescate indispensables:
1. **Salvavidas de Cuota:** Cuando se agota el tier en Antigravity o hay un parate, OpenClaw está ahí para responder consultas inmediatas sin bloquear tu trabajo.
2. **Canal Móvil (Telegram):** OpenClaw está en tu teléfono vía bot de Telegram para consultas cuando no estás sentado frente a la Mac Mini.

> **Principio de Retiro:** *Ninguna herramienta se apaga hasta que su función esté 100% resuelta por una vía más limpia, más rápida y sin fricción.*

---

## 2. Los 4 Frentes de Autonomía

```
┌────────────────────────────────────────────────────────────────────────┐
│                   LOS 4 PILARES DEL RETIRO DEFINITIVO                  │
├───────────────────┬───────────────────┬──────────────────┬─────────────┤
│ 1. CUOTA Y PODER  │ 2. VANE & OLLAMA  │ 3. CANAL MÓVIL   │ 4. MACBOOK  │
│ Google AI Pro     │ Retiro 1 Diciembre│ Desacoplar       │ Modo Liviano│
│ (1 Diciembre)     │ Apagado de Docker │ Telegram de      │ Markdown    │
│ Contexto 2M       │ y cancelación     │ OpenClaw         │ + HANDOFF   │
└───────────────────┴───────────────────┴──────────────────┴─────────────┘
```

---

## 3. Cronograma del Roadmap (4 Fases)

### Fase A: Convivencia Asistida y Paridad de Trabajo (18 Nov – 30 Nov)
**Meta:** Trabajar el 90% del tiempo en Antigravity, usando OpenClaw solo como fallback de emergencia.

- [x] **Reglas sincronizadas:** `Accept: text/markdown` y `DISABLE_TELEMETRY=1` ya incorporados en Antigravity.
- [ ] **Manejo inteligente de modelos:**
  - Uso prioritario de **Gemini 3.8 Flash** para tareas interactivas, consultas de código, redacción y refactors rápidos (evita agotar la cuota diaria).
  - Uso selectivo de **Gemini 3.8 Pro** para arquitectura, revisiones adversariales de `kanam-critic` y diseño complejo.
- [ ] **Sincronización Git inter-runtime:**
  - Aplicación estricta de la regla: *rutas explícitas siempre, cero `git add .`*.
  - Si se consulta algo en OpenClaw, no iniciar tareas paralelas que editen código en Antigravity al mismo tiempo.
- [ ] **Cierre de ciclo de cuota actual:** Evaluar patrones de consumo para llegar fluidos al 1 de diciembre.

---

### Fase B: Hito Google AI Pro, Retiro de Vane y Solución Móvil (1 Dic – 7 Dic)
**Meta:** Liberar la Mac Mini de cargas locales obsoletas y resolver el acceso móvil sin OpenClaw.

1. **Activación de Google AI Pro (1 de Diciembre):**
   - Alta de Google AI Pro (acceso extendido a Gemini y NotebookLM).
   - Cancelación definitiva de Ollama Pro.
   - La restricción de cuota y ventana de contexto deja de ser un problema.
2. **Decommissioning de Vane:**
   - Apagar contenedores: `./scripts/ai-toolbox.py down vane`.
   - Quitar el servicio de arranque de Docker.
   - Liberar puertos y memoria RAM en la Mac Mini M4.
3. **Resolución del Canal Móvil (Telegram):**
   - **Evaluación de alternativa liviana:** En vez de mantener vivo todo el gateway de OpenClaw solo por Telegram, evaluar:
     - *Opción A:* Gemini App oficial en el móvil configurada con las instrucciones/Gems de Kanam.
     - *Opción B:* Un bot de Telegram en Python minimalista (un script único de ~80 líneas corriendo con `systemd`/`launchd`) que pegue directo a la API de Gemini, sin toda la infraestructura de OpenClaw.
   - Decidir y validar la opción elegida.

---

### Fase C: La "Semana Cero OpenClaw" (8 Dic – 14 Dic)
**Meta:** Demostrar que podés operar 7 días consecutivos sin abrir OpenClaw para nada.

- [ ] Apagar el servicio de OpenClaw de fondo (`openclaw gateway stop`).
- [ ] Operar 100% desde Antigravity en la Mac Mini y validar el nodo liviano en la MacBook Air (Markdown + HANDOFF).
- [ ] Verificar que ninguna skill ni script falle por falta de OpenClaw.
- [ ] Si surge una necesidad imprevista, documentarla como "gap a resolver" en vez de encender OpenClaw de forma permanente.

---

### Fase D: Desconexión y Archivo Final (15 de Diciembre)
**Meta:** Retiro formal y cierre limpio.

1. **Backup final del gateway:** Respaldo tar/zip de `~/.openclaw` en almacenamiento frío.
2. **Reubicación del Workspace canónico:**
   - Desacoplar el path del nombre `.openclaw` (ej. mover o consolidar `/Users/gonzoblasco/workspace` o mantener el repo git limpio).
3. **Emisión de ADR:**
   - Crear `ADR-115: Retiro definitivo de OpenClaw y adopción plena de Antigravity OS`.
4. **Kanam 100% independiente:** La totalidad del sistema opera en Antigravity.

---

## 4. Estado de los Hitos

| Hito | Fechas | Estado | Criterio de Éxito |
|---|---|:---:|---|
| **Fase A: Convivencia Asistida** | 18 Nov - 30 Nov | **EN CURSO** | Cero choques de git, uso de Flash para cuidar cuota. |
| **Fase B: Google AI Pro + Retiro Vane** | 01 Dic - 07 Dic | **PENDIENTE** | Vane apagado, Google AI Pro activo, canal móvil resuelto. |
| **Fase C: Semana Cero OpenClaw** | 08 Dic - 14 Dic | **PENDIENTE** | 7 días sin encender OpenClaw con 100% de tareas cubiertas. |
| **Fase D: Desconexión Definitiva** | 15 Dic | **PENDIENTE** | Gateway desinstalado/archivado y ADR-115 emitido. |
