# ADR-010 — File Upload with Streaming and Protected Resource Routes

**Fecha:** 2026-08-05
**Contexto:** Capitulo 10 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de file upload con `unstable_parseMultipartFormData` + upload handlers compuestos para streaming de archivos, y resource routes protegidos para servir archivos privados.

## Detalle

### Componentes del patron

1. **Upload handler compuesto** (`attachments.server.ts`):
   ```ts
   const fileHandler = unstable_createFileUploadHandler({
     directory: './attachments',
     avoidFileConflicts: true,
     maxFileSize: 30_000_000,
   });

   const attachmentsUploadHandler: UploadHandler = async (args) => {
     if (args.name !== 'attachment' || !args.filename) return null;
     const file = await fileHandler(args);
     if (!file) return null;
     return typeof file === 'string' ? file : file.name;
   };

   export const uploadHandler = unstable_composeUploadHandlers(
     attachmentsUploadHandler,
     unstable_createMemoryUploadHandler(),
   );
   ```

2. **Action con multipart condicional:**
   ```ts
   const contentType = request.headers.get('content-type');
   if (contentType?.toLowerCase().includes('multipart/form-data')) {
     formData = await unstable_parseMultipartFormData(request, uploadHandler);
   } else {
     formData = await request.formData();
   }
   ```

3. **Resource route protegido para servir archivos:**
   ```ts
   export async function loader({ request, params }: LoaderFunctionArgs) {
     const userId = await requireUserId(request);
     const expense = await db.expense.findUnique({
       where: { id_userId: { id, userId } }
     });
     if (!expense || !expense.attachment) throw new Response('Not found', { status: 404 });
     return buildFileResponse(expense.attachment);
   }
   ```

4. **Cleanup de archivos:**
   - Al eliminar expense: borrar archivo del filesystem
   - Al remover attachment: borrar archivo + setear attachment a null en DB
   - Usar `fs.unlinkSync()` con try/catch

### Reglas de seguridad

1. NO guardar archivos de usuarios en `public/`
2. Usar `avoidFileConflicts: true` para evitar colisiones de nombres
3. Autenticar en CADA resource route que sirva archivos
4. Query por `id_userId` compuesto (usuario solo ve sus archivos)
5. Limpiar archivos huerfanos al eliminar entidades

### Cuando usar streaming vs memory

| Tamaño | Approach |
|--------|----------|
| < 1MB | Memory upload handler (default) |
| 1-30MB | File upload handler con streaming |
| > 30MB | Custom handler + third-party service |

## Consecuencias

**Positivas:**
- Streaming evita memory overflow con archivos grandes
- Archivos protegidos detras de autenticacion
- Nombres unicos (avoidFileConflicts)
- Composicion de handlers para diferentes tipos de datos

**Negativas:**
- APIs con prefijo `unstable_` (pueden cambiar)
- Complejidad adicional vs `request.formData()` simple
- Requiere cleanup manual de archivos huerfanos
- Filesystem local no escala a produccion

## Notas

Para produccion, reemplazar `unstable_createFileUploadHandler` con un custom handler que streamee a S3/Cloudinary. El resto del patron (resource route protegido, cleanup) se mantiene igual.
