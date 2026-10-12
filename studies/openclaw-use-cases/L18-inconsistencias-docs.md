# Módulo 4 · Lección 18 de 30: Detección de Inconsistencias en Documentación Técnica

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 4 - Gestión Proactiva del Workspace
**Lección:** 18 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Cuando un agente modifica configs, notas de arquitectura o endpoints, la documentación acumula **divergencias silenciosas**: una variable renombrada en el script de deploy sigue documentada con su nombre viejo; un endpoint cambiado contradice la guía de la API. No rompen la ejecución de inmediato, pero degradan la fiabilidad del workspace y provocan **alucinaciones** cuando el agente consulta la base de conocimiento local.

La detección proactiva convierte al agente en un **auditor continuo de coherencia documental**: compara afirmaciones factuales de los Markdown/esquemas contra el código y las referencias canónicas, señalando contradicciones antes de que contaminen decisiones.

---

## Anatomía de una inconsistencia técnica

No es un typo: es una **discrepancia de estado o semántica** entre fuentes de verdad. Tres categorías:

- **Divergencias de interfaz y firma:** la doc describe parámetros/endpoints que difieren de la firma real del código o del esquema OpenAPI.
- **Desajustes de configuración y entorno:** `.env.example` o guías listan variables que ya no existen, cambiaron de tipo o tienen defaults incompatibles.
- **Contradicciones interdocumentales:** dos notas afirman hechos mutuamente excluyentes (versiones mínimas, límites de tasa, flujos de auth).

Para detectarlas de forma determinista, el pipeline **extrae claims factuales** (afirmaciones comprobables), **resuelve las entidades** contra fuentes de verdad y **clasifica severidad**.

---

## Extracción de afirmaciones factuales y cruce canónico

En vez de comparar párrafos enteros por embeddings superficiales (que fallan ante variaciones sintácticas críticas como un puerto o un booleano invertido), el agente segmenta el texto en pares **`(entidad, propiedad, valor, contexto)`**.

Ejemplo del curso: la guía `docs/deploy.md` dice

```markdown
### Worker Configuration
El servicio de colas arranca escuchando en el puerto TCP `8085`.
Requiere la variable `QUEUE_CONCURRENCY=16` para entornos de staging.
```

y el código `src/config/worker.ts` define

```typescript
export const workerConfig = {
  port: parseInt(process.env.WORKER_PORT || '8080', 10),
  concurrency: parseInt(process.env.MAX_WORKERS || '8', 10),
  timeoutMs: 30000,
};
```

El motor construye tablas de aserciones y detecta dos discrepancias: el **valor por defecto** del puerto difiere (8085 vs 8080) y la **variable** fue renombrada (`QUEUE_CONCURRENCY` vs `MAX_WORKERS`).

---

## Implementación del validador proactivo

El agente mantiene una lista de reglas de correspondencia ruta-doc → archivo-fuente. La rutina recorre las rutas, analiza ASTs/esquemas y emite diferencias estructuradas.

```typescript
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

interface InconsistencyReport {
  targetDoc: string; key: string; docValue: string; codeValue: string;
  severity: 'low' | 'medium' | 'high';
}

export class DocumentationAuditor {
  constructor(private workspaceRoot: string) {}

  public extractCodeEnvVars(srcDir: string): Map<string, string | undefined> {
    const envVars = new Map<string, string | undefined>();
    const files = readdirSync(join(this.workspaceRoot, srcDir), { recursive: true }) as string[];
    for (const file of files) {
      if (!file.endsWith('.ts') && !file.endsWith('.js')) continue;
      const content = readFileSync(join(this.workspaceRoot, srcDir, file), 'utf-8');
      const regex = /process\.env(?:\.([A-Z0-9_]+)|\[['"]([A-Z0-9_]+)['"]\])(?:\s*\|\|\s*['"]([^'"]+)['"])?/g;
      let match;
      while ((match = regex.exec(content)) !== null) {
        const varName = match[1] || match[2];
        envVars.set(varName, match[3]);
      }
    }
    return envVars;
  }

  public auditMarkdownDoc(docPath: string, codeEnvVars: Map<string, string | undefined>): InconsistencyReport[] {
    const fullPath = join(this.workspaceRoot, docPath);
    if (!existsSync(fullPath)) return [];
    const content = readFileSync(fullPath, 'utf-8');
    const reports: InconsistencyReport[] = [];
    const docVarRegex = /`([A-Z0-9_]{4,})`(?:\s*=\s*`?([^`\n\r]+)`?)?/g;
    let match;
    while ((match = docVarRegex.exec(content)) !== null) {
      const varName = match[1];
      const docVal = match[2] || 'declared';
      if (!codeEnvVars.has(varName)) {
        reports.push({ targetDoc: docPath, key: varName, docValue: docVal,
          codeValue: 'UNDEFINED_IN_CODE', severity: 'high' });
      } else {
        const codeFallback = codeEnvVars.get(varName);
        if (docVal !== 'declared' && codeFallback && docVal !== codeFallback) {
          reports.push({ targetDoc: docPath, key: varName, docValue: docVal,
            codeValue: codeFallback, severity: 'medium' });
        }
      }
    }
    return reports;
  }
}
```

Según el curso, el reporte devuelto es:

```json
[
  {
    "targetDoc": "docs/deploy.md",
    "key": "QUEUE_CONCURRENCY",
    "docValue": "16",
    "codeValue": "UNDEFINED_IN_CODE",
    "severity": "high"
  }
]
```

("Confirma que el documento exige una variable inexistente en el runtime".)

> ⚠️ **Ver nota crítica al final:** ese JSON **no es lo que devuelve el código.**

---

## Estrategias de resolución y generación de parches

Tres políticas:

- **Autocorrección (parche directo):** cuando el código es indiscutiblemente la fuente canónica y la doc es referencial (un puerto por defecto, una firma de comando).
- **Apertura de issue/ticket:** cuando hay ambigüedad (¿el código introdujo una regresión o la doc quedó rezagada?).
- **Cuarentena documental:** marcar la sección con un bloque de advertencia para que otros subprocesos no usen datos erróneos.

```typescript
export function applyDocumentationPatch(originalDoc: string, issue: InconsistencyReport, actualCodeIdentifier: string): string {
  const regex = new RegExp(`\`${issue.key}\``, 'g');
  return originalDoc.replace(regex, `\`${actualCodeIdentifier}\``);
}
```

> **PITFALL del curso (correcto y crítico):** no dejar que el agente sobrescriba documentación de arquitectura cuando la discrepancia involucre **tipos complejos o contratos de negocio** sin confirmación explícita o validación contra tests. Un agente que asume que "el código siempre tiene razón" puede **normalizar un bug como comportamiento deseado**.

> **REMEMBER del curso (correcto):** el **código y los esquemas tipados** son la fuente de verdad primaria para parámetros técnicos; las **especificaciones de diseño** son la referencia canónica para flujos de negocio.

### Check your understanding
**Si `docs/deploy.md` exige `WORKER_CONCURRENCY=4` pero en el código la variable se renombró a `POOL_SIZE`, ¿acción correcta?**
- [x] **Actualizar `docs/deploy.md` con el identificador real o abrir una advertencia de discrepancia crítica si requiere validación humana.**

---

## Integración con rutinas autónomas

El mecanismo se programa dentro de los ciclos de mantenimiento ya vistos (cron, triggers de filesystem). Cuando un webhook o un commit modifica algo en `src/`, el agente programa una **verificación de impacto documental**. Si detecta discrepancias de alta severidad, registra el incidente y prepara un **diff unificado** para revisión humana o aprobación automática en el siguiente ciclo.

---

## Resumen

Auditoría de coherencia documental procesando documentos en **aserciones estructuradas** (entidad/valor) en vez de comparaciones textuales: identifica variables obsoletas, puertos desalineados y contratos rotos, y genera parches específicos antes de que las divergencias afecten a desarrolladores o agentes.

**UP NEXT · Lección 19 de 30:** *Consolidación Automática de Bitácoras de Trabajo*. Faltan **2 lecciones** para cerrar el Módulo 4.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo evita el agente falsos positivos cuando la doc describe una versión futura aún no implementada?
2. ¿Qué estrategia auditar documentación con fragmentos de código interactivos?
3. ¿En qué casos debe abstenerse de autocorregir y requerir confirmación humana?
4. ¿Cómo impacta el tamaño del workspace en el rendimiento del auditor?

(Anotadas. La #1 y la #4 son huecos reales: doc adelantada por diseño, y costo de indexación a escala.)

---

## Notas de verificación (Kanam)

**El núcleo conceptual es correcto y valioso:**
- ✅ Auditar **claims factuales por estructura** (entidad/valor) en vez de comparar texto entero por embeddings: correcto y central (un embedding no ve "8080" vs "8085").
- ✅ Tres políticas de resolución (parche / issue / cuarentena): buen criterio.
- ✅ **PITFALL correcto:** no normalizar un bug como comportamiento deseado; validar contra tests antes de autocorregir.
- ✅ **REMEMBER correcto:** código = fuente canónica para lo técnico; diseño = canónico para negocio.
- ✅ Acierta el quiz.
- ✅ Las **preguntas #1 y #4** apuntan a huecos reales (doc adelantada por versión; costo a escala).

**HALLAZGO CRÍTICO - el output del curso es FALSO y el código tiene un bug real:**
- ❌ **El JSON prometido NO sale del código mostrado.** Corrí el script exacto (Node) con `docs/deploy.md` y `src/config/worker.ts` tal como los da la lección. Resultado real:
  ```json
  [
    { "targetDoc": "docs/deploy.md", "key": "8085",
      "docValue": "declared", "codeValue": "UNDEFINED_IN_CODE", "severity": "high" }
  ]
  ```
  Es decir: reporta **`8085` (el número de puerto)** como "variable inexistente" - un **falso positivo** - y **nunca** reporta `QUEUE_CONCURRENCY`.
- **Causa (dos bugs en el regex del propio curso):**
  1. El patrón `` /`([A-Z0-9_]{4,})`(?:\s*=\s*...)?/g `` exige el `=valor` **fuera** de los backticks (`` `VAR`=valor ``), pero la doc lo escribe **dentro** (`` `QUEUE_CONCURRENCY=16` ``). Como el backtick de cierre no sigue inmediatamente a `QUEUE_CONCURRENCY`, **no hay match** → la variable renombrada **nunca se detecta**.
  2. `[A-Z0-9_]{4,}` **admite dígitos puros**, así que `` `8085` `` (un puerto entre backticks) **matchea como si fuera un nombre de variable** → falso positivo de severidad `high`.
- **La narrativa del curso tampoco coincide con el código.** Dice que detecta "el valor por defecto difiere (8080 vs 8085)". El código **nunca compara defaults de puerto**; solo busca nombres de vars de entorno. El caso de las dos discrepancias que la tabla promete no lo produce este código.
- Es el patrón de output fabricado (L01/L02/L04/L15) **pero agravado: acá el código además es incorrecto**. El ejemplo no solo no reproduce su salida; la lógica que lo produciría no existe.

**Lo que NO es feature nativa de OpenClaw:**
- ❌ **`DocumentationAuditor` / `auditMarkdownDoc` no existen** en OpenClaw (verificado: no aparecen en docs). Es un módulo a construir, no una capacidad del producto.
- ❌ **No hay un "motor de claims factuales" ni una lista persistente de reglas ruta-doc↔fuente.** Invención.
- ⚠️ **`/workspace/repo`** es ruta ficticia.

**Verificación ejecutable:**
- ✅ Node disponible; el script corre, pero con el **resultado incorrecto** descrito arriba.
- ✅ `pyyaml`/`node` no son el problema: el bug es de diseño del regex.

**Patrón (decimoctavo caso, con el hallazgo más fuerte):** **concepto correcto** (auditar por aserciones estructuradas, no por embeddings) **+ código defectuoso + output fabricado**. Es la primera lección donde la **implementación misma está rota**, no solo la fachada. Traducible al workspace real: esto es, en esencia, lo que `check-refs.py`/`check-content-dirs.py`/`check-adr-*` ya hacen de forma **determinista y probada** - y sin el bug del regex. La lección pide algo que **este repo ya implementa mejor**.

**Nota de contexto (Módulo 4):** tras esta L18 el propio curso indica *"2 lessons left in Gestión Proactiva del Workspace"* → Módulo 4 = 5 lecciones (L16-L20). Lección 19: *Consolidación Automática de Bitácoras de Trabajo*.
