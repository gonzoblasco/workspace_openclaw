# Borrador feedback - astryx PR #5414

> fix(theme): give syntax punctuation its own AA-passing colour - @HelloOjasMutreja
> Estado: OPEN, sin reviews humanos.

---

## Comentario propuesto (en inglés, para el PR)

Hi @HelloOjasMutreja, nice catch - `--color-syntax-punctuation` inheriting a WCAG-exempt disabled token for always-active text is exactly the class of bug that slips through. The measurement (resolving `light-dark()`/`var()` the same way the badge guard does) and the regression test are solid.

I verified the headline numbers independently (WCAG 2.1 relative luminance, 4.5:1): neutral light/dark 4.89:1 / 7.57:1, chocolate 4.84:1 / 6.12:1, matcha 5.19:1 / 7.02:1 all clear AA. Good.

Two things I'd want considered before this lands:

**1. The shared default now makes punctuation visually identical to comments.**
The new default points `--color-syntax-punctuation` at `--color-text-secondary`, which is the same token `--color-syntax-comment` already uses. For the themes that inherit the default (butter, gothic, stone, y2k), punctuation now renders in the exact same colour as comments. That's a semantic distinction the syntax highlighter used to preserve (dim grey for punctuation vs something else for comments), and it's lost in one move. It clears AA, so it's not a correctness issue - but it's a visual-regression concern worth a deliberate decision: either confirm punctuation-as-comment-colour is intended for those themes, or give punctuation its own token so the two roles stay distinguishable. Worth checking against the before/after in those four themes, since they weren't part of the measured three.

**2. The resolver only handles hex - it's worth failing loud when it can't resolve.**
`resolve()` returns `null` for anything that isn't `#rgb`/`#rrggbb`/`#rrggbbaa`. Today every theme ships hex so the pairs all resolve, and the `expect(rows).toHaveLength(14)` guard catches a theme that stops resolving - but the failure message just says "expected 14, got 12" with no hint of *which* theme or *why*. If a future theme defines a colour in `oklch()`/`hsl()`/`rgb()`, the guard trips without telling anyone the resolver doesn't understand the format. A one-line `throw` (or a descriptive assertion) in `resolve()` when it hits an unsupported format would make the next person's debugging much faster. Same spirit as the "guards the resolver itself" test you already wrote - just one step more explicit.

Minor: consider reusing the badge guard's resolver instead of a second copy in `scripts/`, so the `light-dark()`/`var()` indirection logic has a single home. If the badge and syntax guards drift, one will silently cover a format the other doesn't.

Overall a clean, well-scoped fix. The two asks are: make a deliberate call on punctuation-vs-comment colour identity for the default themes, and make the resolver fail loud on unsupported colour formats.

---

## Notas internas para Gonzo

- **Verificado de forma independiente:** los ratios del PR (4.89/7.57 neutral, 4.84/6.12 chocolate, 5.19/7.02 matcha) son correctos según WCAG 2.1. Todos limpian AA.
- **Punto 1 (el de mayor peso):** el cambio hace que punctuation y comment sean **el mismo color** en los 4 themes que heredan el default (butter, gothic, stone, y2k). El changeset del propio PR lo confirma ("used for --color-syntax-comment too"). Es una pérdida de distinción semántica del syntax highlighting. Verificado en el diff + changeset.
- **Punto 2:** el resolver solo acepta hex (`/^#[0-9a-f]{3,8}$/i`, verificado). Hoy los themes usan hex así que funciona, pero el guard `toHaveLength(14)` falla con mensaje poco claro si un theme futuro usa oklch/hsl/rgb. Sugerencia: throw descriptivo.
- **Punto menor:** reusar el resolver del badge guard (#4446) en vez de duplicarlo - el propio changeset dice que es "the pattern from #4446's badge contrast guard", así que ya existe el resolver que podrían compartir.
- **Tono:** constructivo, validando que es un fix limpio. Punto 1 es el de mayor sustancia (regresión visual potencial).
- **Estado:** sin reviews humanos aún - este sería el primero.
