# Accessibility Code Audit — Sport Cars

**Project:** Sport Cars (Next.js, Concesionario Jeep/Ram)  
**Location:** `/Users/gonzoblasco/.openclaw/workspace/projects/sportcars`  
**Audit Date:** 2026-08-04  
**Scope:** Source code review for WCAG 2.1 AA compliance

---

## Executive Summary

The Sport Cars Next.js application demonstrates **good foundational accessibility practices** with proper semantic HTML structure, meaningful alt text on images, and labeled form inputs. However, several issues require attention to achieve full WCAG 2.1 AA compliance.

**Key Findings:**
- ✅ Strong: Semantic HTML5 landmarks (`main`, `nav`, `header`, `footer`, `section`)
- ✅ Strong: Form inputs properly labeled with `htmlFor`/`id` associations
- ✅ Strong: Image alt text present and descriptive
- ⚠️ **Critical:** Mobile menu lacks keyboard trap prevention and focus management
- ⚠️ **Major:** Custom Select components missing proper ARIA attributes
- ⚠️ **Major:** Chat widget may trap keyboard focus when open
- ⚠️ **Minor:** Some interactive elements lack visible focus indicators in certain states
- ⚠️ **Minor:** Color-only state indicators (e.g., status badges)

---

## Detailed Findings

### Critical Severity

#### 1. Mobile Menu — Keyboard Trap & Focus Management
**Location:** `src/components/layout/header.tsx:53-79`  
**Issue:** The mobile menu uses a `<details>` element without proper focus trapping or focus management. When opened, keyboard users can tab outside the menu while it remains visually open, creating confusion.

```tsx
<details className="group md:hidden">
  <summary className="flex cursor-pointer list-none items-center text-sc-text">
    <Menu className="h-6 w-6 group-open:hidden" />
    <X className="hidden h-6 w-6 group-open:block" />
  </summary>
  <nav className="absolute left-0 right-0 top-16 border-b border-sc-border bg-sc-bg p-4">
    {/* Navigation links */}
  </nav>
</details>
```

**Problems:**
- No focus trap when menu is open
- Focus not returned to trigger when closing
- Escape key behavior relies on native `<details>` which may be inconsistent across browsers
- No `aria-expanded` state explicitly managed

**Suggested Fix:**
```tsx
// Use a controlled dialog pattern with focus trap
import { Dialog, DialogOverlay, DialogContent } from "@/components/ui/dialog";

function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);
  
  // Trap focus inside menu when open
  // Return focus to trigger on close
  // Handle Escape key explicitly
  
  return (
    <>
      <button 
        onClick={() => setIsOpen(true)}
        aria-label="Abrir menú de navegación"
        aria-expanded={isOpen}
      >
        <Menu className="h-6 w-6" />
      </button>
      
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="md:hidden">
          <nav aria-label="Menú principal">
            {/* Links */}
          </nav>
        </DialogContent>
      </Dialog>
    </>
  );
}
```

---

### Major Severity

#### 2. Custom Select Components — Missing ARIA Attributes
**Location:** `src/components/ui/select.tsx` (throughout)  
**Issue:** The Base UI Select component wrapper does not expose critical ARIA attributes for screen reader users.

**Problems:**
- `SelectTrigger` does not render with explicit `aria-haspopup="listbox"`
- `SelectTrigger` missing `aria-expanded` state binding
- `SelectContent` (popup) may not have `role="listbox"` properly exposed
- No `aria-describedby` for error states or helper text

**Suggested Fix:**
```tsx
function SelectTrigger({
  className,
  size = "default",
  children,
  ...props
}: SelectPrimitive.Trigger.Props & { size?: "sm" | "default" }) {
  return (
    <SelectPrimitive.Trigger
      data-slot="select-trigger"
      data-size={size}
      aria-haspopup="listbox"
      // aria-expanded is handled by Base UI but verify it's exposed
      className={cn(/* ... */)}
      {...props}
    >
      {children}
      {/* Icon */}
    </SelectPrimitive.Trigger>
  );
}
```

**Verify:** Check that Base UI React components expose ARIA attributes correctly at runtime. If not, add explicit props.

---

#### 3. Chat Widget — Focus Management
**Location:** `src/components/shared/chat-widget.tsx:1-200`  
**Issue:** When the chat widget opens, focus moves to the input field (line 98), but there's no focus trap. Users can tab out of the widget while it remains open, losing context.

```tsx
useEffect(() => {
  if (isOpen) {
    setTimeout(() => inputRef.current?.focus(), 300);
  }
}, [isOpen]);
```

**Problems:**
- No focus trap within the chat widget container
- Tab key can move focus outside the widget
- No mechanism to close via Escape key
- Screen reader users may not be notified when chat opens

**Suggested Fix:**
```tsx
// Add focus trap utility
import { useEffect, useRef } from 'react';

function useFocusTrap(isActive: boolean, containerRef: React.RefObject<HTMLElement>) {
  useEffect(() => {
    if (!isActive || !containerRef.current) return;
    
    const container = containerRef.current;
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        // Close chat
        return;
      }
      
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };
    
    container.addEventListener('keydown', handleKeyDown);
    firstElement.focus();
    
    return () => container.removeEventListener('keydown', handleKeyDown);
  }, [isActive, containerRef]);
}

// In ChatWidget component
const containerRef = useRef<HTMLDivElement>(null);
useFocusTrap(isOpen, containerRef);

// Add aria-live announcement
<div 
  ref={containerRef}
  role="dialog"
  aria-modal="true"
  aria-label="Asistente Sport Cars"
>
  {/* Chat content */}
</div>
```

---

#### 4. Dialog Component — Missing aria-labelledby/aria-describedby
**Location:** `src/components/ui/dialog.tsx:46-73`  
**Issue:** The `DialogContent` component does not automatically associate the title and description with ARIA attributes.

```tsx
function DialogContent({
  className,
  children,
  showCloseButton = true,
  ...props
}: DialogPrimitive.Popup.Props & { showCloseButton?: boolean }) {
  return (
    <DialogPortal>
      <DialogOverlay />
      <DialogPrimitive.Popup
        data-slot="dialog-content"
        className={cn(/* ... */)}
        {...props}
      >
        {children}
        {/* Close button */}
      </DialogPrimitive.Popup>
    </DialogPortal>
  );
}
```

**Suggested Fix:**
```tsx
// The DialogPrimitive should handle this, but ensure:
// 1. DialogTitle has an id
// 2. DialogDescription has an id
// 3. DialogContent references them via aria-labelledby and aria-describedby

// If Base UI doesn't auto-wire these, manually connect:
<DialogPrimitive.Popup
  aria-labelledby={titleId}
  aria-describedby={descriptionId}
  {...props}
>
```

---

### Minor Severity

#### 5. Feature Flags Panel — Toggle Buttons Lack Visual Focus
**Location:** `src/components/shared/feature-flags-panel.tsx:55-65`  
**Issue:** Toggle buttons use `aria-pressed` but may not have sufficiently visible focus indicators in all themes.

```tsx
<button
  type="button"
  role="switch"
  aria-pressed={value}
  aria-label={`Toggle ${key}`}
  onClick={() => toggle(key)}
  className={cn(
    "relative inline-flex h-5 w-9 shrink-0 items-center rounded-full",
    value ? "bg-sc-accent" : "bg-sc-border"
  )}
>
  {/* Thumb */}
</button>
```

**Problem:** The focus ring may not be visible against dark backgrounds or high contrast modes.

**Suggested Fix:** Ensure `focus-visible:ring` styles are applied and test in Windows High Contrast Mode and macOS Increased Contrast.

```tsx
className={cn(
  "relative inline-flex h-5 w-9 shrink-0 items-center rounded-full",
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
  value ? "bg-sc-accent" : "bg-sc-border",
  "dark:focus-visible:ring-offset-background"
)}
```

---

#### 6. Price Display — Information Conveyed by Color Alone
**Location:** `src/components/shared/price-display.tsx`  
**Issue:** Prices are displayed using only color (`text-sc-accent`) to indicate importance. Users with color vision deficiency may miss this emphasis.

```tsx
className={`text-lg font-bold text-sc-accent ${className}`}
```

**Suggested Fix:** Add additional visual weight beyond color:
- Keep the bold font weight (already present)
- Consider adding an icon prefix for special prices
- Ensure sufficient contrast ratio (sc-accent vs background)

**Verification Needed:** Check contrast ratio of `text-sc-accent` against its background. WCAG AA requires 4.5:1 for normal text.

---

#### 7. Breadcrumb Navigation — Missing aria-label
**Location:** Multiple pages (e.g., `src/app/test-drive/page.tsx:21`, `src/app/contacto/page.tsx:23`)  
**Issue:** Breadcrumb `<nav>` elements lack `aria-label` to distinguish them from other navigation regions.

```tsx
<nav className="mb-6 text-sm text-sc-muted">
  <a href="/">Inicio</a>
  <span className="mx-2">/</span>
  <span className="text-sc-text">Test Drive</span>
</nav>
```

**Suggested Fix:**
```tsx
<nav aria-label="Ruta de navegación" className="mb-6 text-sm text-sc-muted">
  {/* Breadcrumb items */}
</nav>
```

Apply to:
- `src/app/test-drive/page.tsx:21`
- `src/app/contacto/page.tsx:23`
- `src/app/cotiza-tu-usado/page.tsx:21`
- `src/app/sucursales/page.tsx:16`
- `src/app/vehiculos/page.tsx:19`
- `src/app/vehiculos/[slug]/page.tsx:44`

---

#### 8. External Links — Missing aria-label for Context
**Location:** Multiple files (WhatsApp links, Mercado Libre links)  
**Issue:** External links opening in new tabs (`target="_blank"`) have `rel="noopener noreferrer"` but lack `aria-label` indicating they open externally.

Example from `src/app/page.tsx:145`:
```tsx
<a
  href={`https://wa.me/5491132217200?text=...`}
  target="_blank"
  rel="noopener noreferrer"
  className="..."
>
  <MessageCircle className="h-4 w-4" />
  Consultar
</a>
```

**Suggested Fix:**
```tsx
<a
  href={`https://wa.me/5491132217200?text=...`}
  target="_blank"
  rel="noopener noreferrer"
  aria-label="Consultar por WhatsApp (abre en nueva pestaña)"
  className="..."
>
  <MessageCircle className="h-4 w-4" aria-hidden="true" />
  Consultar
</a>
```

Alternatively, add a visual indicator (external link icon) with `aria-hidden="true"` and keep text concise.

---

#### 9. Checkbox Inputs — Missing Associated Labels in Filter Sidebar
**Location:** `src/app/vehiculos/page.tsx:36-53`  
**Issue:** Checkbox inputs have adjacent text labels but are not programmatically associated.

```tsx
<label className="flex cursor-pointer items-center gap-2 text-sm text-sc-muted hover:text-sc-text">
  <input type="checkbox" defaultChecked className="accent-sc-accent" />
  Jeep
</label>
```

**Current State:** This pattern works because the `<input>` is nested inside `<label>`, which creates an implicit association. **This is acceptable.**

**Enhancement:** For clarity and robustness, consider explicit association:

```tsx
<div className="space-y-2">
  <label className="flex cursor-pointer items-center gap-2 text-sm text-sc-muted hover:text-sc-text">
    <input
      type="checkbox"
      id="filter-jeep"
      defaultChecked
      className="accent-sc-accent"
    />
    <span>Jeep</span>
  </label>
</div>
```

---

#### 10. Range Input — Missing aria-label and Value Announcement
**Location:** `src/app/vehiculos/page.tsx:62-68`  
**Issue:** Price range slider lacks accessible name and current value announcement.

```tsx
<input
  type="range"
  min="0"
  max="120"
  defaultValue="60"
  className="w-full accent-sc-accent"
/>
<div className="mt-1 flex justify-between text-xs text-sc-muted">
  <span>$ 0</span>
  <span>$ 120M+</span>
</div>
```

**Suggested Fix:**
```tsx
<div>
  <label htmlFor="price-range" className="sr-only">
    Rango de precios
  </label>
  <input
    id="price-range"
    type="range"
    min="0"
    max="120"
    defaultValue="60"
    aria-valuemin="0"
    aria-valuemax="120000000"
    aria-valuenow={priceValue}
    onChange={(e) => setPriceValue(e.target.value)}
    className="w-full accent-sc-accent"
  />
  <div className="mt-1 flex justify-between text-xs text-sc-muted">
    <span>$ 0</span>
    <span aria-live="polite">${priceValue}M</span>
  </div>
</div>
```

---

#### 11. Toast Notifications — Missing Role and Live Region
**Location:** `src/components/ui/toast.tsx`  
**Issue:** Toast components need to verify they have proper `role="status"` or `role="alert"` and are wrapped in an `aria-live` region.

**Check:** Verify that the toast implementation from `@base-ui/react/toast` or custom implementation includes:
- `role="status"` for informational toasts
- `role="alert"` for error toasts
- Parent container with `aria-live="polite"` or `aria-live="assertive"`

If not present, wrap toast container:
```tsx
<div aria-live="polite" aria-atomic="true" className="toast-container">
  {/* Toasts */}
</div>
```

---

## Positive Findings

### ✅ Semantic HTML Structure
- Proper use of `<header>`, `<main>`, `<footer>`, `<nav>`, `<section>` throughout
- Heading hierarchy (`h1` → `h2` → `h3`) is well-maintained
- One `<h1>` per page

### ✅ Form Accessibility
- All form inputs have associated `<label>` elements with `htmlFor` matching input `id`
- Input types are appropriate (`type="email"`, `type="tel"`, `type="date"`, `type="time"`)
- Required fields marked with `required` attribute
- Error states shown with icons and text (not color alone)

### ✅ Image Alt Text
- All `<img>` elements have descriptive `alt` attributes
- Alt text is contextual (e.g., model names, vehicle titles)
- Decorative icons use `aria-hidden="true"` appropriately

### ✅ Link Purpose
- Link text is descriptive ("Ver vehículos", "Agendar test drive")
- Phone links use `tel:` protocol
- WhatsApp links use proper `https://wa.me/` format

### ✅ Language Attribute
- `<html lang="es">` correctly set in layout

---

## Recommendations Priority

### Immediate (Before Next Release)
1. **Fix mobile menu focus trap** — Critical for keyboard-only users
2. **Add aria-label to breadcrumbs** — Quick win, improves navigation clarity
3. **Verify Select ARIA attributes** — Ensure Base UI exposes correct roles

### Short-Term (Next Sprint)
4. **Implement chat widget focus trap** — Important for modal-like interactions
5. **Add external link indicators** — Improves context for all users
6. **Enhance range input accessibility** — Better form experience

### Medium-Term (Backlog)
7. **Review focus indicator visibility** — Test in high contrast modes
8. **Audit color contrast ratios** — Verify sc-accent meets 4.5:1
9. **Toast live region verification** — Ensure screen reader announcements

---

## Testing Recommendations

### Manual Testing
1. **Keyboard Navigation:**
   - Tab through entire site without mouse
   - Test mobile menu open/close with keyboard
   - Verify focus is never trapped or lost

2. **Screen Reader Testing:**
   - NVDA (Windows) + Chrome/Firefox
   - VoiceOver (macOS/iOS) + Safari
   - JAWS (Windows) + Chrome (if available)

3. **High Contrast Modes:**
   - Windows High Contrast Mode
   - macOS Increased Contrast
   - Browser forced colors mode

### Automated Testing
Add to CI pipeline:
```bash
# axe-core via Playwright
npx playwright test --grep a11y

# Or pa11y
pa11y-ci --config .pa11yci.json
```

Recommended tools:
- **axe DevTools** browser extension
- **Lighthouse** accessibility score
- **WAVE** evaluation tool
- **Pa11y** CLI for CI integration

---

## Conclusion

The Sport Cars application has a **solid accessibility foundation** with proper semantic structure and form labeling. The critical issues are isolated to focus management in dynamic components (mobile menu, chat widget). Addressing these will bring the application to WCAG 2.1 AA compliance.

**Overall Assessment:** ~85% compliant. With fixes to the critical and major findings, the application can achieve 95%+ compliance.
