# Directrices editoriales por proyecto

> **Estado: VIGENTE desde 2026-11-06.** Validado por Gonzo en la sesión del
> 2026-11-06. Escrito leyendo material real en disco. Cada regla cita su fuente.
> Lo que no pude verificar está marcado como `[sin evidencia]` - no lo inventé.

**Qué es esto y qué no es.**

- **Esto NO es la voz.** La voz ya vive en `docs/voz-gonzo.md` (13 reglas
  numeradas, 1 retirada por ADR-082, 3 casos). Ese archivo es la fuente única y
  canónica.
- **Esto es lo específico de cada proyecto**: qué palabras no van, qué tono
  pide cada superficie, qué decisiones editoriales ya se tomaron.

La diferencia importa: `voz-gonzo` dice *cómo escribo siempre*; este archivo
dice *qué cambia según dónde publico y en qué proyecto*.

---

## Regla de precedencia

Cuando algo choca, gana el de arriba:

1. Aprobación explícita tuya en el momento
2. Este archivo (por proyecto)
3. `docs/voz-gonzo.md` (voz global)
4. Los defaults de la skill en uso

Si un proyecto contradice la voz global, se anota acá y se dice por qué.
Un proyecto no puede pedir relleno: eso viola una red line, no una preferencia.

---

## Superficies y su registro

Derivado del material real. La columna "evidencia" es lo que leí, no una suposición.

### 1. Artículos técnicos (`docs/articulos/`)

**Evidencia:** 11 artículos, muestra leída: `qwen2-5-1-5b/articulo.md`.

| Dimensión | Registro observado |
|---|---|
| Apertura | Afirmación con filo, sin preámbulo. "Hay modelos que venden humo y otros que hacen lo que dicen" |
| Estructura | Numerales romanos (I, II, III) con subtítulo que es una tesis, no un rótulo |
| Evidencia | Mediciones concretas con unidad: 0.8 s, 32768 tokens, 0.07 s a 2.42 s |
| Veredictos | Palabras técnicas en mayúscula: FALSO, INCOMPLETO, CORRECTO, con severidad |
| Cierre | Utilidad práctica: para qué sirve y para qué no |
| Muletillas | Cero fórmulas de cortesía, cero "en resumen", cero "cabe destacar" |

**Reglas específicas:**

- **Declarar la diferencia entre lo prometido y lo probado**, siempre. El
  artículo lo hace explícito ("lo que el modelo dice que puede atender y lo que
  efectivamente se probó no son lo mismo"). Es un criterio editorial, no un dato.
- **Nunca suavizar un fallo para cerrar lindo.** El texto dice "ocupa el lugar
  de una definición sin entregar la definición".
- **Números con unidad y contexto de medición.** No "rápido", sino "0.07 s".

### 2. READMEs en inglés (`projects/*/README.md`)

**Evidencia:** `projects/preflight/README.md` (8974 bytes, el más completo).

| Dimensión | Registro observado |
|---|---|
| Titular | Una frase que plantea el problema, no el producto: "Your AI built the site. This proves it works" |
| Prueba | Bloque de código con output real, no captura ni promesa |
| Secciones | `Why this exists`, `What makes it different`, `How it works` |
| Voz | Segunda persona al lector ("your page", "you") |

**Reglas específicas:**

- **Mostrar el output real antes de explicar la arquitectura.** El README de
  preflight abre con lo que oye un lector de pantalla, no con un diagrama.
- **Regla dura de USER.md aplica:** GitHub y lo publicado va en inglés.

### 3. GitHub (issues, PRs, comentarios)

**Evidencia:** `docs/OSS-TRACKER.md`, 22 repos, 16 PRs abiertos.

- Inglés técnico, sin adornos. Regida por `AGENTS.md` + `USER.md`, **no** por
  `voz-gonzo` (el corpus lo dice explícito).
- Nunca agradecer a bots de review.
- Nunca repetir un comentario ya hecho en el hilo: aportar algo nuevo.
- No pisar trabajo ajeno: si alguien reclamó un finding, sumar sin duplicar.

### 4. Posts públicos de branding (LinkedIn, X)

**Evidencia:** `content-serializer` Phase 0 + `voz-gonzo`.

**Punto resuelto (2026-11-06, Gonzo):** los posts públicos **usan la voz
`voz-gonzo` modulada**, no un registro aparte. Razón: el contenido de branding
sale de los artículos, READMEs y PRs, que ya están en esa voz. Crear un tono
"de marca" separado sería una cuarta definición donde ya hay una que funciona.

**Acción ejecutada (2026-11-06):** el alcance de `voz-gonzo` ya incluye posts
públicos de branding, con la tabla de modulación por tipo de pieza (deep-dive /
anuncio / opinión / CTA). Vive en el canónico, no duplicada acá. Verificado el
2026-11-09 durante la auditoría de la sesión.

### 5. Carrera: CV, entrevistas, mensajes a reclutadores

**Evidencia:** `cv-tailor`, `mock-interview-drill`, `voz-gonzo` casos 2026-09-11.

- Mensajes a reclutadores: voz completa de `voz-gonzo`.
- CV: formato STAR, sin primera persona narrativa.
- **Regla de `voz-gonzo` que aplica fuerte acá:** no exponer urgencia ni
  necesidad propia. "Se dice con disponibilidad, no con ansiedad."
- No poner números económicos por escrito sin pedido explícito.

---

## Palabras y fórmulas vetadas

Fuente: `voz-gonzo` regla 3 y 9 + `copy-editing` Sweep 2 + AGENTS.md.

**Prohibido siempre, en cualquier superficie:**

- "¡Gran pregunta!", "Excelente punto", "Interesante observación"
- "Espero que esto ayude", "Quedo atento", "Cualquier cosa me decís"
- "En el radar", "para lo que venga" (debilidad según regla 1)
- "En este post voy a enseñarte..." (regla de serializer: contar, no anunciar)
- Adulación vacía de cualquier tipo
- Agradecer a un bot de review

**Cuidado con:**

- "profesional" usado como adorno - el artículo lo usa con ironía
  ("no lo disfrazás para sonar más profesional")
- "solución" genérica, "robusto", "sinergia", "potenciar" - `[sin evidencia de uso negativo explícito; es criterio de lectura, no regla verificada]`

**Sobre guiones:**

- Regla 13 de `voz-gonzo` (2026-11-03): el guion largo **no es veto**, criterio
  laxo. No se reescribe una frase para sacarlo, ni se fuerza a meterlo.

---

## Convenciones de estructura que ya se usaron

Detectadas en el material, no inventadas:

- Tesis en el subtítulo, no rótulo descriptivo (artículos).
- Tabla de ficha/datos al principio cuando hay mediciones.
- Veredicto en mayúscula + severidad cuando se evalúa algo.
- Cierre por utilidad: qué sirve y qué no.
- Separador `---` entre bloques grandes.
- Metadatos en italic con fecha al pie (`_Creado 2026-09-11. Última actualización..._`).

---

## Decisiones editoriales ya registradas

| Fecha | Decisión | Por qué | Fuente |
|---|---|---|---|
| 2026-11-03 | El guion largo deja de ser veto | El uso se extendió, Gonzo lo acepta | voz-gonzo regla 13 |
| 2026-09-14 | La trayectoria sale de `USER.md` a memoria | Cap fijo de 4.000 chars | voz-gonzo límites |
| 2026-08-06 | Regla del guion obligatorio retirada | ADR-082 | git log |

**Log de correcciones de esta pieza:** este archivo todavía no tiene ninguna.
Cuando lo corrijas, la primera entrada va acá.

---

## Validación (2026-11-06)

Validado por Gonzo en la misma sesión:

- (1) Descripción de superficies: **correcta.**
- (2) Posts públicos: **voz global modulada.** Ver acción pendiente en sección 4.
- (3) Frentes: **completos.** No falta ninguno.
- (4) Vetos: **ninguno más.** Los de arriba son todos.

---

_Solo lo verificable. Lo no verificable quedó marcado. Nada inventado._

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
