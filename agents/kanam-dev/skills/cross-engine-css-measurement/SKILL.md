---
name: "cross-engine-css-measurement"
metadata:
  category: "Engineering"
  tags:
    - css
    - browser
    - webkit
    - chromium
    - firefox
    - layout
    - measurement
    - regression
description: "'Works in Chrome, fails in WebKit' CSS: isolate the cause with minimal probes, an A/B against the previous commit, and a per-engine browser matrix."
user-invocable: false
---

# Workflow: Cross-Engine CSS Measurement

## Purpose

Find the exact cause when a CSS declaration behaves differently across browser engines. The deliverable is a measured cause, the fix, and the list of engines that were actually verified.

This is not "try values until it looks right". A property can behave identically in three of your probes and still fail in the real component, because the difference lives in the geometry, the element type, or the engine.

## When to use it

- "It works in Chrome, it fails in WebKit/Safari" (or the reverse).
- A browser test suite fails on one engine while passing on another.
- A CSS feature behaves inconsistently: anchor positioning, container queries, `:has`, logical properties, `inset` versus longhands.
- Before claiming a CSS feature works, to state which engines were measured.

## Steps

1. **Name the engine and the failing assertion before touching code.** Read the failing job's log and quote the assertion: which engine, which test, expected versus received. On a suite that runs several engines, a failure in one engine with a pass in another is a real difference, not flakiness. Completion: you can state "engine X, assertion Y, expected A, got B".

2. **Reproduce with the real component geometry.** A synthetic host with a fixed size hides the bug. Verified 2026-09-24 on adobe/react-spectrum: a probe with `200x44` hosts passed in *every* variant on both engines, while the real component failed. The real host was a static `label` with a natural, content-driven size. Copy the nesting chain too (outer element > wrapper > control), not just the styles. Completion: a probe whose host geometry matches the component reproduces the failure.

3. **Isolate one variable per probe.** Change exactly one declaration between variants and keep everything else identical. A probe that varies two things at once proves nothing about which one caused the difference. Verified 2026-09-24: the change had two candidate causes (the `inset` shorthand versus the `var()` name); a probe matrix that varied each independently showed the `var()` resolved correctly on both engines and the shorthand did not size the control. Completion: each variant differs from its neighbour by one declaration.

4. **Match the element type, including replaced controls.** A replaced control (`input type=checkbox`, `type=radio`, `select`) carries an intrinsic size that a text input does not. Verified 2026-09-24 on WebKit 26: `input type=checkbox` with `inset` only stayed at its intrinsic `12x12` box and covered none of the component, while `input type=text` stretched correctly with the same declarations. Chromium stretched both. Using a text input as the stand-in for a checkbox would have hidden the bug. Completion: the probe uses the same element type (and `type` attribute) as the component.

5. **A/B against the previous commit. This is the decisive step.** Before believing the test is flaky or the assertion is too strict, check out the previous revision's sources into the current tree and run the OLD test against the OLD code:
   ```bash
   git checkout <base-sha> -- <source paths>
   cp <old test> <test path>.bak   # old test from the same sha
   # run it; then restore with: git checkout HEAD -- <paths>
   ```
   Verified 2026-09-24: old code + old test passed WebKit 4/4, new code failed. That single experiment converted "maybe the test is fragile" into "we introduced a regression", which are opposite fixes. Without it, the tempting conclusion was to loosen the assertion and ship the bug. Completion: the A/B result names which side changed behaviour.

6. **Run the engine matrix the repo's CI runs.** A green local run on one engine is evidence about that engine only. On react-spectrum the CI `test-browser` job runs chromium, firefox and webkit; verifying locally on chromium alone passed 6/6 while CI failed on webkit (6 tests) and firefox (1). Read the CI config for the engine list, and scope local runs to engines you have installed with `--browser=<engine>` (engine) or `--project=<instance>` (instance name) - an engine name in `--project` empties the config and errors. Completion: a run per engine in the CI set, or an explicit statement of which engines are unverified.

7. **Wait at least a frame before reading layout for anchor or position work.** The compositor recomputes anchor and positioned elements, so `getBoundingClientRect()` in the same tick returns stale values. Verified 2026-09-24: a positioned element measured synchronously after `scrollTop = 40` read as 40px off, and returned to 0 after about 50ms - in headless and in real Chrome. That false reading was reported as a scroll bug before re-measuring. Wait with `requestAnimationFrame` twice or about 50ms. Completion: the measurement is taken after a frame, not in the same tick as the mutation.

8. **Provision an engine with the workspace script when the installer stalls.** `scripts/playwright-provision.sh <engine> [--repo <dir>]` reads the download URL from `--dry-run`, fetches the zip with `curl`, unpacks it into the cache, and writes both `INSTALLATION_COMPLETE` and `DEPENDENCIES_VALIDATED`. It is idempotent and repairs a build that is incomplete on disk. Both markers matter: a complete build without them is deleted by the next `playwright install` of any engine. Completion: the script prints `LISTO` and the engine binary answers `--version`.

## Decision rules

- **The A/B in step 5 outranks intuition.** "The test looks too strict" and "we broke it" need opposite fixes; only the old-code run separates them.
- **A single-engine run is scoped evidence.** Never report "browser tests pass" from one engine when CI runs more. Name the engines.
- **A capability that does not exist on an engine cannot be compared there.** Assertions about a declaration belong inside the support guard (`if (CSS.supports(...))`); outside it, an unsupported engine drops the declaration and the comparison fails for the wrong reason.
- **When the fix is "add the other declaration", say both.** Verified case: `inset` positions anchor elements but does not size a replaced control, so the fix needed `inset` for offsets *and* `width`/`height: anchor-size()` for size. Keep the declaration whose reason was directional (`inset` is RTL-correct) and add the one whose reason was sizing.
- Record the measured numbers in the test comment or the commit body. A number (`12x12`, `-208px`, `8x6px larger`) survives review; "looked wrong in Safari" does not.

## Evidence

Verified 2026-09-24 on adobe/react-spectrum PR #10517 (RAC Checkbox/Radio hidden input, CSS anchor positioning). Working probes: `docs/test-assets/pr-10517-probes/` in the workspace (sizing matrix, element-type isolation, geometry replication, override paths, scroll timing). Full narrative: `docs/prs/PR-10517-REACT-SPECTRUM-PLAN.md`.

## Related

- `scripts/playwright-provision.sh` (step 8)
- `oss-pr-verification` (the OSS PR verification phase; its browser provisioning reference)
- `browser-testing-with-devtools` (performance measurement, a different question)
