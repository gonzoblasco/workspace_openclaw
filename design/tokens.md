# Kanam OS Design Tokens V1 🌿

Este archivo es la **fuente de verdad única** para los colores y medidas del sistema. Los componentes no deben usar valores hexadecimales directos, sino referenciar estos tokens.

## 🎨 Paleta de Colores

### 1. Primitivas (Valores Crudos)
*Valores base. No se usan directamente en los componentes.*

| Token | Hex | Muestra |
| :--- | :--- | :--- |
| `teal-50` | `#f0fdfa` | ⚪ |
| `teal-500` | `#14b8a6` | 🟢 |
| `teal-600` | `#0d9488` | 🌿 (Primary) |
| `teal-900` | `#134e4a` | 🌲 |
| `slate-50` | `#f8fafc` | ⚪ |
| `slate-200` | `#e2e8f0` | 🔘 |
| `slate-500` | `#64748b` | 🔘 |
| `slate-900` | `#0f172a` | ⚫ |
| `red-600` | `#dc2626` | 🔴 |
| `amber-500` | `#f59e0b` | 🟡 |

### 2. Semántica (Intención)
*Estos son los tokens que los componentes consumen.*

| Intención | Token | Referencia | Uso |
| :--- | :--- | :--- | :--- |
| **Brand Primary** | `--k-brand-primary` | `teal-600` | Acciones principales, identidad. |
| **Brand Subtle** | `--k-brand-subtle` | `teal-50` | Fondos de destaque, badges. |
| **Text Main** | `--k-text-main` | `slate-900` | Cuerpo de texto, títulos. |
| **Text Muted** | `--k-text-muted` | `slate-500` | Etiquetas, captions, ayuda. |
| **BG Main** | `--k-bg-main` | `slate-50` | Fondo de pantalla, superficies base. |
| **BG Surface** | `--k-bg-surface` | `#ffffff` | Cards, inputs, modales. |
| **Border Subtle** | `--k-border-subtle` | `slate-200` | Separadores, bordes de input. |
| **State Danger** | `--k-state-danger` | `red-600` | Errores, borrados, alertas críticas. |
| **State Warning** | `--k-state-warning` | `amber-500` | Advertencias, pendientes. |

---

## 📏 Medidas y Geometría

### 1. Espaciado (Spacing)
*Basado en un sistema de 4px.*

| Token | Valor | Uso |
| :--- | :--- | :--- |
| `space-1` | `4px` | Espacios mínimos. |
| `space-2` | `8px` | Espacio entre elementos relacionados. |
| `space-4` | `16px` | Padding estándar de componentes. |
| `space-8` | `32px` | Margen entre secciones. |

### 2. Bordes (Radius)
*Evitamos el "pill-shape" excesivo.*

| Token | Valor | Uso |
| :--- | :--- | :--- |
| `radius-sm` | `2px` | Inputs, checkboxes. |
| `radius-md` | `4px` | Botones, cards pequeñas. |
| `radius-lg` | `8px` | Modales, contenedores grandes. |

---

*Actualizado el 2026-10-01. Este sistema simplifica la arquitectura anterior para priorizar la legibilidad y la auditoría.*
