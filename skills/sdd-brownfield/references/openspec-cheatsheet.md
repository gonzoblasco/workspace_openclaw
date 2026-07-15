# OpenSpec Quick Reference

## Commands

```bash
# Initialize
npx @fission-ai/openspec init --tools none --force

# List
npx @fission-ai/openspec list --specs    # as-built specs
npx @fission-ai/openspec list             # active changes

# Validate
npx @fission-ai/openspec validate <name>  # spec or change

# Create change
npx @fission-ai/openspec new change <name>

# Status
npx @fission-ai/openspec status --change <name>

# Archive (merge delta to as-built)
npx @fission-ai/openspec archive <name> -y

# Show
npx @fission-ai/openspec show <name>
npx @fission-ai/openspec spec show <name>  # deprecated, use 'show'
```

## Spec file structure

```
openspec/
├── config.yaml
├── specs/                    # as-built
│   ├── <name>/
│   │   └── spec.md
│   └── <name>/
│       └── spec.md
└── changes/
    ├── <name>/               # active change
    │   ├── proposal.md
    │   ├── design.md
    │   ├── specs/
    │   │   └── <name>/
    │   │       └── spec.md   # delta (ADDED/MODIFIED/REMOVED)
    │   └── tasks.md
    └── archive/
        └── <date>-<name>/    # archived changes
```

## Spec template (as-built)

```markdown
# Spec: <Name>

## Purpose

<brief purpose>

## Requirements

### Requirement: <name>
<text with SHALL or MUST>

#### Scenario: <name>
- **WHEN** <condition>
- **THEN** <outcome>
- **AND** <extra>
```

## Delta spec template

```markdown
## ADDED Requirements

### Requirement: <name>
<text with SHALL or MUST>

#### Scenario: <name>
- **WHEN** <condition>
- **THEN** <outcome>

## MODIFIED Requirements

### Requirement: <existing name>
<updated text with SHALL or MUST>

#### Scenario: <all existing scenarios + new ones>
```