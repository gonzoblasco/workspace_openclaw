# Dev Guide Generator

Generador de tutoriales técnicos completos.

## ¿Para qué sirve?

Para **escribir tutoriales técnicos** desde cero con estructura profesional: prerrequisitos, environment setup, pasos core, troubleshooting, temas avanzados y cheatsheet. Un tema → un tutorial listo para publicar.

## ¿Cuándo usarlo?

- Cuando querés documentar una herramienta que usás
- Cuando necesitás un quickstart guide para un proyecto
- Cuando querés escribir un tutorial para el blog o la documentación

## ¿Cómo se usa?

Es conversacional. Le decís el tema y genera el tutorial completo siguiendo 8 fases.

> "Haceme un tutorial de Docker para developers de Node.js que nunca usaron containers."

Dependiendo de cuánta info le des, funciona en distintos modos:

| Tu input | Modo |
|---|---|
| Solo "Docker tutorial" | Te hace preguntas (audiencia, OS, objetivo) |
| "Deployar una app Node con Docker" | Pregunta 1-2 cosas y arranca |
| Descripción detallada | Full-auto desde Phase 2 |
| "Dale nomás, no preguntes" | Quick mode con defaults |

### Output

El tutorial incluye:

1. **Prerequisites** — conocimientos y herramientas necesarias
2. **Environment Setup** — instalación por SO con verificación
3. **Core Steps** — 5-10 pasos progresivos con actions + explanation + verification
4. **Troubleshooting** — 5-8 errores comunes con solución específica
5. **Advanced Topics** — 3-5 direcciones para seguir aprendiendo
6. **Cheatsheet** — referencia rápida de una página

## Skills relacionadas

- [Technical Documentation](../tech-docs) — Para documentación técnica de proyectos
- [Code Mentor](../code-mentor) — Para enseñar conceptos dentro del tutorial
