---
name: "capability-index"
metadata:
  category: "Orchestration"
  tags:
    - skills
    - index
    - capability
    - discovery
description: "Responde 'tenes X?' o 'sabes hacer X?' en cuatro estados verificados (existe / existe en rol Y / no existe + alternativa mas cercana / ambiguo), citando la ruta real del SKILL.md verificada contra el runtime."
user-invocable: "false"
---

# Capability Index

> El CORE no recuerda skills por memoria. El CORE consulta.

## Por qué existe

La memoria de la sesión (contexto) se trunca y miente: el mismo catálogo se ve distinto el lunes y el viernes. Este skill obliga a verificar contra el runtime antes de afirmar que existe algo. Prohibido responder "sí, tengo..." o "no, no tengo..." sin el paso 1.

## Procedimiento (no improvisar)

### 1. Verificar el catálogo real (siempre)

```bash
openclaw skills list --agent main --json
```

Es la única autoridad (SKILLS-INDEX §1). Si `openclaw` no está disponible (offline), degradar al walk de `skills/` y declararlo: "catálogo parcial (offline)".

### 2. Buscar un nombre exacto

Tomar la query del humano, normalizar a slug (`lower`, `-` por espacios, sin acentos), y buscar en el campo `name`:

- **existe** → indicar `name`, `source`, y la ruta verificada (ver §4).
- **existe en rol Y** → cuando el mismo skill vive en `agents/<rol>/skills/<name>`; indicar rol y ruta. Puede coexistir con la versión genérica del Core: se nombran ambas, no se fusionan.

Si hay match exacto, no seguir: no hace falta matcher semántico para "existe".

### 3. Si no hay match exacto: evaluar candidatos

```bash
./scripts/skill-router.py -n 3 "<query>"
```

- **score top-1 ≥ 0.7 y gap con el segundo ≥ 0.10** → el skill más cercano es **alternativa** (no "no existe"): nombrarla + ruta + score.
- **dos o más candidatos a ≤ 0.05 del top** → **ambiguo**: listar los 2-3 con ruta y score, y pedir al humano cuál. No elegir por el CORE.
- **top-1 < 0.5 o listado vacío** → **no existe**: decirlo claro ("no existe, y lo más cercano es X por Y"). Proponer, si aplica, crearlo o usar un procedimiento manual.

### 4. Verificar la ruta (siempre, incluso para las del catálogo)

El catálogo no expone `path`. Determinar la ruta con este orden y **verificarla con `test -e` antes de citarla**; si no existe, el skill NO existe (el catálogo puede estar stale):

1. `skills/<name>/SKILL.md` (Core).
2. `agents/<rol>/skills/<name>/SKILL.md`, probando cada rol del runtime (core, dev, mind, ops, studio, auditor, critic, planner).
3. `~/.openclaw/agents/<agent>/agent/workshop-skills/<name>/SKILL.md` (workshop).
4. `~/.agents/skills/<name>/SKILL.md` (personal).

Citar la **primera** que exista. Si ninguna, marcar `ruta: no verificada (stale)` y no citar el skill como existente.

### 5. Formato de respuesta

```
capability: <name>
estado: existe | existe (rol Y) | alternativa | ambiguo | no existe
ruta: <path> (verificada) | no verificada
fuente: openclaw skills list --agent <id> (--json)
nota: <una linea>
```

Nunca afirmar un estado sin el comando del paso 1 corrido en esta sesión.

## Límites

- No crea skills. Si algo no existe, se propone o se delega a STUDIO/DEV; no "le invento" un SKILL.md ad-hoc en la respuesta.
- No combina el catálogo del `main` con el de otros agentes: cada agente tiene su propio `openclaw skills list --agent <id>`. Si la pregunta es sobre un rol, cambiar `<id>` accordingly.
- Si Ollama está caído, el paso 3 degrada a L1 (keyword) del router; decirlo ("semántico no disponible, solo L1").
- La única fuente del "¿existe?" es el runtime. Docs, memory y SKILLS-INDEX son segundos; si contradicen, manda el runtime y se reporta la contradicción.

## Relacionados

- `skill-router` skill y `scripts/skill-router.py` (lookup semántico).
- `scripts/check-skill-overlap.py` (detección de pares redundantes; este skill es el "lookup", aquel es el gate).
- ADR-088 (+) managed block `#model-operativo` de AGENTS.md (modelo operativo).