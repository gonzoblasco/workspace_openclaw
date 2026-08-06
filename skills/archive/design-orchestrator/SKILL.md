---
name: "design-orchestrator"
description: "Add design research capability via UI/UX Pro: search curated design knowledge for styles, colors, typography, patterns, and stack guidelines."
metadata:
  version: 1.2.0
  author: Kanam
  tags: ["design", "ui", "ux", "wireframes", "design-system", "frontend", "superdesign", "visual-review", "qa", "design-research"]
allowed-tools:
  - exec
  - read
  - write
  - edit
  - file_write
  - file_fetch
  - image
  - web_fetch
  - web_search
  - skill_workshop
---

# Design Orchestrator

Stop shipping AI-slop UI. This skill gives OpenClaw real design judgment so the interfaces it ships look considered, tasteful, and consistent.

It is adapted from the Superdesign methodology: instead of reaching for default component libraries, the agent reads the project context, gathers style references, sets up a design system, and produces branchable design drafts.

## When to use

- A page or component looks generic, default, or "AI-generated".
- Starting a new feature or page and needing visual direction before coding.
- Need a logo, icon, wireframe, or SVG illustration.
- Want to extract a design system from an existing site, screenshot, or reference URL.
- Want to iterate on an existing UI with structured design feedback.
- Need a responsive, accessible layout direction before implementation.
- Need to visually review a UI edit (before/after screenshots + OpenAI Vision).
- Need design research: color palettes, typography pairings, landing patterns, UX guidelines, stack-specific best practices.

## Relationship to other skills

- **`ui-generation`** (via `@elsahafy/ui-toolkit-mcp`): implements components with accessibility audits and shadcn/ui assistant.
- **`image-generation`** (via OpenAI/Gemini): produces image assets.
- **`design-orchestrator`**: decides *how things should look*, researches design knowledge, and reviews visual results.

Use them in sequence: `design-orchestrator` → `image-generation` + `ui-generation` → `design-orchestrator` (visual review).

## Design workspace

Every project that uses this skill should have a `.superdesign/` folder:

```
.superdesign/
├── design-system.md          # Active design tokens and principles
├── design_iterations/         # Draft designs (HTML/SVG/PNG)
├── design_system/             # Extracted or generated design-system JSON
├── replica_html_template/     # Lightweight HTML replicas of existing UI
└── assets/                    # Reference images, screenshots, moodboards
```

Run the helper script to bootstrap it:

```bash
~/.openclaw/workspace/skills/design-orchestrator/scripts/init-design-workspace.sh projects/my-app
```

If you modify any script in this skill, run `npm test` from the workspace root before committing.

## Workflows

### Design direction workflow

1. **Gather context** — read project files and references; ask high-signal questions about taste, constraints, audience.
2. **Research** — use `design-research.py` to find curated colors, styles, patterns, or stack guidelines relevant to the project.
3. **Set/update design system** — create or edit `.superdesign/design-system.md`.
4. **Generate design direction** — produce a spec with layout, color, typography, spacing, motion, responsive, a11y notes. Save as `.superdesign/design_iterations/<name>.md`.
5. **Produce a draft** — wireframe, UI mockup, component draft, logo, or icon. Save under `.superdesign/design_iterations/`.
6. **Iterate** — update spec and draft from user feedback.
7. **Hand off** — to `ui-generation` and/or `image-generation` for production assets.

### Visual review workflow

Use this after making a UI edit to validate it automatically.

1. **Capture before** — screenshot the page/component before the change.
2. **Apply the edit** — make the code change.
3. **Capture after** — screenshot the page/component after the change.
4. **Review** — call `scripts/visual-review.py` with both screenshots and the edit request.
5. **Iterate** — if the verdict is "no", read the explanation, fix, and repeat.

### Design research workflow

Use `scripts/design-research.py` to query UI/UX Pro's curated design knowledge:

```bash
# Search all domains
~/.openclaw/workspace/skills/design-orchestrator/scripts/design-research.py \
  --query "fintech color palette" --domain all --max 3

# Search stack-specific guidelines
~/.openclaw/workspace/skills/design-orchestrator/scripts/design-research.py \
  --query "form validation" --domain stack --stack nextjs --max 3

# Search UI styles
~/.openclaw/workspace/skills/design-orchestrator/scripts/design-research.py \
  --query "minimal dashboard" --domain styles --max 3

# Search landing patterns
~/.openclaw/workspace/skills/design-orchestrator/scripts/design-research.py \
  --query "pricing page" --domain patterns --max 3
```

The script starts a local UI/UX Pro HTTP server on port 3456 if needed, manages the MCP session, and returns ranked results. Use the returned data to inform design decisions and update `.superdesign/design-system.md`.

## Design principles (default)

Use these unless the project design system overrides them:

1. **One strong idea** — each page/component should have one clear visual hook, not ten.
2. **Restrained palette** — 1-2 accent colors; everything else is neutral.
3. **Generous whitespace** — let elements breathe; avoid cramped layouts.
4. **Intentional hierarchy** — size, weight, color, and spacing should guide the eye.
5. **System fonts by default** — use a custom typeface only when it adds real character.
6. **Accessible first** — sufficient contrast, visible focus states, semantic HTML.
7. **Motion with purpose** — only animate to clarify, never to decorate.

## Prompt templates

### Design direction

```
You are a product designer. We are designing a {page/component} for {project}.
Context: {context}
Audience: {audience}
Mood: {mood}

Produce a design spec that includes:
1. Overall layout and composition
2. Color usage (background, surface, text, accent)
3. Typography scale
4. Spacing and rhythm
5. Key interactions and motion
6. Responsive behavior
7. Accessibility considerations

Output as markdown in .superdesign/design_iterations/{name}.md
```

### Wireframe

```
Create a minimal black-and-white wireframe for {description}. Use semantic HTML and CSS. No colors, no images, only structure, hierarchy, and spacing. Save as .superdesign/design_iterations/{name}-wireframe.html
```

### Logo/icon

```
Design a {style} {logo/icon} for {brand}. Output a single, clean SVG. Use geometric shapes, avoid gradients, keep it scalable. Save as .superdesign/design_iterations/{name}.svg
```

### Design system extraction

```
Analyze the reference {URL/image/description} and extract a design system JSON with colors, typography, spacing, radius, and shadows. Save as .superdesign/design_system/{name}.json and summarize in .superdesign/design-system.md
```

### Visual review prompt (used internally by script)

```
You are a strict UI/UX reviewer. A developer was asked to make this UI edit: "{edit_request}".
You are shown two screenshots: BEFORE and AFTER.
Decide whether the AFTER screenshot visually satisfies the request.
Respond in JSON with verdict "yes" or "no" and a short explanation.
```

## Anti-patterns to avoid

- Generic card grids with no hierarchy
- Default shadcn/ui theme without customization
- Indigo-500 everywhere
- Identical padding on every element
- Decorative motion that adds no meaning
- Tiny tap targets or low contrast
- Copy-pasted hero illustrations that do not fit the brand
- UI edits that do not match the agreed design spec

## Tools

- `scripts/init-design-workspace.sh` — bootstrap `.superdesign/` in a project
- `scripts/visual-review.py` — screenshot + OpenAI Vision review of UI edits
- `scripts/design-research.py` — search UI/UX Pro curated design knowledge
- `image` — analyze reference screenshots
- `web_fetch` — extract content/style from reference URLs
- `read/write/edit` — manage design files
- `exec` — run design-related scripts or open gallery HTML

## Notes

- This skill does not replace human designers. It accelerates early design direction and keeps AI-generated UI from looking default.
- Always show the user the design spec or draft before implementing.
- Pair with `ui-generation` and `image-generation` for end-to-end design-to-code.
- Keep reference images and moodboards in `.superdesign/assets/`.
- Visual review depends on Playwright and a valid OpenAI API key; keep keys outside the workspace.
- Design research depends on `ui-ux-pro-mcp` running via `npx`; no API key required.
