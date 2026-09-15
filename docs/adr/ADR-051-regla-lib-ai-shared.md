# ADR-051: Regla de extraccion de `lib/ai` compartido (construir solo con divergencia real)

**Fecha:** 2026-09-15
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** evaluacion de arquitectura por capas (2026-09-15); Gonzo delego la regla en Kanam
**Relacionado:** ADR-036 (Turborepo + pnpm monorepo)

---

## Contexto

La arquitectura por capas propuso un paquete `/packages/ai-core` (clientes IA, prompts, RAG, tools) como capa compartida entre proyectos. En la evaluacion se senalo que conviene extraerlo **cuando 2+ proyectos lo necesiten**, no de forma anticipada. Gonzo pidio dejar la regla precisa de *cuando*.

La tension es la regla de `USER.md` (2026-09-14): ninguna dependencia se adopta por estar presente ni se cita por precedente. Extraer `lib/ai` anticipadamente seria adoptar una abstraccion antes de que resuelva un problema.

**Dato estructural decisivo:** los proyectos de Kanam estan partidos entre **TypeScript** (Next.js/Vite: kanam-forge, kanam-pulse) y **Python** (kanam-lab con Gradio + libreria `ollama` directa). **Nunca van a compartir un paquete de codigo** entre esos dos lenguajes. La unica chance de `lib/ai` compartido es **dentro de un mismo lenguaje**.

---

## Decision

**No se construye `lib/ai` (ni ningun paquete compartido de capa IA) de forma anticipada.**

Se extrae **solo** cuando se cumplen TODAS estas condiciones:

1. **2+ proyectos del mismo lenguaje** (TS o Python, nunca mezclado) duplican al menos una de: (a) el cliente de un proveedor, (b) la logica de retry/fallback/rate-limit, o (c) el loader de prompts versionados.
2. **La duplicacion ya esta causando divergencia**: comportamientos distintos donde deberian coincidir (dos proyectos resuelven el mismo fallback distinto, por ejemplo). No duplicacion benigna.
3. **Hay un consumidor que lo va a usar en este ciclo** (no "algun dia").
4. La extraccion es un refactor que **no cambia comportamiento** (same-behavior move), no una reescritura.

**Si no se cumplen las 4, no se abre el paquete.** El costo de la abstencion es nulo; el costo de una abstraccion prematura es real (dos capas de indireccion que nadie usa se pudren).

### Forma cuando si toca

- TS: un package de Turborepo/pnpm (monorepo ya estandar, ADR-036).
- Python: un paquete interno instalable, nunca un fork que viva fuera del repo.

---

## Consecuencias

### Positivas
- Cero codigo muerto en abstracciones que nadie consume.
- La regla es objetiva (divergencia real, mismo lenguaje, consumidor en el ciclo), no un "por si acaso".
- Respeta el hecho estructural: TS y Python no comparten paquete.

### Negativas
- Si aparece el caso duplicado antes de lo esperado, hay un refactor que hacer en ese momento (no se paga hoy, se paga cuando toca).
- Requiere mantener el criterio de "divergencia real" sin volverse burocratico.

---

## Alternativas consideradas

1. **Construir `lib/ai` ahora "para cuando se necesite"**: abstraccion prematura, viola la regla de precedente-no-motivo. Rechazado.
2. **Un paquete universal (TS + Python)**: imposible por los lenguajes. Rechazado.
3. **No escribir la regla** (decisio implicita): deja la puerta abierta a la deriva cuando "una idea suene bien". Rechazado: la regla escrita es la defensa.

---

## Como se actualiza

Este `workspace_openclaw/docs/adr/ADR-051` es el criterio. Al evaluar un caso, la pregunta no es "¿hay duplicacion?" sino "¿hay **divergencia real** entre 2 proyectos del mismo lenguaje con consumidor en este ciclo?". Solo con los 4 umbrales, se escribe el ADR del paquete (el numero siguiente).
