# Estándar de Entidades de Kanam OS 🌿

Este documento define cómo se almacenan y gestionan las entidades (personas, empresas, proyectos) para evitar la pérdida de contexto y la redundancia de la búsqueda semántica.

## 📂 Estructura de Almacenamiento
Las entidades viven en: `.knowledge/entities/{categoria}/`

Cada entidad se compone de dos archivos obligatorios:
1. **`{nombre}.md` (The Summary):** Vista humana. Contiene la descripción ejecutiva, el estado actual y los vínculos clave. Se actualiza mediante síntesis.
2. **`{nombre}.jsonl` (The Facts):** Vista de datos. Registro append-only de hechos verificables.

### Formato del `.jsonl`
Cada línea es un objeto JSON independiente:
`{"date": "YYYY-MM-DD", "fact": "Descripción del hecho", "source": "Referencia a sesión/archivo"}`

## 🔄 Ciclo de Vida de la Entidad

### 1. Descubrimiento y Creación
Cuando el sistema detecta una entidad nueva:
- Crea la carpeta (si aplica) y los dos archivos.
- Registra el primer hecho en el `.jsonl`.
- Genera un summary inicial básico.

### 2. Alimentación (Feeding)
Cada vez que surge un dato nuevo y concreto:
- Se agrega una línea al `.jsonl`. **Nunca se borran hechos**, solo se agregan.
- Si el dato es disruptivo o cambia el estado de la entidad, se marca la necesidad de actualizar el `.md`.

### 3. Síntesis (Reconciliation)
Periódicamente (o bajo demanda), el sistema lee el `.jsonl` y regenera el `.md` para reflejar la verdad actual, aplicando el principio: **"supersede, don't delete"** (el hecho más reciente tiene prioridad sobre el antiguo).

---

## 🚀 Guía de Categorías
- **People:** Personas reales, contactos, colaboradores.
- **Companies:** Organizaciones, repositorios, entidades legales.
- **Projects:** Iniciativas concretas, repos, productos, metas.
