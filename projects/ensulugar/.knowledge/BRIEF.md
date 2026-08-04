# EnSuLugar — Definición de Producto (Tutor de Cocina IA)

**Estado:** Borrador v1 — para iterar
**Fecha:** 2026-08-04
**Autor:** Gonzo + Kanam
**Artifact espejo:** "Recetario — Definición de Producto (Tutor de Cocina IA)" (id: 53e0b3b0-275f-4724-998a-8fa96c35ca99)

---

## 1. Qué es

Un **tutor de cocina personal** que enseña técnicas culinarias desde cero hasta nivel avanzado. No es un buscador de recetas: es un **mentor que arma un plan de aprendizaje adaptado a tu nivel, te enseña el "porqué" de cada técnica y corrige tus errores comunes**.

**Una frase:** *"Duolingo, pero para cocinar — con IA que se adapta a vos y te explica el porqué."*

---

## 2. El problema que resuelve

- La gente sigue recetas de internet pero **no aprende a cocinar**: repite pasos sin entender la técnica (por eso el huevo siempre les sale mal).
- Los cursos de cocina son rígidos, caros y no se adaptan a tu nivel real.
- No hay un producto que enseñe el **"porqué"** — solo el "qué hacer".

**El insight central del contenido:** cada receta tiene una o más **técnicas** (emulsión, sellado, roux, deglaseado...). Aprender técnicas, no recetas, es lo que hace cocinero a alguien. El contenido ya está escrito así (cada paso explica su porqué).

---

## 3. Usuario objetivo

- **Persona:** alguien que quiere aprender a cocinar de verdad, pero sin pagar un curso ni mirar 40 videos.
- **Nivel:** de "no sé freír un huevo" a "quiero dominar salsas madre".
- **Dolor:** frustración de seguir recetas y que no salgan. No entiende *por qué* falla.
- **Device:** desktop primero (es cocina, se usa con la receta al lado), móvil después.

---

## 4. La propuesta de valor

| Aspecto | Detalle |
|---|---|
| **Adaptación real** | El tutor arma tu ruta según tu nivel declarado + evidencia (qué dominás). |
| **Enseña el porqué** | Cada técnica explica el mecanismo, no solo el paso. |
| **Progresión lógica** | Grafo de prerrequisitos: no podés hacer carbonara sin dominar la emulsión. |
| **Corrección de errores** | Anticipa los errores comunes de cada técnica (ya están en las notas). |
| **Tu clave, tu modelo** | Bring-your-own-key: conectás tu OpenAI/Anthropic o tu Ollama local. Cero costo. |
| **Open source** | El motor es abierto. El contenido curado es el diferencial (ver §9). |

---

## 5. Bring-Your-Own-Key (BYOK) + Ollama local

**Modelo:** el usuario configura un *proveedor de LLM* al primer uso. La app **nunca** pasa por servidores de terceros para la generación — el LLM corre donde el usuario diga.

**Proveedores soportados (v1):**
- **Ollama local** (el que ya usamos en OpenClaw) — gratis, privado, ideal para dev y para el usuario técnico.
- **OpenAI / Anthropic / compatible** con API key propia — para el usuario que quiere mejor calidad.

**Por qué es clave:**
1. **Costo cero de operación** — no pagamos ni un token de LLM por usuario.
2. **Privacidad** — las recetas y el progreso del usuario no salen de su máquina si usa Ollama.
3. **Escalabilidad** — no necesitamos infraestructura de generación.
4. **Perfecto para dev:** usamos el Ollama de OpenClaw en local, sin gastar nada.

**Config en `.env` del usuario (nunca en el repo):**
```env
# Elegí uno:
LLM_PROVIDER=ollama        # o: openai | anthropic
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-v4-flash
# OPENAI_API_KEY=sk-...    # si usás openai
```

---

## 6. Cómo funciona el tutor (arquitectura conceptual)

```
┌─────────────────────────────────────────────────────┐
│                    USUARIO                          │
│  (nivel declarado + qué dominás + objetivos)        │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│          MOTOR DE ADAPTACIÓN (determinístico)       │
│  - Perfil del usuario (nivel, técnicas dominadas)   │
│  - Grafo de prerrequisitos entre técnicas           │
│  - Algoritmo arma la ruta de aprendizaje            │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│            CAPA PEDAGÓGICA (LLM, BYOK)              │
│  - Toma la técnica + la data estructurada           │
│  - Genera la lección en lenguaje natural            │
│  - Adapta tono/complejidad al nivel del usuario     │
│  - Explica el porqué, anticipa errores              │
│  - Corrección y feedback interactivo                │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│            BASE DE CONOCIMIENTO (curated)           │
│  - recetas + técnicas + prerrequisitos (SQLite)     │
│  - fichas markdown como fuente de verdad            │
└─────────────────────────────────────────────────────┘
```

**Clave de diseño:** el motor de adaptación es **determinístico** (no depende del LLM) — el grafo de prerrequisitos y la ruta son lógica pura. El LLM solo se usa para la **capa pedagógica** (generar la lección y el feedback). Esto hace el producto predecible, barato y testeable sin LLM.

---

## 7. El grafo de prerrequisitos (el corazón del producto)

Cada **técnica** (no receta) es un nodo. Las recetas se agrupan por técnica. Ejemplo del contenido actual:

```
Emulsión
 ├─ Vinagreta (básica)
 ├─ Mayonesa (media) ──► Holandesa (avanzada) ──► Carbonara (aplica)
Roux
 └─ Bechamel ──► (base de lasaña, croquetas)
Sellado
 ├─ Bife a la plancha ──► Deglaseado/Salsa de sartén
Hidratación de masas
 ├─ Pâte brisée ──► Pan casero ──► Pizza (reposo en frío)
```

**El tutor usa este grafo para:**
- No enseñarte holandesa si no dominás la emulsión básica.
- Armar una ruta de "principiante → masterchef" coherente.
- Sugerir la próxima técnica según tu progreso.

---

## 8. Modo tutor vs modo receta

**Modo tutor (el core):** cada ficha/receta es la **semilla de una lección**. El tutor toma esa receta como vehículo y te enseña la técnica y la teoría detrás, adaptado a tu nivel. Genera la lección interactiva con el LLM: qué es la técnica, por qué importa, el paso a paso con el mecanismo, errores comunes, y una mini-evaluación. Las fichas markdown son el *material*; la clase la genera la IA al vuelo.

**Modo receta (lo que ya existe):** el `index.html` actual — busca y sigue una receta paso a paso. Se mantiene como acceso rápido.

**Rol de cada pieza (decisión 2026-08-04):**
- **Fichas markdown** = fuente de verdad / material pedagógico (recetas + técnicas + teoría + porqués).
- **Tutor (LLM)** = toma la ficha y genera la **lección** en el momento, adaptada al usuario (nivel, progreso).
- **DB/JSON** = artefacto derivado para consultas y la app.
- **Cada ficha = semilla de una lección** (opción A): se enseña la técnica usando la receta como vehículo.

---

## 9. Estrategia open source — esquema binario local / cloud

**Modelo open-core (patrón n8n / OpenClaw): dos productos, una base de código.**

**A) Local — gratis, open source.** Todo es público: código + contenido (recetas DB + fichas md). El usuario corre el proyecto completo con SU clave de LLM o SU Ollama local (BYOK). Cero costo para nosotros por usuario.

**B) Cloud — premium, hosting gestionado (a futuro).** Seguridad, actualizaciones, sin configurar nada, experiencia pulida. Se paga. No requiere contenido privado: el valor está en el servicio gestionado + tutor adaptado, no en retener las recetas.

**La versión local es la puerta de entrada / canal de adquisición del cloud.** Que sea popular localmente es el embudo hacia el premium. No es un conflicto, es el funnel.

**Las clases NO son contenido estático.** El tutor genera la lección en el momento con el LLM (fresca, adaptada al usuario). El contenido curado (recetas + técnicas) es el *material*; la clase es producida al vuelo por la capa pedagógica. Nada de md pedagógico pre-escrito que envejezca.

**El contenido crece incrementalmente:** a futuro se agregan nuevas recetas a la base de datos. El sistema debe soportar contenido en expansión sin re-diseño.

**La arquitectura queda preparada para el cloud sin romper lo local:** separación clara entre contenido y motor. El mismo motor corre local (BYOK) y puede servirse en cloud (infra propia). No se diseña para proteger contenido — se diseña para que ambos modos compartan la misma base.

**Resumen:** abrimos todo (código + contenido). El valor diferencial y monetizable está en el servicio (tutor adaptado + hosting gestionado cloud). Tú no pagas LLM por usuario (BYOK).

---

## 9bis. Nota de diseño — el motor es dominio-agnóstico

Recetario es el **caso de uso piloto** de un motor de cursos adaptativos genérico, no un producto aislado.

**El patrón (independiente del dominio):**
```
Contenido curado (estructurado, con prerrequisitos)
   ↓
Grafo de prerrequisitos (determinístico)
   ↓
Capa pedagógica LLM (BYOK) que genera la lección fresca
   ↓
Adaptación al perfil del usuario (nivel + progreso)
```

Sirve para cocina, programación, idiomas, música, fotografía... Lo único que cambia por dominio es el **contenido curado** y el **grafo de prerrequisitos**.

**El problema de la desactualización del contenido se resuelve con búsqueda web forzada:** el LLM no genera desde su memoria stale, sino que consulta activamente la fuente viva y sintetiza. En cocina casi no hace falta (la técnica no cambia); en programación es esencial (frameworks, APIs, versiones).

**Decisión de diseño:** el motor debe tener **fuentes de verdad configurables por dominio** — a veces solo contenido curado (cocina), a veces contenido + búsqueda web (programación). Es un componente opcional, no una obligación.

**Estrategia (pragmática):** construir el motor pensado de forma genérica (separación clara contenido/motor), pero **no abstraerlo de más ni publicarlo como producto separado todavía**. Recetario valida el motor; cuando funcione, se extrae como skill/patrón propio (estilo `workflow-kit` / `pipeline-detector`). **Primero el producto, después la abstracción.**

---

## 10. Roadmap propuesto

**Fase 0 — Definición (hoy):** este documento. Decidir: motor-first vs contenido-first.

**Fase 1 — Motor de adaptación (determinístico, sin LLM):**
- Modelar el grafo de prerrequisitos sobre las 23 recetas existentes.
- Perfil de usuario (nivel 1-5 + técnicas dominadas).
- Algoritmo que arma la ruta.

**Fase 2 — Capa pedagógica (LLM, BYOK + Ollama):**
- Config de proveedor (ollama/openai/anthropic) vía `.env`.
- Prompt que convierte una técnica + su data en una lección.
- Modo tutor interactivo con feedback.

**Fase 3 — Producto:**
- Frontend sobre el motor (reusar la app actual o nueva).
- Persistencia del progreso del usuario.
- Publicar repo open source + contenido aparte.

**Fase 4 — Open source & comunidad:**
- Repo público del motor.
- Contribución de contenido (con revisión) para quien quiera aportar técnicas.

---

## 11. Decisiones tomadas (2026-08-04)

| # | Pregunta | Decisión |
|---|---|---|
| 1 | Motor-first vs contenido-first | **Motor-first** |
| 2 | Stack | **TS/Node** (consistente con perfil fullstack React; la IA es consumidor de API BYOK, no cómputo local) |
| 3 | Frontend | **App nueva** (con estado para el tutor) — reusa el contenido existente |
| 4 | Nombre | **EnSuLugar** (con S mayúscula) — hereda el mensaje de "Mise en Place" (todo en su lugar) sin la fricción de pronunciación/escritura |
| 5 | Fuente de verdad | **Markdown como fuente, SQLite/JSON como artefacto generado** (md → DB → JSON) |

**Justificación §11.2 (por qué TS/Node y no Python):** la IA en este proyecto es un consumidor de API (BYOK), no el núcleo de cómputo — la capa pedagógica es "armar prompt + llamar a un endpoint", trivial en TS. El núcleo real es lógica de grafo + frontend, terreno TS. Un solo lenguaje para todo el proyecto (motor + frontend + tooling) = menos fricción y consistencia con el stack de Gonzo. Python tendría sentido solo si el motor hiciera fine-tuning/embeddings offline, que no es el caso.

**Justificación §11.5 (por qué markdown y no SQLite como fuente):** el humano edita markdown (legible, diffeable en git, revisable en PR — crítico para contribución open source); el sistema genera SQLite/JSON para la app (indexado, consultas). md → DB → JSON: una sola fuente de verdad, cero drift. SQLite como fuente mataría el diff de contenido en git y la edición a mano.

---

## 12. Estado actual del contenido (inventario)

- **23 recetas** en SQLite (`ensulugar.db`), 148 pasos, 123 ingredientes, 15 tags.
- **Dificultad:** 4× nivel 1, 4× nivel 2, 11× nivel 3, 3× nivel 4, 1× nivel 5.
- **Categorías:** huevos (5), pasta (4), salsas (5), carnes (4), vegetales (3), masas (3).
- **5 fichas markdown** por categoría (`fichas/*.md`).
- **App single-file** (`index.html`) con las 23 recetas embebidas, filtros, búsqueda, modo oscuro.

**Nota:** falta cubrir el nivel "masterchef" real (técnicas avanzadas: sous-vide, confit, fermentación, panificación avanzada, cocina molecular básica). El contenido actual es sólido de principiante a intermedio-alto.
