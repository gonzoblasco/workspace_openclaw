# Informe de accesibilidad — pro-motors.com.ar

**Fecha:** 2026-11-04  
**Puntaje:** 0/100 (F)  
**Problemas que bloquean una tarea:** 24

---

## Qué significa este número

Una persona con lector de pantalla recorre este sitio y **no puede completar una compra**.
No es una cuestión de estilo ni de cumplimiento formal: los productos del catálogo
existen, para el lector, como diez enlaces sin nombre.

## Lo que escucha una persona

Fragmento real del recorrido, tal como lo pronuncia el lector:

```
button     ← un botón sin nombre — no se puede saber qué hace al pulsarlo
link       ← un enlace sin nombre — no se puede saber a dónde lleva
button     ← un botón sin nombre — no se puede saber qué hace al pulsarlo
button     ← un botón sin nombre — no se puede saber qué hace al pulsarlo
link       ← un enlace sin nombre — no se puede saber a dónde lleva
link       ← un enlace sin nombre — no se puede saber a dónde lleva
image      ← una imagen sin nombre — la persona no sabe qué muestra
link       ← un enlace sin nombre — no se puede saber a dónde lleva
```

## Problemas, por impacto comercial

### El catálogo de productos es inaccesible

*Bloquea una venta · 10 elementos afectados*

Diez enlaces del catálogo no tienen texto: el único contenido es un ícono. Una persona con lector de pantalla escucha "enlace" diez veces y no puede distinguir una moto de otra.

### Los filtros no se pueden identificar

*Bloquea una tarea · 1 elemento afectado*

El selector principal no tiene nombre accesible. La persona no sabe si elige marca, modelo o año.

### No hay forma de saltar al contenido

*Fricción en todo el sitio · 33 elementos afectados*

La página no tiene una región principal ni secciones identificables. Quien navega por landmarks —la vía más rápida— recorre el menú completo en cada página sin llegar nunca al producto.

### No se puede ampliar el texto

*Excluye a personas con baja visión · 1 elemento afectado*

El viewport bloquea el zoom. Quien necesita agrandar para leer no tiene ninguna alternativa.

### Defectos menores

*Calidad · 4 elementos afectados*

Tres roles ARIA inapropiados y un encabezado vacío. No bloquean una tarea, pero degradan la experiencia.

## Qué se puede hacer

Los cinco grupos tienen solución conocida y ninguno requiere rediseñar el sitio:

1. **Catálogo:** cada enlace de producto necesita el nombre del producto como texto (visible u oculto para la vista, presente para el lector), no un ícono solo.
2. **Filtros:** el selector necesita una etiqueta que diga qué se elige.
3. **Navegación:** envolver el contenido en una región principal y nombrar las secciones. Es el cambio más barato y el de mayor efecto.
4. **Zoom:** quitar `maximum-scale` del viewport. Una línea.
5. **Menores:** corregir los roles ARIA y el encabezado vacío.

## Alcance de este informe

Este informe mide **una página**, no el sitio completo, y no certifica cumplimiento (WCAG u otro).
- Las comprobaciones automáticas detectan aproximadamente un tercio de los defectos de accesibilidad. Sigue siendo necesario probar a mano con teclado y un lector de pantalla real.
- El recorrido proviene de un lector de pantalla virtual, no de VoiceOver ni NVDA: refleja lo que declara el DOM, no cómo temporiza sus anuncios un lector concreto.
- El contenido detrás de una interacción (modales, pestañas, menús) solo se analiza si está abierto al cargar.
- Se analiza únicamente la URL indicada; no se siguen los enlaces.

---

Generado por Preflight · lector: virtual (Guidepup) 0.32.1