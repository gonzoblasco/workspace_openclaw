# ADR-002: UI de kanam-lab - mantener Gradio

- **Fecha:** 2026-09-16
- **Estado:** Aceptado
- **Origen:** workspace (discusion de migracion a React, 2026-09-16)
- **Relacionado:** ADR-001 (playground de IA local con Gradio)
- **Nota:** este ADR llego con el numero 048 desde `docs/adr/` del workspace (ADR global), donde colisionaba con otro ADR-048. Es una decision de alcance de proyecto, asi que se movio aca y se renumero como 002 el 2026-09-22. El indice global exige "alcance general, aplicable a cualquier proyecto"; esta decision es especifica de kanam-lab.

## Contexto

kanam-lab es un playground para experimentar con batallas de modelos de IA, RAG, STT, etc. Hoy usa Gradio con varias pestanas. Se considero migrar a una UI en React para una experiencia mas product-like.

## Decision

**Mantener Gradio como framework de UI de kanam-lab por ahora.** El backend ya esta desacoplado, lo que hace directa una futura migracion a React si aparece una necesidad de producto. Gradio da velocidad de iteracion, coincide con la naturaleza experimental actual y evita overhead de desarrollo innecesario.

## Consecuencias

- No hay trabajo inmediato de reescritura de UI.
- El camino de migracion queda abierto: el backend puede reutilizarse desde un front en React.
- La documentacion anota esta decision y la posibilidad abierta de migrar despues.
- Toda feature de UI nueva se sigue construyendo con componentes de Gradio.

## Verificacion (2026-09-22)

La decision sigue vigente: `requirements.txt` declara `gradio>=5.0` y hay imports activos en `kanam_lab/ui.py` y `app/app.py`. No hay indicios de migracion en curso.
