# DEFINITION — Antigravity Developer Stack

## MVP (Estado Actual)

El MVP ya está en producción: v1.3.0 con 80+ skills en 9 playbooks. La definición acá es para la **próxima iteración**.

## Próxima Iteración (v2.0)

### Features Core
1. **CI/CD Pipeline** — GitHub Actions que valide:
   - Estructura de carpetas consistente
   - SKILL.md presente en cada skill
   - Links internos válidos
   - README.md sincronizado con skills reales
2. **Tests de Consistencia** — Script que verifique:
   - Todas las skills listadas en capability map existen
   - No hay skills huérfanas (sin listar)
   - CHANGELOG.md actualizado
3. **Sistema de Tags** — Metadatos YAML en cada skill:
   - Dominio, fase, complejidad, dependencias
4. **Búsqueda** — Index de skills por dominio/fase

### Features Nice-to-Have
- Generación automática de capability map desde metadatos
- Dashboard web de skills (docs/index.html mejorado)
- Template de nueva skill con scaffolding
- Integración con OpenClaw skills

## Personas

### Gonzo (Creador/Mantenedor)
- Quiere que el repo sea su portfolio vivo de ingeniería con IA
- Necesita mantenerlo sin esfuerzo operativo
- Quiere que sea útil para él y para otros

### Desarrollador AI-First (Usuario)
- Llega buscando una skill específica
- Quiere entender rápido qué hay disponible
- Necesita playbooks que conecten skills en workflows

## Métricas de Éxito

- **v2.0:** CI/CD verde, tests pasando, 0 skills huérfanas
- **v2.1:** Metadatos YAML en todas las skills
- **v2.2:** Búsqueda funcional
- **Adopción:** Stars en GitHub, forks, issues de otros usuarios
