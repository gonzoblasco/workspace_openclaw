# Módulo 1 — Qué es n8n (00:00 - 01:45)

> Clase del curso `studies/n8n-ai-automations/`. Fuente primaria: el video. Todo dato del ponente se contrastó contra n8n.io, la doc oficial y la API de GitHub el 2026-11-11; lo verificado va marcado, lo que no, también.

## La idea en una frase

**n8n no es "Zapier con nodos": es un runtime de orquestación que vos hosteás, donde el workflow es código dibujado.** Esa frase es la que hay que poder defender; todo lo demás del módulo se cae si no entendés esa diferencia.

## Lo que dice el ponente — y qué pasa la verificación

| Claim del video | Tiempo | Veredicto |
|---|---|---|
| «n8n is an automation infrastructure and orchestration engine, a backend for intelligent workflows» | 00:48 | ✅ **Correcto como descripción.** Es una definición, no un claim medible |
| «Zapier is just a small subset of what n8n can actually do» | 01:06 | ⚠️ **Impreciso, y el argumento real es otro.** Ver abajo |
| «co-founder and CEO of TechDome [...] number one creator on n8n» | 00:33 | ⚠️ **Anécdota sin fuente.** No es verificable ni importa para el módulo |
| «transformed over 1200 plus businesses» | 00:33 | ⚠️ **Anécdota sin fuente.** No se cita como dato |
| «around 2,000 to 2,500 workflow executions → starter plan» | 01:58 | ✅ **Confirmado con número exacto:** Starter = **2.5K ejecuciones/mes por 20 €/mes** facturado anual (n8n.io/pricing). Que el ASR dijera «2,00» era el bug de la transcripción, no del ponente |

### El claim de Zapier, desarmado

Decir «Zapier es un subconjunto de n8n» no se sostiene: Zapier tiene catálogo propio, y en cantidad de integraciones no lo superás. Lo que **sí** se sostiene — y es el argumento que hay que llevarse — son tres ejes donde n8n es estrictamente más general:

1. **Corre en tu máquina.** Zapier es SaaS puro. n8n self-hosted no manda tus datos a nadie.
2. **Podés escribir código adentro.** El Code node acepta JavaScript/Python real. En Zapier, la lógica no trivial te deja peleando con filtros o pagando paths.
3. **El workflow es un artefacto.** n8n lo exporta como JSON, lo versionás en Git, lo importás. Eso es lo que lo convierte en infraestructura y no en una cuenta.

El punto del módulo no es «n8n es mejor», es **«n8n es de otra categoría»**: Zapier resuelve *integraciones*; n8n resuelve *sistemas*.

## Los números reales (verificados hoy)

| Dato | Valor | Fuente |
|---|---|---|
| Stars | ~210.200 | GitHub API, 2026-11-11 |
| Forks | ~61.470 | ídem |
| Creado | 2019-06-22 | ídem |
| Issues abiertas | ~1.219 | ídem |
| Último push | 2026-11-12 | ídem — repo vivo, no abandonado |
| Nodos/integraciones en `nodes-base` | **308 directorios** | conteo directo del árbol `master` |
| Integraciones que declara el README | «400+» | descripción del repo |

**Nota de honestidad:** 308 es lo que hay en `nodes-base` (los nodos core incluidos en community). El «400+» suma nodos de otros paquetes y credenciales. Los dos números son ciertos y miden cosas distintas; si citás uno, decí cuál.

**Licencia — esto importa y el ponente no lo dice.** n8n **no es open source**: es *fair-code*. La **Sustainable Use License** permite usar, modificar, crear derivados y redistribuir, con tres límites:
- solo para uso interno de tu negocio, o personal/no comercial;
- redistribuir solo gratis y sin fines comerciales;
- no alterar los avisos de licencia.

Consecuencia concreta: **podés correr n8n para tu empresa, no podés revenderlo como producto ni ofrecerlo como servicio de pago a terceros.** Los archivos `.ee.` están bajo licencia Enterprise aparte. Si alguna vez pensás montar una automatización como producto para clientes, esto define la arquitectura (te conviene tu propio backend, no empaquetar n8n).

## Las cinco familias de trigger

El ponente las enumera al pasar (03:06), pero son el **contrato de entrada** de todo workflow. Vale memorizarlas porque más adelante vas a tener que elegir una y justificar por qué:

| Familia | Cuándo | Ejemplo |
|---|---|---|
| **Manual** | Probás o disparás a mano | «Ejecutar workflow» |
| **App event** | La app ya tiene integración nativa | nuevo issue de GitHub, nuevo mail de Gmail |
| **Schedule** | Algo periódico que no emite evento | reporte diario a las 9 |
| **Webhook** | Algo externo te avisa por HTTP | form submit, pago de Stripe |
| **Chat** | Entrada conversacional | mensaje de Telegram, chat trigger del editor |

Regla que el curso repite después (módulo 11): **manual y schedule son los únicos que no reaccionan a un evento real.** Todo lo demás es reactivo, y reactivo es lo que escala.

## El modelo mental correcto de n8n

Si te quedás con una sola cosa de este módulo, que sea el desglose de lo que un workflow *es*:

```
[trigger] → [transformación] → [lógica] → [IA] → [acción]
```

Ninguna pieza es opcional por categoría, pero **todas son reemplazables por otra del mismo tipo**. Un trigger webhook se cambia por un trigger de Telegram sin tocar el resto. Un Set se cambia por un Code node. Eso es lo que el ponente llama «architecture» y es literal: el valor está en la forma, no en las piezas.

Y de acá sale la única pregunta de diseño que importa en todo el curso: **¿qué parte de esto tiene que decidir un modelo, y qué parte tiene que ser determinista?** Todo lo demás es plomería.

## Qué NO es n8n (los malentendidos que cuestan tiempo)

- **No es un backend.** No tiene base de datos de aplicación ni API pública que vos expongas. Es el orquestador *entre* tus servicios.
- **No es un reemplazo de código.** Si tu lógica es un parser complejo o un cálculo numérico pesado, eso va en un nodo de código o en un servicio aparte; n8n lo llama.
- **No es multi-tenant de negocio.** Tiene multi-usuario y proyectos, pero montar una plataforma para N clientes con datos aislados sobre una instancia no es su caso de uso; para eso está Enterprise o tu propio SaaS.
- **No es (del todo) open source.** Ver la sección de licencia arriba.

## Costos: los tres caminos, con números

| Camino | Costo real | Cuándo |
|---|---|---|
| **Cloud Starter** | 20 €/mes anual, 2.5K ejecuciones, 5 concurrentes | probar, primer workflow productivo |
| **Cloud Pro** | 50 €/mes anual, 10K ejecuciones, 50 concurrentes | varios workflows en producción |
| **Self-hosted community** | el de tu VPS (unos pocos €/mes) + tu tiempo de mantenimiento | datos sensibles, volumen alto, control |

**El truco de costos que el video no dice:** las ejecuciones se cuentan por *corrida del workflow*, no por nodo. Un workflow de 40 nodos que corre 1 vez cuenta 1. Por eso un schedule cada 5 minutos = ~8.600 ejecuciones al mes y se come el plan Starter solo. El ponente toca esto de costado en el módulo 14; acá es donde primero muerde.

## Ejercicio del módulo

No es el del outline («listar triggers»); ese es de reconocimiento. El que vale:

**Escribí en 5 líneas `mi-caso.md`** con este formato:

1. El proceso manual que hoy hacés a mano (y cuánto cuesta hacerlo mal).
2. Qué evento lo dispara, de las 5 familias.
3. Qué tiene que **decidir un modelo** — si la respuesta es «nada», no necesitás IA, y el curso te sirve igual pero por otras razones.
4. Qué pasa si falla (¿alguien lo nota?).
5. Por qué esto va en n8n y no en un script de 30 líneas. **Si el script gana, escribí eso**: es una respuesta válida y te ahorra tres módulos.

Pasámelo y lo usamos como hilo conductor del resto del curso: los módulos 3, 6 y 11 los vas a leer contra *tu* caso, no en abstracto.

## Banco de preguntas (respondelas antes de seguir)

1. ¿Por qué «n8n corre en tu máquina» cambia la categoría del producto y no es solo una preferencia de deploy?
2. Zapier factura por tarea. n8n por ejecución de workflow. ¿En qué caso concreto esa diferencia te cambia la arquitectura que elegís?
3. La Sustainable Use License te deja usar n8n internamente pero no revenderlo. Si tu plan fuera «vendo automatizaciones a clientes», ¿cómo montarías el stack sin violarla?
4. De las 5 familias de trigger, ¿cuáles son las dos que **no** son reactiva, y qué problema tienen en producción?
5. El ponente dice que el workflow «es un artefacto». Nombrá dos consecuencias prácticas de que sea JSON versionable que un SaaS cerrado no te da.
6. ¿Qué pregunta de diseño, repetida en todo el curso, separa un workflow de juguete de uno de producción?

## Pendientes para el módulo 2

El módulo 2 (canvas, hosting, self-hosting) es donde hay que ensuciarse. Para eso necesito una decisión tuya: **¿lo montamos local en la Mac mini (docker o npx), o en un VPS?** Según cuál elijas, el módulo 2 cambia de ejercicio.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
