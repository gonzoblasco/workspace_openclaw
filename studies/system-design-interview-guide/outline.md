# Clase: Design Software Systems Like a Senior Engineer

- Fuente: https://www.youtube.com/watch?v=soTfFFIQQ8U
- Canal: freeCodeCamp.org
- Expositor: Hayk Simonyan (@hayk.simonyan)
- Duración: 3:16:48
- Idioma: inglés (subtítulos automáticos)
- Transcripción: `transcripcion.md` (600 bloques, 32.433 palabras)

## Qué es esta clase (y qué no es)

No enseña tecnologías. Enseña **el procedimiento**: cómo se estructura el pensamiento en una entrevista de diseño
de sistemas y cómo ese mismo procedimiento se aplica a diseñar un sistema real. Los tres sistemas (Spotify,
Booking.com, WhatsApp) son el vehículo, no el objetivo.

El valor está en dos cosas concretas:

1. **Un framework temporal de 60 minutos** con presupuesto de tiempo por etapa.
2. **Cálculo de capacidad hecho a mano, a la vista**, en los tres sistemas — no como dato de un slide, sino como
   la cuenta completa que se espera que hagas en el pizarrón.

El curso tiene una carencia declarada que conviene tener presente desde el principio: **no da un solo problema
para resolver solo**. Todo se resuelve acompañado. El que termina el curso sabiendo reconocer un buen diseño
todavía no sabe producir uno; eso requiere práctica deliberada (ver `ADOPCION.md`).

## Resultado esperado

Capacidades verificables al terminar:

1. Aplicar las cinco etapas del framework a un enunciado vago en 60 minutos, con presupuesto de tiempo por etapa.
2. Hacer las tres cuentas de capacidad (storage, QPS/TPS, bandwidth) sin calculadora, dejando el procedimiento visible.
3. Justificar la elección de un componente por sus requisitos y poder nombrar la alternativa que se descartó.
4. Encontrar los puntos únicos de falla de un diseño propio y proponer el fallback antes de que lo pidan.
5. Distinguir entre *leer 1000 QPS* y *escribir 17 TPS* en términos de qué base de datos y qué aislamiento implica.

## Mapa temporal

| Tiempo | Bloque |
|---|---|
| 0:00:00 | Por qué importa el diseño de sistemas |
| 0:02:16 | Formatos de entrevista |
| 0:04:53 | Qué se evalúa: las cinco dimensiones |
| 0:07:30 | Profundidad práctica y manejo del tiempo |
| 0:09:14 | El framework de 5 pasos + presupuesto de tiempo |
| 0:11:08 | Paso 1: clarificar requisitos |
| 0:13:03 | Paso 2: data/API o high-level design |
| 0:16:44 | Paso 3: las cuatro componentes base |
| 0:17:07 | Paso 4: bottlenecks, escala y confiabilidad |
| 0:18:24 | Paso 5: trade-offs y extensiones |
| 0:23:55 | Sistema 1 (Spotify): requisitos y capacidad |
| 0:29:24 | Sistema 1: arquitectura y flujos de datos |
| 0:35:23 | Sistema 1: diseño de API |
| 0:40:04 | Sistema 1: storage y schema |
| 0:44:37 | Sistema 1: escalar a millones |
| 0:48:43 | La pirámide: por qué el mid-level se estanca |
| 0:50:52 | Sistema 2 (Booking.com): targets no funcionales |
| 0:58:22 | Sistema 2: cuentas de capacidad y arquitectura |
| 1:11:02 | Sistema 2: API e idempotencia |
| 1:22:34 | Sistema 2: modelado de datos e inventario |
| 1:33:05 | Sistema 2: concurrencia y race conditions |
| 1:34:44 | Sistema 2: sharding, caching y escala |
| 1:40:41 | Sistema 2: búsqueda a escala (Elasticsearch) |
| 1:45:19 | Sistema 2: replicación y ruteo global |
| 1:50:45 | Sistema 3 (WhatsApp): estimación de escala |
| 1:56:38 | Sistema 3: arquitectura y tiempo real |
| 2:07:04 | Sistema 3: modelado y flujos de API |
| 2:13:10 | Sistema 3: multi-dispositivo y entrega offline |
| 2:22:37 | Sistema 3: fanout, media y CDN |
| 2:31:44 | Sistema 3: event-driven y batch |
| 2:39:18 | Sistema 3: cifrado y rate limiting |
| 2:49:45 | Sistema 3: sharding y jobs de limpieza |
| 2:57:53 | Sistema 3: manejo de fallas y escala global |
| 3:09:08 | Feature flags y rollouts |
| 3:11:14 | Cómo mejorar de verdad + el framework en retrospectiva |

## Módulos

### Módulo 1 — Por qué el diseño de sistemas no se memoriza (0:00:00 – 0:02:16)

- **Objetivo:** entender qué cambia entre una entrevista de código y una de diseño, y por qué la memorización falla.
- **Contenidos:**
  - En código la salida es binaria; acá el enunciado es vago y *es tu trabajo clarificar esos requisitos y fijar el alcance*, en sus palabras: «it is your job to clarify those requirements and lock in the scope and also the output which is the solution» (0:04:13).
  - La diferencia decisiva, ya en el arranque: *no hay una única respuesta correcta* — lo que se mide es cómo pensás, no si acertás.
  - El curso promete tres sistemas *similares a* Spotify, Booking.com y WhatsApp desde cero — no clones, arquetipos.
- **Ejercicio:** escribir, sin mirar el outline, las tres diferencias que esperás encontrar entre una entrevista de código y una de diseño. Comparar después con el módulo 2.

### Módulo 2 — Las cinco dimensiones de evaluación (0:04:53 – 0:09:14)

- **Objetivo:** saber qué se puntúa antes de abrir la boca.
- **Contenidos:** las cinco dimensiones, en orden de aparición:
  1. **Comunicación y colaboración** — *si hacés preguntas de clarificación, si validás supuestos mientras avanzás* o si asumís y construís.
  2. **Pensamiento estructurado** — *romper el problema vago en acciones concretas*; los buenos candidatos *tienen al menos un esquema de los pasos que vamos a tomar*.
  3. **Juicio técnico** — «when you pick a solution let's say database a cache a message queue can you explain your decision why» (0:06:35).
  4. **Profundidad práctica** — «differentiates between two candidates who might have same theoretical knowledge but one of them also has practice with building these type of systems» (0:07:30).
  5. **Manejo del tiempo** — 45 o 60 minutos, y «not get stuck on one area and run out of time by doing highle design only» (0:08:10).
- **Idea fuerza:** «if you can't manage your time during an interview then you're also not good at managing your time during work» (0:08:52).
- **Ejercicio:** sobre una entrevista real que hayas tenido (o una mock), puntuarte 1-5 en cada dimensión y anotar la evidencia concreta que respalda cada nota.

### Módulo 3 — El framework de 5 pasos y su presupuesto de tiempo (0:09:14 – 0:11:08)

- **Objetivo:** tener un plan de 60 minutos que no dependa de la inspiración.
- **Contenidos:** la estructura y los minutos asignados:

  | Paso | Etapa | Tiempo |
  |---|---|---|
  | 1 | Clarificar requisitos (funcionales + no funcionales) | 5-10 min |
  | 2 | Data y API layer **o** high-level design (el orden es libre) | 15-20 min |
  | 3 | La capa que faltó del paso 2 | 15-20 min |
  | 4 | Escala, bottlenecks y confiabilidad (o edge cases si la confiabilidad manda) | 5-10 min |
  | 5 | Wrap-up: trade-offs y qué mejorarías con más tiempo | cierre |

  - El error más común del candidato, dicho literal: «You don't want to start designing anything before you understand the scope and this is the most common mistake candidates make» (0:09:47).
  - El orden entre data/API y high-level *es variable* — arrancá por la que te resulte más fácil de explicar (0:10:27).
- **Ejercicio:** cronometrarte resolviendo en voz alta una entrevista que ya conozcas, respetando los cortes. Anotar en qué minuto te desviaste.

### Módulo 4 — Paso 1: clarificar requisitos (0:11:08 – 0:13:03)

- **Objetivo:** convertir un enunciado vago en un alcance cerrado en menos de 10 minutos.
- **Contenidos:**
  - **Funcionales:** casos de uso principales, y explícitamente **qué queda fuera de alcance**. Con Spotify el argumento es contundente: *nunca podés diseñar eso en 60 minutos*; eso lleva equipos y meses (0:11:46).
  - **No funcionales:** DAU/MAU, ratio lectura/escritura, latencia, downtime aceptable (disponibilidad).
  - **El check de fase:** cerrar cada etapa preguntando «does this scope and these requirements make sense before I move forward to highle design» (0:12:50). Si el entrevistador te da una pista, es porque te faltó algo.
- **Ejercicio:** tomar el ejercicio *diseñá un clon de YouTube* y escribir (a) 3 casos de uso, (b) 3 cosas explícitamente fuera de alcance, (c) 4 números no funcionales. Sin eso, no avanzar al módulo 5.

### Módulo 5 — Paso 2: modelo de datos y contrato de API (0:13:03 – 0:16:44, primera mitad)

- **Objetivo:** modelar qué guardás y cómo interactúa el cliente, con las decisiones justificadas.
- **Contenidos:**
  - Entidades principales y sus relaciones (ejemplo del propio curso: en YouTube son videos y usuarios), claves primarias, foráneas, índices y **cuánto puede crecer cada registro**.
  - Dónde hace falta consistencia fuerte y dónde alcanza consistencia eventual — el curso lo pone como pregunta obligatoria de esta etapa.
  - Contrato de API: endpoints principales con request/response, y las cuatro cosas que *conviene mencionar*: paginación, manejo de errores, rate limiting, versionado.
  - La elección de base de datos va acá, y **con el descarte dicho en voz alta**: «what are other things you considered but you didn't choose» (0:14:59).
- **Ejercicio:** para el clon de YouTube del módulo 4, definir 5 entidades con PK/FK, elegir motor y escribir dos oraciones: por qué ese y qué alternativa descartaste.

### Módulo 6 — Paso 3: high-level design y las cuatro componentes (0:15:00 – 0:17:07)

- **Objetivo:** tener un punto de partida que funcione cuando *no se te ocurre nada*.
- **Contenidos:**
  - Las cuatro componentes que *están casi siempre* en la mayoría de los sistemas: **API servers, load balancer, base de datos, y opcionalmente cache** (0:15:19).
  - Recorrido del user journey de punta a punta: cliente → load balancer → API server → cache → DB → vuelta, **para lecturas y para escrituras**, no solo el happy path de lectura.
  - Si hay cache: decir TTL y mecanismo de invalidación.
  - Elegir por componente entre consistencia, disponibilidad y tolerancia a particiones (CAP), explicitando que **distintas partes del sistema pueden elegir distinto** (0:16:23).
- **Ejercicio:** dibujar el diagrama de las cuatro componentes y recorrer con el dedo el flujo de una lectura y de una escritura. Marcar en qué componente elegiste qué del CAP y por qué.

### Módulo 7 — Paso 4: bottlenecks, escala y confiabilidad (0:17:07 – 0:18:24)

- **Objetivo:** demostrar que pensás en lo que se rompe, no solo en el happy path.
- **Contenidos:**
  - El autor la marca como «one of the clearest signals that separates who's a mid-level candidate here who's a senior level candidate» (0:17:07).
  - Checklist del paso: puntos únicos de falla y su solución; fallbacks a un camino más lento pero funcional; redundancia (réplicas multi-AZ, auto-scaling, cache distribuido con replicación); **monitoreo, logging y alertas** — latencia de API, tasas de error, umbrales.
  - Lo del monitoreo: «This part is often overlooked but it's a strong signal that you think like a senior engineer» (0:18:11).
  - Igual que en el paso 1: chequear con el entrevistador si hay escenarios de falla específicos que quiere cubrir.
- **Ejercicio:** tomar el diagrama del módulo 6 y marcar cada SPOF con su fallback y su alerta. Si un SPOF no tiene alerta, todavía no está resuelto.

### Módulo 8 — Paso 5: trade-offs y la pirámide del senior (0:18:24 – 0:23:55 + 0:48:43)

- **Objetivo:** cerrar con criterio, no con un resumen del diagrama.
- **Contenidos:**
  - El cierre es una pregunta abierta: qué mejorarías, qué priorizaste, qué trade-off hiciste.
  - El marco de la pirámide, que el curso promete desde el minuto 24 y entrega en 0:48:43: abajo y más grande **planning/blueprinting** (requisitos, capacidad, arquitectura); en el medio **tech selection** (SQL o NoSQL, qué SQL, cache y políticas de evicción, storage); arriba y más chico **coding**.
  - La inversión del mid-level: «They start developing things without even having any plan, without having any text selection. They just start coding and see where it takes them» (0:50:07).
  - Y el argumento incómodo: *si lo único que sabés hacer es codear, ahora hay modelos en la nube o GPT que lo hacen más rápido, mejor y más barato*.
- **Ejercicio:** escribir en una frase qué etapa de la pirámide estás haciendo primero en tu trabajo real, y cuál te salteás.

### Módulo 9 — Sistema 1 (Spotify): requisitos y capacidad (0:23:55 – 0:29:24)

- **Objetivo:** hacer las cuentas de capacidad completas y sacar la conclusión de diseño que se sigue de ellas.
- **Contenidos:**
  - Enunciado: 500.000 usuarios, 30 millones de canciones. Artistas suben, usuarios buscan y reproducen, playlists, perfiles, observabilidad básica.
  - Formato como decisión de requisito: OGG/AAC a 64 kbps (móvil), 128 (estándar), 320 (premium); promedio de archivo **3 MB** (0:25:52).
  - Las cuatro cuentas:
    - Audio: 3 MB × 30 M = **90 TB**, *y esto no incluye las réplicas ni el overhead de versionado* — el autor sugiere estimar 2-3× por encima (0:26:53).
    - Metadata de canción: 100 B × 30 M = **3 GB**.
    - Metadata de usuario: 1 KB × 500 K = **0,5 GB**.
    - Bandwidth diario: con 3,5 min de escucha promedio y 128 kbps.
  - La conclusión de diseño que vale más que la cuenta: **el audio domina storage y bandwidth; la metadata es marginal**. Eso es lo que decide que el audio vaya a object storage y el resto a SQL.
- **Ejercicio:** rehacer la cuenta de bandwidth del día con tus propios números y ver si la conclusión (*el audio domina*) se sostiene o se invierte. Si se invierte, ¿qué cambió?

### Módulo 10 — Sistema 1: arquitectura, API y storage (0:29:24 – 0:44:37)

- **Objetivo:** ver el framework aplicado de punta a punta sobre un sistema concreto.
- **Contenidos:**
  - Arquitectura: app móvil/web → load balancer → API servers REST; el flujo de escritura de un upload (artista sube → validación → object storage → CDN → notificación).
  - API: `/search` con `query`, `type`, `limit` (default 20) y `offset` — paginación concreta, no genérica (0:35:31). Trending, follow de artistas con `POST /users/me/follow` y artist ID.
  - Storage: object storage tipo S3/Azure Blob para audio, con la propiedad clave dicha explícita: *los archivos de audio acá son inmutables*, si cambiás uno se re-sube y se borra el viejo (0:40:05). Layout jerárquico `artist/{id}/album/{id}/{song_id}`.
  - SQL para metadata con índices pensados por query: el índice de playlist items para responder *qué playlists contienen esta canción*.
- **Ejercicio:** para el flujo de upload, enumerar los cuatro puntos donde puede fallar (validación, escritura en S3, actualización de metadata, notificación). ¿Cuál deja el sistema inconsistente y cómo lo detectarías?

### Módulo 11 — Sistema 1: escalar a millones (0:44:37 – 0:48:43)

- **Objetivo:** ver cómo cambian las cuentas y las decisiones cuando entra el volumen.
- **Contenidos:**
  - Nuevo escenario: 50 M usuarios, 200 M canciones. Recalcular: metadata 20 GB, usuarios 50 GB, audio ~3 MB × 200 M.
  - «the key, as you can see, is starting simple. We don't want to overengineer for small amount of users and then gradually increasing the scale as we go» (0:48:29).
- **Ejercicio:** identificar el número de usuarios a partir del cual tu diseño simple del módulo 10 deja de alcanzar, y nombrar la primera componente que rompería.

### Módulo 12 — Sistema 2 (Booking.com): targets y las dos formas de estimar (0:50:52 – 1:11:02)

- **Objetivo:** dominar el cálculo de QPS/TPS desde un funnel, que es el núcleo técnico del sistema 2.
- **Contenidos:**
  - No funcionales concretos: «search results should appear under 500 milliseconds and booking confirmations are fine if they are handled between two or 3 seconds» (0:58:07); disponibilidad *four nines* (99,99 %); escalar horizontalmente sin rediseñar.
  - Funnel: 100% de visitantes → 10% buscan → 10% reservan; *la mayoría de los visitantes son tire kickers* pero igual hay que diseñar para su carga de lectura (0:59:29).
  - **Dos caminos de estimación, y alcanza con que el entrevistador te dé uno:** top-down (tráfico histórico: 500 M visitas/mes, 8 páginas por visita) o bottom-up (1.100 M room-nights/año).
  - La cuenta bottom-up completa: 1.100 M ÷ 2 noches = 550 M bookings/año ÷ 365 = 1,5 M/día ÷ 86.400 s = **17 TPS**.
  - La cuenta top-down: 500 M ÷ 40 días = 17 M visitas/día ÷ 86.400 = **200 visitas/s** × 5 lecturas de backend = **1.000 QPS**.
  - La conclusión: sistema «strong read heavy» — 1.000 QPS de lectura contra 17 TPS de escritura — con el desafío de «optimize the architecture for reads while still keeping the rights consistent to avoid the double booking problem» (1:03:41).
- **Ejercicio:** hacer las dos cuentas para un sistema de reserva de canchas (10 M usuarios, 5 % reservan por semana) y ver si el ratio lectura/escritura te lleva a la misma arquitectura que Booking.

### Módulo 13 — Sistema 2: idempotencia y el doble booking (1:11:02 – 1:22:34 + 1:33:05)

- **Objetivo:** entender el problema de concurrencia más citado en entrevistas y sus dos soluciones reales.
- **Contenidos:**
  - Idempotencia: la misma reserva enviada dos veces no crea dos reservas. La solución del curso, simple y concreta: una **reservation key**; el segundo request «any second request will get duplicate key error and we will return the existing reservation» (1:33:27).
  - El caso difícil: **dos usuarios distintos, la última habitación**. Con `read committed` ambos leen «queda 1», ambos pasan el check, ambos escriben — «that's exactly how double bookings happen» (1:34:49).
  - Solución A: `serializable` a nivel de transacción — *simple de implementar y funciona bien para TPS bajas*. Con 17 TPS entra, pero el autor marca los costos: las transacciones se bloquean entre sí (*si tenés TPS altas no escala bien*), riesgo de deadlocks al lockear recursos en distinto orden, y recomienda timeouts de lock y transacciones cortas (1:35:28).
  - Solución B, la que el autor considera mejor: quedarse en `read committed` (el default de PostgreSQL) y **lockear las filas de inventario con `SELECT ... FOR UPDATE`** mientras se chequea y reserva; el segundo que toca la misma fila espera, pero el resto sigue en paralelo (1:36:10). Eso «prevents the race condition by serializing access to» esas filas (1:36:29).
  - Conclusión del autor: `FOR UPDATE` como default, `serializable` reservado para TPS baja.
  - El argumento decisivo del curso para elegir SQL acá: 1.000 lecturas/s contra 17 escrituras/s, más la consistencia ACID que exige el negocio, más joins complejos para disponibilidad y precios → SQL «claramente» (1:33:05).
  - La alternativa de microservicios y por qué se evita: separar hotel y reservation services obliga a transacciones distribuidas; mantener juntos los datos acoplados permite *usar transacciones ACID locales en lugar de distribuidas*, con separación a nivel de aplicación pero datos compartidos (1:11:04).
- **Ejercicio:** implementar en un sandbox SQLite (o Postgres local) las dos transacciones concurrentes del doble booking y reproducir el fallo con `read committed`, y comprobar que `serializable` lo evita. Pegar la salida.

### Módulo 14 — Sistema 2: inventario, cache, búsqueda y ruteo global (1:22:34 – 1:50:45)

- **Objetivo:** ver las cuatro capas que sostienen un sistema read-heavy de verdad.
- **Contenidos:**
  - **Modelo**: se reserva un *room type*, no una habitación — «you book a specific type of room like is it a double queen bed or something else and not a specific room because the room numbers are assigned at the check-in» (1:22:56).
  - **Inventario en cache**: estructura Redis con key `hotel_id + room_type_id + date`, valor con disponible/reservado, y el **overbooking rate (10 %) como número fijo fuera del cache** (1:40:55). Eso último es un detalle de diseño que rara vez aparece explícito.
  - **Búsqueda**: por qué SQL no alcanza — full table scan, sin ranking por relevancia, sin tolerancia a typos («It cannot handle typos» — si el usuario se olvida una letra, el `LIKE` exacto no encontrás nada (1:45:24)). Elasticsearch como capa de lectura de búsqueda, no como source of truth.
  - **Réplicas**: lectura desde réplica salvo escritura reciente; «If it's a recent, write, then we should use the primary because the read replica might not be up to date yet» (1:50:23).
  - **Ruteo global**: geo-routing por cercanía del usuario (US/EU/Asia).
- **Ejercicio:** diseñar el esquema de cache de inventario y responder: ¿qué pasa si el cache se cae durante una ola de reservas? Escribir el fallback.

### Módulo 15 — Sistema 3 (WhatsApp): escala y las cuentas del mensaje (1:50:45 – 1:56:38)

- **Objetivo:** hacer las cuentas de un sistema write-heavy, el espejo del anterior.
- **Contenidos:**
  - Escenario: 1.000 M registrados, 500 M DAU, **50 M conexiones concurrentes** en pico, 10-20 mensajes por usuario por día.
  - Cuentas: 500 M × 20 = **10.000 M mensajes/día** = 10 B de writes/día → **115.000 msg/s** promedio → **350.000-500.000 writes/s** en pico (3-5× la media).
  - Storage: 1 KB por mensaje (contenido + ids + timestamp + status) × 10 B = **10 TB/día** → **3,6 PB/año**.
  - Bandwidth: 50 M conexiones × 10 KB/s promedio.
  - La conclusión que contrasta con Booking: acá el sistema es **write-heavy y de conexiones persistentes**, y eso lleva a Kafka, particionado por usuario e inbox persistente — no a un SQL con índices.
- **Ejercicio:** repetir la cuenta con 100 M DAU y verificar si 115.000 msg/s baja lo suficiente como para permitir un diseño más simple. ¿En qué número deja de ser cierto?

### Módulo 16 — Sistema 3: tiempo real y WebSocket (1:56:38 – 2:07:04)

- **Objetivo:** decidir el canal cliente-servidor con criterio, no por costumbre.
- **Contenidos:**
  - WebSocket frente a long polling y SSE: la elección y sus costos dichos sin maquillar — «it requires special load balancers that support them. So, we'll need to use layer 4 load balancing instead of layer 7. They also use more memory per connection on the server side because you're keeping connections open» (2:07:14).
  - El contraste con el cierre del curso: «for messaging app that tradeoff is worth it. For some other situation, the trade-off might not be» worth it (3:14:48), y ahí conviene polling.
  - Presencia online/offline vía Redis como primera consulta del flujo.
- **Ejercicio:** para el mismo caso de mensajería, escribir el argumento a favor y en contra de WebSocket en tres líneas cada uno. Si no podés escribir el contra sin copiar el del video, no lo entendiste.

### Módulo 17 — Sistema 3: modelado, multi-dispositivo y entrega offline (2:07:04 – 2:22:37)

- **Objetivo:** el núcleo del problema de mensajería: que el mensaje llegue cuando el receptor no está.
- **Contenidos:**
  - Flujos de API completos sobre WebSocket persistente: mensaje con sender, receiver, contenido, media y timestamp; ack de recibido; **ack de leído** (received vs read) con message ID y timestamp (2:13:12).
  - Tablas: users, messages, groups, group_members; historial en Cassandra para volúmenes grandes.
  - Multi-dispositivo: el dispositivo pide los últimos 30 días y el historial viejo «are fetched on demand when needed» (2:19:25).
  - Offline: si Redis marca al usuario offline, «we will add the message to user B's inbox with radius» y se dispara push (2:22:48).
- **Ejercicio:** diseñar el flujo completo de *A manda, B está offline, B prende el celular* con los estados por los que pasa el mensaje y dónde vive cada uno en cada momento.

### Módulo 18 — Sistema 3: fanout, media, CDN y event-driven (2:22:37 – 2:39:18)

- **Objetivo:** los dos problemas que no aparecen en un chat de juguete: fanout a muchos destinatarios y archivos grandes.
- **Contenidos:**
  - Media: pre-signed upload/download URLs desde el cliente contra S3; el chat server nunca proxya los bytes.
  - Entrega: CDN como *el enfoque más escalable*, replicando media cerca de cada usuario (2:32:00).
  - Batch: procesar de a 1.000 mensajes cada 5 s, con **atomic batch insert**, actualización de índices y marcado como procesado.
  - Cuando falla: retry + **dead letter queue** para los que fallan «out of this thousand, we have 10 of them which failed to be processed, we will write them into the dead letter Q» (2:39:23), con persistencia del error en el sistema de logging antes de reintentar.
- **Ejercicio:** escribir el handler de un batch que falla parcialmente. ¿Qué se reintenta, qué va a DLQ y qué se marca como procesado?

### Módulo 19 — Sistema 3: cifrado, rate limiting, sharding y limpieza (2:39:18 – 2:57:53)

- **Objetivo:** cubrir la operación que en las entrevistas se olvida: límites, particiones y basura.
- **Contenidos:**
  - Rate limiting con token bucket: tokens que se reponen, cálculo del próximo refill, y la respuesta al exceso — bloquear y notificar, o pedir CAPTCHA con límite de 1 hora (2:49:47).
  - Límites por acción (mensajes, creación de grupos, conexiones) — no un límite único global.
  - **Sharding por `hotel_id`** en Booking: *la mayoría de las queries filtran primero por hotel*, así todos los datos de un hotel quedan en el mismo shard, sin joins cross-shard y con transacciones locales (1:37:33). El **modulo sharding** aparece como fórmula inicial en el sistema 3, advertido como «this won't be consistent hash initially» (1:38:19), y el problema del usuario que usa mucho (tablas enormes) frente al que usa poco.
  - Cleanup jobs: expired media, mensajes no entregados viejos, conexiones stale; job scheduler tipo Airflow o cron diario.
  - Conexiones WebSocket: abrir solo cuando hay mensajes que escribir, no mantener la conexión ociosa.
- **Ejercicio:** dado el sharding por `hash(user_id) % N`, calcular qué pasa cuando N pasa de 8 a 16 y proponer cómo migrarías sin downtime.

### Módulo 20 — Sistema 3: fallas, feature flags y el cierre (2:57:53 – 3:16:48)

- **Objetivo:** cerrar con lo que hace la diferencia entre un sistema que funciona y uno que sobrevive.
- **Contenidos:**
  - **Redis caído:** background job que sincroniza el inbox desde la DB a Redis (`SELECT ... WHERE delivered IS NULL`), y recién después se retoma la escritura normal. Código completo con `store_undelivered_message` como fallback (3:02:46).
  - **Kafka caído:** los mensajes publicados que quedaron en memoria se republishan al volver; luego se persisten y se reanuda el consumo (3:11:02).
  - Feature flags: key-value con scope por entorno y por porcentaje de usuarios — «when you decide to also roll out it for production, you can still set it to true for only 20% of users» (3:12:26). LaunchDarkly citado como herramienta real usada en una empresa anterior.
  - Compatibilidad de versión de cliente: los features que el cliente de versión < 2.2 no soporta se eliminan del payload en el server.
  - **El framework en retrospectiva (3:13:51):** empezar simple con miles de usuarios, construir con el entrevistador, encontrar bottlenecks, recién entonces hablar de fallas. *No saltes directo a Redis, Postgres o sharding de base de datos* es mi paráfrasis de «So you don't jump straight into radius popsup or database sharding» (3:13:51)..
  - Y el cierre honesto: «You are not expected to design a perfect system in one or two hours» (3:15:48); *pensá en voz alta y el entrevistador te va a corregir*.
- **Ejercicio:** tomar uno de los tres sistemas y escribir el plan de rollback del deploy: qué feature flag, en qué porcentaje, con qué métrica para decidir avanzar o revertir.

## Ejercicios por bloque

- [ ] **M1-M2:** Escribir las diferencias código vs. diseño y autoevaluarte en las cinco dimensiones.
- [ ] **M3:** Resolver una entrevista cronometrada respetando los cortes del framework.
- [ ] **M4-M5:** Cerrar alcance y modelar datos de un clon de YouTube.
- [ ] **M6-M8:** Diagrama de cuatro componentes, SPOFs con fallback y alerta, y ubicarse en la pirámide.
- [ ] **M9-M11:** Rehacer las tres cuentas de Spotify y determinar el punto de quiebre a 50 M usuarios.
- [ ] **M12:** Hacer las dos estimaciones (top-down y bottom-up) de un sistema de reservas propio.
- [ ] **M13:** Reproducir el doble booking en un sandbox SQL y arreglarlo con `serializable`.
- [ ] **M14:** Diseñar el cache de inventario y su fallback.
- [ ] **M15-M16:** Estimar WhatsApp y escribir el argumento contra WebSocket.
- [ ] **M17-M18:** Diseñar el flujo A→B offline y el handler de batch con DLQ.
- [ ] **M19-M20:** Calcular el resharding y el plan de rollback con feature flag.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué el autor dice que las cuentas de capacidad van antes de la arquitectura y no después?
2. Si el ratio es 1.000 QPS de lectura y 17 TPS de escritura, ¿qué te dice eso sobre replicación y sobre aislamiento? ¿Dónde se gana el rendimiento y dónde no se puede aflojar?
3. El doble booking de dos usuarios distintos en una habitación no se arregla con una reservation key. ¿Por qué no, y qué dos soluciones existen?
4. ¿Por qué el curso insiste en que el orden entre data/API y high-level design *es variable*? ¿Qué dice eso sobre lo que realmente se evalúa?
5. ¿Cuál es el argumento honesto en contra de WebSocket y en qué caso lo descartarías?
6. ¿Qué cambia en el diseño de un sistema cuando el ratio se invierte y pasa a ser write-heavy, como WhatsApp?
7. ¿Por qué el curso dice que el monitoreo y las alertas son *una señal de senior* y no un detalle de operaciones?
8. ¿En qué se diferencia lo que este curso deja montado de lo que hace falta para aprobar la entrevista? (pista: no hay un solo problema resuelto solo)
9. Si tuvieras que defender *la pirámide* del minuto 48:43 ante alguien que dice que el trabajo senior de verdad es codear mejor, ¿qué evidencia del curso usarías y qué le faltaría a esa evidencia?

## Notas editoriales

- **Sin discrepancia de identidad.** El ASR deforma el nombre del autor como «Hike Simon»; el hablante se presenta como **Hayk Simonyan** y el canal del curso es el suyo (@hayk.simonyan). Se usa el nombre real en todo el outline.
- **El curso tiene un patrocinador**: la página de Hayk Simonyan con «job guarantee» (link en la descripción). No afecta el contenido técnico, pero el último minuto del video es promoción de su canal.
- **Cifras sin verificación independiente:** los números de Booking.com (500 M visitas/mes, 1.100 M room-nights/año), el *2-3× de overhead* en storage de audio y el *10 % de overbooking* son supuestos del autor para ejercitar el cálculo, no datos de la empresa. Están presentados como supuestos en el video y se registran acá como supuestos, no como hechos sobre esas empresas.
- **Carencia declarada:** no hay ejercicios ni problemas asignados. El curso se ve, no se practica. Por eso el `ADOPCION.md` es particularmente importante acá: lo que el curso no hace por vos es exactamente lo que hay que agregar.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
