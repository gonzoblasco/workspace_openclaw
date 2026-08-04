# Accessibility Code Audit: EnSuLugar

**Project:** EnSuLugar (Vite + React 19, cooking recipes app)  
**Location:** `/Users/gonzoblasco/.openclaw/workspace/projects/ensulugar`  
**Audit Date:** 2026-08-04  
**Auditor:** A11y Audit Agent

---

## Executive Summary

The EnSuLugar application demonstrates **good accessibility awareness** with several implemented best practices, but has notable gaps that impact users with disabilities. The audit identified **15 findings** across the codebase:

- **3 Critical** issues requiring immediate attention
- **7 Major** issues affecting core functionality
- **5 Minor** issues for polish and edge cases

---

## Findings

### 🔴 CRITICAL

#### 1. Missing `html[lang]` attribute in app/index.html
- **Severity:** Critical
- **Location:** `app/index.html:2`
- **Description:** The main application HTML file lacks a `lang` attribute on the `<html>` element. Screen readers cannot determine the content language, leading to incorrect pronunciation.
- **Current Code:**
  ```html
  <html lang="es">
  ```
  Wait - actually it DOES have `lang="es"`. However, the **root index.html** at project root has `lang="es"` but includes inline styles and scripts mixed with content.
- **Fix:** Ensure all HTML entry points consistently declare language. ✅ Already correct in both files.

**Correction:** This is NOT an issue - both files have proper lang attributes.

#### 1. Color-only distinction for quiz feedback (correct/incorrect)
- **Severity:** Critical
- **Location:** `app/src/index.css:407-439`
- **Description:** Quiz answers use only color (green/red background) to indicate correct/incorrect states. Users with color blindness cannot distinguish between success and error states.
- **Current Code:**
  ```css
  .option-btn.correct {
    background: #10b981; /* Green */
    border-color: #059669;
    color: #fff;
  }
  .option-btn.incorrect {
    background: #ef4444; /* Red */
    border-color: #dc2626;
    color: #fff;
  }
  ```
- **Fix:** Add icons or text labels in addition to color:
  ```css
  .option-btn.correct::after {
    content: " ✓ Correcto";
  }
  .option-btn.incorrect::after {
    content: " ✕ Incorrecto";
  }
  ```
  Or add `aria-live` region announcing the result.

#### 2. Focus not trapped in modal dialogs
- **Severity:** Critical
- **Location:** `app/src/App.tsx:293-320`
- **Description:** The feedback modal (`feedbackModal`) does not trap keyboard focus. Users can tab out of the modal into underlying content, creating confusion and navigation issues.
- **Current Code:** Modal renders with overlay but no focus trap implementation.
- **Fix:** Implement focus trap using a library like `focus-trap-react` or custom hook:
  ```tsx
  import { useFocusTrap } from './hooks/useFocusTrap';
  
  const modalRef = useRef<HTMLDivElement>(null);
  useFocusTrap(modalRef, feedbackModal !== null);
  ```

#### 3. Missing close button for feedback modal
- **Severity:** Critical
- **Location:** `app/src/App.tsx:293-320`
- **Description:** The feedback modal has no visible close button. While Escape key works (via `onKeyDown`), mouse users and those unable to use keyboards have no way to dismiss the modal.
- **Current Code:** Only clicking overlay closes it; no explicit close button.
- **Fix:** Add a close button:
  ```tsx
  <button 
    className="modal-close"
    onClick={() => setFeedbackModal(null)}
    aria-label="Cerrar feedback"
  >
    ✕
  </button>
  ```

---

### 🟠 MAJOR

#### 4. Non-semantic heading hierarchy in recipe cards
- **Severity:** Major
- **Location:** `app/src/App.tsx:490, 507`
- **Description:** Recipe cards use `<h2>` for section title AND `<h2>` for each recipe title, creating duplicate heading levels. When expanded, they use `<h3>` for ingredients/steps, but the hierarchy is inconsistent.
- **Current Code:**
  ```tsx
  <section>
    <h2>Recetas ({recetasFiltradas.length})</h2>
    {/* ... */}
    <article>
      <h2>{r.titulo}</h2>  {/* Should be h3 */}
  ```
- **Fix:** Use proper nesting:
  ```tsx
  <section aria-labelledby="recetas-heading">
    <h2 id="recetas-heading">Recetas ({recetasFiltradas.length})</h2>
    <article>
      <h3>{r.titulo}</h3>
  ```

#### 5. Form inputs without associated labels
- **Severity:** Major
- **Location:** `app/src/App.tsx:384, 395`
- **Description:** Search input and técnica filter input lack visible or programmatic labels. They rely on placeholder text only, which disappears on focus and isn't announced properly by all screen readers.
- **Current Code:**
  ```tsx
  <input
    type="text"
    className="search-input"
    value={busqueda}
    onChange={(e) => setBusqueda(e.target.value)}
    placeholder="Buscar receta…"
  />
  ```
- **Fix:** Add `aria-label` or visible label:
  ```tsx
  <label htmlFor="busqueda" className="visually-hidden">
    Buscar recetas
  </label>
  <input
    id="busqueda"
    type="text"
    aria-label="Buscar recetas por nombre, categoría o técnica"
    // ...
  />
  ```

#### 6. Technique suggestion buttons lack proper role and state
- **Severity:** Major
- **Location:** `app/src/App.tsx:412-432`
- **Description:** Technique suggestion buttons act as toggle buttons but don't expose their pressed state to assistive technologies.
- **Current Code:**
  ```tsx
  <button
    className={"tecnica-suggestion" + (seleccionada ? " selected" : "")}
    onClick={() => toggleTecnica(id)}
  >
  ```
- **Fix:** Add `aria-pressed`:
  ```tsx
  <button
    aria-pressed={seleccionada}
    onClick={() => toggleTecnica(id)}
  >
  ```

#### 7. Dynamic content changes not announced
- **Severity:** Major
- **Location:** `app/src/App.tsx:167-188` (generarLeccionParaReceta)
- **Description:** When generating a lesson, the loading state and content updates happen without screen reader announcements. Users won't know when content loads.
- **Current Code:** State changes silently update the UI.
- **Fix:** Use `aria-live` regions:
  ```tsx
  <div aria-live="polite" aria-atomic="true">
    {leccion.loading && "Generando lección..."}
  </div>
  ```

#### 8. Skip link present but target may not exist
- **Severity:** Major
- **Location:** `app/src/index.css:25-43` (skip-link styles exist)
- **Description:** CSS defines a skip link style, but there's no evidence of an actual skip link in the HTML or a `#main-content` target in all views.
- **Current Code:** Styles exist, but implementation incomplete.
- **Fix:** Add skip link to App component:
  ```tsx
  <a href="#main-content" className="skip-link">
    Saltar al contenido principal
  </a>
  <main id="main-content">
  ```

#### 9. Emoji used as icons without text alternatives
- **Severity:** Major
- **Location:** Multiple locations (e.g., `App.tsx:308`, `index.html:314`)
- **Description:** Emojis are used for icons (🔍, 🌙, 🤩, etc.) without consistent `aria-label` or `role="img"` attributes.
- **Current Code:** Mixed usage - some have labels, others don't.
- **Fix:** Standardize emoji usage:
  ```tsx
  <span role="img" aria-label="Buscar">🔍</span>
  <button aria-label="Cambiar a modo oscuro">🌙</button>
  ```

#### 10. Recipe grid lacks list semantics
- **Severity:** Major
- **Location:** `app/src/App.tsx:477`
- **Description:** Recipe cards are rendered in a `<div className="recipe-grid">` instead of a semantic `<ul>` with `<li>` children, losing list context for screen reader users.
- **Current Code:**
  ```tsx
  <div className="recipe-grid">
    {recetasFiltradas.map((r) => (
      <article key={r.id}>...</article>
    ))}
  </div>
  ```
- **Fix:** Use list markup:
  ```tsx
  <ul className="recipe-grid" role="list">
    {recetasFiltradas.map((r) => (
      <li key={r.id}>
        <article aria-labelledby={`recipe-${r.id}`}>
          <h3 id={`recipe-${r.id}`}>{r.titulo}</h3>
  ```

---

### 🟡 MINOR

#### 11. Placeholder text as sole instruction
- **Severity:** Minor
- **Location:** `app/src/App.tsx:384, 395`
- **Description:** Placeholder text ("Buscar receta…", "Técnica…") provides instructions that vanish on focus.
- **Fix:** Keep placeholder as hint, but ensure labels are always visible (see Finding #5).

#### 12. Star ratings use unicode characters without labels
- **Severity:** Minor
- **Location:** `app/src/App.tsx:13, 493`
- **Description:** The `estrellas()` function returns unicode stars (★★★☆☆) without accessible names indicating the rating value.
- **Current Code:**
  ```tsx
  function estrellas(n: number): string {
    return "★".repeat(n) + "☆".repeat(5 - n);
  }
  ```
- **Fix:** Wrap in element with aria-label:
  ```tsx
  <span aria-label={`${n} de 5 estrellas`} role="img">
    {estrellas(n)}
  </span>
  ```

#### 13. Category badges convey info by color alone
- **Severity:** Minor
- **Location:** `index.html:120-126`
- **Description:** Recipe category colors (huevos, pastas, salsas, etc.) are distinguished only by background/text color combinations.
- **Fix:** Ensure category name is always visible (already is) and consider adding patterns/icons for additional distinction.

#### 14. No visible focus indicator for all interactive elements
- **Severity:** Minor
- **Location:** `app/src/index.css` (various)
- **Description:** While `:focus-visible` styles exist for buttons, some interactive elements like technique tags may not have consistent focus indicators.
- **Fix:** Audit all interactive elements and ensure consistent `:focus-visible` styles with sufficient contrast.

#### 15. Loading states lack accessible announcements
- **Severity:** Minor
- **Location:** `app/src/App.tsx:250, 606`
- **Description:** Loading messages ("Cargando recetas…", "Generando lección…") are visually present but not prioritized for screen readers.
- **Fix:** Add `role="status"` and `aria-live="polite"` to loading containers:
  ```tsx
  <div role="status" aria-live="polite">
    <div className="loading-spinner"></div>
    <p>Generando lección personalizada…</p>
  </div>
  ```

---

## Positive Findings ✅

The following accessibility features are **already implemented correctly**:

1. ✅ **Language declared:** Both HTML files have `lang="es"`
2. ✅ **Skip link CSS exists:** `.skip-link` styles are defined
3. ✅ **Some aria-labels present:** Theme toggle, search input, tag remove buttons
4. ✅ **Escape key handling:** Modal closes on Escape key press
5. ✅ **Focus-visible styles:** Most buttons have `:focus-visible` definitions
6. ✅ **Semantic elements used:** `<header>`, `<section>`, `<article>` present
7. ✅ **Form labels in onboarding:** OnboardingScreen uses proper `<label htmlFor>`
8. ✅ **Dialog role on modal:** Feedback modal has `role="dialog"` and `aria-modal="true"`
9. ✅ **Button type attributes:** Some buttons explicitly use `type="button"`
10. ✅ **Color contrast:** Dark/light theme appears to maintain reasonable contrast ratios

---

## Recommendations Priority

### Immediate (Critical - Fix Before Launch)
1. Add close button to feedback modal
2. Implement focus trap in modals
3. Add non-color indicators for quiz feedback

### Short-term (Major - Next Sprint)
4. Fix heading hierarchy
5. Add labels to all form inputs
6. Implement aria-pressed for toggle buttons
7. Add aria-live regions for dynamic content
8. Implement skip link in App component
9. Standardize emoji icon accessibility
10. Convert recipe grid to semantic list

### Medium-term (Minor - Polish Pass)
11-15. Address remaining minor issues for comprehensive accessibility

---

## Testing Recommendations

1. **Automated Testing:**
   - Run axe-core or Lighthouse audits
   - Add eslint-plugin-jsx-a11y to CI pipeline

2. **Manual Testing:**
   - Keyboard-only navigation through entire flow
   - Screen reader testing (NVDA, VoiceOver, JAWS)
   - Color blindness simulation (protanopia, deuteranopia)

3. **User Testing:**
   - Include users with disabilities in usability tests
   - Test with real assistive technology users

---

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Checklist](https://webaim.org/standards/wcag/checklist)

---

**Generated by:** A11y Audit Agent  
**Audit Scope:** Source code review (static analysis)  
**Next Steps:** Address critical findings, then major, schedule user testing
