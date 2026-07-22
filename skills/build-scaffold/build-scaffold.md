---
name: "build-scaffold"
description: "Project scaffolding and construction from scratch or on existing projects."
---

# Workflow: Build & Scaffold

## What it does

Scaffolding and construction of projects from scratch or on existing codebases.

## Phases

### 1. Analysis
Understand requirements, desired stack, features. If the project already went through product discovery, read the definition and roadmap instead of asking everything again.

### 2. Scaffold
Generate base structure (React, Next.js, Vite, etc.).

### 3. Configuration
TypeScript, linting, testing, styling, formatting.

### 4. Verification
Typecheck, lint, test, build.

### 5. Structure
Project documentation templates (adapted to project size).

### 6. Iteration
Modify existing projects (--iterate mode).

### 7. CI/CD
Configure CI pipeline for typecheck + lint + test + build on every PR.

## Outputs
- Functional project with green build
- Project documentation (README, changelog, roadmap)
- Architecture decisions for technical choices
- CI/CD pipeline configured
