---
name: "ui-generation"
description: "Add shadcn/ui assistant capability: list, suggest, and install shadcn components and blocks without a broken MCP server."
metadata:
  version: 1.1.0
  author: Kanam
  tags: ["ui", "components", "react", "vue", "svelte", "angular", "design-tokens", "accessibility", "mcp", "shadcn"]
allowed-tools:
  - exec
  - read
  - write
  - edit
  - file_write
  - file_fetch
  - skill_workshop
---

# UI Generation

Generate React/Vue/Svelte/Angular/Web Components UI components, page layouts, design tokens, and accessibility audits using the `@elsahafy/ui-toolkit-mcp` MCP server.

Also includes a **shadcn/ui assistant** for selecting and installing official shadcn/ui components and blocks without relying on a flaky third-party MCP server.

## When to use

- User needs a UI component from a natural language description.
- Building a landing page, dashboard, form, card, navbar, etc.
- Need to audit an existing component for accessibility, performance, or responsive issues.
- Want to extract design tokens from Figma or import them from an existing design system.
- Need Storybook stories, visual regression screenshots, or responsive previews.
- Want to install official shadcn/ui components or blocks in a project.
- Need help choosing the right shadcn/ui component for a use case.

## Providers

### Component generation & audits

**@elsahafy/ui-toolkit-mcp** — 13 tools, 5 resources, 3 prompts.

Key tools:

- `generate_component` — Create a component from a description in any supported framework.
- `compose_layout` — Combine previously generated components into a full page.
- `audit_component` — Audit markup for WCAG, performance, and responsive issues.
- `auto_fix_component` — Fix common a11y/performance problems automatically.
- `import_design_tokens` / `extract_figma_styles` / `export_tokens` — Manage design tokens.
- `inspect_page` / `live_audit` / `responsive_preview` — Browser-based auditing and screenshots (requires Playwright).
- `generate_story` — Auto-generate Storybook CSF3 stories.
- `visual_diff` — Pixel-by-pixel screenshot comparison.

### shadcn/ui assistant

Helper script `scripts/shadcn-assistant.py`. No API key, no MCP server, just a lightweight CLI wrapper around `npx shadcn@latest`.

Commands:

```bash
# Check if shadcn is initialized in a project
~/.openclaw/workspace/skills/ui-generation/scripts/shadcn-assistant.py --project-dir projects/my-app --check

# List popular components/blocks
~/.openclaw/workspace/skills/ui-generation/scripts/shadcn-assistant.py --list-components
~/.openclaw/workspace/skills/ui-generation/scripts/shadcn-assistant.py --list-blocks

# Suggest components for a use case
~/.openclaw/workspace/skills/ui-generation/scripts/shadcn-assistant.py \
  --project-dir projects/my-app \
  --suggest "date picker inside a form"

# Install components (requires initialized shadcn project)
~/.openclaw/workspace/skills/ui-generation/scripts/shadcn-assistant.py \
  --project-dir projects/my-app \
  --install button card dialog

# Dry-run to preview commands
~/.openclaw/workspace/skills/ui-generation/scripts/shadcn-assistant.py \
  --project-dir projects/my-app \
  --install button card --dry-run
```

## Requirements

- Node.js
- `@elsahafy/ui-toolkit-mcp` installed via `npx`
- Playwright + Chromium for browser-based tools:
  ```bash
  npm install -g playwright
  npx playwright install chromium
  ```
- For shadcn assistant: a project initialized with `npx shadcn@latest init`.

## Helper scripts

### MCP stdio wrapper

Use `scripts/ui-toolkit-mcp.py` to call the stdio MCP server from OpenClaw:

```bash
# List tools
~/.openclaw/workspace/skills/ui-generation/scripts/ui-toolkit-mcp.py list
```

If you modify either script, run `npm test` from the workspace root before committing.

### Generate a component
~/.openclaw/workspace/skills/ui-generation/scripts/ui-toolkit-mcp.py call generate_component '{
  "description": "A responsive navbar with logo, links, and a hamburger menu",
  "framework": "react",
  "component_name": "Navbar",
  "variant": "default",
  "size": "md",
  "auto_audit": true,
  "include_styles": true,
  "responsive": true
}'

# Audit existing markup
~/.openclaw/workspace/skills/ui-generation/scripts/ui-toolkit-mcp.py call audit_component '{
  "markup": "<button>Click me</button>",
  "framework": "react",
  "categories": ["accessibility"],
  "wcag_level": "AA"
}'
```

### shadcn/ui assistant

See commands above. The script:

1. Detects the package manager/runtime (`npx`, `pnpm dlx`, `yarn dlx`, `bunx`).
2. Verifies `components.json` exists.
3. Suggests components based on a curated mapping of common UI patterns.
4. Generates the correct install command.
5. Optionally runs it.

## Workflow

1. **Clarify** — framework, component name, size, variant, style preferences.
2. **Generate** — call `generate_component` and capture the generated code.
3. **Write** — save the component and styles into the project.
4. **Audit** — run `audit_component` on the generated markup.
5. **Fix** — if critical findings, call `auto_fix_component`.
6. **Document** — optionally generate Storybook stories with `generate_story`.
7. **Log** — record prompt, component path, framework, and audit score.

## shadcn/ui workflow

1. **Check** — verify shadcn is initialized (`components.json`).
2. **Suggest** — ask the user what UI pattern they need; use `shadcn-assistant.py --suggest`.
3. **Confirm** — show the suggested components and install command.
4. **Install** — run with `--install` (or `--dry-run` first if uncertain).
5. **Use** — import the installed component in the project code.

## Best practices

- Be explicit in prompts for `generate_component`: include layout, content, behavior, and props.
- Always request `auto_audit: true` on generated components.
- Save generated components in a `components/` or `src/components/` folder.
- For shadcn: prefer installing official components over generating equivalents from scratch.
- For Figma integration, ask the user for their Figma Personal Access Token; never store it.
- Run browser tools only on public URLs; private IPs are blocked by the MCP.

## Notes

- The shadcn assistant intentionally does not use the broken `@heilgar/shadcn-ui-mcp-server` MCP server; it replicates the useful parts locally.
- Pair this skill with `design-orchestrator` for design direction before generating or installing UI.
- Pair with `image-generation` for complete visual assets + UI components workflows.
