# BRIEF — Full-Stack Web Development with GraphQL and React (2nd Edition)

**Book:** Full-Stack Web Development with GraphQL and React - Second Edition
**Author:** Sebastian Grebe
**Publisher:** Packt Publishing
**Start date:** 2026-08-05
**Status:** 🟢 Active

## Objective

Process the book chapter by chapter, extracting concepts, updating deprecated patterns to modern best practices (August 2026), implementing exercises, and documenting everything in ADRs and project artifacts.

## Approach

- Each chapter produces: notes, code exercises (updated to LTS/modern), and ADRs for generalizable patterns
- ADRs worth sharing globally are extracted to the workspace-level ADR collection
- Deprecated packages/patterns are replaced with current LTS equivalents
- Theoretical chapters produce concept notes + pattern updates, not code

## Stack (book baseline, subject to update)

- **Frontend:** React (version TBD per chapter)
- **Backend:** Node.js + GraphQL
- **Database:** TBD per chapter
- **Current LTS:** Node.js 22.x (as of Aug 2026)

## Project Structure

```
projects/fullstack-graphql-react/
├── .knowledge/          # Project documentation
│   ├── BRIEF.md         # This file
│   ├── STATUS.md        # Progress tracker
│   ├── ROADMAP.md       # Chapter roadmap
│   ├── LEARNINGS.md     # Cross-chapter learnings
│   └── ADR-*.md         # Architecture Decision Records
├── chapter-01/          # Code exercises per chapter
├── chapter-02/
└── ...
```

## Deliverables

1. Per-chapter: notes + code (where applicable) + ADRs
2. Global ADRs extracted to workspace docs
3. Working application(s) built incrementally
4. LEARNINGS.md with cross-cutting insights
