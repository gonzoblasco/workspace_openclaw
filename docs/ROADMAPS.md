# ROADMAPS.md - El Roadmap de Roadmaps 🗺️

> **El meta-roadmap del ecosistema de agentes.** No planea una obra ni un producto: planea **la
> madurez del Crew**. Gobierna los siete roadmaps de rol: que existan, que sigan el mismo formato
> (`docs/checklists/roadmap-authoring-guide.md`), que su versión declarada no mienta, y en qué
> orden se escalan.
>
> **Fecha:** 2026-10-07 · **Estado:** vivo · **Dueño:** Kanam CORE · **Base:** `docs/NORTH.md`,
> `docs/ROADMAP.md`, ADR-073/074/083.

---

## Por qué existe

La premisa de esta ronda (Gonzo, 2026-10-07): **el estado por defecto de un rol sin `ROADMAP.md`
es v0.1**, y la meta es conocer y planificar su camino hasta **v0.5**.

El problema no era *saber* que faltaban roadmaps: era que **nadie podía ver, de un vistazo, qué
rol estaba más atrás, cuál era su próximo salto, quién lo decidía, y si ya existía un roadmap
disfrazado de nada.** Cada rol maduraba a ciegas; dos de siete tenían mapa.

Este documento es la respuesta: un solo lugar que responde *"¿en qué versión está cada rol, y qué
sigue?"* para los siete.

---

## La visión v1.0 - "El Crew como estándar"

**El trofeo se gana cuando la madurez del Crew es visible, verificable y repetible.**

No es "que todos tengan un roadmap escrito". Es que los siete roles:
1. tengan su versión declarada y **verificada contra fuentes reales**;
2. avancen por saltos cuyo **criterio de listo se cumple con evidencia reproducible**;
3. sostengan **v0.5 mínimo** - confiables sin supervisión línea por línea;
4. y al menos los gates de calidad (**critic**, **auditor**) lleguen a **v1.0**: invocables por el
   resto, con veredicto que es contrato.

**Criterio de cierre (v1.0 del meta-roadmap):** los 7 roles en v0.5+ verificado, con su roadmap
al día, y el índice de tracking sin drift entre lo declarado y lo real.

---

## El mapa de madurez del ecosistema (hoy, 2026-10-12)

| Rol | Roadmap | Versión declarada | Estado verificado | Próximo salto |
|---|---|---|---|---|
| **kanam-auditor** (UI/UX) | ✅ `agents/kanam-auditor/ROADMAP.md` | v0.1 | 🟡 3 skills sueltos; `pixel-diff` real, `oracle`/`enforcer` parciales | Fase 1 → consolidar arsenal |
| **kanam-critic** (sustancia) | ✅ `agents/kanam-critic/ROADMAP.md` | v0.3 | 🟡 kit verificado (16/16 checks), disparadores montados, 1er veredicto real; falta el loop de retorno | v0.5 "El Retorno" (absorción de VETOs) |
| **kanam-planner** (orquestación) | ✅ `agents/kanam-planner/ROADMAP.md` | v0.3 | 🟢 5 skills; programas + delegación CORE + review semanal | Fase 2: medir demanda y evaluar dispatch directo |
| **kanam-dev** (ingeniería) | ✅ `agents/kanam-dev/ROADMAP.md` | v0.2.1 | ✅ superficie + ejecutables de medición (225 tests); 32/32 skills con verificación; camino a evidencia persistente y gating CI | Tramo 3 (P0) |
| **kanam-mind** (conocimiento) | ✅ `agents/kanam-mind/ROADMAP.md` | v0.1 | 🟡 10 skills; memoria + investigación | Tramo 3 (P1) |
| **kanam-ops** (infraestructura) | ✅ `agents/kanam-ops/ROADMAP.md` | v0.2 | 🟢 E1-E2 completas, E3 3/4, E4 en curso; 7 jobs propios | Tramo 3 (P1) |
| **kanam-studio** (comunicación) | ✅ `agents/kanam-studio/ROADMAP.md` | v0.2 | 🟡 v0.2; contenido + marca | Tramo 3 (P2) |
| **Kanam CORE** (orquestación raíz) | ✅ `docs/ROADMAP.md` | - | 🟢 roadmap del sistema (no de rol) | - |
| **openclaw-agent** (bundled) | n/a | - | - | fuera de alcance |

**Lectura:** 7 de 7 con roadmap (nivelación M1 cumplida; solo critic ya en v0.2). El ecosistema
está en **v0.1** salvo critic (v0.3). La meta de esta ronda es **escalar a v0.5** por dependencia (Tramo 3).

---

## Camino de madurez del meta-roadmap

| Fase | Qué es | Estado | Criterio de listo |
|---|---|---|---|
| **M0 - Diagnóstico y estándar** | Corregir el falso reporte, fijar el formato y el vocabulario de versión | ✅ | `roadmap-authoring-guide.md` existe; el estado real de los 7 está medido |
| **M1 - Nivelación** | Los 7 roles tienen `ROADMAP.md` con el formato estándar | ✅ | 7/7 archivos existen, siguen las 7 secciones y declaran su versión (guard `check-roadmaps.py` en verde) |
| **M2 - Tracking vivo** | Índice único + checklist de revisión + registro de saltos | ⚪ | este documento lista los 7; el checklist corre sobre roadmaps de rol; hay registro de cambios de versión |
| **M3 - Escalada a v0.5** | Cada rol cierra sus dependencias duras (memoria, verificación, autonomía) | ⚪ | los 7 declaran v0.5 con su señal de listo cumplida |
| **M4 - Verificación externa** | Ningún salto se auto-reporta: se verifica contra el filesystem / el runtime | ⚪ | 0 saltos marcados sin evidencia reproducible |
| **M5 - v1.0** | Los gates de calidad son estándar; el resto los invoca | ⚪ | critic y auditor en v1.0, invocables por el Crew |

---

## La secuencia (el orden correcto)

**Regla:** no se escala un rol antes de nivelarlo. Y no se escala un rol que depende de un gate
todavía falso: un pipeline de calidad montado sobre un gate roto devuelve **veredictos fabricados**
- el peor falso verde (lección de `kanam-auditor`, Fase 1).

### Tramo 1 - Nivelar (M1), en paralelo
Los 5 roadmaps faltantes se autoran en paralelo. No hay dependencia entre ellos: cada rol escribe
su propio mapa. El CORE los verifica contra formato y fuentes.

```
dev ─┐
mind ─┤
ops ──┼──► 5 × agents/<rol>/ROADMAP.md  (autoría del rol, verificación del CORE)
studio┤
planner┘
```

### Tramo 2 - Trackear (M2)
Con los 7 escritos, el tracking se vuelve útil: el índice de arriba queda como **la** fuente de
verdad del estado de madurez, y el checklist de revisión se extiende a los roadmaps de rol.

### Tramo 3 - Escalar a v0.5 (M3), por dependencia
Orden por **desbloqueo**, no por importancia:

| Prioridad | Rol | Por qué primero |
|---|---|---|
| **P0** | **critic** | Es el filtro de sustancia. Si está roto, todo lo que pasa por él está mal juzgado. Ya está en marcha (v0.2). |
| **P0** | **auditor** | Filtro de superficie. Misma lógica: primero que el gate sea real, después orquestarlo (su propia Fase 1 → 2). |
| **P0** | **dev** | Construye las obras. Su madurez es la de todo lo entregable. |
| **P1** | **ops** | Sostiene el sustrato; su deuda se paga en cada sesión (config, backups). |
| **P1** | **mind** | Conocimiento y memoria: alimenta a todos, pero no bloquea un gate. |
| **P2** | **planner** | Orquestación: vale cuando ya hay roles que orquestar. |
| **P2** | **studio** | Comunicación: el último eslabón, el que sale al mundo. |

**Regla del tramo:** critic y auditor **primero**, porque son los jueces. Un Crew con jueces
confiables y constructores mediocres se corrige; un Crew con constructores buenos y jueces falsos
se hunde creyendo que va bien.

---

## Tracking

**Fuente de verdad:** la tabla del **Mapa de madurez** arriba. No hay otra lista de versiones.

| Qué se trackea | Dónde |
|---|---|
| Versión declarada y estado por rol | tabla "Mapa de madurez" (este doc) |
| El roadmap de cada rol | `agents/<rol>/ROADMAP.md` |
| El historial de saltos de versión | `CHANGELOG.md` del workspace (una línea por salto) |
| La revisión contra fuentes reales | `docs/checklists/roadmap-review-checklist.md` |
| Los cambios de estado del meta-roadmap | este doc + daily de cierre |

**Señal de drift:** si un `ROADMAP.md` de rol declara una versión que no coincide con la tabla de
arriba, **gana el archivo del rol** y se corrige el índice. La tabla no manda sobre la evidencia.

---

## Enforcement (una regla sin guarda se viola sola)

La ausencia de roadmaps no se detectó durante meses porque **nada la verificaba**. Este
meta-roadmap se cierra con guardas:

1. **Existencia y formato:** `scripts/check-roadmaps.py` verifica que cada rol tenga `ROADMAP.md` con encabezado, versión y secciones del estándar. **Cableado al pre-commit, sin condición.**
2. **Coherencia de versión:** el mismo guard compara la versión declarada en cada `ROADMAP.md` contra la tabla del mapa de madurez y falla si hay drift.
3. **Revisión contra fuentes:** el checklist de roadmap tiene una **variante para roadmaps de rol** (`docs/checklists/roadmap-review-checklist.md`) que corre los mismos pasos contra el archivo del rol.

> **Regla de oro (ADR-083 aplicada):** una regla que vive solo en un documento no se cumple. Por
> eso el estándar vive en un **checklist** que el rol lee al escribir, y la existencia se verifica
> con un **guard**, no con la memoria del CORE.

---

## Red lines del meta-roadmap

- **No se inventa una versión.** El número se gana con la señal de listo; el default es v0.1.
- **No se marca verde por optimismo.** Ni un roadmap ni este índice pasan a 🟢 sin evidencia.
- **El CORE no escribe el roadmap de un rol.** Gobierna el formato y la coherencia; el contenido
  es de cada agente (ADR-083). El CORE delega la autoría y verifica el resultado en el repo.
- **No se escala sobre un gate falso.** Primero el juez real, después el pipeline que lo usa.
- **No se infla el ecosistema.** Un rol madura su rol; no absorbe el de otro.

---

## Cómo se mide el éxito

El meta-roadmap se gana cuando se cumplen las tres, con evidencia:

1. **7/7 roles** tienen `ROADMAP.md` con formato estándar y versión declarada verificada.
2. **0 saltos de versión** marcados sin su señal de listo cumplida (M4 sin excepciones).
3. **critic y auditor en v1.0**: el Crew los invoca por defecto y su veredicto es contrato.

Si esas tres no se cumplen, este documento es propaganda ordenada.

---

*El ecosistema no madura por tener siete documentos: madura cuando cada documento puede probar que
su rol avanzó.*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
