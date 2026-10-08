# Guía de autoría: Roadmap de rol

> El estándar de **cómo se escribe y se mantiene el `ROADMAP.md` de un agente**. No es una plantilla
> de relleno: es el contrato de formato que hace que los siete roadmaps del ecosistema se puedan
> leer, comparar y trackear juntos.
>
> Nace 2026-10-07, junto con el **Roadmap de Roadmaps** (`docs/ROADMAPS.md`). Codifica el patrón que
> `kanam-auditor` y `kanam-critic` ya usaban de hecho, y lo vuelve obligatorio para el resto.

---

## Por qué existe este estándar

Un roadmap por rol, escrito por cada rol con su propio criterio, se vuelve siete documentos que no
se pueden comparar. El valor de tener siete roadmaps está en poder responder de un vistazo:
**¿qué rol está más atrás? ¿cuál es el próximo salto de cada uno? ¿quién decide ese salto?**

Para eso, los roadmaps comparten estructura, vocabulario de versión y criterio de cierre.

---

## Regla madre

**El roadmap no es una lista de deseos: es un mapa de dependencias.**

Cada hito justifica su lugar con la capacidad que desbloquea. Si un hito no desbloquea nada, no
entra. Si desbloquea algo pero cuesta más de lo que paga, tampoco entra. El roadmap del rol más
"creativo" y el del más "técnico" se leen con la misma vara: *¿esto me acerca a la v1.0, o es
ruido bien redactado?*

**Y el versionado es real:** la `Versión actual` declarada en el roadmap es la versión
**verificable** del rol hoy. Ausencia de roadmap = `v0.1` (premisa del ecosistema, 2026-10-07). Un
salto de versión exige su **criterio de listo** cumplido con evidencia, no una edición del número.

---

## Dónde vive

```
agents/<rol>/ROADMAP.md
```

Al lado de `AGENTS.md`, `IDENTITY.md`, `SOUL.md`. Es el mismo árbol que el agente lee; el roadmap
es de la persona, no de un proyecto.

- **Autoría:** el rol, en primera persona. El roadmap habla con la voz del agente.
- **Gobierno:** Kanam CORE. CORE garantiza que exista, que siga el formato y que la versión
  declarada no mienta. El **contenido** es del rol; la **coherencia del conjunto** es del CORE.
- **Revisión:** con el checklist `docs/checklists/roadmap-review-checklist.md`, contra fuentes
  reales (no de memoria).

---

## Estructura obligatoria (7 secciones)

Toda sección es obligatoria salvo que se marque lo contrario. Un roadmap que no cierra las 7 es
un borrador, no un roadmap.

### 1. Encabezado

```markdown
# ROADMAP.md - <Nombre del rol> <emoji>

**Versión actual:** v0.x
**Objetivo:** v1.0 - <nombre del trofeo>
**Última revisión:** YYYY-MM-DD
**Dueño:** <rol> (autoría) · Kanam CORE (gobierno)
```

### 2. Retrato de la versión actual (hoy)

Tabla de capacidades con su estado **verificado** (`✅ operativo` / `🟡 parcial` / `❌ no existe`).
Sin autoelogio: la columna de estado se prueba contra el filesystem, el código o el runtime.

Cierra con una línea de **honestidad**: *"lo que me falta es X, y eso es lo que me hace v0.x"*.

### 3. Visión v1.0 - el trofeo ganado

Qué significa que el rol esté **completo**, y el criterio objetivo que lo confirma (enunciado
como la señal de listo, no como una sensación).

### 4. Camino de madurez (v0.x → v1.0)

Tabla de saltos de versión. Cada fila: **qué es**, **estado** (`✅ completada` / `🟡 en curso` /
`⚪ pendiente`), **criterio de listo** (la señal verificable que autoriza el salto).

```markdown
| Etapa | Qué es | Estado | Criterio de listo |
|---|---|---|---|
| v0.1 - <nombre> | ... | ✅ | ... |
| v0.2 - <nombre> | ... | 🟡 | ... |
| v1.0 - <nombre> | ... | ⚪ | ... |
```

### 5. Hitos de la versión en curso

El foco del roadmap. Cada hito declara **qué eje mueve** (la capacidad que desbloquea), su
**evidencia requerida** para cerrarse (reproducida, no auto-reportada) y su orden respecto de los
demás.

### 6. Lo que rechacé (y por qué)

Los hitos que se evaluaron y **no** entraron, cada uno con el criterio que lo descartó. Esta
sección es la que prueba que el roadmap se pensó: un roadmap sin rechazos es una lista de compras.

### 7. Red lines y criterio de cierre

- **Red lines de mi evolución:** lo que el rol **no** va a hacer aunque parezca un avance (no
  cruzar el dominio de otro rol, no inflar, no cerrar sin evidencia).
- **Cómo se mide el éxito:** 3 condiciones concretas que, si no se cumplen, declaran la versión
  como propaganda.

---

## Vocabulario de versión (compartido)

| Versión | Significado |
|---|---|
| **v0.1** | El rol existe y es útil; tiene su vara o su ritual, pero le falta memoria, cierre o autonomía. Versión por defecto si no hay roadmap. |
| **v0.2-0.4** | Cierra dependencias duras: deja de depender del auto-reporte, gana memoria, gana verificación. |
| **v0.5** | **Punto de madurez intermedio**: el rol es confiable sin supervisión línea por línea. Es la meta de esta ronda de roadmaps. |
| **v1.0** | El rol es un estándar: otros agentes lo invocan por defecto, su salida es contrato y se mide a sí mismo. |

**Estado:** 🔴 no iniciado · 🟡 en curso / con deuda · 🟢 estable · ⚫ retirado.

---

## Antipatrones (vistos en carne propia)

- **Marcar una versión por optimismo.** El número no se edita: se gana con la señal de listo.
- **Usar el roadmap como backlog.** Lo concreto y fechado vive en `memory/memory.db`; el roadmap
  guarda el *estado de madurez*, no las tareas.
- **Escribirlo para la foto.** Un roadmap lindo que nadie va a ejecutar es peor que no tenerlo:
  crea la ilusión de dirección.
- **Copiar la estructura sin el criterio.** Las 7 secciones son el esqueleto; lo que vale es que el
  contenido haya pasado por *"¿esto desbloquea algo?"*.

---

## Relación con otros documentos

- `docs/ROADMAPS.md` - el **Roadmap de Roadmaps**: el índice, el tracking y la secuencia de trabajo
  sobre los siete roadmaps de rol.
- `docs/ROADMAP.md` - el roadmap **del sistema de trabajo** (capas, decisiones por capa). Es a nivel
  del sistema, no de un rol.
- `docs/NORTH.md` - el **"para qué"** de largo plazo. Ni este ni los roadmaps de rol lo redefinen.
- `docs/checklists/roadmap-review-checklist.md` - el procedimiento de revisión contra fuentes reales.
