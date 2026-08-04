# Accessibility Code Audit: Daily Ink

**Project:** daily-ink (Vite + vanilla TS, PWA)  
**Audit Date:** 2026-08-04  
**Location:** `/Users/gonzoblasco/.openclaw/workspace/projects/daily-ink`  
**Auditor:** A11y Code Audit Agent

---

## Executive Summary

Daily Ink is a well-structured writing PWA with solid foundational accessibility. The app uses semantic HTML elements appropriately and has good keyboard navigation structure. However, there are **critical color contrast issues** in dark mode, missing focus indicators, and several ARIA enhancements needed for screen reader users.

**Total Findings:** 14  
- 🔴 **Critical:** 3
- 🟠 **Major:** 7
- 🟡 **Minor:** 4

---

## Findings

### 🔴 Critical Issues

#### 1. Color Contrast - Install Hint Button Text
- **Severity:** Critical
- **Location:** `src/style.css:258`
- **Description:** White text (`#ffffff`) on transparent background with white border (`1px solid white`) in install hint button. In light mode with `--accent: #d97a7a` (light red), this creates insufficient contrast. The button text fails WCAG AA requirements (needs 4.5:1 for normal text).
- **Current CSS:**
  ```css
  .install-hint button {
    background: transparent;
    border: 1px solid white;
    color: white;
  }
  ```
- **Suggestion:** Use a high-contrast color for the button text and border. Consider:
  ```css
  .install-hint button {
    background: white;
    color: var(--accent);
    border: 1px solid white;
  }
  ```
  Or ensure the accent color is dark enough: `--accent: #8b2a2a` minimum for dark mode.

#### 2. Color Contrast - Install Hint Span Text
- **Severity:** Critical
- **Location:** `src/style.css:240-241`
- **Description:** White text on `var(--accent)` background. In light mode, `--accent: #d97a7a` (light red) with white text (#ffffff) yields a contrast ratio of approximately **2.8:1**, failing WCAG AA (requires 4.5:1 for normal text, 3:1 for large text). This is borderline even for large text.
- **Current CSS:**
  ```css
  .install-hint {
    background: var(--accent);
    color: white;
  }
  ```
- **Suggestion:** Either darken the accent color or use a darker text color:
  ```css
  .install-hint {
    background: var(--accent);
    color: #1a1a1a; /* Dark text for better contrast */
  }
  ```
  Or update the accent variable to meet contrast requirements: `--accent: #c14b4b` → `--accent: #8b2a2a`.

#### 3. Missing Focus Indicators
- **Severity:** Critical
- **Location:** `src/style.css` (global)
- **Description:** No `:focus` or `:focus-visible` styles defined for interactive elements (buttons, textarea). Users navigating via keyboard will have no visual indication of which element is focused. This is a WCAG 2.4.7 violation.
- **Affected Elements:** All buttons (`#save-btn`, `#export-btn`, `#history-toggle`, history item buttons, `#install-btn`), textarea (`#editor`)
- **Suggestion:** Add global focus styles:
  ```css
  :focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
  
  button:focus-visible,
  textarea:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
  ```

---

### 🟠 Major Issues

#### 4. Missing ARIA Labels for Icon-Only Buttons
- **Severity:** Major
- **Location:** `src/app.ts:174-177`
- **Description:** History item action buttons ("Export", "Delete") lack accessible names. Screen readers will only announce "button" without context of what they export/delete.
- **Code:**
  ```typescript
  <button data-action="export" data-id="${e.id}">Export</button>
  <button data-action="delete" data-id="${e.id}">Delete</button>
  ```
- **Suggestion:** Add `aria-label` with date context:
  ```typescript
  <button 
    data-action="export" 
    data-id="${e.id}"
    aria-label="Export entry from ${formatDate(e.date)}"
  >Export</button>
  <button 
    data-action="delete" 
    data-id="${e.id}"
    aria-label="Delete entry from ${formatDate(e.date)}"
  >Delete</button>
  ```

#### 5. Missing Live Region for Save Status
- **Severity:** Major
- **Location:** `src/app.ts:48, 85-89`
- **Description:** The save status span (`#save-status`) updates dynamically ("Draft…", "Draft saved", "Saved ✓") but lacks `aria-live` attribute. Screen reader users won't be notified of status changes.
- **Code:**
  ```html
  <span id="save-status"></span>
  ```
- **Suggestion:** Add `aria-live="polite"` and `role="status"`:
  ```html
  <span id="save-status" aria-live="polite" role="status"></span>
  ```

#### 6. Missing ARIA for History Toggle State
- **Severity:** Major
- **Location:** `src/app.ts:49-51, 138-143`
- **Description:** The history toggle button changes state (Show/Hide) but doesn't communicate expanded/collapsed state to assistive technologies via `aria-expanded`.
- **Code:**
  ```html
  <button class="history-toggle" id="history-toggle" type="button">
    Show past entries (<span id="entry-count">0</span>)
  </button>
  ```
- **Suggestion:** Add `aria-expanded` and toggle it:
  ```html
  <button 
    class="history-toggle" 
    id="history-toggle" 
    type="button"
    aria-expanded="false"
  >
    Show past entries (<span id="entry-count">0</span>)
  </button>
  ```
  ```typescript
  historyToggle.addEventListener('click', () => {
    const expanded = historyList.style.display === 'block';
    historyList.style.display = expanded ? 'none' : 'block';
    historyToggle.setAttribute('aria-expanded', String(!expanded));
    // ... rest of code
  });
  ```

#### 7. Heading Hierarchy Issue
- **Severity:** Major
- **Location:** `index.html:12, src/app.ts:24`
- **Description:** Only one `<h1>` exists ("Daily Ink"), which is correct. However, history items use `<strong>` instead of proper heading structure (`<h2>` or `<h3>`) for entry dates, making navigation difficult for screen reader users who navigate by headings.
- **Code:**
  ```typescript
  <article class="history-item" data-id="${e.id}">
    <header>
      <strong>${formatDate(e.date)}</strong>
      ...
    </header>
  </article>
  ```
- **Suggestion:** Use proper heading levels:
  ```typescript
  <article class="history-item" data-id="${e.id}">
    <header>
      <h2>${formatDate(e.date)}</h2>
      <time>${new Date(e.createdAt).toLocaleTimeString(...)}
      </time>
    </header>
    ...
  </article>
  ```
  Add CSS to style h2 appropriately:
  ```css
  .history-item h2 {
    font-size: 1rem;
    font-weight: 600;
    margin: 0;
  }
  ```

#### 8. Missing Skip Link
- **Severity:** Major
- **Location:** `index.html`
- **Description:** No skip link to bypass repetitive content and jump directly to main content. Keyboard users must tab through the header and prompt card before reaching the editor.
- **Suggestion:** Add a skip link at the top of the body:
  ```html
  <body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <main id="app">
      <header class="top">
        <h1>Daily Ink</h1>
        ...
  ```
  Update main element:
  ```html
  <main id="app" tabindex="-1">
  ```
  Add CSS:
  ```css
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: var(--fg);
    color: var(--bg);
    padding: 8px 16px;
    z-index: 100;
    text-decoration: none;
  }
  
  .skip-link:focus {
    top: 0;
  }
  ```

#### 9. Dialog Confirmation Without Keyboard Trap Prevention
- **Severity:** Major
- **Location:** `src/app.ts:180-184`
- **Description:** The delete confirmation uses native `confirm()` dialog which blocks keyboard navigation and may not be fully accessible. While native dialogs are generally accessible, focus management after dismissal is not handled.
- **Code:**
  ```typescript
  if (confirm(`Delete entry from ${entry.date}?`)) {
    deleteEntry(id);
    renderHistory();
  }
  ```
- **Suggestion:** Focus should return to the delete button after confirmation. However, since this uses native `confirm()`, focus management is browser-handled. For better accessibility, consider a custom modal dialog with proper focus trapping and `aria-modal="true"`. If keeping native confirm, at least document this as a known limitation.

#### 10. Word Count Not Announced Dynamically
- **Severity:** Major
- **Location:** `src/app.ts:45, 147-151`
- **Description:** The word count updates as the user types but screen readers aren't notified. While not critical, this provides valuable feedback for writing goals.
- **Suggestion:** Add `aria-live="polite"` with a slight delay to avoid announcing every keystroke:
  ```html
  <span id="word-count" aria-live="polite" aria-atomic="true">0 words</span>
  ```

---

### 🟡 Minor Issues

#### 11. Placeholder Text Contrast
- **Severity:** Minor
- **Location:** `src/style.css:118-120`
- **Description:** Placeholder text uses `var(--muted)` with `opacity: 0.6`, which may reduce contrast below WCAG requirements depending on the computed color. Placeholder text should still meet 3:1 contrast ratio against the background.
- **Current CSS:**
  ```css
  textarea::placeholder {
    color: var(--muted);
    opacity: 0.6;
  }
  ```
- **Suggestion:** Test actual contrast ratio. If using `--muted: #8a8a8a` (dark mode) with 0.6 opacity, verify it meets 3:1. Consider removing opacity and adjusting color directly:
  ```css
  textarea::placeholder {
    color: var(--muted);
    opacity: 1;
  }
  ```

#### 12. Missing Language Attribute Dynamics
- **Severity:** Minor
- **Location:** `index.html:2`
- **Description:** The `lang="en"` attribute is static. If the app ever supports multiple languages, this should be updated dynamically. Currently acceptable for English-only app.
- **Suggestion:** Document that `lang` attribute must be updated if i18n is added:
  ```html
  <html lang="en"> <!-- Update when adding language support -->
  ```

#### 13. Time Element Missing Datetime Attribute
- **Severity:** Minor
- **Location:** `src/app.ts:169`
- **Description:** The `<time>` element in history items displays formatted time but lacks the `datetime` attribute for machine-readable timestamps.
- **Code:**
  ```typescript
  <time>${new Date(e.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</time>
  ```
- **Suggestion:** Add `datetime` attribute:
  ```typescript
  <time datetime="${new Date(e.createdAt).toISOString()}">
    ${new Date(e.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
  </time>
  ```

#### 14. Article Landmark Not Fully Accessible
- **Severity:** Minor
- **Location:** `src/app.ts:166-177`
- **Description:** History items use `<article>` correctly, but lack `aria-labelledby` to associate with their date heading. This would improve navigation for screen reader users.
- **Suggestion:** Add unique IDs to headings and reference them:
  ```typescript
  <article class="history-item" data-id="${e.id}" aria-labelledby="heading-${e.id}">
    <header>
      <h2 id="heading-${e.id}">${formatDate(e.date)}</h2>
      ...
  ```

---

## Positive Findings

✅ **Semantic HTML Structure:** Proper use of `<main>`, `<header>`, `<nav>`, `<article>`, `<time>`  
✅ **Form Label:** Textarea has associated `<label for="editor">`  
✅ **Button Types:** All buttons explicitly declare `type="button"` preventing accidental form submission  
✅ **Logical Reading Order:** DOM order matches visual layout  
✅ **Responsive Design:** Viewport meta tag includes `viewport-fit=cover` for safe areas  
✅ **Color Scheme Support:** Respects `prefers-color-scheme` media query  
✅ **SVG Favicon:** Lightweight, scalable icon format  
✅ **No Color-Only Information:** Status indicators use text ("Saved ✓") not just color  

---

## Recommendations Priority

### Immediate (Before Next Release)
1. Fix install-hint contrast issues (Findings #1, #2)
2. Add focus indicators (Finding #3)
3. Add `aria-live` to save status (Finding #5)

### Short-Term (Next Sprint)
4. Implement ARIA labels for action buttons (Finding #4)
5. Add `aria-expanded` to history toggle (Finding #6)
6. Fix heading hierarchy (Finding #7)
7. Add skip link (Finding #8)

### Medium-Term (Future Enhancements)
8. Improve word count announcements (Finding #10)
9. Add `datetime` attributes to time elements (Finding #13)
10. Consider custom modal for delete confirmation (Finding #9)

---

## Testing Notes

**Manual Testing Recommended:**
- Keyboard navigation through entire app flow
- Screen reader testing (VoiceOver, NVDA, JAWS)
- Color contrast analysis with actual rendered colors
- Focus visibility at various zoom levels (200%, 400%)

**Automated Tools to Run:**
- axe-core browser extension
- Lighthouse accessibility audit
- WAVE evaluation tool

---

## Conclusion

Daily Ink has a solid accessibility foundation with proper semantic structure and thoughtful form design. The critical issues are primarily visual (contrast, focus states) and can be resolved with targeted CSS updates. Addressing the major findings will significantly improve the experience for screen reader users and keyboard-only users.

**Overall Accessibility Maturity:** Intermediate — Good structure, needs polish on ARIA and visual indicators.
