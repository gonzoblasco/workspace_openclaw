# OnWheels - el producto (detalle largo)

> **Dueño:** `MEMORY.md` (entradas de una linea). Este archivo es el detalle que `memory_search` indexa.
> **Contexto de negocio completo:** `docs/ecosystem/CONSOLIDACION-PRODUCTO-DEALER.md` (12 secciones).
> **Roadmap:** `projects/onwheels/.knowledge/ROADMAP.md`.
> **Actualizado:** 2026-10-21.

## Qué es

Un producto único vendible que integra tres cosas que estaban repartidas en tres repos:

```
        ┌────────────── OnWheels: 1 sitio = 1 tenant = 1 dealer ──────────────┐
        │                                                                       │
 Sitio  │  dominio propio (.com/.com.ar) · plantilla/estilos · catálogo        │
        │  fichas técnicas · fotos · chat RAG con evidencia citada · leads      │
        │                                                                       │
 Canal  │  OAuth MeLi · publicar unidad → `item` · sync precio/stock            │
 MeLi   │  preguntas → inbox · borrador IA + aprobación humana · outbox · DLQ   │
        │                                                                       │
 Desk   │  control plane: planes y entitlements · dominios · N cuentas por      │
        │  dominio · roles · KB · analytics · Mercado Pago                       │
        └───────────────────────────────────────────────────────────────────────┘
```

## Las 12 decisiones de negocio (cerradas 2026-10-21)

| # | Decisión | Resuelto |
|---|---|---|
| D1 | Destino vs el regalo a Esteban | **Esteban es tenant 0.** Comercial desde el día uno. La decisión "regalo, sin billing" de OnWheels queda derogada para el producto nuevo |
| D2 | Base del producto | **Base nueva (greenfield).** No se heredan los 26.530 LOC de los tres repos dormidos |
| D3 | SoporteML y kanam-query | **Dormidos.** Se pueden leer como referencia; no se toca ni se toma nada |
| D4 | OnWheels (repo) | **Dormido** también |
| D5 | Distribución | **Multi-tenant estilo WordPress.com**: `account` paga / `site` es el tenant con dominio y plantilla propios / `membership` da acceso. `site_id` + RLS en todas las tablas. **El control plane es la primera migración, no la última** |
| D6 | App de Mercado Libre | **Central ahora, una por dealer después.** Dos caminos de OAuth desde el diseño, con migración por tenant |
| D7 | Nombre | **OnWheels**, sin prefijo `kanam-` (marca de autor, no de producto) |
| D8 | Precio | **USD 80-200 por plan.** Se define solo el de 80; premium abierto. **Ningún precio es final** |
| D9 | Cobro | **Mercado Pago**, registrado al amparo del punto 2 de ADR-042 (que permite que un proyecto evalúe otro proveedor) |
| D10 | Dominios | **`.com.ar` primero, `.io` después.** No se registran hasta que haya landing |
| D11 | Hosting | **Hostinger como referido**, no revendedor. Máquina: KVM 2 actual |
| D12 | Ritmo | **Sin apuro.** Side project de largo plazo, en paralelo a la búsqueda laboral y el TOEFL |

## Precio: el 80 en concreto

- **USD 80 = ARS 123.600** (FX de referencia: 1 USD = 1.545 ARS, dólar oficial).
- **USD 200 = ARS 309.000** (techo de la banda, plan premium futuro).
- Capa gratuita limitada + trial de 15 días con subdominio.
- **Mercado Libre e IA quedan FUERA de lo gratuito**: son el diferenciador y lo que se cobra.
- La IA que el plan incluye es **"la necesaria"** (responder consultas del catálogo, armar borradores), no ilimitada.
- **Ningún precio se publica hasta medir el costo por consulta real** (tokens in + out + embeddings). Se mide en F0.11 con el catálogo de Esteban.
- Benchmark de mercado (Tiendanube, 2026-10-21): ARS 27.999 / 79.999 / 244.999 = **USD 18,12 / 51,78 / 158,58**. No es comparable línea a línea (ellos venden marketplace con carrito y logística; nosotros sitio + dominio + hosting + catálogo + canal MeLi + chat con evidencia). Se conserva como **techo de percepción del mercado**.
- El argumento de venta que sirve: **una unidad extra vendida al año paga la suscripción**. No el "10% de un empleado".

## Dominios (verificado 2026-10-21)

| Dominio | Estado |
|---|---|
| `onwheels.com.ar` | **LIBRE.** ARS 8.500 = **USD 5,50/año** (NIC Argentina) |
| `onwheels.io` | Libre. USD 50/año |
| `onwheels.com` | **Tomado desde 1997** (Tucows, transferencia bloqueada, vence 2026-12-30) |
| `onwheels.app` | Tomado desde 2023 |
| `onwheels.dev` | Tomado desde 2022 |
| `onwheels.ai` | **Tomado desde 2026-01-17** (GoDaddy, proxy de privacidad, 4 candados). USD 180/año con mínimo de 2 años = USD 360. **No se persigue**: 33x el `.com.ar` por una señal que el cliente no lee |
| `getonwheels.com`, `onwheelscloud.com`, `myonwheels.com` | Libres |

## Hosting (Hostinger, precios verificados 2026-10-21)

| Plan | vCPU | RAM | Intro | **Renovación** |
|---|---|---|---|---|
| KVM 1 | 1 | 4 GB | 6,49 | 11,99 |
| **KVM 2** | 2 | 8 GB | 8,79 | **14,99** ← el actual |
| KVM 4 | 4 | 16 GB | 12,99 | 28,99 |
| KVM 8 | 8 | 32 GB | 25,99 | 49,99 |

- **El VPS existe** (KVM 2, con n8n sin uso). Lo que se dio de baja en 2026-09-06 fue el OpenClaw que corría ahí, no la máquina. Dato de Gonzo, corregido en `docs/learnings/infraestructura.md`.
- **Afiliado/referido, no reseller.** Cuando revendés un dominio, el expuesto ante el cliente por un vencimiento sos vos.
- **F0-F1 entran en el KVM 2.** Cuando entre el segundo dealer: o el producto sube a KVM 4 y n8n se queda en el 2, o segundo KVM 4 y cada carga en su máquina. **Separar por máquina es más barato que compartir y depurar.**
- Regla vigente del 2026-09-06: auditar *fallbacks de modelo* antes de correr nada en una instancia nueva. Este producto no necesita gateway de agentes: es la mejor razón para no mezclarlo con el VPS de automatizaciones.

## n8n y LangChain

- **n8n sí puede recibir y encolar el webhook de MeLi** (la Sustainable Use License lo permite: solo el backend le habla, el usuario final no configura workflows).
- **La línea está en el envío**: `POST /answers` va en código, con idempotencia por pregunta, máquina de estados (`queued` → `sending` → `confirmed`) y reconciliación del huérfano. No por licencia, sino porque un duplicado le llega a un comprador real y penaliza al dealer.
- **Prohibido** que el dealer construya o edite workflows (aunque sea por UI propia, API o agente). El test es quién controla la lógica, no quién ve la interfaz.
- **LangChain** queda como capa de ejecución del RAG del chat (ADR-099), no como capa web ni canal. Hoy corre en el Mac Mini con ChromaDB local.

## Cobro

- **Mercado Pago**: `preapproval` + planes, recurrente en **ARS**, reintentos automáticos, período de prueba, prorrateo. Medios: dinero en cuenta, tarjeta crédito/débito, Rapipago, Pago Fácil.
- **Stripe sigue siendo el proveedor reconocido del ecosistema y sí opera en Argentina.** El ADR-103 que escribí declarando lo contrario fue un error y está borrado. Lección: antes de declarar que una capacidad no existe, se pregunta a quien ya la usa.
- Modelo de datos con `provider` como dato: `account.plan`, `billing_provider` (`mercadopago` | `stripe`), `external_customer_id`, `external_subscription_id`, `subscription_status`. Cero `if provider == ...` en la lógica de features.
- **Costo a asumir:** precio pensado en USD, cobrado en ARS → hace falta una **política de ajuste periódico** escrita (Tiendanube publica ajuste trimestral en sus términos).

## El hallazgo de User Products (verificado 2026-10-21)

MeLi está migrando el modelo de publicación. Antes: un ítem agrupa sus variantes, con precio a nivel de ítem. Nuevo: un **User Product (UP)** es el producto físico (`user_product_id`); los ítems son las condiciones de venta; cada UP pertenece a una **familia** (`family_id`).

1. El contrato depende del **tag `user_product_seller`** en `GET /users`. Si lo tiene, **no se puede enviar el array `variations`**.
2. **Un dealer de vehículos es el caso exacto que UP viene a resolver**: precio por variante es algo que el modelo viejo no permite.
3. En UP el `title` no debe enviarse (lo reemplaza el `family_name`), y `condition` está deprecado: ahora es `item_condition` dentro de `attributes`.
4. La migración (UPtin) genera ítems nuevos y notifica por el tópico de ítems.

**Por qué está en F0 y no en F3:** el publicador no se puede escribir sin saber qué modelo aplica. Y el modelo de datos debe guardar `item_id`, `user_product_id` y `family_id` desde el inicio.

## Lo que está fuera, y por qué

- Publicación automática sin revisión (MeLi modera y penaliza).
- Auto-respuesta a preguntas (riesgo de baneo a nivel de app compartida).
- PII del comprador: `buyer_id` alcanza para agrupar el hilo.
- Panel de construcción de workflows para el dealer (licencia n8n).
- Multiempresa / multi-sitio en el mismo dealer (ningún cliente conocido lo necesita).
- Sincronización bidireccional MeLi ↔ catálogo (el catálogo es el maestro).
- Micro-frontends / plugins por cliente.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
