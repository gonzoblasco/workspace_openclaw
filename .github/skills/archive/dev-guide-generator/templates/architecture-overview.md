# Architecture Overview Template

# {{Project Name}} — Architecture

> {{One-line summary of the architecture}}

## Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Server    │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | {{tech}} | {{reason}} |
| Backend | {{tech}} | {{reason}} |
| Database | {{tech}} | {{reason}} |
| Hosting | {{tech}} | {{reason}} |

## Directory Structure

```
{{project}}/
├── src/
│   ├── app/        # {{purpose}}
│   ├── components/ # {{purpose}}
│   └── lib/        # {{purpose}}
├── public/         # {{purpose}}
└── package.json
```

## Key Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| {{decision}} | {{why}} | {{alternatives}} |

## Data Flow

1. {{Step 1}}
2. {{Step 2}}
3. {{Step 3}}

## Deployment

- **Hosting:** {{platform}}
- **CI/CD:** {{tool}}
- **Environments:** {{list}}
