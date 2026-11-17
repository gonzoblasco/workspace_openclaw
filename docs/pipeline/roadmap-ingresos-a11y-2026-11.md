# Roadmap: de credencial OSS a ingreso

> **Qué es:** el plan de un programa, no un roadmap de rol. Responde "¿cómo se convierte lo que ya
> está hecho en trabajo pago, y en qué orden?".
> **Qué no es:** no es el sistema de trabajo (`docs/ROADMAP.md`), ni la madurez del Crew
> (`docs/ROADMAPS.md`), ni la lista de tareas (`memory/memory.db` → `todos`). Las tareas fechadas
> viven en la DB; acá viven las fases y sus criterios de salida.
> **Dueño:** Kanam CORE. **Fecha:** 2026-11-16. **Estado:** borrador para aprobación de Gonzo.
> **Cómo se mantiene:** cada fase se cierra con su señal de salida **medida**, no declarada.

---

## 1. Estado real de partida (verificado el 2026-11-16)

| Activo | Estado | Fuente |
|---|---|---|
| PRs mergeados upstream | **12** (react-spectrum 2, carbon 1, ibm-products 2, astryx 4, base-ui 1, material-ui 1, shadcn 1) | GitHub search + `career-facts.md` §5.1 (corregido hoy: decía 11) |
| Piezas publicadas sobre esos PRs | **2** (#10503 el 22/10, #10554 el 09/09) | `docs/linkedin/react-spectrum-*.md` |
| Piezas posibles con material ya existente | 10 | §5.1 |
| Canal que ya convirtió | LinkedIn (la propuesta EIT/HTC/Disney llegó por ahí) | `memory/user-profile.md` |
| Vidriera pública | **rota**: la bio apunta a `gonzoblasco.github.io/a11y-portfolio` → 404 | `curl` 2026-11-16 |
| Producto propio con tesis | `preflight-a11y`, README listo, **sin URL pública ni landing** | repo |
| Audiencia en GitHub | 7 seguidores, 49 repos, 0 estrellas | API |
| Canal de marketplace | Mercor habilitado (W-8BEN firmado 2026-10-29) | `career-facts.md` |
| Inglés | B2+ | `career-facts.md` §7 |

**El diagnóstico en una línea:** la credencial existe y no se ve. El cuello de botella no es el
trabajo técnico, es que no hay superficie donde un comprador lo lea.

**Restricción que ordena todo el plan:** inglés B2+. Todo lo que dependa de una llamada de venta en
vivo pierde contra lo que dependa de texto escrito.

---

## 2. Fases

### Fase 0: cerrar la fuga (1 sesión corta)

**Objetivo:** que quien llegue por cualquier vía lea algo, en menos de 60 segundos.

- Cambiar la bio de GitHub a la versión verificada (solo repos con merge) y el campo website a un
  destino que responda 200.
- Elegir casa para la pieza larga y publicarla.

**Señal de salida:** `curl` a la URL de la bio devuelve 200 y el HTML contiene la pieza.
**Dueño del cambio externo:** Gonzo aprueba; CORE redacta y verifica.
**Riesgo:** ninguno técnico. El costo es que la bio nueva dice menos que la vieja.

### Fase 1: storefront mínimo (1 a 2 sesiones)

**Objetivo:** que Preflight sea la puerta de entrada, no un repo más.

- Landing con: qué hace, el ejemplo real del README (página válida, dos imágenes y un botón sin
  nombre), y un CTA de escaneo gratis.
- La pieza larga enlazada desde ahí y desde la bio.
- README del repo con topics y homepage apuntando a la landing.

**Señal de salida:** existe una URL pública; un tercero puede pedir un escaneo sin hablar con nadie.
**Dueño:** DEV para la landing, CORE para el texto, OPS para el deploy.
**Riesgo:** que la landing prometa más de lo que el CLI hace hoy.

### Fase 2: motor de contenido y watcher de tendencias (recurrente)

**Objetivo:** que el material se produzca solo y que sepamos qué se está publicando en el mercado.

- Cadencia: **1 pieza larga por mes, 2 cortas por mes**, desde los 10 PRs que faltan.
- **Watcher de dev.to** (ver §3).
- El registro de piezas sigue en `docs/linkedin/`, con estado y fecha de publicación.

**Señal de salida:** cola de 6 piezas por delante y un digest semanal con items verificados.
**Dueño:** CORE redacta, STUDIO edita, MIND verifica.
**Riesgo:** publicar por cadencia en vez de por sustancia. Un PR flojo no se convierte en post.

### Fase 3: canal outbound (2 a 3 sesiones)

**Objetivo:** conversaciones iniciadas por escrito, no por llamada.

Dos compradores, con motivo y con fecha:

1. **Con plazo legal.** European Accessibility Act en enforcement desde junio de 2025 (e-commerce,
   banca, SaaS europeo) y demandas ADA web en EE.UU., concentradas en retail. El comprador tiene una
   fecha encima y no tiene a nadie in-house.
2. **AI builders.** Lovable, v0, Bolt, Framer: sus sitios salen inaccesibles por default y la
   accesibilidad es una feature que necesitan. Gonzo tiene commits en los design systems de los que
   sus componentes bajan (Radix, shadcn, MUI).

- Mensaje escrito, corto, con un hallazgo concreto sobre *su* sitio. No un CV adjunto.
- El destino es la landing, no el perfil.

**Señal de salida:** N conversaciones por semana, con N definido por Gonzo antes de arrancar.
**Dueño:** CORE. **Riesgo:** que se lea como el mail de ZeroApply. La defensa es el hallazgo
concreto y verificable sobre el sitio del otro.

### Fase 4: medir y decidir (60 días después de Fase 1)

| Qué se mide | Por qué |
|---|---|
| visitas a la landing | ¿existe el tráfico o hay que comprarlo? |
| escaneos pedidos | ¿el producto atrae sin que se lo empuje? |
| conversaciones iniciadas / respondidas | ¿el mensaje escrito funciona? |
| propuestas enviadas / cerradas | ¿esto es un negocio o un ejercicio? |

**Decisión que habilita:** si en 60 días no hay escaneos ni conversaciones, se elige una sola cosa
entre producto, servicio o empleo, y se abandona el resto. El plan no se estira por inercia.

---

## 3. El watcher de dev.to: diseño

**Por qué:** Gonzo no conocía dev.to y quiere el mismo mecanismo que ya existe para Moltbook: mirar
qué se publica hoy, filtrar, y **verificar antes de adoptar**.

**Precedente que se copia:** `memory/moltbook/YYYY-Www.md`, generado por el job `moltbook-weekly-digest`
(lunes 09:00). Cada item lleva `status`, `source`, `verified_against`, `category`, `tags`. Un item sin
`verified_against` no entra.

**Lo medido hoy contra la API real:**

| Prueba | Resultado |
|---|---|
| `GET https://dev.to/api/articles?tag=accessibility` | 200, 8 items, ~17 KB |
| `...&top=30` | 200, **1 item**: `top` recorta demasiado y no sirve como filtro |
| `.../api/articles/latest?tag=accessibility` | **429** a las dos llamadas seguidas |
| `...?tag=X&per_page=10` en 5 tags con 6s de pausa | **200 en los 5**, 8 a 10 items cada uno |
| `GET /api/tags?per_page=60` | 200, lista real de tags para elegir sin inventar nombres |

Consecuencia de diseño: `per_page=10` sin `top`, **6 segundos entre tags**, y el ranking se
calcula del lado nuestro (`public_reactions_count`, `comments_count`, fecha).

**Alcance: no es solo a11y.** Gonzo lo pidió explícito el 2026-11-16: "leer los últimos 10 posts de
cada categoría". El digest cubre los tres nichos de marca (`memory/user-profile.md`) más mercado.
Los nombres de tag están validados contra `/api/tags`, no inventados:

| Nicho | Tags |
|---|---|
| a11y (diferenciador) | `accessibility`, `frontend` |
| fullstack (base) | `react`, `typescript`, `webdev` |
| agentic / AI-native (laboral) | `ai`, `agents`, `llm` |
| mercado y oficio | `career`, `discuss`, `opensource` |

Once tags, 10 posts cada uno: 11 requests con 6 segundos de pausa, **menos de 90 segundos** por
corrida semanal. La lista vive en un array del script y se edita sin tocar la lógica.

**Forma propuesta:**

- Script propuesto `scripts/watch-devto-trends.sh` (a crear): recorre el array de tags con pausa, y escribe
  `memory/devto/YYYY-Www.md`.
- Trigger condicional, igual que los otros watchers: solo dispara si hay items nuevos desde la última
  corrida. Sin novedad, `fire:false` y no consume modelo.
- Cada item conserva el contrato: qué dice, `source`, y **`verified_against`** (la afirmación técnica
  se contrasta contra la fuente primaria: spec, doc oficial, repo).
- Categorías del digest: `a11y`, `fullstack`, `agentic`, `mercado`, `contenido` (títulos, formatos,
  qué funciona).
- Cadencia: semanal, **sin chocar con `moltbook-weekly-digest`** (lunes 09:00). Va martes.

**La regla que evita que esto sea un lector de feeds:** el digest no lista links. Cada item responde
**"¿qué haríamos distinto?"**. Si un item no cambia una acción, no entra.

**Quién lo construye:** OPS (script + automation, es infraestructura). La selección y el criterio de
contenido son de CORE/MIND.

### 3.1 Estado: construido y verificado (2026-11-17)

- Script `scripts/watch-devto-trends.sh`: hecho. Corre en 61s, 11 tags, 6s entre requests, sin 429.
  Filtra a los últimos 90 días (el endpoint devolvía un post de 2024 cuando no hay volumen) y aplica
  el cupo de 3 por nicho antes de rankear.
- Digest `memory/devto/2026-W47.md`: 11 items reales, 5.9 KB. Títulos cruzados contra un `curl`
  fresco a la API: coinciden.
- Automation `watch-devto-trends` (`fb02a0f2-c787-4796-b4c9-279b964a4316`): miércoles 09:00
  `America/Buenos_Aires`, payload script sin modelo, corrida de prueba `status: ok` en 61.3s.
- **Deuda conocida:** `discuss` y `career` traen ruido de comunidad ("What are your goals this
  week"). No se filtra en el script a propósito: ese juicio es del campo `cambio:`, que completa
  CORE. Si el ruido sigue, se sacan esos dos tags.
- **Nota para el próximo:** los dos intentos de delegar esto a OPS devolvieron un stub y un fallo
  sin salida. El script lo escribió CORE. Verificar el archivo antes de creer un auto-reporte.

---

## 4. Lo que NO entra en este plan

- Un ATS nuevo, un CV reescrito o una postulación masiva. El CV ya está bien; el problema es la
  vidriera.
- Más PRs como objetivo. Ya hay 12; el material rinde más publicado que acumulado.
- Pagar por un servicio de lead-gen. Es el error de ZeroApply: comprar la esperanza del match.
- Español para las piezas de a11y. Esa materia va en inglés por mercado y por audiencia
  (`memory/user-profile.md`).

---

## 5. Decisiones tomadas (2026-11-16, Gonzo dio "vamos")

1. **Casa de la pieza larga:** repo con GitHub Pages. El dominio propio está pendiente desde
   2026-08-06 y no bloquea el plan.
2. **N de Fase 3:** 5 conversaciones iniciadas por semana, meta de 1 respuesta. Ajustable.
3. **Preflight:** producto con puerta a servicio (escaneo gratis como lead, auditoría con precio
   fijo como venta).

---

## 6. Secuencia revisada (planner 2026-11-16, corregida por CORE)

El planner entregó el orden de sesiones, los gates y las dependencias. **La estructura se adopta;
los mecanismos de Fase 0 se corrigen**, porque tres de ellos recreaban el bug que el programa viene
 a arreglar.

### 6.1 Lo que el planner propuso y se rechaza

| Propuesta | Por qué se rechaza |
|---|---|
| Website del perfil apuntando a `github.io/a11y-portfolio` como "landing provisional" | Esa URL es **la que devuelve 404 hoy**. Apuntar ahí reproduce exactamente el bug |
| Hacer commit y push al repo `gonzoblasco/a11y-portfolio` | **Ese repo no existe.** La bio no vive en un repo: es un campo del perfil |
| Bio primero, página después | Invierte la causa: se apuntaría a algo que todavía no responde 200 |
| Digest generado por `planner-weekly-plan` | Job equivocado. El watcher es de OPS y vive aparte de los de planner |
| Google Analytics como instrumentación por defecto | Es una decisión de privacidad, no un detalle. Contradice el pilar local-first del portfolio |

### 6.2 Fase 0 corregida (orden real)

1. **Publicar primero, apuntar después.** Crear el repo de las piezas con Pages, subir la pieza
   larga y verificar `curl -o /dev/null -w '%{http_code}'` = **200**.
2. **Recién entonces** cambiar el perfil: bio (139 caracteres) y campo `blog` al destino ya
   verificado. Se hace con `gh api -X PATCH user -f bio=... -f blog=...`, que necesita el scope
   `user`; si el token no lo tiene, se hace a mano en Settings.
3. **Verificar los dos campos por API** (`gh api user --jq '{bio,blog}'`), no por `curl` al perfil:
   GitHub renderiza el perfil con JS y el `curl` no prueba nada.
4. **Gate 0:** el `blog` guardado coincide con la URL publicada, y esa URL responde 200.

### 6.2.1 Estado al 2026-11-17

- **Hecho:** repo público `gonzoblasco/a11y-portfolio` creado, sitio publicado, Pages activo.
  `https://gonzoblasco.github.io/a11y-portfolio/` responde **200** y la pieza larga también
  (`/writing/the-quieter-announcement.html`, 200). El campo `blog` del perfil ya apuntaba a esa URL,
  así que **no hay que tocarlo**: el 404 se cerró publicando en el destino que ya estaba escrito.
- **Pendiente:** el texto de la `bio` todavía dice "Contribuciones a Facebook, shadcn/ui, Radix UI,
  IBM Carbon". Hay que reemplazarlo, y no se puede por API: el token de `gh` no tiene el scope
  `user`. Se hace en Settings o con `gh auth refresh -s user`.

### 6.3 Sesiones y gates

| Sesión | Entregable | Gate |
|---|---|---|
| 0 | perfil apuntando a una URL viva + pieza larga publicada | los dos campos verificados por API y la URL en 200 |
| 1 | landing de Preflight con CTA de escaneo | URL pública en 200, sin autenticación |
| 2 | cola de 6 piezas + watcher de dev.to (martes) | digest con 6 items verificados |
| 3 | 5 conversaciones semanales con hallazgo concreto | 1 respuesta por semana |
| 4 | medición a 60 días | decisión escrita: continuar, producto, servicio o empleo |

**Paralelo seguro:** la sesión 2 (script del watcher) no compite por archivos con la 0 ni la 1. La
sesión 1 y la redacción de piezas se solapan, porque la landing solo necesita la URL de la pieza,
que la produce la sesión 0.

### 6.4 Riesgo principal que el planner acertó

Que el programa se coma el tiempo sin producir ingreso. El corte está en el Gate 4: si a los 60 días
no hay visitas ni escaneos, se archiva el programa y se elige una sola cosa.
