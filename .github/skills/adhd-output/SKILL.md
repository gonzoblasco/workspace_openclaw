---
name: "adhd-output"
metadata:
  category: "Life"
  tags:
    - adhd
    - comunicacion
    - formato
    - estilo
description: "Formato de respuesta ADHD-friendly: accion primero, pasos numerados, next step concreto. Para cuando el usuario pide respuestas directas sin preambulo ni relleno."
user-invocable: true
---

# Workflow: ADHD Output

## Proposito

Forzar un formato de respuesta que no entierre la respuesta. Accion primero, pasos numerados, un next step concreto al final. Sin preambulo, sin recap, sin cierres.

Basado en [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT), adaptado al contexto del workspace de Kanam.

## Diferencia con `adhd-assistant`

| Skill | Que hace |
|---|---|
| `adhd-assistant` | Sistema de vida: planificar el dia, desglosar tareas, body doubling, regulacion emocional |
| `adhd-output` | Formato de la respuesta: como se comunica, no que se comunica |

Son complementarios. Uno puede estar activo sin el otro.

---

# Cuando usarlo

- El usuario pide "se directo", "sin vueltas", "accion primero"
- Sesiones de debugging o coding donde la respuesta esta enterrada en prosa
- Cuando el usuario viene sobrecargado y necesita el siguiente paso, no el analisis
- Reviews o analisis largos donde hay que separar hallazgo de accion
- Invocacion explicita: "formato ADHD", "i-have-adhd"

**NO usarlo cuando:** la lista ES el entregable (catalogo, comparativa, inventario), o cuando el recap es la memoria (cierre de sesion, handoff).

---

# Las 10 reglas

## 1. Liderar con la proxima accion
La primera linea es lo que hay que hacer, no el contexto de por que. Si el usuario tiene que scrollear para encontrar la accion, fallo.

## 2. Numerar tareas multi-paso
Si hay mas de un paso, va numerado. Prosa para secuencias es donde se pierde la gente.

## 3. Cerrar con un next step concreto
Una sola accion, la mas chica y verificable. No "avanzar con el proyecto" - "correr `npm test -- auth.spec.ts`".

## 4. Suprimir tangentes
Lo que aparece de costado se omite o se registra aparte. No interrumpir la accion principal con un "por cierto, tambien...".

## 5. Restatear el estado cada turno
Que esta corriendo, que quedo pendiente, donde estamos parados. Version workspace: no el recap completo, solo lo que cambio.

## 6. Time estimates en minutos
"10 minutos", "2 horas", no "un rato" ni "un poco". La time blindness necesita numeros concretos.

## 7. Hacer visibles las victorias
Nombrar lo que se completo. No como felicitacion vacia, sino como marcador de progreso: "build verde, 3 tests nuevos pasando".

## 8. Errores matter-of-fact
Sin drama, sin disculpas largas. Que fallo, por que, que sigue. "El test rompe en la linea 42. Sigue: revisar el mock."

## 9. Cap de listas a 5 items
Si hay mas de 5, agrupar o priorizar. Una lista de 12 items no se lee, se saltea.

**Excepcion:** cuando la lista ES el entregable (inventario, catalogo, comparativa pedida). En ese caso, usar tabla en vez de bullets.

## 10. Sin preambulo, sin recap, sin cierres
No "Gran pregunta", no "Espero que ayude", no "avanzame si queres profundizar". La respuesta termina cuando termina la informacion.

---

# Formato

## Estructura base

```
<accion concreta, imperativa>

<contexto minimo necesario, solo si cambia la accion>

1. <paso>
2. <paso>
3. <paso>

Next: <una accion, la mas chica>
```

## Antes / despues

**Antes:**
> Gran pregunta! Tu flujo de auth tiene varias piezas: el middleware, la verificacion de token y el manejo de cookies. Mirando src/auth.ts, la funcion verifyToken (lineas 42-58) parece usar una API vieja de jsonwebtoken. Un enfoque seria actualizar el paquete y reescribir esa funcion. Despues querrias correr los tests de auth para confirmar que nada rompe. Por cierto, tambien podrias revisar las versiones de dependencias. Espero que ayude!

**Despues:**
> Correr `npm install jsonwebtoken@latest`, despues editar `src/auth.ts:42`.
>
> 1. Abrir `src/auth.ts`
> 2. Reemplazar `verifyToken` (lineas 42-58) con el snippet de abajo
> 3. Correr `npm test -- auth.spec.ts`
>
> Next: pegame la primera linea del test que falla, si falla.

## Errores

**Antes:**
> Hmm, parece que hubo un problema con el build. Lamento el inconveniente! Puede ser que haya algo mal configurado...

**Despues:**
> El build rompe: `TS2345` en `src/api/client.ts:88` - `string` no asignable a `Response`.
>
> 1. Revisar el tipo de retorno de `fetchUser`
> 2. Castear o corregir la firma
>
> Next: pegame las lineas 80-95 de `src/api/client.ts`.

---

# Reglas de interaccion con otras skills

- **`anti-ai`:** se complementan. `anti-ai` limpia modismos de IA en texto publicado; `adhd-output` limpia estructura de respuesta en conversacion. Aplicar ambos cuando se publica.
- **`adhd-assistant`:** si el usuario pide plan del dia, ese skill define el contenido y este define el formato.
- **`session-lifecycle`:** al guardar sesion, el recap ES la memoria. La regla 10 (sin recap) no aplica ahi.
- **`progress_card`:** el restateo de estado (regla 5) puede vivir en el progress card en vez del mensaje, para sesiones largas.

---

# Helper Scripts

| Script | Uso |
|---|---|
| `scripts/check-output.sh` | Heuristicas de lint sobre un texto: detecta preambulo, cierres, em dashes y listas largas. Uso: `check-output.sh <archivo>` o `echo "texto" \| check-output.sh` |

# Referencias y templates

| Archivo | Uso |
|---|---|
| `references/rules.md` | Las 10 reglas en detalle, con racional y contraejemplos |
| `references/adaptations.md` | Que se cambio respecto al original de ayghri y por que |
| `templates/response.md` | Plantilla de respuesta ADHD-friendly |

# Related Skills

- [adhd-assistant](../adhd-assistant) - Sistema de vida y planificacion
- [anti-ai](../anti-ai) - Limpieza de modismos de IA
- [session-lifecycle](../session-lifecycle) - Estructura de sesiones de trabajo
