# KANAM DESIGN SYSTEM 🌿

> La identidad visual de todo producto Kanam. Fuente de verdad única, versionada, aplicable a
> cualquier stack (Python/Gradio, React, HTML plano).

**Qué es:** el sistema que hace que kanam-lab, SoporteML, Kanam Desk y todo lo que salga de acá
**se vean y se sientan como Kanam** - sin re-decidir colores, tipografía y espaciado en cada
proyecto, sin repetir los errores del "AI look".

**Qué no es:** un documento de gustos. Es un sistema de tokens verificables, con contraste WCAG
medido, y una arquitectura pensada para multi-marca.

---

## Arquitectura (3 capas + temas)

```
design/tokens/
  kanam.tokens.json          <- CAPA 1 (primitivas) + CAPA 2 (semántica de marca Kanam)
  themes/
    plaza.tokens.json        <- TEMA de producto (sobreescribe SOLO la capa semántica)
    terrario.tokens.json     <- TEMA de producto (idem)
  build-tokens.py            <- resuelve referencias y genera CSS
  dist/                      <- CSS GENERADO (no editar a mano)
    kanam.css                  sistema base
    plaza.css                  [data-theme="plaza"]
    plaza.root.css             :root (apps de un solo tema)
    terrario.css               [data-theme="terrario"]
    terrario.root.css          :root (apps de un solo tema)
```

| Capa | Qué contiene | Regla |
|---|---|---|
| **1. Primitivas** | Valores crudos: `teal.600`, `space.4`, `radius.md` | Nunca se usan directo en producto |
| **2. Semántica** | Intención: `brand.primary`, `text.secondary`, `state.danger` | Es lo que usan los componentes. **Los temas redefinen solo esta capa** (intent over value) |
| **3. Componente** | Tokens específicos de un componente; viven en el proyecto | Solo si no se resuelve con semántica |

**Por qué así:** un producto nuevo (o un cambio de marca) redefine ~40 tokens semánticos y **no
toca un solo componente**. Eso es lo que hace escalable al sistema multi-marca: los componentes
hablan de intención, no de color.

---

## Uso

### Generar el CSS
```bash
python3 design/tokens/build-tokens.py
```
Verifica que **todas** las referencias se resuelvan; si alguna queda sin resolver, falla con aviso
(no esconde el error).

### En HTML/CSS
```html
<link rel="stylesheet" href="design/tokens/dist/kanam.css">
<link rel="stylesheet" href="design/tokens/dist/plaza.css">
<html data-theme="plaza">
```
```css
.boton { background: var(--k-brand-primary); color: var(--k-text-onBrand); }
.aviso { color: var(--k-state-danger); border: 1px solid var(--k-border-subtle); }
```
Cambiar de tema = cambiar `data-theme`. Los componentes no se tocan.

**Apps de un solo tema (ej. Gradio)** que no controlan el atributo del root: usar la variante
`.root.css` en lugar de la de scope:
```html
<link rel="stylesheet" href="design/tokens/dist/kanam.css">
<link rel="stylesheet" href="design/tokens/dist/terrario.root.css">
```

### En Python (Gradio)
Leer el CSS generado (`kanam.css` + `<tema>.root.css`) y pasarlo a `launch(css=...)`, con un
adapter que mapee los `--k-*` a las variables que consume Gradio. **kanam-lab es la
implementación de referencia**: `projects/kanam-lab/app/app.py` (`_load_ds_css()` + adapter),
que además corre el build una vez si el `dist/` no existe.

---

## Principios no negociables

1. **Contraste verificado, no sentido.** Todo par texto/fondo sale de un token medido: 4.5:1 mínimo
   para cuerpo, 3:1 para texto grande. Cada tema documenta su matriz de contraste.
2. **El estado nunca depende solo del color.** Siempre icono o texto además del color.
3. **Foco visible siempre.** Anillo de 2px en todo elemento interactivo (WCAG 2.2).
4. **Semántica única de color.** verde = éxito, ámbar = atención, rojo = peligro. Nunca se invierte.
5. **Sin sombras decorativas por defecto.** La separación la hacen borde y superficie. Las sombras
   del sistema son mínimas y con intención.
6. **Tipografía con jerarquía, no con decoración.** Display para títulos, body para lectura, mono
   para datos.
7. **Nada del "AI look".** Sin gradientes decorativos, sin morado por defecto, sin radios
   exagerados, sin padding inflado. Ver `skills/frontend-ui-engineering` para la lista completa.
8. **Voz consistente.** El sistema cubre lo visual; la voz de marca vive en `docs/voz-gonzo.md` y
   en el manual de cada producto.

---

## Temas registrados

| Tema | Para qué | Paleta base | Contraste mínimo |
|---|---|---|---|
| **Kanam** (base) | El sistema mismo, docs internas | Teal `#0d9488` | 4.5:1+ |
| **Plaza** | Productos comerciales / seller-facing (Kanam Desk, SoporteML) | Cream `#FFF8EC` + Navy `#12294B` + Sun `#FFDD3A` | 4.9:1 (coral) / 13.5:1 (texto) |
| **Terrario** | Herramientas internas / laboratorio (kanam-lab, dashboards) | Sand `#FAF9F5` + Verde `#3D7A4D` | 6.4:1 (primary) / 15.4:1 (texto) |

Para agregar un tema: copiar `themes/plaza.tokens.json`, ajustar la capa semántica, agregarlo a la
lista `THEMES` de `build-tokens.py`, correr el build, y documentar su matriz de contraste acá.

---

## Verificación

- **Contraste:** cada tema declara su matriz en el JSON (`$contrast`). Antes de publicar un tema,
  comprobar cada par con un verificador WCAG (no a ojo).
- **Tokens sin resolver:** el build falla. No se commitea un `dist/` con referencias rotas.
- **A11y en la implementación:** para componentes con ARIA/anuncio, la validación manual con
  screen reader es obligatoria antes de dar por terminado (skill `a11y-at-validation`).

---

_Última actualización: 2026-09-14 · Owner: Kanam · Institucionalizado en ADR-047._
