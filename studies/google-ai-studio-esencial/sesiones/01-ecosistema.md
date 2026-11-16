# 01 — El Ecosistema de Google AI (2:18)

**Qué dice.** AI Studio como punto centralizado para tres cosas distintas: (a) gestión de APIs de Gemini —probar modelos, generar imagen/video/código, comparar rendimiento, ver consumo, precio por token y *definir presupuesto*, generar y gestionar API keys—; (b) creación de aplicaciones desde un prompt, web **y Android nativo**, con integración a Workspace (leer un documento, crear eventos de calendario); (c) tres casos de uso: apps de uso interno, reemplazo de herramientas de terceros, y prototipado como punto de partida.

**Confirma el pasaje dudoso del tráiler:** era Docs y Calendar. "Consumir información de un documento de texto o crear eventos en tus calendarios".

**Lo que sostiene.** La arquitectura mental es correcta y es el valor real del video: un solo lugar para modelos, costos, claves y apps. Y el tercer caso de uso (prototipado) es la descripción honesta de lo que la herramienta hace.

**Lo que no sostiene.** "Las aplicaciones que produce son de muy alta calidad". Alta calidad en una app de un prompt significa que corre. No significa mantenible, testeable, con modelo de datos, auth ni observabilidad. El propio instructor se contradice dos frases después al llamarlo "punto de partida para productos completos" — esa es la versión verdadera.

**Claim a verificar en el capítulo 2.** "Código nativo para Android" generado desde un prompt. Build históricamente produce apps web (React/TS). Si el capítulo 2 no lo muestra funcionando, es claim de venta.

**Matiz sobre «presupuesto».** En Google Cloud el presupuesto es una alerta, no un freno: lo que efectivamente corta son las cuotas. Un curso de 2 minutos no va a distinguirlo y es la diferencia entre "me avisaron" y "me bloqueó".

**Conexión con el workspace:** el caso de uso "app interna que reemplaza herramientas de terceros" es literalmente el producto de reservas del avión. Y para el fleet de agentes: la atribución de costo por agente se consigue con una API key por agente, porque el consumo se mide por clave/proyecto, no por rol.
