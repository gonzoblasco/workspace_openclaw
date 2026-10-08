# Design Captures Directory

Esta carpeta contiene capturas manuales de diseño que sirven como especificación visual para el pixel-diff.

## Formatos soportados
- `.png` - Capturas de pantalla de alta fidelidad
- `.jpg` - Fotos o capturas con compresión
- `.webp` - Formatos eficientes para web

## Estructura recomendada
```
design-captures/
├── card.png           # Componente Card
├── home.png           # Página Home
├── checkout.png        # Página Checkout
└── navigation.png     # Componente Navigation
```

## Uso
```bash
# Modo comp: comparar captura vs realidad
npx pixel-diff --mode comp \
  --design ./design-captures/card.png \
  --url http://localhost:3000 \
  --route /card

# Modo interactivo: preguntar valores al usuario
npx pixel-diff --mode comp \
  --design ./design-captures/home.png \
  --url http://localhost:3000 \
  --interactive
```

## Generación
Estas capturas pueden venir de:
- Figma (exportadas manualmente)
- Sketch
- Adobe XD
- Captura de pantalla de otra app
- Diseño en papel escaneado

*Nota: En el futuro, este directorio podría ser reemplazado por la API de Figma.*
