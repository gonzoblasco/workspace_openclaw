# Estudio: React Essential (roadmap.sh/ai)

Objetivo: repasar bases de React/JS moderno de abajo hacia arriba, con foco en
preparación para entrevistas que empiecen desde los fundamentals.

Método: Gonzo pasa una sección → Kanam la enseña (fundamentos + trampas) →
turno de evaluación tipo entrevista → corrección con criterio de entrevistador.
Se guarda el resultado de cada turno.

Fuente de las guías: `https://roadmap.sh/ai/...` (client-side; se lee con reader
`r.jina.ai` porque el fetch directo devuelve "Please wait...").

## Progreso

| Sección | Estado | Nota |
|---|---|---|
| modern-javascript-for-react | 🟡 en curso | Sección 1 (arrow fns, destructuring, spread/rest, array methods, template literals, `\|\|`/`??`/`?.`) |

## Resultados de evaluación

### Sección 1 - turno 1 (2026-10-25)
| # | Tema | Resultado |
|---|---|---|
| 1 | Arrow function inline rompe `React.memo` | ⚠️ parcial - "cada instancia del memo" impreciso; falta: se re-crea en cada render del **padre**, comparación shallow de punteros, `useCallback` + deps (stale closure) |
| 2 | `\|\|` vs `??` | ✅ correcta |
| 3 | Spread shallow + mutación anidada | ❌ no vio el bug - faltaba: `prev.user.name = "x"` muta in-place, spread superficial deja `user` con misma referencia → `useEffect` no dispara, UI inconsistente. Cada nivel necesita su spread, o `structuredClone` / estado normalizado |
| 4 | `sort()` muta in-place | ❌ confundió con "cambiar el index" - fix: `[...arr].sort()` / `slice().sort()` / `toSorted()`; nunca mutar props |
| 5 | Zero rendering bug (`0 &&`) | ❌ no lo recordaba - `0` es falsy pero número válido → React lo pinta en el DOM. Fix: `length > 0 &&` |
| 6 | Rest props | ✅ correcta (le faltaba la aplicación: wrapper `<Input>` transparente que reenvía atributos nativos) |

**Debilidad central detectada:** mutación vs. identidad referencial (ítems 3, 4, 5 y 1).
Regla a fijar: *"React detecta cambios comparando referencias. Si mutás in-place, React no se entera."*

### Sección 1 - turno 2 (2026-10-25)
| # | Tema | Resultado |
|---|---|---|
| 1 | Deps de `useEffect` vs. referencias | ⚠️ knew el fix (spread por nivel) pero no la explicación: dep apuntaba a un subárbol sin cambios → `Object.is` igual → effect no corre. Fix: dep = expresión exacta que querés observar |
| 2 | Updater funcional | ✅ bien - le falta el caso "dos updates en el mismo tick se pierde un incremento" |
| 3 | Batched updates / stale closure | ❌ no lo tenía - `setA(a+1); setB(b+1)` → ambos en 1 (no 2); React 18+ batchea. Bug real cuando dos valores dependen del mismo dato → derivar en render, no sincronizar con dos setters |
| 4 | Detección de mutación accidental | ❌ no lo tenía - ESLint (`react/jsx-no-bind`, `no-param-reassign`, `exhaustive-deps`), `Object.freeze` en dev, `readonly` de TS, `structuredClone`, immer/RTK, RTL tests, disciplina de repo |
| 5 | Componente `<Input>` | ❌ - confused uso con implementación; le faltan controlled/uncontrolled, `useId`, a11y (`htmlFor`, `aria-invalid`, `aria-describedby`, `role="alert"`), y el orden del spread de props nativas |

**Debilidad central (confirmada):** modelo mental de React - batching, identidad referencial, inmutabilidad de props/state. No es JS lo que falla.

Pendiente: deep dive de batching + stale closures + detección de mutación; repetir turno 2 con set nuevo.
