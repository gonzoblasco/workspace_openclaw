# Accessibility Code Audit: Kanam's Solitaires

**Project:** kanam-solitaires (Vite, 4 solitaire games)  
**Audit Date:** 2026-08-04  
**Auditor:** A11y Code Audit Agent  
**Lighthouse Score:** 100 (Accessibility)

---

## Executive Summary

The project demonstrates **strong foundational accessibility** with excellent semantic HTML structure, comprehensive ARIA labeling, live region announcements, and keyboard support. The Lighthouse score of 100 is **justified for automated checks**.

However, manual code review reveals **several issues that Lighthouse cannot detect**, particularly around focus management, keyboard navigation, and information conveyed through visual states alone.

**Total Findings:** 14 issues
- **Critical:** 2
- **Major:** 5
- **Minor:** 7

---

## Findings

### Critical Issues

#### 1. Focus Not Restored After Modal Close

**Severity:** Critical  
**Location:** `src/lib/modal.js:73-75`, `src/main.js:179-182`  
**Description:** When modals (sound settings, stats, help, new game confirmation) are closed, focus is not returned to the triggering element. This disorients keyboard and screen reader users, leaving them unsure where focus went.

**Current behavior:**
```javascript
// Modal closes but focus stays on last focused element inside modal
// or is lost entirely when overlay is removed from DOM
overlay.remove();
```

**Suggested fix:**
```javascript
// Store reference to trigger element before opening modal
const previouslyFocused = document.activeElement;

// On close, restore focus
setTimeout(() => {
  overlay.remove();
  soundToggle.setAttribute('aria-expanded', 'false');
  previouslyFocused?.focus(); // Return focus to trigger
}, 200);
```

**Impact:** Screen reader users lose context; keyboard users must manually tab through the entire page to find their place.

---

#### 2. No Keyboard Trap Prevention in Modals

**Severity:** Critical  
**Location:** `src/lib/modal.js:66-71`, `src/main.js:170-175`  
**Description:** Modals do not implement focus trapping. Users can tab outside the modal into the background content, creating a keyboard trap where they cannot easily return to the modal.

**Current behavior:**
```javascript
// Only Escape key is handled
document.addEventListener('keydown', function handler(e) {
  if (e.key === 'Escape') {
    close();
  }
});
// Tab key is not intercepted
```

**Suggested fix:**
```javascript
// Implement focus trap
const focusableElements = box.querySelectorAll(
  'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
);
const firstEl = focusableElements[0];
const lastEl = focusableElements[focusableElements.length - 1];

document.addEventListener('keydown', function handler(e) {
  if (e.key === 'Escape') {
    close();
    return;
  }
  
  if (e.key === 'Tab') {
    if (e.shiftKey && document.activeElement === firstEl) {
      e.preventDefault();
      lastEl.focus();
    } else if (!e.shiftKey && document.activeElement === lastEl) {
      e.preventDefault();
      firstEl.focus();
    }
  }
});
```

**Impact:** Keyboard users can become trapped or lose access to modal controls.

---

### Major Issues

#### 3. Cards Lack Keyboard Activation Beyond Click Simulation

**Severity:** Major  
**Location:** `src/main.js:133-143`, `src/lib/dom.js:12-16`  
**Description:** While cards have `role="button"` and `tabindex="0"`, the keyboard handler only simulates a click. Card interactions (drag-to-move, double-click auto-move) have **no keyboard equivalent**. Screen reader users cannot perform complex moves.

**Current behavior:**
```javascript
// Only basic click simulation
if (e.key !== 'Enter' && e.key !== ' ') return;
active.click();
```

**Suggested fix:**
- Implement keyboard shortcuts for common actions (e.g., arrow keys to navigate between piles, 'M' to move selected card)
- Add a "selection mode" activated by Enter/Space, then arrow keys to choose destination, Enter to confirm
- Provide keyboard-only instructions in the Help modal

**Impact:** Screen reader and motor-impaired users cannot fully play the game.

---

#### 4. Drag-and-Drop Has No Keyboard Alternative

**Severity:** Major  
**Location:** All renderer files (`klondike/renderer.js:245-260`, `spider/renderer.js:189-203`, `freecell/renderer.js:233-247`)  
**Description:** All games rely heavily on drag-and-drop for card movement. There is **no keyboard-accessible alternative mechanism** for moving cards between piles.

**Current behavior:**
```javascript
cardEl.draggable = true;
cardEl.addEventListener('dragstart', (e) => ...);
// No keyboard equivalent exists
```

**Suggested fix:**
- Implement "pick up / put down" pattern:
  1. User tabs to card, presses Space to "pick up"
  2. Arrow keys cycle through valid drop targets
  3. Press Space again to "put down"
  4. Press Escape to cancel
- Announce available moves via live region when a card is picked up
- Visual indicator showing which card is "held"

**Impact:** Users who cannot use a mouse (motor impairments, screen readers) cannot move cards.

---

#### 5. Selected State Conveyed Only by Color + Border

**Severity:** Major  
**Location:** `src/styles/base.css:268-270`, `src/games/pyramid/renderer.js:92-94`  
**Description:** Selected cards use a golden border/shadow (`--color-selected: rgba(255, 200, 50, 0.4)`). While this meets contrast requirements, the **state change relies heavily on color**. Users with color vision deficiency may miss it.

**Current behavior:**
```css
.card.selected {
  box-shadow: 0 0 0 3px var(--color-selected), 0 4px 12px rgba(0, 0, 0, 0.4);
}
```

**Suggested fix:**
- Add a visible icon/indicator (e.g., checkmark ✓ in corner)
- Add slight vertical offset (`transform: translateY(-8px)`)
- Ensure the border has sufficient non-color contrast (already present with 3px width)
- Announce selection state via aria-live region (partially implemented in Pyramid)

**Impact:** Users with color blindness may not notice which cards are selected.

---

#### 6. Hint Highlights Use Color Alone

**Severity:** Major  
**Location:** `src/styles/base.css:286-299`, all `showHint()` functions  
**Description:** Hint highlights use a golden pulse animation. While animated, this **relies on color perception** to distinguish hinted cards from others.

**Current behavior:**
```css
.card.hint-source {
  box-shadow: 0 0 0 3px var(--color-gold), 0 0 12px rgba(212, 160, 23, 0.5);
  animation: hintPulse 1s ease-in-out infinite;
}
```

**Suggested fix:**
- Add a text label or icon overlay ("HINT" badge)
- Increase the pulse amplitude for better visibility
- Announce hints via the live announcer: "Hint: Move King of Hearts to Column 3"

**Impact:** Users with low vision or color blindness may miss hint indicators.

---

#### 7. Game Options Lack Accessible Labels

**Severity:** Major  
**Location:** `src/main.js:66-78`  
**Description:** The mode selector buttons (Draw mode, Scoring mode) have visual labels but **no programmatic association** between the label and the button group.

**Current behavior:**
```html
<div class="mode-group">
  <span class="mode-label">Draw</span>
  <button class="mode-btn">1</button>
  <button class="mode-btn active">3</button>
</div>
```

**Suggested fix:**
```html
<div class="mode-group" role="group" aria-labelledby="draw-mode-label">
  <span id="draw-mode-label" class="mode-label">Draw</span>
  <button class="mode-btn" aria-pressed="false">1</button>
  <button class="mode-btn active" aria-pressed="true">3</button>
</div>
```

**Impact:** Screen reader users hear "1, button" without context about what the number means.

---

### Minor Issues

#### 8. Skip Link Target Exists But May Not Be First Focusable

**Severity:** Minor  
**Location:** `index.html:35`, `index.html:38-41`  
**Description:** Skip link exists (`#game-container`) but the game nav buttons appear before the main content in tab order. The skip link target should be the first interactive element in the main region.

**Suggested fix:**
- Ensure `#game-container` receives focus properly: add `tabindex="-1"` to make it programmatically focusable
- Verify that focus lands on the first game control, not just the container div

```html
<main id="game-container" aria-label="Game board" tabindex="-1"></main>
```

**Impact:** Keyboard users using skip link may still need to tab through header navigation.

---

#### 9. Timer Updates Not Announced

**Severity:** Minor  
**Location:** All renderer files (e.g., `klondike/renderer.js:85-87`)  
**Description:** Timer display updates every second but uses `aria-live="off"`. While this prevents announcement spam, blind users have **no way to know elapsed time**.

**Current behavior:**
```html
<span>⏱ <span id="timer-display" aria-live="off">00:00</span></span>
```

**Suggested fix:**
- Add a keyboard shortcut (e.g., 'T') to announce current time
- Or announce at milestones (every 5 minutes, or on game win)

```javascript
// On 'T' key press
announce(`Elapsed time: ${formatTime(state.elapsed)}`);
```

**Impact:** Blind users cannot track game duration independently.

---

#### 10. Stock Pile Empty State Label Could Be Clearer

**Severity:** Minor  
**Location:** `klondike/renderer.js:169-176`, similar in other games  
**Description:** Empty stock shows "↻" symbol. While the parent has an aria-label, the refresh symbol itself has no text alternative.

**Suggested fix:**
```html
<div class="stock-empty" aria-label="Click to reshuffle waste into stock">↻</div>
```

**Impact:** Screen reader users may not understand the purpose of the circular arrow.

---

#### 11. Foundation Piles Don't Announce Completed Runs

**Severity:** Minor  
**Location:** All foundation drop handlers  
**Description:** When a full suit sequence is completed in Spider or Klondike, there's **no specific announcement** distinguishing it from a regular move.

**Suggested fix:**
```javascript
if (isFoundationComplete(state, index)) {
  announce(`Foundation complete: ${suitName} sequence finished!`);
  playVictory(); // Already done
}
```

**Impact:** Screen reader users miss the成就感 of completing a foundation.

---

#### 12. Confetti Animation May Trigger Vestibular Disorders

**Severity:** Minor  
**Location:** `src/styles/base.css:510-524`, all renderer win handlers  
**Description:** Confetti uses falling animation with rotation. While `prefers-reduced-motion` is respected globally, the confetti container itself doesn't check this preference before spawning.

**Current behavior:**
```javascript
function spawnConfetti() {
  // Creates 40 animated pieces unconditionally
}
```

**Suggested fix:**
```javascript
function spawnConfetti() {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) return; // Skip confetti
  
  // ... existing confetti code
}
```

**Impact:** Users with vestibular disorders may experience discomfort despite system preferences.

---

#### 13. Stats Table Header Scope Not Defined

**Severity:** Minor  
**Location:** All `showStatsPanel()` functions  
**Description:** Stats table uses `<th>` elements without `scope` attribute, which helps screen readers associate headers with cells.

**Current behavior:**
```html
<th>Mode</th><th>Played</th><th>Won</th>...
```

**Suggested fix:**
```html
<th scope="col">Mode</th><th scope="col">Played</th><th scope="col">Won</th>...
```

**Impact:** Screen readers may not clearly communicate which column each cell belongs to.

---

#### 14. SVG Suit Icons Have Redundant role="img"

**Severity:** Minor  
**Location:** `src/lib/suits.js:6-34`  
**Description:** SVGs have `role="img"` but also `aria-hidden="true"`, which is contradictory. Since the card's aria-label already describes the suit, the SVG should simply be hidden.

**Current behavior:**
```svg
<svg ... aria-hidden="true" focusable="false" role="img">
```

**Suggested fix:**
```svg
<svg ... aria-hidden="true" focusable="false">
<!-- Remove role="img" since it's decorative -->
```

**Impact:** Minor confusion for assistive technology parsing redundant roles.

---

## Strengths Identified

The following accessibility implementations are **excellent** and should be maintained:

✅ **Semantic HTML Structure**
- Proper use of `<main>`, `<header>`, `<nav>`
- Correct heading hierarchy (`h1` for title, `h2` for modals)
- Skip link implemented

✅ **ARIA Live Regions**
- Global announcer (`#announcer`) for game state changes
- Strategic use of `aria-live="polite"` and `aria-atomic="true"`
- Score bar updates announced appropriately

✅ **Card Accessibility**
- Every card has descriptive `aria-label` (e.g., "King of Spades, column 1")
- Face-down cards labeled as such
- Cards are keyboard-focusable with `tabindex="0"`

✅ **Focus Styles**
- Visible focus indicators with gold outline (`outline: 3px solid var(--color-gold-light)`)
- `:focus-visible` used appropriately
- High contrast focus rings

✅ **Reduced Motion Support**
- Global `@media (prefers-reduced-motion: reduce)` query
- Animations reduced to 0.01ms

✅ **Modal Accessibility**
- `role="dialog"` and `aria-modal="true"` on overlays
- `aria-labelledby` pointing to modal title
- Escape key closes modals

✅ **Color Contrast**
- Text colors meet WCAG AA standards
- Gold accent color (`#d4a017`) on dark background has sufficient contrast

---

## Recommendations Priority

### Immediate (Before Next Release)
1. ✅ Fix focus restoration after modal close (#1)
2. ✅ Implement focus trapping in modals (#2)
3. ✅ Add keyboard alternative for drag-and-drop (#4)

### Short-Term (Next Sprint)
4. ✅ Enhance keyboard interaction model for cards (#3)
5. ✅ Add non-color indicators for selected state (#5)
6. ✅ Improve hint accessibility (#6)
7. ✅ Add aria-pressed to mode selector buttons (#7)

### Medium-Term (Backlog)
8. ✅ Skip link target refinement (#8)
9. ✅ Time announcement shortcut (#9)
10. ✅ Empty stock label improvement (#10)
11. ✅ Foundation completion announcements (#11)
12. ✅ Confetti reduced-motion check (#12)
13. ✅ Stats table scope attributes (#13)
14. ✅ Clean up SVG roles (#14)

---

## Conclusion

The Lighthouse score of 100 accurately reflects **automated accessibility checks**, but manual review reveals gaps that require human judgment to detect. The most critical issues involve **keyboard accessibility** and **focus management**—areas where automated tools have limited coverage.

The development team has demonstrated strong accessibility awareness. With the fixes outlined above, this project can achieve **genuine accessibility excellence** beyond automated scores.

**Overall Assessment:** Good foundation, needs keyboard interaction improvements to be truly accessible.

---

*Generated by A11y Code Audit Agent*
