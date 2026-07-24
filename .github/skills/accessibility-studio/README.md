# Accessibility Studio

Diseñá, auditá y corregí accesibilidad en productos digitales.

## ¿Para qué sirve?

Para asegurarte de que tu app web sea usable por **todas las personas**, incluyendo quienes usan lectores de pantalla, navegación por teclado, o tienen baja visión. Hace un loop de **auditar → corregir → verificar** hasta que todo cumpla WCAG 2.2.

## ¿Cuándo usarlo?

- Antes de un launch (validación final)
- Después de cambios grandes de UI
- Cuando querés un reporte de cumplimiento (A, AA, AAA)
- Cuando un componente nuevo no es accesible

## ¿Cómo se usa?

### Modo Report (solo auditar)

```bash
./scripts/a11y-audit.sh https://tusitio.com
```

Genera un reporte Markdown con violations de axe-core y score de Lighthouse.

### Modo Fix (auditar + corregir + verificar)

El workflow te guía issue por issue: identifica el problema, lo corregís, re-audita, pasa al siguiente. Prioriza por severidad: Critical → Major → Minor.

### CI Mode

```bash
./scripts/a11y-ci.sh https://tusitio.com
```

Falla si hay violations. Ideal para GitHub Actions.

### Verificar contraste de colores

```bash
python3 scripts/contrast-report.py tailwind.config.js --backgrounds "#fff,#f8f9fa"
```

Analiza todos los colores de tu Tailwind config y te dice cuáles no pasan AA/AAA.

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/wcag-22-criteria.md` | Catálogo completo de criterios WCAG 2.2 (A/AA/AAA) |
| `references/testing-setup.md` | Cómo configurar axe-core, Lighthouse, Playwright |
| `references/aria-patterns.md` | Patrones WAI-APG: modal, tabs, combobox, disclosure |

## Skills relacionadas

- [Review & Quality](../review-quality) — Revisión pre-merge con accesibilidad
- [Pre-Deploy QA](../pre-deploy-qa) — Validación pre-deploy
