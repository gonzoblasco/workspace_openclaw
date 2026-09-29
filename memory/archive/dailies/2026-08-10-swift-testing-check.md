# 2026-08-10

## Cron: swift-testing serialization check (thread 86096)

Revisado el pitch "Data-dependent test serialization" (forums.swift.org/t/86096).

**Estado: SIN movimiento relevante desde la última revisión.** Sigue siendo Pitch (no avanzó a proposal), thread abierto, sin aceptación.

- Último post: 2026-06-30 (maartene probándolo con GRDB/SQLite in-memory; grynspan aclaró que no serializa tests no anotados).
- Propuesta en swift-evolution sigue como `NNNN-serialization-dependencies.md` (sin número asignado = no aceptada formalmente).
- Timeline: pitch 2026-04-17, discusión activa hasta 04-20 (debate sobre el operador `*` vs `.everything`, y si deprecar `.serialized`), workgroup meeting 05-04, último movimiento 06-30.

**Implicación para PR swiftlang/swift-testing#1813 (serialización de suites anidadas):** sigue hold-eado. El proposal no avanzó, así que no hay señal de que vaya a dejar obsoleto el PR en el corto plazo. No reactivar todavía. Revisar de nuevo en ~1 mes o si el pitch avanza a proposal.
