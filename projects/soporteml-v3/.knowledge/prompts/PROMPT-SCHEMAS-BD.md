# Prompt: Schemas de BD + Edge Functions de SoporteML (para Lovable)

> **Cuándo usar:** para pedirle a Lovable la documentación técnica del backend (schemas de Supabase + edge functions + integraciones).
> **Estado:** PENDIENTE DE EJECUTAR (Gonzo lo pide cuando renueve créditos, ~2026-08-08).
> **Nota:** el prompt pide SOLO nombres de variables de entorno, nunca valores secretos.

---

```
Necesito que me pases la documentación técnica completa del backend de SoporteML para poder reconstruir la base de datos y la lógica de servidor en una nueva versión del proyecto.

Por favor, generá un documento Markdown con:

1. **Schemas de la base de datos (Supabase/PostgreSQL)**
   - Todas las tablas, con sus columnas, tipos, constraints (PK, FK, UNIQUE, NOT NULL, DEFAULT).
   - Las relaciones entre tablas (qué FK apunta a qué tabla).
   - Los índices y políticas de seguridad (RLS - Row Level Security) si existen, con el detalle de qué políticas aplican a qué rol.
   - Los triggers, funciones SQL o stored procedures si hay.
   - Los enums o tipos custom si se usan.

2. **Edge Functions (Supabase)**
   - Lista de todas las edge functions existentes.
   - Para cada una: su propósito, los endpoints/rutas que expone, los métodos HTTP, los parámetros de entrada y la forma de la respuesta.
   - Qué integraciones externas usan (Mercado Libre API, OpenAI, etc.) y cómo se autentican (tokens, headers).

3. **Integraciones externas**
   - Detalle de la integración con la API de Mercado Libre: qué endpoints se consumen, qué datos se sincronizan (preguntas, productos, stock, envíos, garantías), y con qué frecuencia.
   - Cualquier otra integración (IA, notificaciones, email, etc.).

4. **Autenticación y roles**
   - Cómo funciona el login (Supabase Auth, OAuth con Google, etc.).
   - Los roles y permisos (admin, vendedor, super admin) y qué puede hacer cada uno.

5. **Variables de entorno**
   - Lista de las variables de entorno necesarias (sin valores secretos, solo los nombres y para qué sirven), para poder configurar el entorno de la nueva versión.

Devuelve todo en un único documento Markdown, organizado por secciones, listo para ser usado como referencia técnica para reconstruir el backend. Si algo no existe o no aplica, indicá "No aplica" en esa sección.
```
