# Consolidación: un producto vendible único (dealer + canal Mercado Libre)

**Fecha:** 2026-10-21
**Origen:** pedido de Gonzo - *"basta de kanam store, kanam cars, kanam market y cosas sueltas;
hagamos un único producto que integre todo y lo podamos revender como paquete cerrado"* - con el
análisis de Vane adjunto (`media/inbound/pasted-text-1792600438153.txt`).
**Estado:** decisiones de negocio **CERRADAS** (§7). No hay código escrito por este doc.
**Nombre:** temporal, sin marca todavía. En este documento: *el paquete*.

---

## 1. Lo primero: los nombres no existen

`kanam-store`, `kanam-cars` y `kanam-market` **no existen como proyectos**. Verificado:

| Verificación | Resultado |
|---|---|
| `grep -ril "kanam[-_ ]?(store\|cars\|market)"` sobre el workspace | 0 resultados |
| `ls ~/projects/*store* *cars* *market* *shop* *coche*` | sin coincidencias |
| `gh repo list gonzoblasco --limit 200` | ningún repo con esos nombres |
| `MEMORY.md` | ninguna entrada |

El único repo parecido es `gonzoblasco/catalogo-de-venta-de-coches` (agosto 2026, TypeScript/Next.js,
sin descripción, ~5 archivos), que es el **ancestro** de `kanam-onwheels`, no un producto aparte.

**La dispersión que hay que matar no son tres marcas: son tres piezas reales, y el desperdicio está
en que dos de ellas hacen el mismo trabajo.**

---

## 2. Inventario real (verificado hoy)

| Proyecto | Qué es de verdad | Código | Base | Mercado Libre |
|---|---|---|---|---|
| **`kanam-onwheels`** | Storefront + catálogo + inventario + chat RAG con evidencia citada | 7.493 LOC TS/TSX, Next.js 16 App Router | Supabase, 17 tablas, 10 migraciones, RLS con `company`/`membership` | **ninguna** (`grep meli` = 0) |
| **`soporteml`** | Bandeja de preguntas de MeLi + copiloto IA con RAG + KB + billing + multi-tenant | 19.037 LOC TS/TSX, React+Vite SPA | Supabase, 23 tablas, 25 Edge Functions, 54 migraciones, 354 `company_id` | OAuth, webhook, sync de preguntas, `POST /answers`, proxy/GET de items |
| **`kanam-query`** | **Papel.** La misma bandeja de preguntas, respecada y verificada contra la doc oficial | 0 LOC | - | spec completa, sin código |
| `vane` | El RAG que produjo el documento adjunto | - | SQLite | - |

### 2.1 El hallazgo que ordena todo

**`soporteml` y `kanam-query` son el mismo producto.** Uno está construido (19k LOC, con Pro Motors
como cliente real y `meliUserId 48316325` verificado), el otro está planificado (verde, sin una línea
de código, con un encuadre que dice explícitamente que *no* tiene relación con SoporteML).

Eso es la duplicación concreta. No es "store + cars + market": es **una bandeja de preguntas escrita
dos veces, una en código y otra en papel**.

### 2.2 Y son complementarios, no competidores

- **OnWheels tiene el catálogo canónico** (`unit` = la unidad física publicable) y **no tiene canal**.
- **SoporteML tiene el canal** y **no tiene catálogo propio**: su tabla `products` es un espejo
  (`meli_item_id NOT NULL`) - asume que el ítem **ya existe** en MeLi y solo lo lee.
- Verificado: en las 25 Edge Functions **no hay un solo `POST /items`**, ni `predictor`, ni mapeo de
  categoría para crear. `meli-item-proxy` es solo GET. SoporteML **no publica**, solo responde.

Traducido: no hay dos apps que fusionar. Hay **un core de dealer** (OnWheels) y **un conector de canal
que nunca se construyó sobre ese core** (lo que SoporteML hace para preguntas + lo que la spec de
kanam-query describe completo).

---

## 3. El documento adjunto: ya está analizado, y es el mismo archivo

`diff` byte a byte contra `media/inbound/pasted-text-1792597850483-...txt`: **IDÉNTICOS**. Es el mismo
texto de Vane que ya se analizó hoy en
`projects/kanam-onwheels/.knowledge/VEREDICTO-CONECTOR-MELI.md`. No hace falta reanalizarlo; lo que
cambia es **el pedido**, no el documento.

Lo que vale del documento (y ya está incorporado): distinguir dealer-SaaS-con-canal de
SaaS-independiente-de-preguntas; la regla de fuente de verdad (el catálogo es maestro, MeLi es
proyección); modelar alrededor del vehículo y no del `item_id`; publicación asíncrona con estados y
validación previa; y la honestidad de que **MeLi no tiene sandbox**.

Lo que no vale: su encuadre comercial es un SaaS multi-tenant facturable para muchos dealers - que es
exactamente el negocio de `kanam-query`, no el destino actual de OnWheels. Y como pieza técnica tiene
12 defectos de forma (razonamiento del modelo filtrado, fragmentos en chino) y de evidencia (la cita
dominante es la doc de **El Salvador** para un dealer **argentino**; 4 de 13 fuentes no se usan; una
no resuelve).

**Un detalle que el documento no dice y define el negocio:** la cuota de rate limit de MeLi es **por
Client ID**, compartida entre todos los tenants de esa app. Si el paquete se revende a 30 dealers con
una sola app, el techo de clientes lo pone MeLi, no la demanda. Esto está verificado en
`projects/kanam-query/.knowledge/EVIDENCIA-VERIFICADA.md` y es la restricción comercial número uno.

---

## 4. El paquete cerrado, en concreto

**Se construye de cero (D2), y no se hereda nada de los tres repos (D3, D4).** Lo que sigue no es un
plan de fusión: es **el mapa de capacidades que el producto nuevo tiene que cubrir**, y de dónde sale
el conocimiento de cada una -como referencia de lectura, no como código.

```
        ┌────────────── El paquete: 1 sitio = 1 tenant = 1 dealer ──────────────┐
        │                                                                       │
 Sitio  │  dominio propio (.com/.com.ar) · plantilla/estilos · catálogo        │
        │  fichas técnicas · fotos · chat RAG con evidencia citada · leads      │
        │                                                                       │
 Canal  │  OAuth MeLi · publicar unidad → `item` (POST /items + predictor)      │
 MeLi   │  sync precio/stock · snapshot · preguntas → inbox                     │
        │  borrador IA + aprobación humana · outbox · DLQ · rate budget         │
        │                                                                       │
 Desk   │  control plane: planes y entitlements · dominios · N cuentas por      │
        │  dominio · roles · KB · analytics · Stripe                            │
        └───────────────────────────────────────────────────────────────────────┘
```

### Las seis capacidades, y el estado real de cada una

| Capacidad | Existe en algún repo | Qué se lee de referencia | Qué hay que construir |
|---|---|---|---|
| Catálogo + inventario canónico (`brand`/`model`/`spec`/`unit`) | OnWheels lo modeló y lo verificó | su `data-model.md` y sus migraciones - **como lectura** | el esquema, con VIN resuelto desde el día uno |
| Chat RAG con evidencia citada | OnWheels lo tiene andando | su enfoque de "responde solo con evidencia" | el motor, con la KB por tenant |
| Publicación outbound en MeLi | **Nadie.** Cero `POST /items` en los 25 functions de SoporteML | - | todo: predictor de categoría, mapeo de atributos por país, `user_product_seller` |
| Ingesta de preguntas + respuesta | SoporteML lo tiene probado; la spec lo verificó | los flujos y **las trampas ya pagadas** (que están escritas) | el módulo completo con `api_version=4`, dedup, lock por pregunta |
| Multi-tenant con RLS | SoporteML (354 `company_id`) y OnWheels (36 policies) | ambas implementaciones, para no repetir sus errores | el aislamiento, pero **con el tenant = sitio** (§8), no el tenant = dealer |
| Billing + entitlements + dominios | SoporteML tiene Stripe (3 functions); nadie tiene dominios ni planes | el flujo de Stripe | control plane completo: planes, gates por dato, provisión de dominio |

**Lo que ninguna pieza existente cubre y es el 60% del producto:** el control plane (§8) y la
publicación outbound. Los 26.530 LOC de OnWheels + SoporteML cubren el 40% restante, y se reescriben.

Ese es el costo real de "base nueva", dicho sin maquillaje: **se paga dos veces lo que ya estaba
escrito**, a cambio de no arrastrar dos stacks incompatibles y dos modelos de datos invertidos entre sí.

---

## 5. Contradicciones con decisiones vigentes (hay que resolverlas, no promediarlas)

| # | Decisión vigente | Lo que implica este pedido | Estado |
|---|---|---|---|
| C1 | **D4 de OnWheels: regalo para el local de Esteban, sin billing** (`docs/adr/`, `architecture.md`) | "Revender como paquete cerrado" exige billing y multi-dealer | **RESUELTA** (§7 D1): Esteban es tenant 0, el paquete es comercial. D4 queda derogada para el producto nuevo y vigente solo para OnWheels dormido. |
| C2 | **kanam-query es greenfield e independiente, "bajo ningún concepto relacionado a SoporteML"** (corrección explícita de Gonzo, 2026-10-21 00:24, en su BRIEF) | Integrar todo pone a los dos en el mismo producto | **RESUELTA** (§7 D3): ambos quedan dormidos. El producto nuevo es greenfield y no hereda de ninguno. La restricción de Gonzo se cumple por partida doble: no hay relación, hay producto distinto. |
| C3 | **ADR-042: Stripe es el proveedor único** | Nada que ver con este doc; se respeta | Vigente |
| C4 | `soporteml/README.md` dice *"EL-1 Billing migrado de Stripe → Mercado Pago Preapproval ✅"* y `PLAN.md` dice *"Billing MP - nunca operativo"* | El código real tiene **solo** `stripe-*` (3 funciones), ninguna dependencia de mercadopago, y `mp_webhook_events` en migraciones | **Dos verdades en el mismo repo.** El README miente sobre el estado del billing |

C4 se corrige con una línea, pero es el caso testigo de la regla de fuente única: si el README de un
producto que queremos vender dice que cobra por Mercado Pago y el código cobra por Stripe, la due
diligence de un comprador lo encuentra en diez minutos.

---

## 6. Costo honesto de "base nueva"

No hay merge que hacer, y eso es una ventaja: **los dos stacks existentes son incompatibles entre sí**
(Next.js 16 App Router con lógica en el server vs React + Vite SPA contra Edge Functions) y sus modelos
de datos están invertidos (en OnWheels el catálogo es maestro; en SoporteML el maestro es MeLi).
Unificarlos habría costado más que reescribir, porque además cada uno arrastra su propia deuda.

El costo que sí se paga, y hay que decirlo: **26.530 LOC ya escritos quedan sin usar.** El esquema
Supabase de OnWheels ya está aplicado y verificado en un proyecto real (17 tablas, 36 policies) y no se
hereda. Con 1 dev, esto es un producto de varios meses, no un refactor de un fin de semana.

A favor: el producto nuevo **no arrastra** el destino "regalo, sin billing", el espejo de `products`,
la ambigüedad de `kanam-query` ni dos formas distintas de hacer lo mismo.

Riesgo de secuencia: **construir el paquete entero antes de que algo lo use.** Esteban es tenant 0, pero
un tenant 0 no valida precio. Con apuro, la secuencia sería cerrar canal + catálogo, conseguir un segundo
dealer que pague y recién entonces el control plane completo. **Sin apuro (§12) eso se relaja:** con
tiempo, el control plane completo de entrada sale más barato que retrofitearlo. Lo que **no** se relaja
es que cada etapa deje algo en uso.

---

## 7. Decisiones cerradas (2026-10-21, Gonzo)

| # | Decisión | Resuelto | Consecuencia asumida |
|---|---|---|---|
| **D1** | Destino del paquete vs el regalo a Esteban | **Esteban es el tenant 0.** Su local estrena el paquete. | El paquete es **comercial desde el día uno**: billing, planes y entitlements no son Fase 5, son parte del MVP. D4 ("regalo, sin billing") queda **derogada para el producto nuevo**; sigue vigente solo para `kanam-onwheels` como pieza dormida. |
| **D2** | Base del producto único | **Base nueva (greenfield).** | Se escriben de cero el core, el canal y el desk. Cero deuda heredada y cero acoplamiento a dos stacks incompatibles. Costo: nada de los 26.530 LOC existentes se reutiliza. |
| **D3** | SoporteML y kanam-query | **Quedan por fuera, dormidos.** Se pueden leer como referencia, **no se toca ni se toma nada de ellos**. | Ni código, ni esquema, ni migraciones, ni decisiones de esos repos se heredan. La evidencia verificada de la API de MeLi (cuota por Client ID, `api_version=4`, estados, `response_time`) **se re-verifica** contra la doc oficial en la Fase 0 del producto nuevo; no se cita como fundamento heredado. |
| **D4** | OnWheels | **Dormido**, igual que SoporteML. | El esquema Supabase ya aplicado y verificado (17 tablas, 36 policies) queda como referencia dormida. Si Esteban es tenant 0, su catálogo se carga de cero en el producto nuevo. |
| **D5** | Modelo de distribución | **Centralizado, con dominio propio por cliente**, estilo WordPress.com: capa gratuita limitada para captar, mensualidad para dominio + funciones avanzadas, y N cuentas profesionales por dominio. | Ver §8: **el tenant deja de ser el dealer** y pasa a ser el *sitio*. Es el cambio de modelo de datos más grande de todo el paquete. |
| **D6** | App de Mercado Libre | **Una app central ahora, una por dealer después**, cuando la cuota apriete. | Dos caminos de OAuth conviven desde el diseño: `ml_connection` tiene que soportar credenciales de app central *y* de app propia, con migración por tenant. La cuota central **es el techo comercial del arranque** y hay que medirlo desde el día uno. |

### Lo que estas decisiones cierran, y lo que abren

**Cierran:** no hay fusión de código, no hay comparación de stacks, no hay "cuál de los dos productos sigue". El paquete es un producto nuevo, con Esteban como primer cliente.

**Abren (bloqueante para el discovery, no para empezar a escribir):**
- **El nombre.** No hay marca. El producto nuevo necesita un slug para el repo y un nombre para el dominio raíz de la capa gratuita.
- **El precio de la mensualidad** y qué separa exactamente gratis de pago. Sin esto no hay entitlements.
- **Quién registra el dominio:** ¿el cliente trae su `.com` o el paquete lo compra y lo revende? Cambia el modelo de billing (suscripción sola vs suscripción + reventa de dominio con markup).

---

## 8. El modelo WordPress.com: sí se puede, y cambia el esquema

**Respuesta corta: sí.** No es una rareza: es multi-tenant con dominios propios, que es exactamente
lo que hacen WordPress.com, Shopify, Webflow, Squarespace y Tiendanube. Nada de eso requiere
infraestructura exótica. Lo que sí cambia -y hay que decidirlo ahora, no después- es **qué es un
tenant**.

### 8.1 El cambio que ordena todo: `account` ≠ `site`

En WordPress.com una persona tiene **una cuenta** y esa cuenta puede tener **varios sitios**, cada uno
con su dominio. El que paga es la cuenta; el que tiene catálogo, plantilla y dominio es el sitio.

Modelo de tres niveles:

```
account   (la persona/empresa que paga, con su método de pago y su plan)
   └── site        (el tenant real: dominio, plantilla, catálogo, canal MeLi)
         └── membership   (quién puede administrar este sitio, con qué rol)
```

| Concepto | Qué es | Ejemplo |
|---|---|---|
| `account` | Quien paga. Tiene plan, Stripe customer, y N sitios permitidos por plan | Esteban |
| `site` | **La frontera de aislamiento.** Dominio, plantilla, catálogo, inventario, conexión MeLi | `estebanmotos.com.ar` |
| `membership` | Acceso de una cuenta a un sitio, con rol | Esteban es `owner` de 2 sitios; su encargado es `editor` de uno |

**Consecuencia directa:** `site_id` (no `account_id`) va en **todas** las tablas de datos, con RLS.
`account_id` solo aparece en billing. Si esto se hace al revés -`account_id` como frontera- el día que
un cliente quiera su segundo dominio hay que migrar la base entera.

### 8.2 Qué separa gratis de pago (propuesta, no decisión)

| | Gratis | Pago |
|---|---|---|
| Dominio | subdominio del producto (`esteban.paquete.com`) | `.com` / `.com.ar` propio, con TLS automático |
| Catálogo | hasta N unidades, 1 plantilla | ilimitado, plantillas y estilos propios |
| Cuentas | 1 | N cuentas profesionales por dominio |
| **Canal MeLi** | **no incluido** | sí |
| Chat RAG | límite mensual de consultas | incluido |
| Analítica | básica | completa |

**El punto crítico, y es de negocio:** la capa gratuita **no puede incluir publicación en Mercado
Libre**. Con una app central (D6), la cuota es una sola y compartida; si 200 sitios gratis publican,
el techo se consume antes de que el primer cliente pague. El canal MeLi es el mejor gancho comercial
precisamente porque es lo que se cobra.

### 8.3 Dominios propios: el camino técnico real

No es "apuntar un DNS y listo". Las tres piezas:

1. **Verificación de propiedad** antes de emitir el certificado: el cliente agrega un registro `TXT`
   (o `CNAME` a un host de verificación) y el sistema confirma que el dominio es suyo. Sin esto
   cualquiera podría apuntar un dominio ajeno al producto y quedarse con el certificado.
2. **Emisión de TLS on-demand**: un proxy inverso tipo Caddy o Traefik pide el certificado en el primer
   hit del dominio, previa llamada a un endpoint de autorización que consulta la tabla de sitios
   verificados. Sin ese endpoint de autorización, un atacante puede agotar el rate limit de Let's Encrypt.
3. **Enrutamiento por `Host`**: el middleware resuelve `host → site_id` en una consulta cacheada y
   recién ahí renderiza con la plantilla de ese sitio. Un dominio no verificado no resuelve.

**Y una advertencia concreta:** un dominio mal configurado no da error, da *otro sitio*. Si el
`middleware` cae a un default silencioso cuando el `Host` no matchea, un cliente ve el catálogo de otro.
Eso es un incidente de datos entre tenants, no un bug de UI.

### 8.4 Lo que este modelo rompe (y hay que resolver al diseñar)

| Tensión | Por qué | Cómo se resuelve |
|---|---|---|
| **`site` vs conexión MeLi** | La conexión MeLi es de un **vendedor legal** (la cuenta de MeLi), pero el catálogo es del **sitio**. Un dealer con dos dominios tiene **una** cuenta de MeLi y dos sitios | `ml_connection` cuelga de `account`, y `channel_listing` de `site`. El mapeo `site → ml_connection` es explícito, no implícito |
| **Plan por cuenta, límites por sitio** | `account.plan` dice cuántos sitios y cuántas unidades; el consumo se mide por `site` | entitlements como **datos** (`plan`, `feature`, `limit`), nunca `if plan == "pro"` |
| **Billing de dominios** | Si el cliente trae su dominio, es una suscripción. Si el producto lo compra y lo revende, es suscripción + reventa con markup y una obligación de renovación hacia el cliente | **Decisión abierta** (§7, punto 3). Cambia el modelo de datos de billing |
| **SEO de la capa gratuita** | Subdominios del producto compiten entre sí y con el dominio raíz; los dealers quieren SEO propio | La capa gratuita es captación, no permanencia: el subdominio debe ser `noindex` o tener `canonical` claro |
| **Plantillas distintas** | "Estilos distintos por cliente" es theming multi-tenant: variables por sitio, no un fork del front | tokens de diseño en base, no CSS compilado por cliente |

### 8.5 Qué significa para el orden de construcción

El control plane **no es una fase final**: es la primera migración. `account`, `site`, `membership`,
`plan`, `domain` y RLS por `site_id` tienen que existir antes que el catálogo, porque todo lo demás
cuelga de ahí. Lo que sí puede esperar es la **reventa de dominios** (§7, punto 3): el MVP puede
arrancar con dominio propio del cliente y verificación por `TXT`, sin comprar dominios por nadie.

---

## 9. Nombre: OnWheels, y lo que se puede comprar hoy (verificado 2026-10-21)

**OnWheels es el nombre.** Gonzo lo propuso al jubilar el repo, y es la decisión correcta por tres
razones que no son estéticas:

1. **No hay que inventar marca.** La marca ya existió, ya se pensó y ya tiene historia en el workspace.
   Un nombre nuevo agrega una decisión y no agrega nada.
2. **Describe el producto, no la tecnología.** "On wheels" habla de vehículos, que es el vertical real.
   No promete "IA" ni "SaaS" ni "plataforma", que es lo que envejece mal.
3. **Es coherente con el recambio.** El repo dormido se llama `kanam-onwheels`; el producto nuevo toma
   el nombre y deja el prefijo `kanam-` (que es marca de autor, no de producto, y no se vende).

### Disponibilidad real de dominios

| Dominio | Estado | Evidencia |
|---|---|---|
| **`onwheels.com.ar`** | **LIBRE** | `whois -h whois.nic.ar` → "El dominio no se encuentra registrado en NIC Argentina" |
| `onwheels.io` | **LIBRE** | RDAP Identity Digital → HTTP 404; `dig NS` vacío |
| `onwheels.com` | **TOMADO desde 1997** | Verisign RDAP: registrado 1997-12-31, registrador **Tucows**, *client transfer prohibited*, vence **2026-12-30**, sin sitio activo (HTTP 000) |
| `onwheels.app` | TOMADO desde 2023 | Google RDAP: registrado 2023-02-17, vence 2027-02-17, resuelve a `85.208.21.159` |
| `onwheels.dev` | TOMADO desde 2022 | Google RDAP: registrado 2022-07-07, vence 2027-07-07, *client delete prohibited* |
| `getonwheels.com` | LIBRE | Verisign: "No match for domain" |
| `onwheelscloud.com`, `myonwheels.com` | LIBRE | Verisign: "No match for domain" |

**Costo de `.com.ar` (verificado en NIC Argentina):** alta **ARS 8.500**, renovación anual **ARS 8.500**,
transferencia **ARS 8.500** (≈ USD 5,5/año a ~1.545 ARS/USD). Validez de un año.

**Recomendación:** registrar **`onwheels.com.ar` ahora** - es el mercado, cuesta lo que dos cafés, y un
`.com.ar` libre con el nombre del producto no dura. Sumar **`onwheels.io`** como respaldo técnico y para
el dominio raíz de la capa gratuita si se quiere evitar el `.com.ar` en los subdominios. **No** intentar
comprar `onwheels.com`: está registrado desde 1997 por un tercero con candado de transferencia;
recuperarlo es una negociación, no una compra, y no es un problema que este proyecto tenga que resolver
para arrancar.

**Riesgo de marca a futuro:** `onwheels.com` es de un tercero. Con el producto en Argentina y Esteban
como tenant 0 no es un bloqueante hoy, pero es una razón más para no salir a vender afuera con este
nombre sin resolverlo antes.

---

## 10. Precio: 150-250 USD, con el benchmark real al lado

**Decisión:** entre **USD 150 y 250/mes** por sitio durante el PoC. Capa gratuita limitada + trial de
15 días con subdominio, con límites en MeLi y en IA.

### El argumento del 10% es bueno, pero no es el que cierra

"Menos del 10% de lo que cuesta un empleado" es un anclaje correcto para justificar el precio **ante
alguien que ya quiere comprar**. No es un argumento de venta: un dealer no compara un SaaS con un
sueldo, compara con lo que gana o deja de perder. El argumento real, y es verificable:

- **Un vehículo vendido** en este vertical (motos, cuatris, náutica) tiene un margen que en la mayoría
  de los casos supera los USD 1.800 - el año entero de suscripción a USD 150. **Una unidad extra al año
  paga el producto.** Ese es el número que va en la landing, no el del sueldo.
- **`sales_percent_increase`** -la métrica que MeLi calcula sola cuando el vendedor baja el tiempo de
  respuesta- es la palanca directa: el producto mejora la métrica con la que MeLi rankea. Eso es valor
  medible por el propio marketplace, no una promesa nuestra.

### Benchmark verificado (Tiendanube, 2026-10-21)

| Plan | ARS/mes | ≈ USD/mes |
|---|---|---|
| Inicial | gratis | - |
| Esencial | 27.999 | ≈ 18 |
| Impulso | 79.999 | ≈ 52 |
| Escala | 244.999 | ≈ 159 |

**Lectura honesta:** USD 150-250 pone el producto **en la banda del plan más alto del líder local**, y
es 3 a 5 veces el plan medio. Eso se sostiene **solo** si hace algo que Tiendanube no hace: publicar y
responder en Mercado Libre sobre un catálogo de vehículos. Si se vende como "una tienda online más", el
precio es indefendible y el cliente se va a Tiendanube por 52 dólares.

**Traducción operativa:** el precio alto obliga a que **el canal MeLi esté en el plan pago y funcione**.
Es la razón por la que §8.2 excluye MeLi de la capa gratuita: si el diferenciador se regala, no queda
producto que vender.

### Lo que el precio todavía no cubre, y hay que medir en la Fase 0

| Costo variable | Estado | Qué hay que medir |
|---|---|---|
| Consultas al modelo (chat RAG) | **desconocido** | tokens por consulta y consultas por sitio/mes → costo real por tenant. Sin este número el margen es una suposición |
| Embeddings de la KB | desconocido | ídem, con el tamaño típico de catálogo de un dealer |
| Cuota de MeLi | **no es costo, es techo** | llamadas por tenant/mes, para saber cuántos sitios entran con la app central (D6) |
| Infra (VPS) | conocido (§11) | USD 13-29/mes, fijo, no por tenant |

**Regla que no se negocia:** el plan pago no se publica con precio final hasta tener el costo por
consulta medido. USD 150 con IA ilimitada puede ser margen negativo si el chat se usa mucho. La salida
es un **límite de consultas por plan** (como hace Tiendanube con "usos de IA": 30 / 150 / ilimitado), no
un precio más alto.

---

## 11. Dominios y VPS en Hostinger: qué se puede y qué no

### 11.1 Dos figuras distintas que se confunden todo el tiempo

| Figura | Qué es | Obligación | Sirve para el arranque |
|---|---|---|---|
| **Afiliado / referido** | Se recomienda Hostinger con un link; si el cliente compra, comisión | Ninguna. El dominio es del cliente, a su nombre | **Sí, es lo recomendado** |
| **Revendedor (reseller)** | El paquete compra el dominio y lo revende al cliente | Ser titular o intermediario, gestionar renovaciones, responder cuando el cliente no renueva | **No al principio** |

Hostinger tiene **programa de afiliados** y **reseller master agreement** publicados. La diferencia
importa: cuando revendés un dominio, el que queda expuesto ante el cliente por un vencimiento o una
pérdida **sos vos**, no Hostinger. Es soporte de nivel 1 que hoy no existe.

**Recomendación:** arrancar como **referido** (link de afiliado + guía de 3 pasos: comprar, apuntar el
`CNAME`, verificar el `TXT`). Reventa recién con volumen y alguien atendiendo soporte. La comisión de
afiliado, además, es ingreso que no requiere cambiar una línea de código.

**Y algo que ningún proveedor permite sin ser revendedor con API:** automatizar la compra del dominio en
nombre del cliente. Si el flujo tiene que ser "el cliente pone su tarjeta y el dominio aparece solo", eso
es reventa, con las obligaciones de arriba.

### 11.2 El VPS: precios verificados, y una ambigüedad que hay que resolver antes

**Hostinger hoy** (plan a 24 meses, promoción vigente, verificado 2026-10-21):

| Plan | vCPU | RAM | Disco | Intro USD | **Renovación USD** |
|---|---|---|---|---|---|
| KVM 1 | 1 | 4 GB | 50 GB NVMe | 6,49 | 11,99 |
| KVM 2 | 2 | 8 GB | 100 GB NVMe | 8,79 | 14,99 |
| **KVM 4** | **4** | **16 GB** | **200 GB NVMe** | **12,99** | **28,99** |
| KVM 8 | 8 | 32 GB | 400 GB NVMe | 25,99 | 49,99 |

Todos incluyen backups semanales, firewall, API pública y dominio gratis por un año.

**Cuál sirve:** con **Postgres + worker + Next.js + proxy con TLS on-demand** en la misma máquina,
**KVM 2 (8 GB) queda corto** - Postgres y el build de Next compiten por RAM y no queda margen para un
segundo worker. **KVM 4 (4 vCPU / 16 GB / USD 28,99 al renovar)** es el punto de entrada realista. Y ojo
con el número: **8,79 es introductorio**, no el costo del año 3.

**La ambigüedad que bloquea:** `docs/learnings/infraestructura.md` (2026-09-06) registra que "el VPS se
dio de baja" tras el incidente del modelo caro, y `memory/inbox.md` dice que hay **n8n corriendo en un
VPS de Hostinger**. No hay host en `~/.ssh/config` ni acceso verificado desde esta máquina. Antes de
decidir "usamos el VPS que ya tengo" hay que confirmar **cuál es, si sigue vivo, qué corre hoy y qué
comparte**. Reutilizarlo **no es gratis**: si ya hospeda cosas, el producto comparte destino y
superficie de ataque con ellas.

**Y la regla del 2026-09-06 sigue vigente:** cualquier instancia nueva se audita por *fallbacks de
modelo* antes de correr nada. Este producto no necesita gateway de agentes - y esa es la mejor razón
para **no mezclarlo** con el VPS de automatizaciones.

---

## 12. Ritmo: sin apuro, y por qué eso cambia el plan

**Dato nuevo:** no hay fecha. El proyecto avanza mientras Gonzo busca trabajo y se prepara para el TOEFL.
Es un *side project* de largo plazo - "crear el bebé que siempre tuvo que ser".

Eso cambia el cálculo, y hay que decirlo en las dos direcciones.

**Lo que mejora.** Sin deadline no hay razón para aceptar deuda técnica por velocidad. Se puede hacer
bien lo que con apuro se hace dos veces: el control plane antes que el catálogo, los tests del camino de
envío antes que la UI, la verificación de esquema antes del seed. La secuencia de §6 ("validar con un
segundo dealer antes de construir el control plane") **se relaja**: con tiempo, construir el control
plane completo de entrada es más barato que retrofitearlo.

**Lo que empeora, y es el riesgo real.** El riesgo deja de ser "el alcance es demasiado" y pasa a ser
**"nunca se termina"**. Un side project sin fecha, sin usuario esperando y sin presión externa es el
formato exacto en el que los proyectos mueren a los cuatro meses con el 40% hecho. Contra eso hay una
sola defensa, y no es disciplina: **tener algo funcionando pronto y alguien usándolo.**

**La secuencia que respeta las dos cosas:**

| Etapa | Qué entrega | Por qué ahora y no después |
|---|---|---|
| **0** | Spike de MeLi: permisos, `POST /items` real, cuota medida | Es el único riesgo que puede matar el producto entero; todo lo demás se corrige después |
| **1** | Control plane mínimo + catálogo + sitio de Esteban con su dominio | Primera cosa real y visible, con un usuario que la usa. Sin esto el proyecto es un documento |
| **2** | Canal MeLi: publicar + ingestar preguntas + responder | El diferenciador. Es lo que justifica el precio |
| **3** | Planes, entitlements, Stripe, capa gratuita, trial | Recién acá hay producto vendible a un segundo dealer |
| **4** | IA del chat y del borrador, con costo por consulta medido | Se puede construir antes, pero se **calibra** con datos de uso real |

**El criterio de éxito de un side project sin fecha no es "terminado": es "cada etapa deja algo que se
usa".** Si la etapa 1 no la usa Esteban, la etapa 2 no se empieza.

---

## Trazabilidad

- Inventario y LOC: `find`/`wc` sobre `projects/kanam-onwheels/src` y `projects/soporteml/src`.
- Tablas y functions: `projects/*/supabase/migrations`, `projects/soporteml/supabase/functions/`.
- Ausencia de MeLi en OnWheels: `grep -ril "mercadolibre\|meli" src supabase` → 0.
- Ausencia de publicación en SoporteML: `grep "api.mercadolibre.com"` → solo GET/answers/oauth.
- Documento adjunto idéntico: `diff` contra `media/inbound/pasted-text-1792597850483-...txt`.
- Evidencia de MeLi (cuota por Client ID, `api_version=4`, estados): `projects/kanam-query/.knowledge/EVIDENCIA-VERIFICADA.md`.
- Veredicto previo del mismo documento: `projects/kanam-onwheels/.knowledge/VEREDICTO-CONECTOR-MELI.md`.
- Destino D4 y schema de OnWheels: `projects/kanam-onwheels/docs/ADR*`, `supabase/migrations/`.

- Nombres del pedido inexistentes: `grep` sobre workspace, `gh repo list --limit 200`, `MEMORY.md` → 0.
- Dominios: `whois -h whois.nic.ar` (com.ar), Verisign RDAP (`.com`), Google Registry RDAP (`.app`, `.dev`), Identity Digital RDAP (`.io`), `dig NS`.
- Precio `.com.ar`: `nic.ar/es/dominios/aranceles` (alta/renovación/transferencia ARS 8.500).
- Precios VPS: `hostinger.com/pricing/vps-hosting` (leído 2026-10-21; el valor de renovación está en la misma tarjeta).
- Benchmark de precio: `tiendanube.com/planes-y-precios` (leído 2026-10-21).
- Afiliado vs reseller: `hostinger.com/affiliates` y `hostinger.com/legal/reseller-master-agreement`.
- VPS previo: `docs/learnings/infraestructura.md` (2026-09-06) y `memory/inbox.md` #1 - **contradicción sin resolver**, ver §11.2.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
