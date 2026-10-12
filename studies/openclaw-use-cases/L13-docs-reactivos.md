# Módulo 3 · Lección 13 de 30: Actualización Reactiva de Documentación Interna

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 3 - Ingesta Dirigida por Eventos
**Lección:** 13 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Cuando un webhook entrega una carga útil confirmada y filtrada, el siguiente desafío es **sincronizar ese cambio con los registros vivos** de la organización. Mantener la documentación técnica al día suele recaer en tareas manuales que se postergan. La solución: convertir cada evento validado en una **mutación granular** sobre archivos Markdown, asegurando que esquemas, endpoints y catálogos reflejen el estado real del sistema.

La actualización reactiva **no reescribe documentos enteros**: un reemplazo indiscriminado destruye contexto histórico, sobrescribe anotaciones humanas y satura el control de versiones. El agente debe actuar **quirúrgicamente**: localizar la sección exacta, verificar diferencias con un **diff semántico** y aplicar cambios **respetando el frontmatter**.

---

## Anatomía del pipeline de actualización reactiva

Se activa cuando el módulo de extracción emite un payload normalizado. Cuatro etapas secuenciales: **resolución de ruta de destino → lectura y parseo → mutación dirigida por AST → persistencia atómica con control de versiones**. El flujo desacopla recepción del evento del formato de almacenamiento final.

### Mutación dirigida por AST (no regex)

Manipular Markdown con expresiones regulares o concatenación falla cuando hay bloques de código, listas anidadas o tablas: produce cierres de bloques rotos y títulos desalineados. Por eso se opera sobre un **árbol de sintaxis abstracta** - deserializar con **unified/mdast**, modificar el subárbol objetivo y recompilar a Markdown con un formateador determinista.

### Localización semántica y mutación

El núcleo ubica la sección por su **encabezado**, identifica el contenido y reemplaza/inserta sin tocar explicaciones contextuales. Ejemplo: un webhook notifica que se agregó el parámetro `tax_id` al endpoint `POST /v1/invoices`. La rutina (Node.js) carga el archivo, transforma la tabla bajo `### Parámetros de Creación` y escribe:

```typescript
import fs from 'node:fs/promises';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkStringify from 'remark-stringify';
import remarkGfm from 'remark-gfm';
import type { Root, Heading, Table, TableRow } from 'mdast';

interface ParameterPayload { name: string; type: string; required: boolean; description: string; }

export async function syncEndpointParameters(
  filePath: string, targetSection: string, newParam: ParameterPayload
): Promise<boolean> {
  const content = await fs.readFile(filePath, 'utf-8');
  const processor = unified().use(remarkParse).use(remarkGfm).use(remarkStringify);
  const ast = processor.parse(content) as Root;

  let inTargetSection = false;
  let targetTable: Table | null = null;
  let sectionHeadingDepth = 0;

  for (let i = 0; i < ast.children.length; i++) {
    const node = ast.children[i];
    if (node.type === 'heading') {
      const heading = node as Heading;
      const headingText = heading.children
        .filter(c => c.type === 'text').map(c => ('value' in c ? c.value : '')).join('');
      if (headingText.trim().toLowerCase() === targetSection.toLowerCase()) {
        inTargetSection = true; sectionHeadingDepth = heading.depth; continue;
      } else if (inTargetSection && heading.depth <= sectionHeadingDepth) {
        inTargetSection = false; break;
      }
    }
    if (inTargetSection && node.type === 'table') { targetTable = node as Table; break; }
  }
  if (!targetTable) {
    throw new Error(`No se localizó una tabla válida bajo el encabezado "${targetSection}"`);
  }

  const existingRowIndex = targetTable.children.findIndex((row, idx) => {
    if (idx === 0) return false;
    const cell = row.children[0];
    const cellText = cell?.children[0]?.type === 'text' ? cell.children[0].value : '';
    return cellText.trim() === newParam.name;
  });

  const formattedRow: TableRow = {
    type: 'tableRow',
    children: [
      { type: 'tableCell', children: [{ type: 'text', value: newParam.name }] },
      { type: 'tableCell', children: [{ type: 'text', value: `\`${newParam.type}\`` }] },
      { type: 'tableCell', children: [{ type: 'text', value: newParam.required ? '**Sí**' : 'No' }] },
      { type: 'tableCell', children: [{ type: 'text', value: newParam.description }] },
    ]
  };
  if (existingRowIndex > 0) targetTable.children[existingRowIndex] = formattedRow;
  else targetTable.children.push(formattedRow);

  const updatedMarkdown = processor.stringify(ast);
  if (updatedMarkdown === content) return false;

  // Escritura atómica
  const tempPath = `${filePath}.tmp.${Date.now()}`;
  await fs.writeFile(tempPath, updatedMarkdown, 'utf-8');
  await fs.rename(tempPath, filePath);
  return true;
}
```

La función **no altera** párrafos introductorios, bloques de advertencia ni ejemplos `curl` posteriores. Si la tabla no contiene el parámetro, inserta fila; si ya figuraba, sincroniza tipo/descripción sin alterar el orden.

> **PITFALL del curso (correcto):** escribir directo con `fs.writeFile` en alta concurrencia puede producir archivos truncados si el proceso se interrumpe. Usar **archivo temporal + `fs.rename`** (atómico en POSIX).

---

## Preservación de frontmatter

Generadores de sitios (Docusaurus, VitePress, Astro) dependen del **YAML frontmatter** (enrutamiento, título, tags, fecha). Al parsear con AST hay que **separar el bloque de metadatos** del árbol markdown para no transformar campos tipados en texto plano.

```markdown
---
title: Facturación y Cobros
sidebar_position: 4
last_synced: 2025-01-10T14:32:00Z
auto_generated_sections:
  - parameters
  - error_codes
---
# Facturación y Cobros
```

Con **gray-matter**: extraer el frontmatter, validar que la sección a mutar esté listada en `auto_generated_sections`, mutar el AST y recomponer.

```typescript
import matter from 'gray-matter';

export function prepareDocumentForMutation(rawFileContent: string, requestedSection: string) {
  const parsed = matter(rawFileContent);
  const metadata = parsed.data;
  const allowedSections: string[] = metadata.auto_generated_sections || [];
  if (!allowedSections.includes(requestedSection)) {
    throw new Error(`La sección "${requestedSection}" está protegida y no admite actualizaciones automáticas por evento.`);
  }
  metadata.last_synced = new Date().toISOString();
  return {
    contentWithoutFrontmatter: parsed.content,
    updatedFrontmatter: metadata,
    rebuild: (newMarkdownContent: string) => matter.stringify(newMarkdownContent, metadata)
  };
}
```

> **REMEMBER del curso (correcto):** un agente reactivo solo debe modificar secciones **explícitamente declaradas como autogeneradas** en los metadatos. Si un webhook intenta mutar una sección no autorizada, la operación se **rechaza y registra** en logs de auditoría.

### Check your understanding
**Un webhook notifica que un endpoint eliminó un parámetro obsoleto. ¿Estrategia recomendada?**
- [x] **Transformar el Markdown a AST, localizar el nodo de la tabla bajo el encabezado objetivo, mutar las filas y serializar de vuelta.**

---

## Control de versiones y trazabilidad

Tras mutar, el cambio debe quedar en el historial de Git. Tres pasos obligatorios:

1. **Inspección de diferencias reales:** `git diff --exit-code docs/api/invoices.md` antes de commitear; si no hay cambios efectivos (payload idéntico a lo documentado), terminar sin contaminar el log.
2. **Autoría estructurada:** autor dedicado (`OpenClaw Bot <bot@openclaw.internal>`), no un desarrollador ni un usuario genérico.
3. **Mensaje con el ID del evento:** trazabilidad bidireccional webhook ↔ commit.

```bash
git add docs/api/invoices.md
git -c user.name="OpenClaw Documentation Agent" \
    -c user.email="agent-docs@internal.domain" \
    commit -m "docs(api): sincronizar parámetros de POST /v1/invoices [event: evt_984fbc21]"
git push origin main
```

Si el push falla por concurrencia, **reintento con rebase**:

```typescript
import { exec } from 'node:child_process';
import { promisify } from 'node:util';
const execAsync = promisify(exec);

export async function commitAndPushDocs(filePath: string, commitMessage: string, maxRetries = 3): Promise<void> {
  await execAsync(`git add ${filePath}`);
  try {
    await execAsync('git diff --cached --quiet');
    return; // sin cambios en staging
  } catch { /* hay cambios */ }
  await execAsync(`git -c user.name="OpenClaw Docs" -c user.email="docs-bot@internal" commit -m "${commitMessage}"`);
  let attempts = 0;
  while (attempts < maxRetries) {
    try { await execAsync('git push origin main'); return; }
    catch (err) {
      attempts++;
      if (attempts >= maxRetries) throw new Error(`Fallo definitivo al empujar cambios: ${(err as Error).message}`);
      await execAsync('git pull --rebase origin main');
    }
  }
}
```

> **TIP del curso (correcto):** con protección de rama / PR obligatorio, configurar al agente para crear una rama temporal `docs/sync-[timestamp]` y abrir **PR automatizado** con etiqueta `automated-docs`.

---

## Manejo de conflictos y drift documental

**Drift documental** = la especificación real y la doc divergen (cambios manuales sin webhook, o eventos desordenados). Dos reglas de validación en ingesta:

| Situación | Comportamiento | Justificación |
|---|---|---|
| Parámetro nuevo | Inserta fila al final de la tabla | Coherencia sin alterar orden previo |
| Tipo de dato modificado | Actualiza celda, mantiene descripción existente | Preserva anotaciones humanas |
| Parámetro eliminado | Etiqueta `[Obsoleto]` o elimina según política | No rompe integraciones de clientes |
| Sección objetivo no encontrada | Alerta al log de auditoría, no modifica | Evita secciones huérfanas |

Si un webhook referencia un endpoint sin archivo creado, el agente **no adivina**: genera un **borrador en staging** y notifica para que un operador defina la taxonomía.

---

## Resumen

Actualización reactiva de documentación sobre **AST** en lugar de cadenas planas: precisión quirúrgica (modifica tablas/notas sin tocar introducciones), preservación estricta de frontmatter y confirmaciones atómicas en Git → cambios **auditables, reproducibles, sin intervención manual**.

**UP NEXT · Lección 14 de 30:** *Alertas Automatizadas Frente a Errores Críticos*. Faltan **2 lecciones** para cerrar el Módulo 3.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo evita OpenClaw que dos webhooks casi simultáneos corrompan el mismo Markdown?
2. ¿Por qué un parser AST es preferible a regex para tablas técnicas?
3. ¿Qué pasa si el webhook muta una sección no declarada como autogenerada?
4. ¿Cómo se maneja la eliminación de parámetros sin desorientar a usuarios de versiones anteriores?

(Anotadas para profundizar. La #2 y #3 las responde el material; la #1 es un agujero real: el curso **no** resuelve la concurrencia de dos writers sobre el mismo archivo.)

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto** (estilo L08/L10/L12). Todo lo metodológico aplica:

- ✅ **AST en vez de regex** para mutar Markdown estructurado: correcto y central (regex rompe bloques/tablas).
- ✅ **Escritura atómica (tmp + `rename`)**: correcto y POSIX-correcto (PITFALL válido).
- ✅ **Preservar frontmatter** separándolo del cuerpo antes de mutar: correcto (riesgo real de degradar metadatos tipados).
- ✅ **Allowlist de secciones autogeneradas** (`auto_generated_sections`): correcto, evita sobrescribir prosa humana.
- ✅ **`git diff --exit-code`** antes de commitear (no ensuciar el log con no-cambios) y **autoría dedicada** (`-c user.name/email`): buenas prácticas reales de git.
- ✅ **Reintento con `pull --rebase`** ante push fallido: patrón correcto (aunque naive vs. force-push/races).
- ✅ **TIP de PR automatizado** con rama temporal + etiqueta: correcto para flujos con protección de rama.
- ✅ **Diff semántico / drift documental** con tabla de casos: criterio profesional.
- ⚠️ **La pregunta #1 del propio curso apunta a un agujero real que el material no resuelve:** dos webhooks casi simultáneos sobre el mismo archivo → el curso **no** da locking/cola; con `tmp+rename` el "último gana" y se pisa el primero. (Coherente con el problema de concurrencia ya visto en L08/L10.)

**Lo que NO es feature nativa de OpenClaw (el curso lo presenta como "OpenClaw implementa…"):**
- ❌ **No hay un "submódulo/motor reactivo de documentación" en OpenClaw.** No existe `syncEndpointParameters`, ni un updater AST, ni la sincronización Git automática como parte del producto. Esto es un **pipeline que uno construye encima** (un worker/plugin propio), no una capacidad integrada.
- ❌ **Las librerías del curso no están instaladas aquí:** verificado → `unified`, `remark-parse`, `remark-stringify`, `remark-gfm`, `unist-util-visit`, `gray-matter`, `mdast` **no** resuelven (MISS todas). El código **no corre tal cual** sin `npm install`. Node sí está (v26.8.1).
- ❌ **`auto_generated_sections` no es un concepto de OpenClaw** ni aparece en ningún doc del workspace. Es una **convención inventada** por el curso.
- ⚠️ **`OpenClaw Bot <bot@openclaw.internal>` / `agent-docs@internal.domain`**: autores ficticios. El agente real de este workspace commitea con la identidad de Gonzo (`git add/commit` en cierre de sesión usa su config), no con un "OpenClaw Bot".

**Verificación ejecutable:**
- ❌ El código TypeScript **no se puede correr** sin instalar las 7 dependencias (ninguna presente). Es un ejemplo correcto **conceptualmente**, no ejecutable en este entorno.
- ✅ La **lógica** es válida y traducible: en este workspace el equivalente real es la disciplina de `apply_patch`/`edit` acotado + commit por path explícito (ya documentada en la memoria del proyecto).

**Patrón (decimotercer caso, consistente):** **buena ingeniería** (AST, atomicidad, allowlist de secciones, git hygiene) montada sobre una **feature que el producto no tiene** (un doc-sync reactivo nativo). El *qué* (mutar quirúrgicamente y commitear con trazabilidad) es correcto; el *cómo* hay que construirlo como worker/plugin propio, no invocarlo como capacidad de OpenClaw. Y, como en L08/L10, la concurrencia multi-writer queda sin resolver (su propia pregunta #1 lo delata).

**Nota de contexto (Módulo 3):** tras esta L13 el propio curso indica *"2 lessons left in Ingesta Dirigida por Eventos"* → Módulo 3 = 5 lecciones (L11-L15). Lección 14: *Alertas Automatizadas Frente a Errores Críticos*.
