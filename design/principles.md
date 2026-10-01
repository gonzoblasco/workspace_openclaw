# Principios de Diseño de Kanam OS 🌿

Este documento define la filosofía estética y los límites visuales de todo lo que produzca Kanam. No es una guía de gustos, sino un conjunto de **restricciones** para evitar la mediocridad visual y el "estética genérica de IA".

## 🚫 El "AI Look" (Prohibiciones)
Para alejarnos de la apariencia de "chatbot genérico", queda estrictamente prohibido:
- **Gradientes decorativos:** Nada de fondos con degradados suaves y etéreos.
- **El "Morado IA":** Prohibido el uso de púrpuras/morados como color primario por defecto.
- **Radios exagerados:** Nada de botones "pastilla" (pill-shaped) o bordes excesivamente redondeados que resten seriedad.
- **Padding inflado:** Evitar el espaciado excesivo y vacío que busca parecer "moderno" pero sacrifica la densidad de información.
- **Sombras difusas:** Sin sombras suaves y profundas para crear profundidad artificial. La separación se hace con bordes y superficies.

## ✅ Estándares de Calidad (Obligatorios)

### 1. Contraste y Accesibilidad (WCAG 2.2)
- **Contraste verificado:** Todo par texto/fondo debe cumplir el ratio mínimo de 4.5:1 para cuerpo y 3:1 para texto grande.
- **Foco visible:** Todo elemento interactivo debe tener un anillo de foco claro (mínimo 2px) al ser seleccionado.
- **Más que color:** El estado (error, éxito, aviso) nunca debe depender solo del color; debe ir acompañado de un icono o texto explícito.

### 2. Jerarquía y Estructura
- **Tipografía funcional:** 
  - *Display:* Para títulos y énfasis.
  - *Body:* Para lectura prolongada.
  - *Mono:* Para datos, rutas y código.
- **Alineación Precisa:** La consistencia en la alineación no se negocia. Un pixel de desfase es un error.
- **Whitespace como Feature:** El espacio en blanco se usa para agrupar y separar conceptos, no para rellenar huecos.

### 3. Semántica de Color
El color tiene una función, no una decoración:
- **Verde:** Éxito / Confirmación.
- **Ámbar:** Atención / Advertencia.
- **Rojo:** Peligro / Error Crítico.
- **Neutrales:** Estructura y soporte.

---

*Actualizado el 2026-10-01. Fuente: Rescate de ADR-047 y evolución Kanam OS.*
