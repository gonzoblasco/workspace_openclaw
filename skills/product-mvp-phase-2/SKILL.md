# product-mvp-phase-2 Skill

## Purpose
Close Phase 2 MVP development with documentation closure (BRIEF, ROADMAP, ADRs) + git commit + memory file update.

## Trigger Condition
Project has:
1. Scaffold base created (Phase 1 complete)
2. MVP features in progress or complete
3. Technical decisions documented but not yet committed to product memory

## Phase Stages

### Stage 0: Intake / Diagnosis
Input: Project state snapshot - Current scaffold files listed, Feature list with status, Tech stack selection (local/cloud)
Output: Initial diagnosis report

### Stage 1: Foundation Closure
Using tee or echo for safe file writing:
echo '# Product BRIEF' > PROJECT/docs/BRIEF.md
echo '## Vision' >> PROJECT/docs/BRIEF.md
echo '<product-purpose>' >> PROJECT/docs/BRIEF.md
echo '' >> PROJECT/docs/BRIEF.md
echo '## Current State Phase 2' >> PROJECT/docs/BRIEF.md
echo '- Scaffold base completed' >> PROJECT/docs/BRIEF.md
echo '- MVP features listed' >> PROJECT/docs/BRIEF.md

Why: Establishes baseline before building Phase 3+ features.

### Stage 2: Roadmap Planning
Using tee or echo for safe file writing:
echo '# PRODUCT ROADMAP' > PROJECT/docs/ROADMAP.md
echo '## Phase 1 Foundation Completed' >> PROJECT/docs/ROADMAP.md
echo '- Scaffold with Biome build system' >> PROJECT/docs/ROADMAP.md
echo '- Basic editor with localStorage' >> PROJECT/docs/ROADMAP.md
echo '- AI streaming integration' >> PROJECT/docs/ROADMAP.md

Why: Makes future progress visible and measurable.

### Stage 3: Decision Recording ADRs
Using tee or echo for safe file writing:
echo '# ADR NUMBER: TECHNICAL DECISION TITLE' > PROJECT/docs/ADR_001.md
echo '## Context' >> PROJECT/docs/ADR_001.md
echo '<problem or situation>' >> PROJECT/docs/ADR_001.md
echo '' >> PROJECT/docs/ADR_001.md
echo '## Decision' >> PROJECT/docs/ADR_001.md
echo '<decision made>' >> PROJECT/docs/ADR_001.md

Why: Documents WHY we made decisions, not just WHAT.

### Stage 4: Memory Closure
Using tee or echo for safe file writing:
echo '# DAY DATE: PHASE 2 CLOSURE SUMMARY' > MEMORY/YYYY-MM-DD.md
echo '## Key Learnings' >> MEMORY/YYYY-MM-DD.md
echo '- Local models beat cloud APIs for MVP (cost + latency)' >> MEMORY/YYYY-MM-DD.md
echo '- OpenSpec docs guide decisions, serve as go/no-go gates' >> MEMORY/YYYY-MM-DD.md

Why: Preserves knowledge across sessions when context is lost.

## Complete Workflow

Step 0: Verify project state
cd PROJECT_PATH
ls -la docs/
git status

Step 1: Create BRIEF 5 min
echo 'Vision <purpose>' > docs/BRIEF.md
echo 'Current <achievements>' >> docs/BRIEF.md
Why: Establishes baseline before moving forward.

Step 2: Build ROADMAP 10 min
echo 'Phase 1 <completed> Phase 2 <current> Phase 3 <pending>' > docs/ROADMAP.md
Why: Makes progress visible and measurable over time.

Step 3: Document ADRs 15 min each per decision
echo 'Context <problem> Decision <choice> Reasoning <trade-offs>' > docs/ADR_N.md
Why: Documents WHY, not just WHAT. Team handoff clear.

Step 4: Commit & Push 5 min
cd PROJECT_PATH
git add docs/
git commit -m "Phase 2 closure: BRIEF+ROADMAP+ADRs complete"
git push
Why: Makes decisions permanent and traceable in history.

Step 5: Memory File Update 10 min
echo 'Key learnings' > MEMORY/YYYY-MM-DD.md
echo 'Skills created today' >> MEMORY/YYYY-MM-DD.md
echo 'Next session guidance' >> MEMORY/YYYY-MM-DD.md
Why: Preserves knowledge across session boundaries and model changes.

## Usage Examples

Example 2: Sprint Closure Without Model Loss
Scenario: User switches from qwen3.5 to deepseek-v4 model
Using echo for safe writing:
echo '# ADR 002: MODEL MIGRATION' > PROJECT/docs/ADR_002.md
echo '## Context Previous local decision New hardware upgrade' >> PROJECT/docs/ADR_002.md
echo '## Decision Migrate to deepseek-v4-flash int4 10B context' >> PROJECT/docs/ADR_002.md

Example 3: Day Closure Without Model Loss
Scenario: 4-day sprint with Phase 1 complete
Using echo for safe writing:
echo 'Day 18: Sprint Completion ACHIEVED' > MEMORY/2026-07-18.md
echo 'Achievements Scaffold base Ollama integration Editor tabs' >> MEMORY/2026-07-18.md
echo 'Skills Created Local AI pattern MVP closure memory file' >> MEMORY/2026-07-18.md

## Safety Rules

Rule 1: NEVER use heredocs with backticks or code blocks
Reason: Shell parser terminates heredoc early, losing content after first ```

Example that fails:
cat > file.sh << EOF
\`\`\`bash
curl http://localhost:11434/api/generate
\`\`\`
EOF

Rule 2: ALWAYS use echo or tee for scripts with code
Reason: Shell handles it correctly without parsing issues

Example that works:
echo '#!/bin/bash' > script.sh
echo 'curl http://localhost:11434/api/generate' >> script.sh

OR write in editor then:
cat > script.sh << SHELL
# Shell-only content, no backticks
SHELL

Rule 3: ALWAYS document BEFORE coding ADRs first
Reason: Decisions guide implementation and make team handoffs clear

## Related Skills

- product-mvp-phase-1: Scaffold + basic features creation
- ai-local-dev: Local AI model integration without cloud costs
- security-audit: Security gates for ADR decisions
