---
name: "db-readonly"
description: "Queries read-only seguras a PostgreSQL y MySQL"
---

# db-readonly

## Descripción
Ejecuta consultas SELECT, WITH y EXPLAIN contra bases de datos PostgreSQL o MySQL. Bloquea INSERT, UPDATE, DELETE, DROP y ALTER para prevenir modificaciones accidentales. Exporta resultados a CSV, TSV o JSON.

## Cuándo usarlo
- Para inspeccionar schemas de tablas antes de escribir una migración
- Para contar rows y verificar que un import de datos se completó
- Para samplear registros y debuggear un issue reportado
- Para exportar resultados de queries a CSV para reportes
- Para ejecutar EXPLAIN en queries lentas y diagnosticar performance

## Workflow
1. Configurar variables de entorno con credenciales de DB (PGHOST, PGDATABASE, etc.)
2. Escribir la consulta SELECT/WITH/EXPLAIN
3. Ejecutar db-readonly con la consulta
4. Recibir resultados en el formato solicitado

## Notas
- Bloquea writes a nivel skill, no solo a nivel de promesa
- Requiere configurar conexión vía environment variables
- Soporta múltiples conexiones (PostgreSQL y MySQL)
