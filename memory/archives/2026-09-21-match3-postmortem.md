# Post-Mortem: Match‑3 Game Experiment (Phaser.js)

## 1. Contexto y Objetivo
El objetivo fue crear un prototipo rápido de un juego de puzzle Match‑3 basado en la web utilizando **Phaser 3**. Se buscaba una implementación funcional que sirviera como base para un proyecto más ambicioso.

## 2. Logros Técnicos (Lo que se implementó)
A pesar de haber sido un experimento corto, se logró desarrollar un núcleo mecánico completo:
- **Estructura de Proyecto:** Scaffold limpio con separación entre `public/` (distribución) y `src/` (fuente).
- **Lógica de Grid:** Implementación de una matriz 8 × 8 con generación aleatoria de colores.
- **Interacción:** Sistema de selección de fichas y validación de adyacencia para intercambios (swaps).
- **Algoritmos de Match:** Detección recursiva de líneas horizontales y verticales de 3 o más fichas del mismo color.
- **Física y Gravedad:** Implementación de "colapso" de columnas donde las fichas superiores caen para llenar huecos y se generan nuevas fichas en la parte superior.
- **Cascadas:** Sistema de recursividad que detecta nuevos matches automáticamente después de un colapso.
- **Feedback Visual:** Animaciones mediante `tweens` para swaps, desvanecimientos y caídas, junto con un contador de puntuación en tiempo real.

## 3. Lecciones Aprendidas (Datos y "Jugos")

### Sobre Phaser 3 y el despliegue:
- **Rutas de Servidor:** Se identificó un problema común de 404 al servir la carpeta `public` aisladamente mientras el script referenciaba `../src/main.js`. La solución fue unificar el script en el directorio servido o ajustar la ruta absoluta.
- **Rendimiento de Tweens:** El uso de `tweens.timeline` es fundamental para coordinar la gravedad y las cascadas, asegurando que el juego no intente calcular matches mientras las fichas aún se están moviendo.

### Sobre el Flujo de Trabajo (Agentic):
- **Iteración Rápida:** El ciclo *Idea $\rightarrow$ Scaffold $\rightarrow$ Implementación de Lógica $\rightarrow$ Prueba de Usuario* funcionó eficientemente.
- **Cierre Limpio:** La capacidad de eliminar el proyecto de raíz una vez decidido el abandono mantiene el workspace sano.

## 4. Evaluación de Habilidades (Kanam)

| Habilidad | Evaluación | Nota |
|---|---|---|
| **Arquitectura Web** | ⭐⭐⭐⭐⭐ | Scaffold correcto y resolución efectiva de problemas de rutas/servidor. |
| **Lógica de Juego** | ⭐⭐⭐⭐ | Implementación sólida de mecánicas Match‑3, aunque simplificada en colores básicos. |
| **Sintaxis JS/Phaser** | ⭐⭐⭐⭐⭐ | Uso correcto de la API de Phaser 3 y manejo de estados de escena. |
| **Adaptabilidad** | ⭐⭐⭐⭐⭐ | Respuesta inmediata al cambio de dirección del usuario (borrado del proyecto). |

## 5. Estado Final
**Proyecto:** Eliminado.  
**Valor Extraído:** Código base para mecánicas de grid y cascada, conocimiento sobre despliegue de assets en Phaser.  
**Sugerencia para el futuro:** Si se retoma un juego similar, iniciar con un `package.json` y un bundler (Vite/Webpack) desde el día 1 para evitar problemas de rutas y facilitar la carga de assets complejos.
