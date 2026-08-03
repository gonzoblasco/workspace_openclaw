---
name: "dev-guide-generator"
metadata:
  category: "Content"
  tags:
    - tutoriales
    - documentacion
    - guias
    - aprendizaje
description: "Generar tutoriales técnicos completos: prerrequisitos, setup, pasos core, troubleshooting, temas avanzados y cheatsheet."
user-invocable: false
---

# Workflow: Dev Guide Generator

## Propósito

Generar tutoriales técnicos completos desde un tema hasta un documento listo para publicar. Incluye prerrequisitos, environment setup, pasos core, troubleshooting, temas avanzados y cheatsheet.

## Cuándo usarlo

- Escribir un tutorial técnico
- Crear una guía de setup
- Documentar un proceso paso a paso
- Generar quickstart guide

## Fases

### 1. Topic Scoping
Definir tema, audiencia, objetivo, alcance.

### 2. Prerequisites
Lista de conocimientos y herramientas necesarias, categorizadas en "Must know" y "Nice to know".

### 3. Environment Setup
Instalación y configuración por SO, con comandos de verificación.

### 4. Core Steps
5-10 pasos progresivos, cada uno con: actions + explanation + verification.

### 5. Troubleshooting
5-8 errores comunes con causa y solución específica.

### 6. Advanced Topics
3-5 direcciones de aprendizaje avanzado + proyectos prácticos.

### 7. Cheatsheet
Referencia rápida de una página: comandos, snippets, troubleshooting.

## Outputs

- Tutorial completo en Markdown
- Cheatsheet de una página
- Troubleshooting table
- Advanced learning roadmap

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `tech-docs/scripts/analyze_codebase.py` | Extraer ejemplos reales del codebase para ilustrar pasos core. |
| `tech-docs/scripts/generate-adr.sh` | Documentar decisiones técnicas del tutorial si las hay. |
| `knowledge-management/scripts/check-refs.sh` | Verificar links internos del tutorial. |

## Related Skills

- [Technical Documentation](../tech-docs): Para documentación técnica de proyectos
- [Code Mentor](../code-mentor): Para enseñar conceptos dentro del tutorial
