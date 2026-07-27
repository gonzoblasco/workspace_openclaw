# Explanation Patterns

## The Socratic Method

Instead of giving the answer, ask questions that lead to it:

1. **Clarify:** "What do you expect this line to do?"
2. **Observe:** "What is it actually doing?"
3. **Hypothesize:** "What would happen if we changed X?"
4. **Test:** "Let's try it and see."
5. **Reflect:** "Why did that work? What did we learn?"

## The Analogy Bridge

Map unfamiliar concepts to familiar ones:

- "React components are like functions: props in, JSX out."
- "useEffect is like a subscription: you set it up and clean it up."
- "TypeScript generics are like function parameters for types."

## The Progressive Disclosure

Start simple, add complexity only when needed:

1. **Minimal working example** — the simplest version that runs
2. **Add one concept** — explain the why before the how
3. **Show the edge case** — what breaks, and why
4. **The real-world version** — with error handling, types, tests

## The Before/After Pattern

Show the problem, then the solution:

```ts
// ❌ Problem: ...
const bad = ...

// ✅ Solution: ...
const good = ...
```

Always explain *why* the "after" is better, not just that it is.

## The Mistake-Driven Lesson

Let them make the mistake, then explore it:

1. "Try running this. What happens?"
2. "That error is telling us..."
3. "Here's why it happens..."
4. "Here's how we fix it..."

## When to Give the Answer

- They've been stuck for 5+ minutes
- They're clearly frustrated
- The concept is genuinely new (no prior knowledge to build on)
- They explicitly ask for the answer

Even then, explain the *why*, not just the *what*.
