# Nomad — Brief

## Nombre
Monad (@gonzoblasco/monad)

## Concepto
Un sistema operativo personal en iOS. Una sola app que unifica proyectos, vida, escritura, fotografía y métricas personales en un dashboard privado con IA local.

## Problema que resuelve
Gonzo tiene múltiples facetas digitales dispersas: proyectos de software en GitHub, notas en el workspace, registro fotográfico, actividad física, escritura de ficción. No existe un punto único que las unifique. Cada faceta vive en su propia app, con su propia lógica, sin conexión entre sí.

## Visión
Una app que abre y ves **tu** estado completo: qué proyectos avanzaron, cómo fue tu día, qué escribiste, qué fotos tomaste. Con IA local que analiza patrones y sugiere próximas acciones. Privado. Offline-first. Hecho por y para vos.

## Stack
- **Frontend:** SwiftUI + SwiftData (local) + CoreML (IA local)
- **Backend:** Supabase (sync, auth, storage)
- **Edge:** Supabase Edge Functions (webhooks, push)
- **IA:** Gemma 4 2B via CoreML (local, sin APIs externas)
- **Workspace:** Sincronización bidireccional con el workspace de OpenClaw

## Target
Un solo usuario: Gonzo. Escalable a sharing limitado si algún día tiene sentido.

## Estado
Discovery en curso.
