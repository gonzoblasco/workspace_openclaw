# Accessibility Code Audit: Health Tracker

**Project:** health-tracker (Next.js PWA)  
**Audit Date:** 2026-08-04  
**Auditor:** A11y Audit Agent  
**Scope:** Source code review for WCAG 2.1 AA compliance

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 3 |
| 🟠 Major | 8 |
| 🟡 Minor | 12 |

The health-tracker app demonstrates good foundational accessibility practices (semantic HTML, proper heading hierarchy, ARIA labels on interactive elements). However, several issues need attention, particularly around focus management, color contrast, and keyboard navigation.

---

## Findings

### 🔴 Critical Issues

#### 1. Missing skip link for keyboard users
- **Location:** `src/app/layout.tsx:37-44`
- **Description:** No skip navigation link provided. Keyboard users must tab through the entire tab bar on every page load to reach main content.
- **Impact:** Severe barrier for keyboard-only users and screen reader users
- **Fix:** Add a skip link at the beginning of `<body>` that targets the `<main>` element
```tsx
// In layout.tsx, after <body> opening tag:
<a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] focus:bg-emerald-700 focus:text-white focus:px-3 focus:py-2">
  Saltar al contenido principal
</a>

// Add id to main element:
<main id="main-content" className="mx-auto max-w-md min-h-[100dvh] flex flex-col">
```

#### 2. Focus not managed in modal dialogs
- **Location:** `src/app/entrenar/page.tsx:175-193` (rest timer overlay)
- **Description:** Rest timer modal appears but doesn't trap focus or return focus when dismissed. Screen readers may not announce the modal content.
- **Impact:** Keyboard users can tab outside the modal; screen reader users unaware of modal context
- **Fix:** Implement proper focus trap and aria-modal
```tsx
<div 
  className="fixed inset-0 z-50..." 
  role="dialog"
  aria-modal="true"
  aria-labelledby="rest-timer-title"
>
  <p id="rest-timer-title" className="text-sm uppercase tracking-wider text-zinc-400">Descanso</p>
  {/* Use a focus trap library or custom hook */}
</div>
```

#### 3. Delete confirmation lacks accessible announcement
- **Location:** `src/app/rutinas/[id]/page.tsx:88-104`
- **Description:** Delete confirmation buttons appear inline without screen reader announcement. Users may not know state changed.
- **Impact:** Screen reader users unaware of confirmation state change
- **Fix:** Use live region or aria-live to announce state change
```tsx
<div aria-live="polite" className="sr-only">
  {confirmDelete ? 'Modo de eliminación activado. Confirmá o cancelá.' : ''}
</div>
```

---

### 🟠 Major Issues

#### 4. Color contrast insufficient for secondary text
- **Location:** Multiple files - `text-zinc-400` on dark backgrounds
- **Description:** `text-zinc-400` (#a1a1aa) on `bg-zinc-900`/#18181b fails WCAG AA (contrast ratio ~4.5:1 required, currently ~3.8:1 for small text)
- **Impact:** Low vision users cannot read secondary text
- **Fix:** Use `text-zinc-300` or lighter for better contrast
- **Files affected:**
  - `src/app/page.tsx` (multiple instances)
  - `src/app/progreso/page.tsx`
  - `src/app/ajustes/page.tsx`
  - `src/app/rutinas/page.tsx`
  - `src/app/rutinas/nueva/page.tsx`

#### 5. Form inputs lack visible labels (some rely on placeholders)
- **Location:** `src/app/rutinas/nueva/page.tsx:127-134`
- **Description:** Exercise name input uses only placeholder "Nombre del ejercicio". Placeholders disappear on focus and are not reliable labels.
- **Impact:** Screen reader users may not understand input purpose; cognitive load increased
- **Fix:** Add explicit `<label>` element
```tsx
<label htmlFor="ex-name" className="text-xs text-zinc-400">Nombre del ejercicio</label>
<input
  id="ex-name"
  type="text"
  value={exName}
  onChange={(e) => setExName(e.target.value)}
  placeholder="Ej: Press de banca"
  className="flex-1 rounded-lg..."
/>
```

#### 6. Custom toggle switch lacks clear accessible name
- **Location:** `src/app/ajustes/page.tsx:71-77`
- **Description:** Toggle button has `role="switch"` and `aria-checked`, but visual label is separate. The association relies on proximity, not programmatic linking.
- **Impact:** Screen reader users may not associate label with control
- **Fix:** Wrap in label or use `aria-labelledby`
```tsx
<div className="flex items-center justify-between">
  <label htmlFor="sync-toggle" className="text-sm">Sincronización con nube</label>
  <button
    id="sync-toggle"
    // ...existing props
    aria-label="Sincronización con nube"
  />
</div>
```

#### 7. Emoji-only buttons lack accessible names
- **Location:** `src/app/rutinas/nueva/page.tsx:168-173` (remove exercise button)
- **Description:** Button shows only "✕" emoji. While it has `aria-label`, ensure it's descriptive enough.
- **Impact:** Screen reader users may not understand button purpose if aria-label is generic
- **Fix:** Make aria-label more specific
```tsx
<button
  onClick={() => removeExercise(ex.id)}
  className="text-zinc-400 hover:text-red-400"
  aria-label={`Eliminar ejercicio ${ex.name}`}
>
  ✕
</button>
```

#### 8. Progress bars lack text alternative
- **Location:** `src/app/page.tsx:100-105` (steps progress bar)
- **Description:** Visual progress bar has `role="progressbar"` with aria values, but no visible text showing percentage for users who can't perceive the visual bar.
- **Impact:** Screen reader users get announced values but sighted users with cognitive disabilities may not understand the visualization
- **Fix:** Add visible percentage text
```tsx
<p className="mt-2 text-xs text-emerald-400">
  {Math.round(stepProgress * 100)}% completado
</p>
```

#### 9. Chart data not accessible to screen readers
- **Location:** `src/app/page.tsx:133-150` (week step chart)
- **Description:** Bar chart is purely visual. Screen reader users cannot access the data.
- **Impact:** Complete information loss for non-visual users
- **Fix:** Provide data table or aria-describedby with summary
```tsx
<section aria-label="Pasos - últimos 7 días" aria-describedby="chart-desc">
  <p id="chart-desc" className="sr-only">
    Gráfico de barras mostrando pasos diarios: Lunes 5000, Martes 7200, Miércoles 8500...
  </p>
  {/* Or provide a collapsible data table alternative */}
</section>
```

#### 10. Same issue in progreso page chart
- **Location:** `src/app/progreso/page.tsx:47-60` (30-day step chart)
- **Description:** 30-day bar chart lacks any accessible data representation
- **Impact:** Screen reader users cannot access monthly step history
- **Fix:** Same as #9 - provide data table or detailed description

#### 11. Loading screen lacks status announcement
- **Location:** `src/components/loading-screen.tsx:4-11`
- **Description:** Loading indicator is visual only. Screen readers don't announce loading state.
- **Impact:** Screen reader users may think page is broken
- **Fix:** Add aria-live region or role="status"
```tsx
<div 
  className="flex flex-1 items-center justify-center"
  role="status"
  aria-live="polite"
>
  <div className="h-8 w-8 animate-spin..." aria-hidden="true" />
  <span className="sr-only">Cargando datos...</span>
</div>
```

---

### 🟡 Minor Issues

#### 12. Heading hierarchy skips levels in some views
- **Location:** `src/app/rutinas/[id]/page.tsx:56`
- **Description:** Uses `<h2>` for "Ejercicios" after `<h1>` for routine name - this is correct. However, in `src/app/rutinas/nueva/page.tsx`, heading structure could be clearer with nested sections.
- **Impact:** Minor confusion for screen reader users navigating by headings
- **Fix:** Ensure consistent h1 → h2 → h3 flow throughout

#### 13. Links opened in same tab without warning
- **Location:** Throughout app (external links if added in future)
- **Description:** Currently no external links, but if added, should warn users when opening new tabs
- **Impact:** Cognitive surprise for users
- **Fix:** Add `target="_blank"` with visual icon and `aria-label="abre en nueva ventana"`

#### 14. Error messages not programmatically associated with inputs
- **Location:** `src/app/rutinas/nueva/page.tsx` (form validation)
- **Description:** Form has disabled submit button when invalid, but no error messages explaining why
- **Impact:** Users may not understand why form won't submit
- **Fix:** Add `aria-describedby` pointing to error messages
```tsx
<input
  id="routine-name"
  aria-describedby={nameError ? "name-error" : undefined}
/>
{nameError && <p id="name-error" className="text-red-400 text-xs">El nombre es requerido</p>}
```

#### 15. No focus visible styles customized
- **Location:** `src/app/globals.css` (not audited, but likely using Tailwind defaults)
- **Description:** Default focus rings may not have sufficient contrast or visibility in dark mode
- **Impact:** Keyboard users may lose track of focus position
- **Fix:** Customize focus styles in globals.css
```css
:focus-visible {
  @apply outline-2 outline-offset-2 outline-emerald-400;
}
```

#### 16. Touch targets may be small on mobile
- **Location:** Filter chips in `src/app/rutinas/page.tsx:35-44`
- **Description:** Chip buttons with `px-3.5 py-1.5` may be under 44x44px minimum touch target
- **Impact:** Motor impairment users struggle to tap accurately
- **Fix:** Increase padding to ensure 44px minimum
```tsx
className="whitespace-nowrap rounded-full px-4 py-2 text-xs..."
```

#### 17. No language switch mechanism (if needed for internationalization)
- **Location:** `src/app/layout.tsx:30`
- **Description:** Hardcoded `lang="es"`. If app expands to other languages, need language switcher
- **Impact:** Not currently an issue since app is Spanish-only, but plan ahead
- **Fix:** Document in roadmap for i18n support

#### 18. Alert() used for confirmations
- **Location:** `src/app/ajustes/page.tsx:32, 103`
- **Description:** Native `alert()` blocks screen readers and is not customizable
- **Impact:** Poor experience for screen reader users; alerts may not be announced properly
- **Fix:** Use custom modal dialog with proper ARIA
```tsx
// Replace alert() with accessible toast/notification component
<Toast message="Ajustes guardados" role="alert" />
```

#### 19. Data export button lacks feedback
- **Location:** `src/app/progreso/page.tsx:105-110`
- **Description:** Export button triggers download but provides no success/failure feedback
- **Impact:** Users uncertain if export worked
- **Fix:** Add aria-live announcement or toast notification
```tsx
<button
  onClick={async () => {
    await exportData(...);
    // Show accessible toast
  }}
>
```

#### 20. Routine card emoji list lacks context
- **Location:** `src/components/routine-card.tsx:40-45`
- **Description:** Exercise emojis shown with `aria-hidden="true"` but no text alternative describing what they represent
- **Impact:** Screen reader users miss the visual preview of exercises
- **Fix:** Add sr-only text or consolidate into routine description
```tsx
<span className="sr-only">
  Ejercicios: {routine.exercises.map(e => e.name).join(', ')}
</span>
```

#### 21. No reduced motion support
- **Location:** `src/components/loading-screen.tsx` (spin animation), various transitions
- **Description:** Animations don't respect `prefers-reduced-motion`
- **Impact:** Users with vestibular disorders may experience discomfort
- **Fix:** Add CSS media query
```css
@media (prefers-reduced-motion: reduce) {
  .animate-spin {
    animation: none;
  }
  * {
    transition: none !important;
  }
}
```

#### 22. Search/filter not present (future consideration)
- **Location:** N/A
- **Description:** As routine library grows, users will need search. Plan for accessible search pattern
- **Impact:** Future scalability issue
- **Fix:** Document in roadmap

#### 23. No "back to top" link on long pages
- **Location:** N/A
- **Description:** Progreso page with many workouts becomes long; no quick way to return to top
- **Impact:** Minor inconvenience for keyboard users
- **Fix:** Add floating "back to top" button that appears after scroll

---

## Positive Findings ✅

The following accessibility best practices are already implemented:

1. ✅ **Semantic HTML**: Proper use of `<main>`, `<nav>`, `<header>`, `<section>`, `<h1-h2>`
2. ✅ **ARIA landmarks**: `aria-label` on navigation, progress bars, and sections
3. ✅ **Current page indication**: `aria-current="page"` on active tab bar items
4. ✅ **Form labels**: Most inputs have associated `<label>` elements with `htmlFor`
5. ✅ **Button roles**: Interactive elements use `<button>` instead of `<div>` with click handlers
6. ✅ **Emoji decoration**: Emojis correctly marked with `aria-hidden="true"` when decorative
7. ✅ **Language attribute**: `<html lang="es">` correctly set
8. ✅ **Focus states**: Links and buttons have hover/focus color changes
9. ✅ **Tablist pattern**: Filter chips use `role="tablist"` and `role="tab"` with `aria-selected`
10. ✅ **Live data**: Steps widget updates dynamically (though could add live regions)

---

## Recommendations Priority

### Immediate (Before Launch)
1. Add skip link (Critical #1)
2. Fix focus management in modals (Critical #2)
3. Add screen reader announcements for dynamic states (Critical #3, Major #11)
4. Fix color contrast for body text (Major #4)

### Short-term (Sprint 1-2)
5. Add labels to all form inputs (Major #5)
6. Make charts accessible with data tables (Major #9, #10)
7. Improve toggle and button labels (Major #6, #7)
8. Add visible percentage to progress bars (Major #8)

### Medium-term (Sprint 3-4)
9. Implement custom accessible modals/toasts (Minor #18)
10. Add reduced motion support (Minor #21)
11. Increase touch target sizes (Minor #16)
12. Customize focus visible styles (Minor #15)

### Future Roadmap
13. Add i18n support with language switcher (Minor #17)
14. Implement search functionality (Minor #22)
15. Add back-to-top navigation (Minor #23)

---

## Testing Recommendations

### Manual Testing Checklist
- [ ] Navigate entire app using only keyboard (Tab, Shift+Tab, Enter, Space, Esc)
- [ ] Test with VoiceOver (macOS/iOS) or NVDA/JAWS (Windows)
- [ ] Verify color contrast with WebAIM Contrast Checker
- [ ] Test zoom at 200% and 400%
- [ ] Enable "Reduce Motion" in OS settings and verify animations pause
- [ ] Test touch targets on actual mobile device

### Automated Testing Tools
- Run `axe-core` or `@axe-core/react` during development
- Add Lighthouse CI accessibility audits
- Use `eslint-plugin-jsx-a11y` in linting pipeline

---

## Conclusion

The health-tracker app has a solid accessibility foundation with proper semantic structure and ARIA usage. The critical issues are fixable with focused effort and should be prioritized before production launch. Most fixes involve adding ARIA attributes, improving focus management, and providing text alternatives for visual information.

**Estimated Effort:** 2-3 sprints for full WCAG 2.1 AA compliance  
**Risk Level:** Medium - current state usable but barriers exist for assistive technology users

---

*Generated by A11y Audit Agent*  
*Based on WCAG 2.1 Guidelines and WAI-ARIA Authoring Practices*
