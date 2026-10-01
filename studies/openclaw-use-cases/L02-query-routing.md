# Lección 2: Enrutamiento de Consultas Entrantes con Personas Personalizadas
Clase: OpenClaw Use Cases

## Concepto Central
Evitar la "dilución del prompt" mediante la especialización. En lugar de un único agente monolítico con instrucciones infinitas, OpenClaw utiliza un sistema de enrutamiento que asigna la consulta a una **Persona** experta según la intención detectada.

## El Flujo de Enrutamiento
1. **Detección de Intención (Etapa 1)**: Un modelo ligero (Tier 1) analiza la consulta y determina el dominio (ej. Facturación, Soporte Técnico, SRE).
2. **Asignación de Persona**: Basado en el `routes.yaml`, se selecciona la Persona que posee el contexto y las herramientas necesarias.
3. **Ejecución Especializada (Etapa 2)**: El agente final procesa la solicitud usando solo el set de instrucciones y herramientas permitidas para esa Persona.

## Detalles Técnicos Clave
- **Aislamiento de Herramientas**: Cada Persona tiene su propia lista blanca de herramientas. Esto permite que varias personas lean datos comunes, pero solo una tenga permisos de escritura críticos.
- **Confidence Score**: El enrutador devuelve un puntaje de confianza. Si es inferior al umbral (threshold), el sistema puede pedir aclaraciones al usuario o derivar a un agente generalista.
- **Persona Handoff**: Capacidad de transferir la sesión de una persona a otra si la conversación evoluciona hacia un dominio diferente.

## Notas
El enrutamiento reduce drásticamente las alucinaciones y el consumo de tokens, ya que el modelo final no recibe instrucciones irrelevantes para la tarea actual. Es la base de la escalabilidad de OpenClaw en entornos empresariales.
