---
name: "pre-deploy-qa"
description: "Pre-deployment validation: build, routes, SEO, API, performance, security, and cleanup."
---

# Workflow: Pre-Deploy QA

## What it does

Systematic validation before deploying to production. Runs after merge, before deploy.

## Phases

### 1. Build
- Build without errors
- Verify no compilation warnings

### 2. Routes
- Regression of all public routes (200)
- Protected routes (401/403 without auth)
- API endpoints (health, auth, core)
- sitemap.xml and robots.txt accessible

### 3. SEO
- Title 30-60 chars, unique per page
- Meta description present
- og:title, og:description, og:image (≥ 1200×630)
- twitter:card = summary_large_image
- Canonical self-referencing
- favicon.ico responds 200
- JSON-LD structured data if applicable

### 4. API
- Health check responds 200
- Auth endpoints work (login, session, logout)
- Errors return consistent JSON `{ error, message }`
- CORS headers correct if cross-origin

### 5. Performance
- Lighthouse ≥ 90 (Performance, A11y, SEO)
- Images with lazy loading and WebP/AVIF
- Dynamic imports for heavy components
- font-display: swap, no FOIT
- Total page weight < 1MB

### 6. Security
- No critical/high vulnerabilities
- No secrets in the diff
- No eval/new Function/document.write
- No stack traces in API errors

### 7. UI/UX
- Error boundaries at root + route level
- Not-found and loading pages exist
- Loading, error, and empty states in client fetches
- Buttons with hover, focus-visible, active, disabled, loading states
- No horizontal scroll at 320-1440px

### 8. Database
- Migrations applied and idempotent
- No hardcoded DB credentials in source
- No raw SQL injection risk
- No N+1 queries

### 9. Cleanup
- No console.log/debugger in staged code
- No unresolved TODOs/FIXMEs
- No dead imports
- No temporary files

## Outputs
- QA report with each phase (✅/❌/⚠️)
- Issues found with priority (Critical / Major / Minor)
- Decision: Go / No-Go for deploy
