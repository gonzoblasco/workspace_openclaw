---
title: dependency-advisor
description: TODO: add description
metadata:
  owner: kanam-dev
  status: active
---
# dependency-advisor

Recomendar, evaluar y gestionar dependencias de un proyecto: qué librería elegir hoy, por qué, y cómo planificar su ciclo de vida y migración.

## Pasos

1️⃣ **Inventariar las dependencias actuales**  
   - Leer el manifiesto del proyecto (`package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, etc.).  
   - Listar cada dependencia con su versión declarada y la resuelta en el lockfile.  
   - Evidencia: tabla en `dep-advisor/inventory.md` con nombre, versión declarada, versión resuelta y tipo (directa/transitiva).

2️⃣ **Clasificar por criticidad y salud**  
   - Marcar cada dependencia según su rol: runtime, build, test, dev-only.  
   - Consultar el registro de origen (npm, PyPI, crates.io) para obtener: última versión, fecha del último release, licencia y si está deprecada.  
   - Evidencia: columnas de estado en `dep-advisor/inventory.md`: mantenida / estancada / deprecada.

3️⃣ **Detectar riesgo y deuda**  
   - Cruzar contra el registro de vulnerabilidades (`npm audit`, `pip-audit`, `cargo audit` o el advisories feed del ecosistema).  
   - Marcar versiones con advisories abiertos, licencias incompatibles con el proyecto, o forks sin mantenimiento.  
   - Evidencia: sección `dep-advisor/risks.md` con advisory, severidad y versión afectada.

4️⃣ **Justificar cada dependencia vigente**  
   - Para cada dependencia directa, responder: ¿qué hace? ¿por qué se eligió? ¿sigue siendo la mejor opción hoy?  
   - Si una dependencia no puede justificarse por su valor actual, marcarla como candidata a reemplazo.  
   - Evidencia: ficha en `dep-advisor/rationale/<paquete>.md` con qué hace, por qué se elige hoy y decisión explícita.

5️⃣ **Proponer alternativas y planes de migración**  
   - Para cada candidata a reemplazo, listar al menos una alternativa con su huella de mantenimiento y licencia.  
   - Estimar esfuerzo (S/M/L), riesgo de migración y orden de ejecución.  
   - Evidencia: `dep-advisor/migration-plan.md` con tabla actual → alternativa → esfuerzo → riesgo → orden.

6️⃣ **Fijar la política de actualización**  
   - Definir con qué frecuencia se revisan dependencias y quién es responsable.  
   - Establecer reglas para majors (breaking), minors y parches.  
   - Evidencia: `dep-advisor/policy.md` con cadencia, owner y reglas por tipo de versión.

## Resultado esperado

- Un inventario verificado con estado de salud y riesgo de cada dependencia.
- Una justificación explícita de cada dependencia vigente: qué hace, por qué se mantiene hoy.
- Un plan de migración priorizado para las dependencias que ya no se justifican.
- Una política de actualización con cadencia y responsables.

## Prerequisitos

- Acceso al manifiesto y lockfile del proyecto.
- Acceso a la red para consultar registros de paquetes y advisories.
- Conocimiento del ecosistema del proyecto (npm, PyPI, crates.io, etc.).

## Regla dura

- Nunca recomendar adoptar una dependencia por precedente: primero qué hace, después por qué se elige hoy, después la decisión explícita. Toda alternativa propuesta debe citar su huella de mantenimiento y licencia con evidencia del registro.
