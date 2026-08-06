# Audience Analysis

## Identify Your Reader

Before writing, answer:

1. **Who are they?** (role, experience level)
2. **What do they already know?** (assumed knowledge)
3. **What do they need?** (their goal)
4. **Where are they?** (in their workflow, emotionally)
5. **How will they read this?** (skimming, searching, learning)

## Audience Levels

### Beginner
- **Knows:** Basic programming concepts
- **Needs:** Explicit steps, no assumed knowledge
- **Style:** "First, install Node.js. You can check if it's installed by running..."
- **Avoid:** Jargon without explanation, skipping steps

### Intermediate
- **Knows:** The ecosystem, common patterns
- **Needs:** The "why" behind decisions, best practices
- **Style:** "We use Zod here instead of plain TS types because..."
- **Avoid:** Over-explaining basics, hand-holding

### Advanced
- **Knows:** Deep understanding, wants edge cases
- **Needs:** Trade-offs, performance implications, architecture
- **Style:** "This approach is O(n) but the constant factor matters because..."
- **Avoid:** Basic explanations, obvious warnings

## Writing for Multiple Levels

When you can't pick one audience:

1. **Lead with the simple version** — everyone can follow
2. **Add depth in callouts** — "For the curious: ..." or "Under the hood: ..."
3. **Link out for prerequisites** — don't derail the main flow
4. **Use progressive disclosure** — collapsible sections, "Advanced" sections at the end

## Common Mistakes

- **Assuming too much:** "Just set up OAuth" — which provider? what flow?
- **Assuming too little:** Explaining what `npm install` does to a senior dev
- **Mixing audiences mid-doc:** Switching from beginner hand-holding to advanced jargon
- **No clear goal:** Reader finishes and thinks "...ok, now what?"
