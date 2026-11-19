# Plan de marcha

> **Qué es:** el ritmo con el que se trabaja. Responde "¿cómo reparto el tiempo para que el sistema
> siga funcionando **y** algo se termine?".
> **Qué no es:** no es el norte (`docs/NORTH.md`), no es el estado de las capas
> (`docs/ROADMAP.md`), no es el programa de ingresos (`docs/pipeline/roadmap-ingresos-a11y-2026-11.md`)
> ni la lista de tareas (`memory/memory.db`). Este documento solo ordena **el tiempo**.
> **Dueño:** Kanam CORE. **Fecha:** 2026-11-19. **Estado:** vigente hasta el 31/12/2026.

---

## 1. El diagnóstico que este plan resuelve

En las últimas tres semanas la actividad fue casi toda **sistema**: revisar el ROADMAP, revisar el
NORTH, arreglar automations, adoptar una skill, instalar un CLI, documentar la coexistencia. Todo
defendible, todo verificable. Y mientras tanto:

- OnWheels, la única obra activa, **no arrancó F0** (definida el 27/10).
- La búsqueda laboral tiene 3 procesos vivos y **cero horas asignadas**.
- Mercor, el único con una acción concreta pendiente, sigue sin postular.

Eso no es falta de disciplina: es que **el sistema no tiene techo**. Siempre hay una mejora
defendible, y una mejora defendible gana siempre contra una obra que da miedo. Este plan pone el
techo.

---

## 2. Las tres cubetas

Todo lo que se hace entra en una sola de estas tres. Si no entra, no se hace.

| Cubeta | Qué incluye | Techo semanal |
|---|---|---|
| **OBRA** | OnWheels F0 → entrega a Esteban. Nada más. | **~50%** |
| **INGRESO** | Aplicaciones, OSS a11y, contenido, vidriera. El programa de `roadmap-ingresos-a11y` | **~30%** |
| **SISTEMA** | Gates, backups, automations, memoria, docs de gobierno | **~20%**, con piso y con techo |

**La regla dura:** el sistema tiene **piso y techo**. Piso = lo que nunca se rompe (§3). Techo = no
se invierte más que eso, aunque haya algo roto y defendible. Un sistema al 95% que no entrega una
obra vale menos que uno al 80% que entrega.

**Lo que no entra en ninguna cubeta:** frentes nuevos. Si aparece uno, va a `memory/inbox.md` y
sigue lo que estaba. Esto ya lo dice `NORTH.md`; acá se cobra en tiempo, no en intención.

---

## 3. El piso funcional (30 minutos por semana, no negociable)

Esto es lo que hace que "funcional" signifique algo. Es barato y se corre junto, un solo bloque.

```bash
cd ~/.openclaw/workspace
python3 scripts/check-bootstrap-budget.py     # el bootstrap no se trunca
python3 scripts/check-refs.py                  # ningún doc apunta al vacío
python3 scripts/check-adr-integrity.py         # los ADRs siguen indexados
bash scripts/gateway-config-drift.sh           # el config no divergió solo
git status --short && git log --oneline -1     # nada sin pushear
openclaw automations list | grep -c '"error"'  # ninguna automation caída
```

**Criterio de piso roto:** cualquiera de esos seis falla dos semanas seguidas. Ahí el sistema deja
de ser soporte y pasa a ser el trabajo — se corrige esa semana y se descuenta de la cubeta OBRA,
no de INGRESO.

**Lo que NO es piso** (y por lo tanto no se toca en el bloque semanal): mejoras de pipeline,
adopción de herramientas, revisión de roadmaps de rol, reescrituras de documentación. Eso es
SISTEMA con techo, y compite con las otras dos cubetas.

---

## 4. El ritmo semanal

Cuatro bloques fijos. Si un día se pierde, se pierde ese bloque; no se corre al siguiente.

| Día | Bloque | Qué se hace | Salida |
|---|---|---|---|
| **Lunes** | 15 min | Elegir **una** cosa de OBRA para la semana y una de INGRESO. Escribirlas como todo con fecha. | 2 todos con fecha |
| **Mar–Jue** | 2 bloques/día | Bloque 1: OBRA. Bloque 2: INGRESO. El orden no se invierte. | Commits y evidencia |
| **Viernes** | 45 min | Piso funcional + revisión: ¿se cerró algo? ¿qué se cayó del plan? | Delta anotado, semana cerrada |

**Por qué la obra va primero en el día:** si INGRESO va primero, las aplicaciones y el contenido se
comen el día — son infinitas y tienen feedback inmediato. La obra es la que se posterga sola, así
que va en el bloque donde hay energía, no en el que sobra.

**El viernes no se trabaja en la obra.** Es el día que evita que la deuda se acumule en silencio.

---

## 5. La secuencia: 19 de noviembre → 31 de diciembre (6 semanas)

Un hito medible por semana. Si un hito no se cumple, **la semana siguiente lo absorbe** y se cae el
hito de esa semana, no la secuencia entera.

### S1 · 19–22 nov — destrabar lo que está frenado por mí
- **OBRA:** OnWheels F0 arranca. Lo que no depende de nadie: nota de compliance (hecha), evaluación
  del MCP oficial de MeLi, y el esqueleto de `EVIDENCIA-MELI.md`.
- **BLOQUEO DE GONZO:** registrar la app central en el panel de developers (Client ID + permisos).
  Sin eso, 0.3 a 0.6 no corren y F0 no puede cerrar.
- **INGRESO:** postular a Mercor (cuenta, PDF, Practice Interview). Es gratis, el CV está listo, y
  es el único proceso con acción del lado nuestro.
- **INGRESO:** resolver los 18 claims de CV sin respaldo en `memory/career-facts.md`. **Va primero
  que cualquier aplicación nueva**, porque un CV con hechos no registrados es un riesgo de
  credibilidad, y el criterio del workspace es que el hecho vive en el archivo dueño.
- **Gate S1:** app registrada + Mercor enviado + claims resueltos.

### S2 · 23–29 nov — F0 cierra o se escala
- **OBRA:** 0.3 a 0.6 (los cuatro GET/POST contra la API real). 0.9 (calibración de cuota hasta el
  primer 429). 0.10 (MCP oficial sí/no, 2 h tope).
- **OBRA:** 0.8 (User Products: `user_product_seller`, variations o no). Es la decisión que define
  el modelo de publicación antes de escribir el publicador.
- **INGRESO:** Fase 0 del programa de ingresos — arreglar la bio que apunta a un 404.
- **Gate S2:** criterio de salida de F0 cumplido en 6 de sus 8 checkboxes, o el proyecto se detiene
  y se escala. Sin Fase 1 "provisoriamente".

### S3 · 30 nov–6 dic — la publicación real y la decisión de stack
- **OBRA:** 0.7 — publicar una unidad real en MeLi y actualizarla (precio y stock), con los IDs
  anotados. Es el 60% del producto y el camino que nadie probó nunca.
- **OBRA:** 0.11 — costo por consulta de IA medido con el catálogo de Esteban.
- **OBRA:** ADR de stack, recién ahora. Antes de esto era una suposición.
- **INGRESO:** storefront mínimo (Fase 1): URL pública + landing de `preflight-a11y`.
- **Gate S3:** una unidad publicada y actualizada + ADR de stack escrito.

### S4 · 7–13 dic — F1 arranca con stack decidido
- **OBRA:** control plane y landing de OnWheels. Si F0 falló, esta semana es la escalada a Gonzo,
  no código.
- **INGRESO:** 3 piezas publicadas sobre PRs ya mergeados (hay material para 10).
- **Gate S4:** la landing carga y muestra el inventario de Esteban (aunque sea de prueba).

### S5 · 14–20 dic — catálogo y primer sync
- **OBRA:** catálogo + sitio público de Esteban; sync de precio y stock contra MeLi.
- **INGRESO:** canal outbound (Fase 3) — primer movimiento hacia afuera, con OK explícito de Gonzo
  para cualquier cosa pública.
- **Gate S5:** cambiar el precio en el panel y verlo reflejado en MeLi sin intervención manual.

### S6 · 21–31 dic — cerrar el año midiendo, no construyendo
- **OBRA:** entrega a Esteban si el sync está estable. Si no, se entrega lo que sí esté y se
  documenta lo que falta.
- **INGRESO:** Fase 4 — medir y decidir. Qué convirtió, qué no, y qué se descarta.
- **SISTEMA:** cierre de año: limpiar la cola de todos viejos, archivar lo que ya no es norte.
- **Gate S6:** OnWheels entregado o con fecha de entrega firmada, y una decisión escrita sobre el
  canal de ingresos.

---

## 5-bis. Quién hace qué (agregado 2026-11-19)

El plan decía *qué* y *cuándo*, pero no *quién*. Sin esto, cada bloque arranca con una decisión de reparto que consume el bloque. Reparto fijo por tipo de tarea:

| Tarea | Ejecuta | Verifica |
|---|---|---|
| Registrar la app de MeLi (0.1) | **Gonzo** — no es delegable | CORE transcribe Client ID + permisos |
| Nota de compliance (0.2) | MIND | CORE reproduce las citas |
| Llamadas a la API: 0.3 a 0.6, 0.9 (cuota) | DEV | CORE corre la misma llamada y compara |
| Publicación real y IDs (0.7) | DEV | CORE abre la unidad publicada y confirma |
| User Products (0.8) | DEV decide, CORE escribe el ADR | — |
| Evaluación del MCP oficial (0.10) | MIND (2 h tope) | CORE |
| Costo por consulta de IA (0.11) | DEV mide | CORE registra el número |
| Aplicaciones laborales | CORE prepara el paquete | **Gonzo envía** |
| Piezas publicadas | STUDIO redacta | CORE verifica hechos; **Gonzo publica** |
| Landing / storefront | DEV construye | AUDITOR revisa UI y a11y |
| Claims de CV | CORE cruza contra `career-facts.md` | MIND audita la procedencia |

**La regla que evita el ping-pong:** el CORE no implementa y el rol no se auto-aprueba. Un reporte de DEV o de MIND es un reporte, no una prueba: el CORE reproduce la salida antes de dar el bloque por cerrado.

---

## 5-ter. Contingencias (qué pasa si el hito no llega)

Ninguna de estas tres es hipotética: son los tres lugares donde este plan se puede trabar.

**1. La app de MeLi no se registra en S1.** Es el único bloqueo que depende de una sola persona y de un panel externo.
- S2 arranca igual con lo que no la necesita: 0.10 (MCP) y 0.11 (costo de IA) son medibles sin app.
- Si al viernes de S2 sigue sin registrarse, **F0 se detiene y se escala**. No se simula con una cuenta de prueba ni se sigue "provisoriamente": el criterio de salida de F0 exige una unidad real publicada.
- Lo que sí se gana en ese caso: el plan de ingresos avanza una semana con el tiempo liberado, y la app queda como el primer todo de la semana siguiente.

**2. La API devuelve 429 antes de lo esperado.** No es una falla: **es el experimento**. 0.9 existe para encontrar ese techo, y encontrar un techo bajo es un hallazgo sobre la viabilidad del producto — se documenta con los headers tal como vinieron y se decide si el modelo de negocio entra en ese presupuesto. Lo que sería falla es no medirlo.

**3. La publicación real (0.7) no sale.** Es el riesgo que el roadmap de OnWheels ya declaró: si 0.3-0.7 falla, el proyecto se detiene y se escala. F0 sin publicación real no es F0, es una opinión. Se reporta con el error exacto de la API, no con "no funcionó".

---

## 6. Orden de sacrificio (qué se cae primero)

Cuando la semana no alcanza —y no va a alcanzar— se corta **en este orden**, sin negociar:

1. **Mejoras de sistema** (pipeline, herramientas, reescrituras de docs). Se cortan primero, enteras.
2. **Contenido** (posts, OSS). Se corta el volumen, no la cadencia: si el mes tenía 3 piezas, se
   publica 1.
3. **Nada más.**

**Lo que no se corta nunca:** el piso funcional (30 min), las aplicaciones ya comprometidas, y el
bloque de OBRA. Si hay que cortar la obra, no es que falte tiempo: es que el plan está mal y hay
que reescribirlo.

---

## 7. Señales de que el plan falló

Tres, y las tres se detectan sin opinar:

- **Dos semanas seguidas sin tocar la cubeta OBRA.** El sistema se comió el tiempo otra vez.
- **El piso funcional falla dos viernes seguidos.** El sistema ya no es soporte.
- **Aparece un frente nuevo en la lista de trabajo.** No se registró en `inbox` y ganó por
  cansancio, no por decisión.

Cuando pasa cualquiera, no se "ajusta el plan": se lee esta página y se corta lo que corresponda.

---

## 8. Lo que este plan asume

- **OnWheels sigue siendo la única obra.** Si Gonzo decide otra cosa, este plan se reescribe, no se
  parchea.
- **CPACC está retirado** (2026-11-16, sin fondos). No hay credencial de por medio: el tramo T1
  cierra con OnWheels entregado y nada más.
- **La búsqueda laboral sigue siendo P0** aunque no sea la cubeta más grande. Es la única que
  depende de terceros, así que su parte accionable se hace temprano y no se posterga.
- **Una persona, una máquina.** No hay colchón para dos obras ni para un segundo producto.

---

## Referencia cruzada

- `docs/NORTH.md` — el para qué. Este plan no lo redefine.
- `docs/ROADMAP.md` — estado de las capas y la ruta por tramos.
- `docs/pipeline/roadmap-ingresos-a11y-2026-11.md` — fases 0 a 4 del programa de ingresos.
- `memory/memory.db` → `todos` — las tareas fechadas. Acá solo vive el ritmo.
