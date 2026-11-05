---
name: "voz-gonzo"
metadata:
  category: "Career"
  tags:
    - voz
    - redaccion
    - linkedin
    - email
    - corpus
description: "Redactar cualquier texto que sale hacia afuera (LinkedIn, mail, carta, mensaje a reclutador) con la voz de Gonzo: directo, sin servilismo, pide en presente. La fuente de verdad es docs/voz-gonzo.md; esta skill solo la lee y aplica el gate de reglas prohibidas."
user-invocable: true
---

# Skill: voz-gonzo - Redaccion con voz

> **Fuente de verdad unica:** `docs/voz-gonzo.md`. Esta skill **no tiene reglas propias**: las
> deriva de los casos reales. Si hay discrepancia, gana el corpus y se corrige la skill.
> (AGENTS.md §0: si un dato vive en dos archivos, uno de los dos es un bug.)

## Trigger

**Cualquier texto que cruza la frontera.** Antes de enviar:

| Se usa | No se usa |
|---|---|
| LinkedIn (mensajes, comentarios, posts) | commits, PRs, issues, READMEs (ingles tecnico) |
| Mail a reclutador / cliente / equipo | notas internas, dailies, ADRs |
| Cartas de motivacion, screenings | documentacion de proyecto |
| Respuestas a procesos de entrevista | mensajes entre Kanam y Gonzo |

Excepcion explicita: **GitHub y la capa tecnica van en ingles** y se rigen por `USER.md` +
`AGENTS.md`, no por esta skill.

## Procedimiento

### 1. Leer el corpus ANTES de escribir

```bash
sed -n '1,200p' docs/voz-gonzo.md
```

No improvises la voz. Los patrones ya estan extraidos de ediciones reales.

### 2. Redactar

Aplicar los patrones vigentes del corpus. Los confirmados hasta hoy:

| Patron | Regla |
|---|---|
| **Directo, incluso con la emocion** | se admite "no te voy a mentir", "me hubiera gustado otro resultado" |
| **Sin servilismo** | prohibido "seria un honor", "quedo a la entera disposicion", "me alegro" |
| **Pide en PRESENTE** | "ahora", no "a futuro" / "en el radar" |
| **Alcance amplio** | la flexibilidad se ofrece como posicion, no como rebaja |
| **Vineta en chat, numero en documento** | `*` si hay que enumerar en mensaje; `1. 2. 3.` solo en doc formal |
| **Corta lo que no pide ni informa** | sin cierre de cortesia de relleno |
| **Confianza con filo** | "si me das una oportunidad, no te vas a arrepentir" |

### 3. Gate automatico (obligatorio antes de mostrar)

```bash
python3 skills/voz-gonzo/check-voz.py <archivo.txt>
```

Falla si encuentra:

| Prohibida | Por que |
|---|---|
| "Estimado" | registro corporativo |
| "Me alegro" | servilismo de apertura |
| "Excelente oportunidad" | relleno |
| "No dude en contactarme" | cortesia vacia |
| "Quedo a la entera disposicion" | sumision |
| "Seria un honor" | epica decorativa |
| "Un abrazo grande" | cierre de relleno |
| Numeracion `1.` en texto corto | formato de documento en un chat |

### 4. Entregar

Borrador + **lista de violaciones** si el gate marco algo. Gonzo edita; **su edicion se agrega al
corpus** (ese es el ciclo que mantiene la voz viva):

```markdown
### YYYY-MM-DD - <contexto> (<destinatario>)
**Mi borrador:** ...
**Su edicion final:** ...
**Que cambio y por que:** ...
**Patron que refuerza o emerge:** ...
```

## Modelo

El del rol que la invoca, **sin override**. La voz no mejora con un modelo mas caro: mejora con
el corpus. Medido 2026-11-04: Kimi K3.1 Pro redacto mejor que DeepSeek en matiz (*"me hubiera
gustado otro resultado"* vs *"me rechazaron"*), pero eso justifica invocarlo a mano para un texto
importante - **no** convertirlo en default de la skill.

Regla practica: si el texto es **decisivo** (carta, mensaje a un contacto que importa), invocar
`sessions_spawn(model: "ollama/kimi-k3.1-pro:cloud")`. Si es rutina, el modelo del rol alcanza.

## Reglas duras

- **No inventa hechos.** Si el corpus o el contexto no dan un dato (empresa, rol, logro), va
  placeholder `[Empresa]` - nunca un dato plausible inventado.
- **No suaviza por educacion.** El corpus es explicito: la confianza cierra mejor que la cortesia.
- **No cambia de idioma de registro:** la voz es la misma en espanol y en ingles; cambia el idioma.
- **No envia nada.** Entrega el borrador; el envio es de Gonzo (AGENTS.md: nada sale sin OK).
