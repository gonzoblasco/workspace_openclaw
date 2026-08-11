# Prompt: Reconciliación de tokens de diseño (para Lovable)

> **Cuándo usar:** para pedirle a Lovable la definición exacta de los tokens de diseño que su guía propone y que v1 de SoporteML no tiene. Complementa `PROMPT-SCHEMAS-BD.md` (ya ejecutado).
> **Estado:** ✅ EJECUTADO (2026-08-11). Respuesta guardada en `DESIGN-TOKENS-LOVABLE.md`.
> **Nota:** pedir SOLO valores de tokens y reglas de uso, nunca secretos.

---

```
Estoy reconstruyendo SoporteML (CRM multi-tenant para vendedores de Mercado Libre) en una nueva versión, y tengo tu guía de diseño oficial como fuente de verdad visual. Necesito que me aclares la definición exacta de algunos tokens y reglas que tu guía menciona pero que no están completamente especificados, para implementarlos correctamente en el design system.

Por favor, generá un documento Markdown con:

1. **Tokens semánticos faltantes** - para cada uno, el valor exacto en HSL (claro y oscuro), su propósito, y en qué componentes/estados se usa:
   - `--primary-muted` (fondo suave, chips activos)
   - `--primary-strong` (texto/íconos de marca con contraste AA)
   - `--informative` (estado informativo del sistema)
   - `--surface-active` (estado active de botón secundario)
   - Cualquier otro token semántico que tu guía use y que no esté en esta lista.

2. **Regla de estado (fondo 12-15% + texto 100%)** - confirmá si es una regla global para todos los estados (success, warning, destructive, informative, primary) o solo para algunos. Detallá cómo se aplica: ¿el fondo siempre es el color base al 12-15% de opacidad y el texto/ícono al 100%? ¿Hay excepciones (ej. badges con fondo sólido)?

3. **Escala tipográfica** - tu guía define Display/H1/H2/H3/Body/Small/Caption/Micro/Overline. Para cada nivel: tamaño (px o rem), line-height, font-weight, letter-spacing, y en qué contexto se usa (título de página, título de sección, label de campo, etc.).

4. **Tokens de color base** - confirmá la paleta completa de tokens semánticos que SoporteML debería tener en v3 (los que ya existen en v1 más los nuevos), con su valor HSL en claro y oscuro, para que el design system quede completo y consistente.

5. **Reglas de uso** - para los tokens nuevos, indicá en qué componentes se aplican (botones, badges, chips, estados de pregunta, sidebar, etc.) y si hay alguna regla de contraste AA que deba respetarse.

Devuelve todo en un único documento Markdown, organizado por secciones, listo para ser usado como referencia técnica para implementar el design system de la nueva versión. Si algo no aplica o no existe, indicá "No aplica" en esa sección.
```

---

## Contexto para Gonzo

**Tokens que v1 ya tiene** (no hace falta pedirlos, solo confirmar): `--primary`, `--primary-foreground`, `--background`, `--card`, `--muted`, `--accent`, `--border`, `--foreground`, `--muted-foreground`, `--sidebar-*`, `--success`, `--warning`, `--destructive`, badges de categoría (precio/stock/tecnico/envio/garantia).

**Tokens que faltan** (los que pide el prompt): `--primary-muted`, `--primary-strong`, `--informative`, `--surface-active` + regla de estado 12-15% + escala tipográfica fina.
