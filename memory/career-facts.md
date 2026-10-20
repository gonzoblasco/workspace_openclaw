# Hechos de carrera - fuente única de los CVs

> **Dueño único** de los hechos duros de la carrera: fechas, años, títulos por rol, nivel de idioma, certificaciones y contacto. Los CVs y las cartas **citan** este archivo; ninguno lo reescribe por su cuenta.
>
> Un **perfil** distinto (a11y, fullstack, evaluator, no técnico) puede cambiar el **relato**: el resumen, el orden de los bullets, qué proyecto se destaca. **Nunca los hechos.** Si un CV necesita otro número, primero se cambia acá y después se propaga.
>
> Gate: `scripts/check-cv-facts.py` (pre-commit + CI). Ver ADR-101.

---

## Bloque de hechos (lo lee el gate)

```facts
total_years: 10
a11y_years_internal: 5
a11y_claim: roles
ai_years: 1
backend_years_internal: 1
sdlc_years: 3
english: B2
contact_phone: +54 11 4937 4656
contact_email: gonzoblasco@icloud.com
contact_linkedin: linkedin.com/in/gonzalo-blasco
contact_github: github.com/gonzoblasco
role_freelance: 05/2025 - Present
role_ey: 09/2021 - 05/2025
role_super7: 08/2020 - 05/2021
role_minutentag: 02/2016 - 11/2019
pending: 0
```

### Años

- **Desarrollo total: 10+ años** (feb 2016 - hoy). Único headline permitido.
- **Accesibilidad: SIN número declarado (decisión de Gonzo, 2026-10-20).**
  - **Nunca** escribir "N years of accessibility" ni "N+ años de accesibilidad", en ningún CV, carta ni screening. Ni 5, ni 6.
  - **Por qué:** la aritmética de las fechas canónicas da 4.42 años de función central (Super7 0.75 + EY 3.67) y 5.83 si se cuenta todo el freelance. Un número redondo obliga a elegir entre quedar corto o inflar, y el reclutador puede hacer la misma suma.
  - **Cómo se cuenta:** nombrando los roles donde fue central - **Super7UI** (auditoría de remediación de Warner Bros. Screeners) y **EY** (referente de a11y, 50+ componentes enterprise a WCAG) - más las contribuciones OSS continuas a Adobe, IBM, Meta y MUI. Los hechos, las fechas y los PRs hablan solos.
  - `a11y_years_internal: 5` es **calibración interna** para decidir si una propuesta tiene sentido. No es un dato de salida.
- **AI-first: desde 05/2025, ~1 año y medio. NUNCA 3 ni 5 (corrección de Gonzo, 2026-10-20).** Usa IA para desarrollo **desde que dejó EY**. Antes NO. Prohibido "5+ years working AI-first", "three years" o "since 2021": es el mismo período que el freelance.
- **Backend de producción: ~1 año y medio, NUNCA 4 (corrección de Gonzo, 2026-10-20).** Node.js/TypeScript con Supabase, Edge Functions y Stripe, todo del período freelance (05/2025-hoy). En EY el rol fue **full stack con foco frontend**, no backend de producción. Split declarado: 70/30 frontend/backend.
- **Nombre del rol 05/2025-presente: FREELANCE (corrección de Gonzo x2, 2026-10-20).** Se dice **"Freelancer" / "freelance"**. Prohibido "Independent", "Independiente" y "Founder" en CVs, formularios, screenings y entrevistas.
- **SDLC en fases concurrentes: 3+ años** (EY).
- **NO se suma** el backend PHP 2001-2008: hay gap 2008-2016 y no es a11y. Solo defendible como "20+ años en software" ante audiencia que no pregunte por el gap.

### Roles y fechas (idénticos en todos los perfiles)

| Período | Empresa | Título canónico | Lugar |
|---|---|---|---|
| 05/2025 - Presente | Freelancer | Software Engineer (sufijo por perfil: Accessibility Expert / Full Stack / Frontend) | Remoto |
| 09/2021 - 05/2025 | EY (Ernst & Young) | Senior Frontend Engineer, Accessibility Lead | Híbrido |
| 08/2020 - 05/2021 | Super7UI | Accessibility Engineer (Contractor) | Remoto |
| 02/2016 - 11/2019 | Minutentag | Frontend Developer, Accessibility Owner | Híbrido |

**Variante admitida:** en el perfil fullstack, EY puede leerse "Senior Full Stack / Frontend Engineer, Team Lead". Es el mismo hecho con otro encuadre, no otro empleo. No inventar un quinto rol ni cambiar fechas.

### Idioma

- **Declarado: B2.** Dato duro, decisión de Gonzo, reafirmado tras un error que lo declaró C1.
- **Nunca** C1, C2, "fluent", "bilingual" ni "Advanced" en formularios, screenings, CVs o entrevistas.
- El gap es **oral**, no escrito: lectura, escritura y trabajo diario están aceitados. No ofrecerle cursos generales.

### Certificaciones

- **Deque University - Accessibility Specialist Program (2021).** Es un **programa de cursos**, NO una certificación profesional.
- **NO tiene certificación IAAP** (CPWA / WAS / CPACC). Ese es el gap real y único.
- Prohibido escribir "accessibility certification" o insinuar credencial IAAP: un reclutador lo verifica en el registro de IAAP y el costo es la credibilidad completa.
- **CPACC antes del 30/11** es la palanca en curso, no un hecho consumado.

### Contacto

Fijo y verificable: `+54 11 4937 4656` · `gonzoblasco@icloud.com` · `linkedin.com/in/gonzalo-blasco` · `github.com/gonzoblasco`. Núñez, Buenos Aires, Argentina. Remoto LATAM, alineado a US EST.

### Proyectos que van al CV

- **SoporteML** (05/2025-presente, bajo Freelancer): CRM multi-tenant con IA para vendedores de Mercado Libre, Pro Motors como primer cliente, billing con Stripe operativo. **Sí va al CV** (regla 2026-10-20).
- **AI Engineering OS / OpenClaw**: sistema propio de trabajo con IA. Diferenciador, no relleno.
- **OSS mergeado**: Adobe React Spectrum, IBM Carbon, Meta Astryx, MUI. Solo PRs **mergeados** propios.

### Reglas del archivo

1. Este archivo es **doc-only** (ADR-065): no hay tabla en `memory.db`, no hay export.
2. Un cambio acá se propaga a los CVs en la misma sesión. Si un CV queda desalineado, el gate falla.
3. Un hecho nuevo se agrega **después** de decidirlo con Gonzo, nunca por inferencia desde un CV.
