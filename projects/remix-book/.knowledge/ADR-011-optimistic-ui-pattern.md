# ADR-011 — Optimistic UI with navigation.formData / fetcher.formData

**Fecha:** 2026-08-05
**Contexto:** Capitulo 11 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de optimistic UI usando `navigation.formData` y `fetcher.formData`/`fetcher.data` para actualizar la UI antes de la respuesta del server, aprovechando la revalidation automatica de Remix para sincronizar.

## Detalle

### El patron

Remix proporciona acceso a los datos del form en progreso sin estado React adicional:

```tsx
// Para Form component (global navigation)
const navigation = useNavigation();
const attachment = navigation.formData?.get('attachment');
const isUploading = attachment instanceof File && attachment.name !== '';

// Para useFetcher (aislado)
const fetcher = useFetcher<{ success: boolean }>();
const isSubmitting = fetcher.state !== 'idle';
const hasFailed = fetcher.data?.success === false;
```

### Cuando aplicar

| Mutacion | Optimistic? | Como |
|----------|-------------|------|
| Create | No | Necesitas id del server para acciones posteriores |
| Update | Si | Mostrar valores ingresados, no deshabilitar submit |
| Delete | Si | `if (isSubmitting) return null` — ocultar item |
| Upload attachment | Si | Mostrar Attachment component aunque no haya terminado |
| Remove attachment | Si | Ocultar Attachment, mostrar file input inmediatamente |

### Manejo de errores

1. **Action devuelve `{ success: false }`** en lugar de throw
2. **Cliente checkea `fetcher.data?.success === false`**
3. **Estilo condicional** (text-red-600) para senialar rollback
4. **No mostrar ErrorBoundary** si podemos dar feedback inline
5. **Loader revalidation** sincroniza automaticamente

### Reglas

- No usar optimistic UI cuando la tasa de error es alta
- No usar cuando necesitas datos del server para acciones posteriores
- Siempre comunicar rollbacks visualmente
- `navigation.formData` es `undefined` si no hay submission activa
- `fetcher.data` persiste entre submissions (no se resetea hasta la proxima)

## Consecuencias

**Positivas:**
- UI mas rapida (feedback instantaneo)
- Sin estado React adicional (no useState, no useReducer)
- Revalidation automatica mantiene sincronizado
- Rollbacks manejados por el framework

**Negativas:**
- Complejidad adicional para errores y rollbacks
- No aplicable a creates (necesitas id del server)
- `if (isSubmitting) return null` puede ser confuso para lectores de pantalla
- `fetcher.data` persiste entre submissions (hay que limpiar manualmente si es necesario)

## Notas

Este patron se apoya en la revalidation automatica de Remix (ADR-005). Sin esa revalidation, el optimistic UI requeriria sincronizacion manual de estado cliente-servidor.
