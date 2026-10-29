# Evidence-First Follow-up

How to answer a follow-up comment on an issue we already joined. Written 2026-10-29 from astryx #3335, where three drafts were discarded before one was published.

## Why this exists

The first draft for #3335 opened with "Thanks for laying this out" and agreed with the other contributor. It was accurate, polite, and worthless: it revalidated a conclusion the thread already had. Gonzo's correction was blunt - *"estamos comentando, no escribiendo archivos"*, *"no quiero escribir por escribir"*.

The published version did three things the first one didn't: it named **our own** earlier claim that had no mechanism, it stated **what the code does at line level**, and it left **one decision open** that only the repo owner can make.

## Before drafting: three questions

Answer all three or don't comment.

1. **What did the thread not know?** If a maintainer or contributor already said it, we add nothing by repeating it. A follow-up that resolves the thread is fine; a follow-up that restates it is noise.
2. **Does this come from the code, or from our reading of the code?** A claim from reading is not evidence. If it can be checked, check it.
3. **Who can act on it?** If the answer is "the maintainers", the comment should narrow their decision, not widen it.

## The verification ladder

Run as far down as the claim needs, and know which rung you stopped at.

| Rung | What it proves | How |
|---|---|---|
| 1. Read the source | What the code says it does | `grep -n`, read the file at the commit |
| 2. Read the history | Why it is that way | `git log -S`, the PR that introduced it |
| 3. Read the current state | Whether it still holds | `gh api`, the issue timeline, open PRs touching it |
| 4. Run the suite | That the existing behaviour is what we think | `pnpm vitest run <file>` |
| 5. Write a probe test | That **our specific claim** is right or wrong | temporary test, deleted after |
| 6. Real browser | Layout, pixels, AT behaviour | Playwright |

**Rung 5 is where claims actually break.** In #3335 two of five probes failed, and both failures were our assumptions, not the repo's: we invented a `items` prop for `TabMenu` (it is `label` + `options`), and we assumed a click opened the popover (it needs `userEvent` and `hidden: true`). Both would have shipped as confident, wrong statements in a public thread.

State which rung you stopped at. "jsdom has no layout, so this proves the mechanism, not the pixels" is a stronger comment than implying you measured pixels.

## Writing rules

- **No opener that thanks anyone for the thread.** No "great point", no "thanks for laying this out", no "worth noting".
- **No hedging verbs.** "is" not "does seem"; "that's the cost" not "that's worth considering as a cost".
- **No offer of future work** unless we intend to do it and the maintainer asked. Not "happy to open an RFC".
- **No environment detail.** The version of the package manager, a broken install, our local setup: that is our debt, not their problem. It belongs in the daily note.
- **Cite lines when the claim is about code.** `TabList.tsx:628` travels; "the component checks its children" does not.
- **One open question at most.** A comment that leaves three things undecided hasn't narrowed anything.
- **Corrections to ourselves go first.** If our earlier comment rested on something wrong, say it plainly at the top. It costs one sentence and buys the rest of the comment credibility.

## The three shapes worth publishing

1. **We were wrong, here is the mechanism.** Names our own earlier gap, closes it.
2. **This is what the code does, and it changes the options.** Line-level fact that removes one branch of the discussion.
3. **The decision splits by X.** One variable the maintainers haven't named, which turns one question into two known ones.

Anything else is likely restating the thread.

## Repo hygiene during this work

- Clone to `clones/<repo>` (gitignored), not `/tmp`, when the analysis will last more than one turn or may become an RFC.
- A temporary probe test lives inside that clone, marked `TEMPORARY probe` in the file header, and is deleted with the clone.
- Never change the clone's install or global tooling as a side effect of writing a comment. Verify first; do not "fix the environment" to make a test run and then leave it changed.
- Delete the clone once the comment is published and the session closes.

## Checklist before publishing

- [ ] Every code claim has a line or a probe behind it
- [ ] We said which rung of the ladder we stopped at
- [ ] No agreement-only paragraphs left
- [ ] No thanks, no hedges, no promised work
- [ ] One open decision, framed for the people who can decide it
- [ ] Gonzo approved the final text
