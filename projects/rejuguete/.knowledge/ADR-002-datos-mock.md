# ReJuguete — ADR-002: Datos Mockeados en V1

## Contexto

En v1 no tenemos backend ni base de datos. Necesitamos una forma de mostrar el producto funcionalmente sin persistencia real.

## Decisión

Usar un archivo `lib/data.ts` con datos mockeados (array de objetos) que simula la base de datos. Los formularios de "publicar" agregan al array en memoria (se pierde al recargar).

## Razones

- Desarrollo más rápido: cero setup de DB
- Permite iterar diseño y UX sin depender de infraestructura
- Los tipos y estructura de datos ya quedan definidos para migración futura
- Podemos demostrar el flujo completo (ver catálogo, filtrar, ver detalle, publicar)

## Consecuencias

- Los datos nuevos se pierden al recargar la página
- No hay persistencia entre usuarios
- En v2 migramos a SQLite con Prisma

## Estado

Aceptado.
