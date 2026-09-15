# Nivel 4 - Radix en el stack real

Capa 2 (cuaderno). Primer nivel que **no se cierra con la doc**: se verifica contra los repos.
Fuente: `gh api` sobre los repos de `gonzoblasco`, 2026-09-14 (package.json, arbol de archivos y componentes).

---

## 4.0 Alcance del barrido (que se mira y que no)

**Se mira:**

| Proyecto | Por que entra |
|---|---|
| `kanam-forge` | Ancla del portfolio. Next.js + shadcn. 6 paquetes Radix. |
| `kanam-mind` | Archivado del portfolio pero con codigo real. 3 paquetes Radix. |
| `quedamos` | Declara shadcn en su `.knowledge/`. |
| `kanam-pulse` | **Contraejemplo:** a11y WCAG 2.2 AA desde el dia uno y **NO usa Radix**. |

**No se mira: toda la familia `soporteml`** (v1, v3, v4). Decision de Gonzo (2026-09-14) + ADR-001: queda fuera de narrativa publica y de auditorias. No se toca, no se lista, no se decide su destino.

---

## 4.1 Radix y shadcn: quien es quien

### 4.1.1 shadcn no es una dependencia

**Verificado, no asumido:** en los `package.json` de `kanam-forge` y `kanam-mind` **no hay ninguna entrada `shadcn`**. Lo que hay es:

```
kanam-forge:  @radix-ui/react-avatar, -collapsible, -dialog, -separator, -slot, -tooltip
kanam-mind:   @radix-ui/react-dialog, -label, -slot
```

shadcn es **una CLI que copia archivos a tu repo**. Las dependencias reales son los paquetes `@radix-ui/*` que esos archivos importan. Por eso la distincion importa en serio:

- **Radix** = dependencia de runtime. Se versiona, se actualiza, puede romper.
- **shadcn** = codigo tuyo, en `components/ui/`. Se edita libremente y **no se actualiza solo**: si shadcn mejora un componente, no te llega hasta que lo re-generes.

### 4.1.2 Y se nota en el codigo: dos generaciones conviviendo

Al comparar los mismos componentes en los dos repos aparece algo que la doc no dice: **son generaciones distintas de shadcn**.

**`kanam-mind/components/ui/dialog.tsx`** (generacion vieja):
```tsx
const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay ref={ref} className={cn("...", className)} {...props} />
));
```

**`kanam-forge/components/ui/dialog.tsx`** (generacion nueva):
```tsx
function DialogOverlay({
  ...props
}: React.ComponentProps<typeof DialogPrimitive.Overlay>) {
  return <DialogPrimitive.Overlay data-slot="dialog-overlay" {...props} />
}
```

Diferencias concretas:

| | Generacion vieja (`kanam-mind`) | Generacion nueva (`kanam-forge`) |
|---|---|---|
| Componente | `React.forwardRef` | funcion simple |
| Tipos | `ElementRef` + `ComponentPropsWithoutRef` | `ComponentProps` |
| Marca | `displayName` | `data-slot="..."` |

**Por que esto es relevante para el estudio:** `asChild` necesita `forwardRef` **solo cuando el wrapper se compone a si mismo** (Nivel 2, 2.2.2). La generacion nueva reemplazo el `forwardRef` por `data-slot` como mecanismo de identificacion, lo que **cambia la regla**: el requisito de `forwardRef` aplica a *tu* componente hoja, no al wrapper de shadcn. Es exactamente el tipo de detalle que solo se ve mirando el codigo.

---

## 4.2 Cuando bajar al primitive

### 4.2.1 El sintoma

El wrapper de shadcn es un **default**: tiene estilos, estructura y una API fija. Se estorba cuando:

- Necesitas una **parte** que el wrapper no expone (el wrapper viejo de `kanam-mind` no re-exporta `Dialog.Anchor`, por ejemplo).
- Necesitas **controlar el comportamiento** (los 4 hooks de foco del Nivel 3) y la API del wrapper no los pasa.
- El wrapper **impone estructura** (un `DialogOverlay` fijo, un `Close` con icono auto-insertado).

### 4.2.2 Como bajar sin romper

**Regla: extender, no forkear.** El codigo de shadcn es tuyo, pero si lo editas en el lugar, la proxima regeneracion te pisa el cambio. Las dos salidas:

1. **Editar `components/ui/`** si el cambio es del componente base (y entonces ese archivo ya no es "shadcn", es tuyo - anotarlo).
2. **Importar el primitive directo** en tu componente de feature cuando necesitas algo que el wrapper no da.

**Verificado en el repo:** `kanam-forge/components/ui/button.tsx` usa `Slot` de `@radix-ui/react-slot` con `cva` (variantes) - o sea que el wrapper ya esta haciendo composicion real, no solo estilos. Es el patron correcto: el primitive da el comportamiento, `cva` da las variantes, y el consumidor usa una API de producto.

---

## 4.3 Cuando NO usar Radix

### 4.3.1 El contraejemplo que vale: `kanam-pulse`

**Verificado:** `kanam-pulse` (ancla del pilar Local-First, **WCAG 2.2 AA desde el dia uno**) **no usa Radix ni shadcn**. Su stack es: Vite + React + TypeScript, Lucide, y CSS propio.

Y no es una omision: es **coherente con su diseño**. Un dashboard que lee metricas de la maquina tiene una UI de **lectura** -cards, un gauge, una lista de checks, toggles-, no de patrones interactivos complejos. Los primitives de Radix resuelven *dialog, select, combobox, tooltip, menu*: la parte cara de las UIs **interactivas**. Un dashboard necesita sobre todo **semantica limpia y contraste verificado**, que Radix no aporta igual (Nivel 3, 3.5.2: contraste, jerarquia y landmarks no son su contrato).

**La conclusion del nivel:** a11y-first no implica Radix. La pregunta correcta no es "usamos Radix?" sino **"tenemos un patron interactivo complejo que no queremos reimplementar?"**. Si la respuesta es no, sumar la dependencia **agrega peso sin agregar accesibilidad** - y encima pone una capa entre vos y el DOM, que para auditar a11y es una desventaja.

### 4.3.2 Lo que el HTML nativo ya resuelve

- Un `<details>`/`<summary>` para disclosure simple: no necesita `Collapsible`.
- Un `<dialog>` nativo para un modal basico (con `showModal()`): atrapa el foco y da el backdrop sin dependencia.
- Un `<select>` nativo, si el diseño lo acepta.
- Un `<button>` real en vez de un `div` con `role` - el caso que la propia doc de Radix marca como limite (Nivel 3, 3.2.1).

El `<dialog>` nativo merece una nota: cubre modal + foco + `Esc`, que es buena parte de lo que se usa Radix para. Se pierde personalizacion y el manejo de anuncios con `Title`/`Description`. La decision es caso por caso, pero **existe la alternativa sin dependencia** y vale sopesarla.

---

## 4.4 Aplicacion a los proyectos propios

### 4.4.1 Que hay de verdad, repo por repo

| Proyecto | Radix instalado | Componentes shadcn | Estado real |
|---|---|---|---|
| **`kanam-forge`** | 6 paquetes (avatar, collapsible, dialog, separator, slot, tooltip) | 11 en `components/ui/` (avatar, breadcrumb, button, collapsible, dialog, input, separator, sheet, sidebar, skeleton, tooltip) | Codigo activo. Next 16.3, React 19.2, Tailwind 4 |
| **`kanam-mind`** | 3 paquetes (dialog, label, slot) | 5 (button, dialog, input, label, textarea) | Codigo real, proyecto **archivado del portfolio**. Next 16.2, React 19.2 |
| **`quedamos`** | **ninguno** | **ninguno** | Solo `.knowledge/`, README, docs y `.gitignore`: **no hay codigo**. Declara shadcn como **stack planeado** (su ROADMAP tiene el paso sin marcar) |
| **`kanam-pulse`** | **ninguno** | **ninguno** | Decidido a proposito (ver 4.3.1) |

**Hallazgo del barrido:** de los 4, solo **2 usan Radix de verdad**. `quedamos` lo declara pero no existe el codigo (no es un error de la doc: el proyecto esta sin arrancar), y `kanam-pulse` lo evita a proposito.

### 4.4.2 Donde el uso es correcto y donde es inercia

**Correcto:**
- `dialog` en ambos: es el caso de uso canonico (modal + foco + anuncios). Reimplementarlo es caro y fragil.
- `collapsible`, `avatar`, `tooltip`, `separator`, `sheet`, `sidebar` en `kanam-forge`: patrones con comportamiento o semantica especifica.
- `slot`: no es un componente, es el **mecanismo de composicion** (`asChild`) - su presencia es correcta y es la unica dependencia que "habilita" a las demas.

**A revisar:**
- **`separator`**: un `<hr>` o un `border` resuelve lo mismo en la mayoria de los casos. El primitive aporta el `role="separator"` correcto y la orientacion, pero suele ser un candidato a salir.
- **`input`, `textarea`, `skeleton`**: no envuelven Radix - son codigo de shadcn puro (estilos + `className`). No son dependencia, **son archivos tuyos**: si se quieren limpiar, se editan sin tocar paquetes.

### 4.4.3 Y aparece la regla de idioma

En `kanam-mind/components/ui/dialog.tsx`, el boton de cerrar trae:

```tsx
<X className="h-4 w-4" />
<span className="sr-only">Cerrar</span>
```

Es la regla del workspace aplicada **dentro de un componente generado**: shadcn viene con `Close`/`Close` en ingles, y este fue traducido a `Cerrar`. Detalle chico, pero es exactamente la clase de cosa que se pierde al regenerar el componente: **el codigo de shadcn es tuyo, pero tambien es tuyo mantenerlo traducido y accesible.**

---

## Verificacion del Nivel 4

1. Por que "shadcn" no aparece en el `package.json` y que implica eso para actualizaciones?
2. `kanam-pulse` no usa Radix y es a11y-first: **que dice eso** sobre la relacion entre primitives y accesibilidad?
3. Nombrar **un primitive que podria salir** de `kanam-forge` y con que se reemplaza.
