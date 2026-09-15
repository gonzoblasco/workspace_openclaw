# Nivel 5 - Criterio de decision y mantenimiento (jefe final)

Capa 2 (cuaderno). Ultimo nivel: aca el estudio deja de aprender y pasa a **decidir**.
Datos verificados el 2026-09-14 (GitHub API + npm registry).

---

## 5.1 Radix contra las alternativas

### 5.1.1 Los criterios comparables

| Criterio | Por que importa |
|---|---|
| **Cobertura de APG** | Es la razon de existir de la libreria. Cobertura declarada y verificable por componente. |
| **Licencia** | Permite uso comercial y modificacion sin riesgo legal. |
| **Mantenimiento** | Frecuencia real de push, releases en npm, y **tiempo de respuesta a PRs** (lo medimos en carne propia). |
| **Granularidad** | Si expone partes componibles o un componente cerrado. Define si se puede integrar a un design system. |
| **Estabilidad de API** | Si esta en `1.0` estable o en RC/alpha. Un RC significa que puede romper. |
| **Peso** | Tree-shaking real y cantidad de dependencias internas arrastradas. |
| **DX / tipos** | API tipada y consistente. Afecta el costo de mantenimiento diario. |

### 5.1.2 La tabla, con numeros reales

| | **Radix Primitives** | **Base UI** | **Ariakit** | **HTML nativo** |
|---|---|---|---|---|
| Repo | `radix-ui/primitives` | `mui/base-ui` | `ariakit/ariakit` | - |
| Stars | **19.270** | 10.902 | 8.611 | - |
| Licencia | MIT | MIT | MIT (npm) | - |
| Creado | 2020-06 | 2024-02 | 2017-09 | - |
| Ultimo push | 2026-08-08 | **2026-09-15** | **2026-09-15** | - |
| Issues abiertos | 351 | 454 | **44** | - |
| Version npm | `radix-ui` **1.6.7** (2026-07-24) | `1.0.0-rc.0` (2025-12-04) | `2.0.0-next.44` (**2023-04-11**) | - |
| Estado de API | **estable** | **RC** | **prerelease** | estable |
| Granularidad | por partes (`Root`/`Trigger`/`Content`...) | por partes | por partes | ninguna |

### 5.1.3 Lo que dicen los numeros (y lo que no)

**1. Base UI es la alternativa mas fuerte, pero todavia no esta lista.**
La mantiene el equipo que hizo **Radix, Floating UI y Material UI** (esta en la descripcion del repo). Esta activa (push de hoy) y su arquitectura es comparable. Pero la version publicada es **`1.0.0-rc.0`**: *release candidate*. Adoptar un RC como base de accesibilidad es cambiar un problema de conocimiento por un problema de estabilidad. **No hoy.**

**2. Ariakit tiene el repo mas sano por actividad, pero su npm miente.**
Los 44 issues abiertos (vs 351 de Radix) y el push de hoy sugieren un proyecto cuidado. Pero el dist-tag `latest` de npm apunta a **`2.0.0-next.44`, publicada en abril de 2023**: quien hace `npm i ariakit` sin mirar instala un **prerelease de hace mas de dos anos**. Es el hallazgo mas util de la comparacion y no se ve leyendo el README: **el estado del repo no es el estado del paquete**. Se aplica a las tres librerias.

**3. Radix tiene la cadencia mas lenta de las tres.**
Ultimo push 2026-08-08, mas de un mes antes de hoy, contra push del mismo dia en las otras dos. La licencia y el estado estable juegan a favor; la cadencia, en contra. Y hay evidencia propia que lo confirma: **los 4 PRs nuestros a Radix se cerraron por inactividad**, sin review, tras un mes. No hubo respuesta del maintainer.

**4. HTML nativo gana en una sola cosa pero decisiva: no es dependencia.**
`<dialog>` (con `showModal()`) cubre modal, trampa de foco y `Esc`. `<details>` cubre el disclosure. `<select>` cubre la seleccion simple. Lo que no da: personalizacion, posicionamiento, y los anuncios de screen reader que Radix resuelve con `Title`/`Description` (Nivel 3). El costo es **escribir y verificar a mano** lo que falta - y ahi esta el punto de la decision.

---

## 5.2 La decision documentada (el jefe final)

### 5.2.1 Por que el ADR era necesario

`docs/adr/ADR-037-lucide-iconos-base.md` cita **"el ecosistema shadcn/Radix"** como si fuera un hecho del stack, y el propio ADR-037 admite que la eleccion **no estaba documentada como decision**. O sea: un ADR funda una eleccion (los iconos) en otra eleccion **que nunca se tomo explicitamente**.

Hoy existe la regla (2026-09-14): **el precedente no es un motivo**. Consecuencia directa: o se justifica Radix/shadcn con criterios verificables, o se deja de citar.

### 5.2.2 La decision

Redactada en **`docs/adr/ADR-048-shadcn-radix-stack-ui.md`**. Resumen:

- **Se mantiene** Radix como capa de comportamiento accesible y shadcn como codigo propio.
- **Fundamento:** cobertura APG, granularidad por partes, API estable (`1.6.7`), MIT, y el hecho de que la alternativa mas fuerte (Base UI) esta en RC.
- **Con reglas de uso** (cuando si, cuando no) y **disparadores de revision** (que la harian cambiar de opinion).
- **Explicito:** no se cita el precedente como razon. El ADR existe **porque** el precedente no era razon.

### 5.2.3 Los dos casos que el ADR tiene que explicar

Son las dos puntas reales del uso (Nivel 4):

- **`kanam-pulse`:** a11y-first y **sin Radix**, a proposito. El ADR tiene que justificar por que eso tambien es correcto: no hay patron interactivo complejo, y sumar la dependencia agrega peso sin agregar accesibilidad (contraste, jerarquia y landmarks -lo que ese proyecto necesita- no son su contrato).
- **`quedamos`:** declara shadcn como stack planeado **sin codigo escrito**. El ADR no lo "arregla": registra que una declaracion sin implementacion **no es evidencia de uso**.

---

## 5.3 Mantenimiento

### 5.3.1 Lo que hay que monitorear

| Riesgo | Senal | Accion |
|---|---|---|
| **Divergencia de generaciones** | Ya detectada: `kanam-mind` (shadcn viejo, `forwardRef`) vs `kanam-forge` (nuevo, `data-slot`) | Decidir si unificar; no es urgente |
| **Drift de los componentes propios** | shadcn no se actualiza solo: si mejora upstream, no llega | Re-generar por componente cuando hace falta |
| **Multiplicacion de paquetes Radix** | Hoy 6 en `kanam-forge`, 3 en `kanam-mind` | Instalar `radix-ui` unico en proyectos nuevos (Nivel 2: evita duplicacion de las 55 dependencias internas) |
| **Cadencia upstream** | Sin releases hace mas de un trimestre, o PRs sin review | Reabrir este ADR |

### 5.3.2 Re-evaluacion programada

**Disparador concreto:** cuando **Base UI llegue a `1.0.0` estable**. Ese es el momento de reabrir el ADR, no antes. Mientras siga en RC, cambiar Radix por Base UI es intercambiar un riesgo conocido por uno nuevo.

---

## Verificacion del Nivel 5 (jefe final)

1. Nombrar **el dato** que descarta a Base UI hoy y **el disparador** que la vuelve a poner en la mesa.
2. Por que "el repo esta activo" **no alcanza** como criterio de mantenimiento? (Ariakit.)
3. Radix tiene la cadencia mas lenta y nuestros 4 PRs se cerraron sin review: **por que se mantiene igual**?
