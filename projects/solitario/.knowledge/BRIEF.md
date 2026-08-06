# Solitario

Colección de solitarios y puzzles sencillos de naipes.

## Stack

- TypeScript
- HTML5 Canvas
- Vite

## Primer juego

Klondike Solitaire clásico:
- 7 columnas de tableau
- Stock y waste
- 4 foundations (uno por palo)
- Reglas: rojo sobre negro descendente, mismo palo ascendente en foundation

## Estructura

```
src/
  main.ts      # Entry point
  game.ts      # Lógica del juego
  render.ts    # Dibujo en canvas
  deck.ts      # Baraja y utilidades
  types.ts     # Tipos
  input.ts     # (futuro)
public/
```

## Comandos

- `npm run dev` — servidor de desarrollo
- `npm run build` — build de producción
- `npm run preview` — preview del build
