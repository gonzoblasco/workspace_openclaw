---
name: dependency-advisor
description: Dependencias con criterio: inventario, salud, riesgo y licencia, justificacion de la eleccion y plan de migracion. Usar antes de adoptar una libreria, al auditar un proyecto heredado, o cuando hay que decidir si una dependencia se actualiza, se reemplaza o se saca.
metadata:
  owner: kanam-dev
  status: active
---
# dependency-advisor

Recomendar, evaluar y gestionar dependencias de un proyecto: qué librería elegir hoy, por qué, y cómo planificar su ciclo de vida y migración.

## Pasos

1️⃣ **Inventariar las dependencias actuales**

   - Atajo ejecutable: `python3 ~/.openclaw/workspace/agents/kanam-dev/bin/dep_inventory.py <dir>` lee manifiesto y lockfile, cruza declarada vs resuelta, separa directas de transitivas y escribe `dep-advisor/inventory.md`. Exit 0 coherente, 1 directa ausente del lockfile, 2 sin manifiesto reconocible. Los rangos abiertos se marcan como senal, no como error: el juicio sigue siendo tuyo.
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

## Verificacion

- [ ] El inventario sale del manifiesto **y** del lockfile, y las dos versiones coinciden con lo declarado. Comando: el lector del proyecto (`npm ls --all`, `pip freeze`, `go list -m all`).
- [ ] Cada dependencia directa tiene su justificacion en una linea: que hace, por que se mantiene hoy, que pasaria si se saca. Una dependencia sin justificacion es candidata a salir, no a quedarse.
- [ ] La salud esta medida con una fuente: ultima publicacion, advisories abiertos, licencia. Sin fuente, no es salud, es impresion.
- [ ] Las que no se justifican tienen plan de migracion con paso concreto y responsable, o estan marcadas como aceptadas con motivo.
- [ ] La politica de actualizacion tiene cadencia y responsable explicitos.

Lo que NO es criterio: que el proyecto compile con las dependencias actuales. Eso prueba que existen, no que esten justificadas.

## Prerequisitos

- Acceso al manifiesto y lockfile del proyecto.
- Acceso a la red para consultar registros de paquetes y advisories.
- Conocimiento del ecosistema del proyecto (npm, PyPI, crates.io, etc.).

## Regla dura

- Nunca recomendar adoptar una dependencia por precedente: primero qué hace, después por qué se elige hoy, después la decisión explícita. Toda alternativa propuesta debe citar su huella de mantenimiento y licencia con evidencia del registro.
