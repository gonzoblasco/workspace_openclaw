Domain / Role:
DSD - Software & AI/ML Engineering. Software engineer with 10+ years
building production web applications in TypeScript and React, specialised
in digital accessibility on enterprise component libraries.

Goal:
Diagnose and fix a screen-reader announcement defect in a React combobox
component, where the live-region message fires on every keystroke instead
of only when the active section changes, which makes VoiceOver repeat the
section name and override its native per-item announcement.

Starting materials:
A small React and TypeScript project created from scratch for this task:
one combobox component with two grouped sections of options, a live region
that announces the current section, a unit test asserting the announcement
count, and a README describing the expected accessibility behaviour. The
defect is present and the fix is not included.

Steps (with the apps for each):
1. Run the failing test in Terminal and read which assertion breaks and
   how many announcements the component produced (VS Code).
2. Read the component's live-region logic and locate where the announcement
   is triggered, following the state that changes on each keystroke (VS Code).
3. Confirm the cause: the effect depends on the active option rather than
   on the active section, so every arrow-key move re-announces the section
   (VS Code).
4. Apply a minimal fix: gate the announcement to changes of the active
   section only, leaving the per-item announcement to the native behaviour
   (VS Code).
5. Re-run the unit test, then the full suite, and confirm the announcement
   count matches the expected one (Terminal).

Deliverable:
The corrected component source file, saved in the project directory, with
the full test suite passing and the announcement count reduced from one per
keystroke to one per section change.

Apps: VS Code, Terminal
