# Kanam Story Bible

> Especificacion tecnica generada con kanam-spec. Ultima actualizacion: 24/9/2026, 7:40:39 p. m..

## Brief

- **Producto:** Kanam Story Bible
- **Problema:** Permite usando IA construir un mundo literario mediante la toma de decisiones, fichas. Se conecta como RAG a Kanam Writer quien de este modo conoce el mundo completo de la historia a escribir...
- **Objetivo:** servir de fuente de la verdad para las historias de Kanam Writer (aun no esta creada)... mi meta es absorber todas las features de SudoWrite (la cual sí tiene la idea de crear un Story Bible con las secciones: braindump, genre, style, synopsis, characters, worldbuilding, outline... los campos braindump, genre, stlye y synopsis hacen de fuente base para todo el conocimiento, y tanto characters como Worldbuilding tienen la opción de agregar fichas desde cero, generar el personaje y elementos usando IA basado en el contexto, y sorprendente que crea un nuevo personaje o elemento que aportaría y aun falta... ) agregando el mundo este que se construye con personajes, lugares, Lore, todo...
- **Stack:** auto alojada, corre local...

## Indice

- [Contexto y problema](#contexto-y-problema)
- [Alcance y no-alcance](#alcance-y-no-alcance)
- [Objetivos y metricas de exito](#objetivos-y-metricas-de-exito)
- [Requisitos funcionales](#requisitos-funcionales)
- [Requisitos no funcionales](#requisitos-no-funcionales)
- [Usuarios, roles y permisos](#usuarios-roles-y-permisos)
- [Flujos principales](#flujos-principales)
- [Modelo de datos](#modelo-de-datos)
- [Interfaces y contratos](#interfaces-y-contratos)
- [Arquitectura y stack](#arquitectura-y-stack)
- [Seguridad y privacidad](#seguridad-y-privacidad)
- [Estrategia de testing](#estrategia-de-testing)
- [Despliegue y operacion](#despliegue-y-operacion)
- [Riesgos, supuestos y decisiones abiertas](#riesgos-supuestos-y-decisiones-abiertas)


## Contexto

- Kanam Story Bible es un producto autoalojado que corre local. No depende de servicios externos ni de credenciales de terceros.
- Su funcion prevista es construir un mundo literario mediante decisiones del autor y fichas estructuradas: personajes, lugares y lore.
- El consumidor previsto es Kanam Writer, un producto de escritura que todavia no existe. El consumidor principal es futuro, no actual.
- La conexion entre ambos esta definida como RAG: Kanam Story Bible aporta el conocimiento del mundo, Kanam Writer lo consulta al escribir.
- El brief fija una meta de alcance: absorber las features de SudoWrite, que organiza el Story Bible en braindump, genre, style, synopsis, characters, worldbuilding y outline.
- En SudoWrite, braindump, genre, style y synopsis operan como fuente base de conocimiento. Characters y worldbuilding admiten fichas creadas desde cero, generadas por IA a partir del contexto, y sugerencias de elementos faltantes que aportarian al mundo.
- Kanam Story Bible agrega a ese esquema el mundo construido: personajes, lugares y lore como entidades conectadas entre si, no como campos de texto sueltos.

### Restricciones del contexto

- Ejecucion local: el modelo de IA disponible es el que corra en la maquina del usuario. [supuesto a validar: tamano de modelo y VRAM objetivo]
- Autoalojado: sin telemetria, sin cuentas, sin sincronizacion en la nube.
- Sin consumidor activo: Kanam Writer no esta creada, por lo que no hay contrato de integracion validado ni feedback de uso real.
- Alcance definido por comparacion con otro producto, no por un conjunto cerrado de requisitos propios.

## Problema

No existe hoy una fuente de la verdad del mundo literario que sea a la vez estructurada, generada con asistencia de IA y consumible por un escritor automatico.

Desglose del problema:

1. **El conocimiento del mundo vive disperso.** Sin un artefacto unico, braindump, genero, estilo, sinopsis, personajes, worldbuilding y outline quedan en documentos separados sin relaciones entre si. Un cambio en un personaje no se propaga a las escenas que lo mencionan.

2. **La generacion por IA sin contexto acumulado produce entidades genericas.** Un personaje generado sin acceso al genero, al estilo y al lore existente tiende a contradecir decisiones previas del autor.

3. **No hay mecanismo de deteccion de vacios.** El autor no sabe que le falta: un lugar sin habitante, una faccion sin conflicto, un personaje sin arco. SudoWrite cubre esto parcialmente con sugerencias de elementos faltantes; el brief pide llevarlo al mundo completo.

4. **La relacion entre fichas no esta modelada.** Personajes, lugares y lore se referencian entre si (quien vive donde, quien pertenece a que faccion, que evento afecta a quien). Sin ese grafo, el RAG recupera fragmentos aislados y pierde el vinculo entre ellos.

5. **El consumo por RAG impone requisitos que el formato de fichas no resuelve por si solo.** Que se recupera, con que granularidad, como se evita traer contexto irrelevante o contradictorio, y como se mantiene la coherencia cuando el mundo cambia despues de que Kanam Writer ya genero texto.

6. **El alcance esta definido por comparacion.** "Absorber todas las features de SudoWrite" es una meta, no una lista priorizada. No hay criterio de corte ni orden de implementacion derivado del brief.

### Preguntas abiertas que el problema deja sin responder

- Que ocurre cuando una ficha cambia despues de que Kanam Writer genero texto que la usaba.
- Quien gana cuando dos fichas se contradicen entre si.
- Si el mundo es unico por instalacion o si un usuario mantiene varios mundos en paralelo. [supuesto a validar]
- Si el autor puede editar a mano una ficha generada por IA sin perder la trazabilidad de su origen.

## Costo de no resolverlo

| Costo | Efecto concreto |
|---|---|
| Inconsistencia narrativa | Kanam Writer escribe con datos contradictorios; el autor corrige a mano escena por escena. |
| Retrabajo de fichas | Cada entidad se reescribe cuando cambia el contexto base; el esfuerzo crece con el tamano del mundo. |
| RAG de baja calidad | Recuperacion de fragmentos irrelevantes o desactualizados; el texto generado ignora decisiones que el autor ya tomo. |
| Mundo incompleto | Vacios detectados tarde, cuando ya hay texto escrito que depende de ellos. |
| Reescritura del modelo de datos | Si las fichas se modelan como texto plano, migrar a entidades relacionadas despues obliga a reprocesar todo el contenido. |
| Bloqueo de Kanam Writer | Sin fuente de la verdad, el producto consumidor no tiene contrato estable sobre el cual construirse. |
| Perdida de la ventaja diferencial | Sin el grafo de mundo, el producto queda como un clon de SudoWrite sin el agregado que el brief declara como meta. |

El costo se concentra en el autor: cada decision no registrada estructuralmente se paga en correccion manual y en perdida de coherencia del mundo. El costo se traslada tambien a Kanam Writer, que hereda el desorden como parte de su contexto de generacion.

## Antecedentes

- **SudoWrite**: referencia funcional directa. Story Bible con braindump, genre, style, synopsis, characters, worldbuilding y outline. Generacion de fichas desde cero, generacion por IA basada en contexto y sugerencia de elementos faltantes. Es el piso de features a igualar.
- **Kanam Writer**: producto consumidor, no construido. Define el caso de uso (escribir historias) pero no aporta requisitos tecnicos verificables todavia.
- **RAG**: patron de integracion previsto entre ambos productos. El brief lo menciona como mecanismo de conexion, sin especificar estrategia de indexado, chunking ni recuperacion.
- **Autoalojamiento local**: restriccion transversal de despliegue. Condiciona el modelo de IA usable, el almacenamiento disponible y la ausencia de servicios gestionados.

### Vacios de antecedentes

- No hay usuarios reales ni metricas de uso.
- No hay especificacion de Kanam Writer: ni formato de consulta, ni frecuencia, ni volumen.
- No hay definicion medible de que significa "mundo completo".
- No hay inventario cerrado de las features de SudoWrite a absorber, ni su prioridad.

## Alcance

### Unidad de trabajo y persistencia

- Proyecto Story Bible como unidad raiz: crear, nombrar, describir, duplicar y borrar. Un proyecto agrupa campos base, fichas, relaciones e indice vectorial.
- Multiples proyectos en la misma instalacion, sin cuentas de usuario ni autenticacion remota.
- Persistencia 100% local: base relacional para campos y fichas, indice vectorial local para RAG. Ningun servicio en la nube es obligatorio para operar.
- Exportacion e importacion del proyecto completo en JSON y en Markdown legible, para respaldo y portabilidad.
- Historial de cambios por ficha con recuperacion de la version anterior. (supuesto a validar: retencion de las ultimas N versiones, N a definir)

### Campos base (fuente del conocimiento)

- Braindump: texto libre sin estructura, punto de entrada del mundo.
- Genero y subgenero.
- Estilo: voz, tono, persona y tiempo verbal, nivel de violencia y romance, referencias declaradas.
- Sinopsis: resumen del mundo y de la historia marco.
- Edicion manual de los cuatro campos y generacion o refinamiento asistido por IA a partir del braindump.
- Los campos base son la primera capa de contexto que se inyecta en toda consulta RAG y tienen precedencia sobre las fichas cuando hay conflicto.

### Fichas de entidades

- Tipos de ficha en esta version: personaje, lugar, lore o concepto, objeto o elemento, organizacion, evento. (supuesto a validar: lista cerrada y ampliable por configuracion)
- Cada ficha combina campos estructurados (nombre, alias, rol, atributos propios del tipo) con texto libre.
- Relaciones tipadas entre fichas: pertenencia, parentesco, ubicacion, origen, conflicto, mencion.
- Vista de grafo navegable sobre las relaciones declaradas.
- Busqueda por texto y por similitud semantica sobre el conjunto de fichas.

### Generacion asistida por IA

- Alta manual de ficha desde cero, sin intervencion del modelo.
- Generacion de ficha completa a partir del contexto del proyecto: campos base mas fichas existentes.
- Generacion o completado de campos individuales dentro de una ficha ya existente.
- Deteccion de vacios: sugerencia proactiva de entidades que el mundo necesita y todavia no existen, con justificacion de que aporta cada una.
- Toda salida del modelo es una propuesta editable. Nada se persiste sin confirmacion explicita del usuario.
- Proveedor de LLM configurable: modelo local (Ollama, llama.cpp, vLLM) o API externa opcional. La instalacion funciona sin API externa.

### Consistencia

- Deteccion de contradicciones entre fichas: atributos incompatibles, relaciones imposibles, datos que chocan con los campos base.
- Reporte de inconsistencias con referencia a las fichas y campos involucrados. (supuesto a validar: revision bajo demanda, no en cada edicion)

### Estructura narrativa de alto nivel

- Arcos y tramas declarados como fichas de tipo arco, con planteo, conflicto y resolucion a nivel mundo.
- Vinculo entre arcos y las fichas de personaje, lugar y evento que participan.

### Interfaz RAG para Kanam Writer

- API local de consulta: dada una consulta o un fragmento de texto, devuelve los fragmentos relevantes de la biblia con su origen (proyecto, ficha, campo, seccion).
- Pipeline de indexado: chunking por ficha y por campo, embeddings, reindexado incremental al editar.
- Contrato de respuesta estable y versionado, para que Kanam Writer lo consuma sin acoplarse al modelo interno ni al esquema de almacenamiento.
- Endpoints de salud y de metadatos del proyecto: tipos de ficha, conteos, version del esquema.
- Kanam Writer no existe todavia, por lo que el contrato se valida contra un cliente stub incluido en el repositorio. (supuesto a validar: el stub se descarta cuando el consumidor real exista)

### Interfaz de usuario

- Aplicacion web local servida por el mismo proceso autoalojado.
- Vistas: campos base, listado y detalle de fichas, grafo de relaciones, panel de sugerencias, panel de inconsistencias, configuracion de modelo y proveedor.

### Trazabilidad con Sudowrite

| Feature de Sudowrite | Decision | Nota |
| --- | --- | --- |
| Braindump | Incluido | Campo base, editable y generable |
| Genre | Incluido | Campo base |
| Style | Incluido | Campo base |
| Synopsis | Incluido | Campo base |
| Characters | Incluido y ampliado | Ficha tipada, relaciones y grafo |
| Worldbuilding | Incluido y ampliado | Se desdobla en lugar, lore, objeto, organizacion y evento |
| Outline | Parcial | Arcos y tramas a nivel mundo, sin planificacion de escenas |
| Generacion de fichas con IA | Incluido | Desde el contexto del proyecto |
| Sugerencia de entidades faltantes | Incluido | Con justificacion y confirmacion previa |
| Generacion de prosa y capitulos | Fuera | Dominio de Kanam Writer |
| Reescritura y estilos de prosa | Fuera | Dominio de Kanam Writer |

## No-alcance (fuera de esta version)

- Kanam Writer: editor de prosa, generacion de capitulos, continuacion de texto, reescritura y control de calidad de escenas. Esta version solo expone el contexto; no escribe la historia.
- Planificacion escena por escena, beat sheets y outline de capitulos. Solo se cubre estructura de alto nivel.
- Multiusuario, roles, permisos y edicion colaborativa en tiempo real.
- Cuentas, autenticacion remota, sincronizacion en la nube y facturacion. El producto no es SaaS.
- Fine-tuning, entrenamiento o destilacion de modelos propios.
- Generacion de imagenes, portadas, mapas ilustrados o cualquier asset visual.
- Traduccion de la biblia a otros idiomas.
- Exportacion editorial con formato: EPUB, DOCX maquetado, PDF.
- Apps moviles o de escritorio nativas.
- Integraciones con terceros (Scrivener, Notion, World Anvil, Obsidian) mas alla de import y export en JSON y Markdown.
- Marketplace, plantillas compartidas o bibliotecas de mundos de otros usuarios.
- Control de versiones con ramas, merge y diff semantico entre versiones del mundo.
- Migracion automatica desde Sudowrite u otras herramientas.
- Analitica de uso, telemetria y reportes de producto.
- Busqueda semantica sobre obras externas o corpus ajenos al proyecto.
- Colaboracion con lectores beta, comentarios y anotaciones sobre el texto.
- Audio, TTS y narracion.
- Edicion concurrente del mismo proyecto desde dos instancias de la aplicacion.

## Criterio de corte

- Entra todo lo que Kanam Writer necesita para recibir contexto correcto y trazable del mundo. Si una feature no mejora la cobertura o la calidad de ese contexto, no entra.
- Entra lo que el usuario puede completar dentro de la instalacion local, sin cuentas ni servicios obligatorios de terceros.
- Sale todo lo que produce prosa o decide como se escribe la historia: es dominio de Kanam Writer.
- Sale todo lo que requiere infraestructura multi-tenant, sincronizacion entre dispositivos o tiempo real.
- Sale toda feature que duplique estado. La biblia es la unica fuente de la verdad y ningun dato del mundo se edita fuera de ella.
- Las features de Sudowrite se adoptan por funcion, no por paridad literal: se prioriza el mecanismo (generacion desde contexto, deteccion de vacios) sobre la forma de la interfaz.
- Una feature nueva entra en la version siguiente solo si cumple al menos una condicion: cierra un vacio del pipeline RAG, es requisito de un tipo de ficha ya soportado, o reemplaza una capacidad existente sin agregar superficie de mantenimiento.
- Todo pedido que no cumpla lo anterior se registra como candidato post-version. No se implementa por excepcion ni por pedido puntual.

## Objetivos

| Objetivo | Metrica | Meta | Prioridad |
|---|---|---|---|
| Cobertura funcional del Story Bible (paridad con SudoWrite) | Secciones con alta, edicion, persistencia y recuperacion: braindump, genre, style, synopsis, characters, worldbuilding, outline | 7 de 7 | Obligatorio |
| Story Bible como fuente de la verdad para Kanam Writer | API de consulta que devuelve contexto del mundo para una consulta dada, con contrato versionado | 1 endpoint estable y documentado | Obligatorio |
| Generacion de fichas asistida por IA | Tipos de ficha con generacion desde cero y generacion contextual: personaje, lugar, lore, elemento | 4 de 4 | Obligatorio |
| Contexto base para toda generacion | Fichas generadas que citan como insumo braindump, genre, style y synopsis | 100% de las generaciones | Obligatorio |
| Consistencia interna del mundo | Contradicciones detectadas por el validador sobre un corpus con contradicciones sembradas | >= 90% (supuesto a validar) | Obligatorio |
| Autonomia de despliegue | Funcionalidad operativa sin red externa, excluyendo el proveedor LLM configurado | 100% de las features core | Obligatorio |
| Sugerencia proactiva de fichas faltantes | Tasa de aceptacion de sugerencias de IA (personaje, lugar o elemento no existente) por sesion | >= 30% (supuesto a validar) | Deseable |
| Latencia de recuperacion RAG | p95 de respuesta de consulta con contexto sobre un mundo de hasta 500 fichas | < 2 s (supuesto a validar) | Deseable |
| Trazabilidad de cambios | Fichas con historial de versiones recuperable | 100% de las fichas | Deseable |
| Coste de generacion | Tokens consumidos por ficha generada respecto al baseline definido en validacion | <= baseline (supuesto a validar) | Deseable |
| Cobertura de pruebas | Cobertura sobre modulos de dominio, generacion y recuperacion | >= 70% (supuesto a validar) | Deseable |
| Onboarding | Tiempo desde instalacion hasta primer mundo usable en hardware de referencia | < 30 min (supuesto a validar) | Deseable |

### Supuestos a validar

- Los umbrales numericos (90% de deteccion, 30% de aceptacion, 2 s p95, 70% de cobertura, 30 min de onboarding) no surgen del brief y se fijan como punto de partida para la primera iteracion.
- El tamano de referencia del mundo (500 fichas) se asume como techo de la fase inicial.
- El proveedor LLM es el unico componente que puede requerir red externa; el resto del stack corre en el host autoalojado.

## Criterios de aceptacion del proyecto

- Un mundo creado en Kanam Story Bible es consultable por Kanam Writer mediante la API y devuelve contexto coherente con las fichas persistidas.
- Las 7 secciones del Story Bible persisten y son editables sin perdida de datos tras reiniciar el servicio.
- La generacion IA de una ficha toma como contexto braindump, genre, style y synopsis, y el resultado es editable antes de persistir.
- El sistema propone al menos una ficha nueva (personaje, lugar o elemento) ausente en el mundo, con justificacion derivada del contexto existente.
- El validador reporta contradicciones entre fichas sobre el corpus de prueba con la tasa definida en la tabla de objetivos.
- El despliegue completo corre en un unico host autoalojado sin servicios gestionados externos, salvo el proveedor LLM configurado.
- Existe un mundo semilla versionado que reproduce de forma automatizada los criterios anteriores.

## Requisitos funcionales

Los umbrales numéricos marcados como (supuesto a validar) no surgen del brief y deben confirmarse con el product owner antes de implementarse.

### Gestión de la Story Bible

| ID | Requisito | Prioridad |
|---|---|---|
| RF-01 | El sistema debe permitir crear una Story Bible con nombre, idioma y descripción. | Alta |
| RF-02 | El sistema debe permitir editar el campo braindump como texto libre sin límite de longitud fijo. | Alta |
| RF-03 | El sistema debe permitir registrar el género principal y hasta 3 subgéneros por Story Bible. | Alta |
| RF-04 | El sistema debe permitir registrar el estilo narrativo en texto libre y como selección de atributos predefinidos (voz, tiempo verbal, tono, nivel de violencia). | Alta |
| RF-05 | El sistema debe permitir editar la sinopsis de la obra. | Alta |
| RF-06 | El sistema debe marcar explícitamente braindump, género, estilo y sinopsis como campos de contexto base para la generación. | Alta |
| RF-07 | El sistema debe permitir importar el braindump desde un archivo de texto plano o Markdown. | Media |
| RF-08 | El sistema debe autoguardar cada cambio de campo en un intervalo no mayor a 5 segundos (supuesto a validar). | Alta |
| RF-09 | El sistema debe permitir duplicar una Story Bible completa, incluyendo fichas y relaciones. | Media |
| RF-10 | El sistema debe permitir exportar e importar una Story Bible completa en un archivo JSON versionado. | Alta |
| RF-11 | El sistema debe permitir eliminar una Story Bible con confirmación explícita del usuario. | Media |

### Fichas de personajes

| ID | Requisito | Prioridad |
|---|---|---|
| RF-12 | El sistema debe permitir crear una ficha de personaje desde cero. | Alta |
| RF-13 | Cada ficha de personaje debe requerir nombre y rol narrativo como campos obligatorios. | Alta |
| RF-14 | Cada ficha de personaje debe ofrecer campos opcionales de descripción física, psicología, motivación, conflicto, arco y trasfondo. | Alta |
| RF-15 | El sistema debe permitir generar una ficha de personaje completa con IA a partir del contexto base de la Story Bible. | Alta |
| RF-16 | El sistema debe permitir generar o completar un campo individual de una ficha con IA. | Alta |
| RF-17 | El sistema debe permitir regenerar una propuesta de IA descartando la anterior. | Alta |
| RF-18 | El sistema debe permitir editar manualmente cualquier campo generado por IA antes de guardarlo. | Alta |
| RF-19 | El sistema debe permitir definir relaciones tipadas entre dos personajes (por ejemplo aliado, rival, familiar) con descripción. | Alta |
| RF-20 | El sistema debe permitir adjuntar una imagen de referencia a una ficha de personaje. | Baja |
| RF-21 | El sistema debe permitir etiquetar fichas de personaje con etiquetas libres. | Media |
| RF-22 | El sistema debe permitir archivar una ficha sin eliminarla del índice de contexto. | Media |

### Worldbuilding

| ID | Requisito | Prioridad |
|---|---|---|
| RF-23 | El sistema debe permitir crear fichas de lugar, lore o evento, objeto o artefacto, facción u organización y regla del mundo. | Alta |
| RF-24 | Cada ficha de worldbuilding debe requerir nombre y tipo como campos obligatorios. | Alta |
| RF-25 | El sistema debe permitir definir jerarquía padre-hijo entre fichas de lugar. | Media |
| RF-26 | El sistema debe permitir generar una ficha de worldbuilding completa con IA a partir del contexto base. | Alta |
| RF-27 | El sistema debe permitir generar o completar un campo individual de una ficha de worldbuilding con IA. | Alta |
| RF-28 | El sistema debe permitir vincular fichas de worldbuilding entre sí con una relación tipada. | Alta |
| RF-29 | El sistema debe permitir vincular personajes con fichas de worldbuilding. | Alta |
| RF-30 | El sistema debe permitir definir reglas del mundo (sistema de magia, tecnología, límites físicos) como fichas consultables por el motor de contexto. | Alta |
| RF-31 | El sistema debe permitir adjuntar mapas o imágenes a fichas de lugar. | Baja |
| RF-32 | El sistema debe permitir crear tipos de ficha personalizados además de los predefinidos. | Baja |

### Outline

| ID | Requisito | Prioridad |
|---|---|---|
| RF-33 | El sistema debe permitir crear una estructura de outline jerárquica de al menos 3 niveles (acto, capítulo, escena). | Alta |
| RF-34 | El sistema debe permitir reordenar nodos del outline mediante arrastrar y soltar. | Media |
| RF-35 | El sistema debe permitir generar un outline completo con IA a partir del contexto base. | Alta |
| RF-36 | El sistema debe permitir expandir un nodo del outline en subnodos con IA. | Alta |
| RF-37 | El sistema debe permitir asociar personajes y fichas de worldbuilding a cada nodo del outline. | Alta |
| RF-38 | Cada nodo del outline debe tener un estado configurable (pendiente, en borrador, escrito). | Media |

### Generación asistida por IA

| ID | Requisito | Prioridad |
|---|---|---|
| RF-39 | El sistema debe permitir configurar el endpoint y el nombre del modelo local usado para la generación. | Alta |
| RF-40 | El sistema debe construir cada prompt de generación con el contexto base más las fichas relevantes de la Story Bible. | Alta |
| RF-41 | El sistema debe permitir generar propuestas de elementos ausentes (personaje, lugar, lore) que aporten al mundo según el contexto existente. | Alta |
| RF-42 | El sistema debe presentar cada propuesta de IA como borrador no persistido hasta que el usuario la acepte. | Alta |
| RF-43 | El sistema debe permitir aceptar, editar o descartar cada propuesta de IA de forma individual. | Alta |
| RF-44 | El sistema debe mostrar qué fichas y campos se usaron como contexto en cada generación. | Media |
| RF-45 | El sistema debe permitir configurar el límite de tokens de contexto enviados al modelo. | Media |
| RF-46 | El sistema debe permitir cancelar una generación en curso. | Media |
| RF-47 | El sistema debe operar sin conexión a servicios externos cuando el modelo local está disponible. | Alta |

### Consistencia y detección de vacíos

| ID | Requisito | Prioridad |
|---|---|---|
| RF-48 | El sistema debe listar las fichas con campos obligatorios o recomendados incompletos. | Media |
| RF-49 | El sistema debe detectar y listar contradicciones entre fichas sobre un mismo atributo del mundo. | Media |
| RF-50 | El sistema debe sugerir elementos faltantes según el género y la sinopsis declarados. | Media |
| RF-51 | El sistema debe permitir marcar cada campo como canon o borrador. | Alta |

### Búsqueda y navegación

| ID | Requisito | Prioridad |
|---|---|---|
| RF-52 | El sistema debe ofrecer búsqueda de texto completo sobre todas las fichas y campos base. | Alta |
| RF-53 | El sistema debe permitir filtrar fichas por tipo, etiqueta y estado. | Media |
| RF-54 | El sistema debe mostrar un grafo navegable de relaciones entre fichas. | Baja |
| RF-55 | El sistema debe mostrar un índice en árbol de toda la Story Bible. | Media |

### Integración con Kanam Writer

| ID | Requisito | Prioridad |
|---|---|---|
| RF-56 | El sistema debe indexar las fichas marcadas como canon en un almacén vectorial local. | Alta |
| RF-57 | El sistema debe reindexar una ficha automáticamente al modificarse. | Alta |
| RF-58 | El sistema debe exponer un endpoint de consulta que reciba un texto y devuelva los fragmentos de contexto relevantes. | Alta |
| RF-59 | El sistema debe exponer un endpoint que devuelva el contexto base completo de una Story Bible. | Alta |
| RF-60 | El sistema debe autenticar las llamadas de Kanam Writer mediante token local configurable. | Media |
| RF-61 | El sistema debe permitir exportar la Story Bible como bundle de contexto para consumo offline de Kanam Writer. | Media |

### Versionado y auditoría

| ID | Requisito | Prioridad |
|---|---|---|
| RF-62 | El sistema debe registrar un historial de cambios por ficha con fecha y autor. | Media |
| RF-63 | El sistema debe permitir restaurar una versión anterior de una ficha. | Media |
| RF-64 | El sistema debe registrar si el contenido de cada campo proviene de IA o de edición humana. | Media |

### Administración

| ID | Requisito | Prioridad |
|---|---|---|
| RF-65 | El sistema debe permitir ejecutar backup y restauración completa de la base de datos local. | Alta |
| RF-66 | El sistema debe funcionar en un despliegue auto alojado sin dependencia de servicios cloud. | Alta |

## Reglas de negocio

| ID | Regla |
|---|---|
| RN-01 | Una ficha sin nombre no se persiste ni se indexa para contexto. |
| RN-02 | Solo los campos marcados como canon se incluyen en el contexto enviado al modelo y en el índice vectorial. |
| RN-03 | Los campos base (braindump, género, estilo, sinopsis) tienen precedencia sobre las fichas cuando hay conflicto de contexto. |
| RN-04 | Ninguna propuesta de IA se persiste sin aceptación explícita del usuario. |
| RN-05 | Toda ficha generada por IA queda marcada como borrador hasta que el usuario la promueva a canon. |
| RN-06 | Una relación entre fichas es bidireccional y se refleja en ambas fichas. |
| RN-07 | Eliminar una ficha elimina sus relaciones y la quita del índice vectorial en la misma operación. |
| RN-08 | Archivar una ficha la excluye de la generación nueva pero la mantiene disponible para consulta RAG. |
| RN-09 | El contexto enviado al modelo nunca excede el límite de tokens configurado; el sistema trunca por prioridad de campo base a ficha. |
| RN-10 | Una Story Bible pertenece a un único proyecto y no comparte fichas con otra Story Bible. |
| RN-11 | El historial de versiones conserva al menos las últimas 20 revisiones por ficha (supuesto a validar). |
| RN-12 | El sistema no envía datos a servicios externos salvo que el usuario configure explícitamente un endpoint remoto. |

## Requisitos no funcionales

Los valores numericos de esta seccion son supuestos a validar con producto y contra el hardware de referencia. Solo derivan del brief: despliegue auto alojado, ejecucion local, ausencia de dependencia de servicios externos y uso como fuente RAG de Kanam Writer.

| ID | Categoria | Requisito | Verificacion |
|---|---|---|---|
| RNF-01 | Rendimiento | Lectura de fichas (abrir, listar, buscar por texto) con p95 <= 200 ms y p99 <= 500 ms sobre un mundo de 5.000 fichas. | Benchmark automatizado en CI con dataset sintetico de 5.000 fichas. |
| RNF-02 | Rendimiento | Generacion asistida por IA: primer token en <= 3 s y throughput >= 15 tokens/s en el hardware de referencia. | Medicion de streaming sobre 20 generaciones de 300 palabras. |
| RNF-03 | Rendimiento | Recuperacion RAG: embedding de consulta + busqueda vectorial top-k=20 sobre 200.000 chunks en <= 800 ms p95. | Test de latencia con 1.000 consultas contra indice precargado. |
| RNF-04 | Rendimiento | Indexado incremental: alta o edicion de una ficha reindexa en <= 2 s. Reindexado completo de 5.000 fichas en <= 30 min en background sin bloquear la UI. | Cronometro sobre operaciones de escritura y job de reindexado completo. |
| RNF-05 | Concurrencia | 3 sesiones simultaneas del mismo usuario sin degradacion mayor al 20% en las latencias de RNF-01. Escritura sobre una misma ficha serializada con lock optimista y deteccion de conflicto. | Test de carga k6 con 3 sesiones concurrentes y test de escritura conflictiva. |
| RNF-06 | Concurrencia | 1 generacion IA simultanea por instancia. Las solicitudes adicionales se encolan con timeout de 120 s y devuelven estado de cola a la UI. | Test de 5 solicitudes concurrentes de generacion. |
| RNF-07 | Escalabilidad | Capacidad soportada por instancia: 10.000 fichas, 200.000 chunks, 500 MB de texto fuente por mundo. Por encima de ese limite la degradacion debe ser gradual y documentada, no un fallo. | Test de carga con dataset al limite y al 150% del limite. |
| RNF-08 | Disponibilidad | 99% mensual en horario de uso, sin HA multi-nodo. El modo offline total es el caso base: la app opera sin conectividad a Internet. | Monitoreo de uptime del proceso y prueba con interfaz de red sin salida. |
| RNF-09 | Fiabilidad | Si el motor de inferencia no responde, la app sigue operativa en modo lectura y edicion manual. Reintentos con backoff 1 s / 2 s / 4 s, 3 intentos, luego error explicito. | Chaos test: detener el contenedor de inferencia con la UI en uso. |
| RNF-10 | Recuperacion | RPO <= 5 min y RTO <= 30 min. Snapshot automatico cada 15 min y backup diario con retencion de 7 dias. | Restore drill trimestral con medicion de tiempo y perdida de datos. |
| RNF-11 | Capacidad | Base de datos mas indice vectorial <= 5 GB para 10.000 fichas. Los pesos de los modelos no se incluyen en la imagen: se montan como volumen de 4 GB a 40 GB segun cuantizacion. | Medicion de uso de disco tras cargar el dataset al limite. |
| RNF-12 | Rendimiento | Cold start del stack completo <= 90 s. La UI responde en <= 10 s aunque el modelo siga cargando, mostrando estado de carga. | Medicion de arranque en hardware de referencia y en hardware minimo. |
| RNF-13 | Seguridad | Bind por defecto a 127.0.0.1. Si se expone en red, autenticacion obligatoria (token o usuario/clave) y TLS 1.3. Cifrado en reposo delegado al volumen cifrado del host. | Revision de configuracion por defecto y test de acceso sin credenciales. |
| RNF-14 | Privacidad | Cero llamadas salientes a terceros en la configuracion por defecto. Telemetria desactivada por defecto y opt-in explicito. El contenido del mundo no sale del host. | Inspeccion de trafico con tcpdump durante 24 h de uso normal. |
| RNF-15 | Portabilidad | Imagenes OCI para linux/amd64 y linux/arm64. GPU opcional: fallback a CPU con latencia hasta 5x mayor, informada en la UI. | Build multi-arquitectura y benchmark en modo CPU. |
| RNF-16 | Compatibilidad | Soporte de al menos 2 backends de inferencia locales (por ejemplo llama.cpp/GGUF y Ollama) y modelos de 3B a 70B parametros. Embeddings de 384 a 1024 dimensiones, con reindexado obligatorio al cambiar de modelo. | Matriz de pruebas por backend y por rango de dimension de embedding. |
| RNF-17 | Observabilidad | Logs estructurados en JSON con rotacion a 100 MB y retencion de 14 dias. Metricas por operacion: latencia p50/p95/p99, tasa de error, profundidad de cola de generacion. Sin exportacion externa por defecto. | Revision de logs y dashboard local tras una corrida de carga. |
| RNF-18 | Mantenibilidad | Cobertura de tests >= 70% en logica de dominio. Migraciones de esquema versionadas y reversibles. Build reproducible desde el mismo commit. | Reporte de cobertura en CI y test de migracion up/down. |
| RNF-19 | Usabilidad | Alta de ficha desde cero en <= 3 clics. Generacion asistida devuelve un borrador editable en <= 10 s p95 para 300 palabras. | Test de usabilidad con 5 usuarios y medicion de tiempos. |
| RNF-20 | Integracion | API de lectura para Kanam Writer: contexto base (braindump, genero, estilo, sinopsis) en <= 2 s y busqueda semantica en <= 800 ms p95. Contrato versionado v1 con compatibilidad hacia atras de 2 versiones menores. | Test de contrato contra el esquema v1 y prueba de compatibilidad con v1.0 y v1.1. |
| RNF-21 | Accesibilidad | WCAG 2.1 nivel AA en las vistas de fichas, editor y arbol de mundo. | Auditoria axe-core en CI sobre las vistas principales. |
| RNF-22 | Internacionalizacion | UI en es y en. Contenido del mundo sin restriccion de idioma. UTF-8 en toda la cadena, incluidos nombres de ficha y busqueda. | Test de renderizado con contenido en 3 alfabetos y busqueda con acentos. |
| RNF-23 | Costo | Costo marginal de operacion 0 en despliegue local. Consumo en reposo <= 1 GB de RAM y <= 2% de CPU. El pico en inferencia lo define el modelo elegido. | Medicion de consumo en reposo durante 1 h y perfilado durante generacion. |

## Restricciones de plataforma

### Despliegue

- Auto alojado y ejecucion local: no existe componente cloud obligatorio ni cuenta remota requerida.
- Docker Compose es el unico metodo de despliegue soportado en v1. Kubernetes y orquestacion multi-nodo quedan fuera de alcance.
- Sin HA, sin multi-tenant y sin escalado horizontal en v1. Una instancia atiende un mundo (supuesto a validar).
- Los pesos de los modelos no se distribuyen con el producto: el usuario los aporta y asume su licencia.

### Hardware de referencia

| Perfil | CPU | RAM | Acelerador | Disco libre | Uso |
|---|---|---|---|---|---|
| Minimo | 4 nucleos | 16 GB | ninguno | 50 GB | Lectura, edicion y generacion en CPU con latencia 5x |
| Recomendado | 8 nucleos | 32 GB | GPU 8 GB VRAM o Apple Silicon 16 GB unificada | 80 GB | Cumple RNF-02 y RNF-12 |

### Sistema operativo y red

- Linux x86_64: soporte primario. macOS arm64: soporte secundario. Windows via WSL2: best effort.
- Puertos por defecto: 8080 para la UI y la API, 11434 para el backend de inferencia. Ambos en loopback salvo configuracion explicita.
- Sin acceso a Internet requerido en runtime. La descarga inicial de imagenes y pesos es el unico paso que lo necesita.

### Integracion con Kanam Writer

- Kanam Writer no existe al momento de esta especificacion: la integracion se define contra un contrato de API versionado, no contra un cliente real.
- El contrato de lectura debe cubrir contexto base, fichas de personaje, fichas de lugar, lore y busqueda semantica. Cualquier campo nuevo entra como version menor.
- El Story Bible es la fuente de la verdad: Kanam Writer consume, no escribe. La escritura queda restringida a la UI de Story Bible en v1.

## Roles

| Rol | Descripcion | Alcance | Asignacion |
|---|---|---|---|
| Administrador | Opera la instancia: usuarios, roles, tokens de API, configuracion, backups y auditoria. Acceso total al contenido de todos los proyectos. | Instancia completa | Primer usuario creado en el despliegue; luego asignado por otro Administrador |
| Autor | Construye el Story Bible: edita campos base, crea y genera fichas, aprueba y consolida contenido, exporta. | Todos los proyectos de la instancia | Asignado por un Administrador |
| Colaborador | Aporta contenido sobre los proyectos o tipos de recurso que se le asignan. Todo lo que crea o edita queda en estado borrador hasta que un Autor o Administrador lo consolida. | Solo proyectos asignados | Asignado por un Administrador, con lista explicita de proyectos |
| Lector | Consulta el Story Bible consolidado. No genera, no edita, no exporta. | Proyectos visibles para su rol | Asignado por un Administrador |
| Servicio RAG | Rol no humano. Consume el indice RAG y el contenido consolidado via API con token. Es el punto de integracion de Kanam Writer. | Proyectos habilitados en el token | Token emitido por un Administrador |

### Supuestos

- Instancia auto alojada, mono inquilino: los roles son globales a la instancia, no por proyecto. La unica granularidad por proyecto es la asignacion del Colaborador. Supuesto a validar.
- Autenticacion local con usuario y contrasena, sin proveedor de identidad externo ni envio de correo. Supuesto a validar.
- El rol Servicio RAG no accede a la interfaz web, solo a la API.
- Los roles no son jerarquicos por herencia: cada rol tiene su propia fila en la matriz.

## Matriz de permisos

Convenciones:

- `Si`: permitido sin restriccion.
- `Asignado`: permitido solo sobre los proyectos o recursos asignados al usuario.
- `Borrador`: permite crear y editar en estado borrador. Publicar o consolidar requiere rol Autor o Administrador.
- `No`: denegado.

| Recurso | Accion | Administrador | Autor | Colaborador | Lector | Servicio RAG |
|---|---|---|---|---|---|---|
| Interfaz web | Acceder | Si | Si | Si | Si | No |
| API | Autenticarse con token | Si | Si | No | No | Si |
| Proyecto | Ver | Si | Si | Asignado | Si | Si |
| Proyecto | Crear | Si | Si | No | No | No |
| Proyecto | Editar metadatos | Si | Si | Asignado | No | No |
| Proyecto | Archivar o eliminar | Si | Si | No | No | No |
| Proyecto | Exportar o importar | Si | Si | No | No | No |
| Campos base (braindump, genre, style, synopsis) | Ver | Si | Si | Asignado | Si | Si |
| Campos base (braindump, genre, style, synopsis) | Editar | Si | Si | Borrador | No | No |
| Campos base (braindump, genre, style, synopsis) | Generar con IA | Si | Si | No | No | No |
| Campos base (braindump, genre, style, synopsis) | Restaurar version anterior | Si | Si | No | No | No |
| Personajes | Ver | Si | Si | Asignado | Si | Si |
| Personajes | Crear ficha manual | Si | Si | Borrador | No | No |
| Personajes | Generar ficha con IA | Si | Si | Borrador | No | No |
| Personajes | Editar ficha | Si | Si | Borrador | No | No |
| Personajes | Aprobar o consolidar ficha | Si | Si | No | No | No |
| Personajes | Eliminar ficha | Si | Si | No | No | No |
| Worldbuilding (lugares, Lore, elementos) | Ver | Si | Si | Asignado | Si | Si |
| Worldbuilding (lugares, Lore, elementos) | Crear elemento manual | Si | Si | Borrador | No | No |
| Worldbuilding (lugares, Lore, elementos) | Generar elemento con IA | Si | Si | Borrador | No | No |
| Worldbuilding (lugares, Lore, elementos) | Editar elemento | Si | Si | Borrador | No | No |
| Worldbuilding (lugares, Lore, elementos) | Aprobar o consolidar elemento | Si | Si | No | No | No |
| Worldbuilding (lugares, Lore, elementos) | Eliminar elemento | Si | Si | No | No | No |
| Outline | Ver | Si | Si | Asignado | Si | Si |
| Outline | Crear o editar | Si | Si | Borrador | No | No |
| Outline | Generar con IA | Si | Si | No | No | No |
| Outline | Reordenar o eliminar | Si | Si | No | No | No |
| Relaciones entre fichas | Ver | Si | Si | Asignado | Si | Si |
| Relaciones entre fichas | Crear o editar | Si | Si | Borrador | No | No |
| Relaciones entre fichas | Eliminar | Si | Si | No | No | No |
| Indice RAG | Consultar via API | Si | Si | No | No | Si |
| Indice RAG | Ver estado y cobertura | Si | Si | Asignado | Si | Si |
| Indice RAG | Reindexar | Si | Si | No | No | No |
| Usuarios y roles | Ver | Si | No | No | No | No |
| Usuarios y roles | Crear o invitar | Si | No | No | No | No |
| Usuarios y roles | Asignar o cambiar rol | Si | No | No | No | No |
| Usuarios y roles | Desactivar | Si | No | No | No | No |
| Configuracion de instancia | Ver | Si | No | No | No | No |
| Configuracion de instancia | Editar | Si | No | No | No | No |
| Configuracion de instancia | Gestionar tokens de API | Si | No | No | No | No |
| Configuracion de instancia | Backup y restauracion | Si | No | No | No | No |
| Auditoria | Ver registro | Si | No | No | No | No |
| Auditoria | Exportar registro | Si | No | No | No | No |

## Casos de borde de permisos

- Ultimo Administrador activo: el sistema rechaza desactivar, degradar o eliminar al ultimo usuario con rol Administrador. Respuesta 409 con el motivo.
- Instancia sin autenticacion: si se despliega con `auth.enabled = false` para uso local de un solo operador, la sesion local opera como Administrador. Supuesto a validar: definir el valor por defecto del flag en el despliegue auto alojado.
- Colaborador sin asignaciones: ve la lista de proyectos vacia y no puede crear proyectos. No recibe error, recibe estado vacio.
- Contenido en borrador: las fichas generadas con IA y las creadas o editadas por un Colaborador quedan en estado `borrador`. Son invisibles para Lector y Servicio RAG hasta su consolidacion.
- Token de servicio revocado o vencido: las consultas RAG devuelven 401. Kanam Writer debe degradar a escritura sin Story Bible, no bloquear la sesion de escritura.
- Token con alcance por proyecto: un token emitido para el proyecto A devuelve 403 al consultar el proyecto B.
- Cambio de rol con sesion activa: el nuevo rol aplica en la siguiente peticion. Si el cambio es a Lector, o si el usuario se desactiva, se invalidan sus sesiones activas.
- Eliminacion de usuario con contenido: las fichas y ediciones se conservan. El autor pasa a `usuario eliminado` y el historial de versiones se mantiene.
- Eliminacion de ficha referenciada: si un personaje, lugar o elemento esta referenciado en el outline o en relaciones, se exige confirmacion explicita y se listan las referencias que quedarian rotas.
- Edicion concurrente: bloqueo optimista por numero de version. El segundo guardado recibe 409 y debe recargar la ficha antes de reintentar.
- Exportacion con alcance: la exportacion incluye solo los recursos visibles para el rol. Lector y Servicio RAG no tienen la accion habilitada.
- Recuperacion de contrasena: sin servidor de correo, el reset se ejecuta por CLI en el host. Supuesto a validar: comando y requisito de acceso local al servidor.
- Degradacion de Administrador a Autor: pierde de inmediato el acceso a configuracion, usuarios y auditoria, y no puede revertir el cambio por si mismo.

## Flujo 1: Creacion del Story Bible y generacion de la fuente base

1. El usuario crea un Story Bible nuevo. Sistema: registro en estado `draft`, sin fuente base y sin indice.
2. Carga el braindump como texto libre. Sistema: persiste `braindump.v1`, estado `braindump_ok`.
3. Define `genre` y `style`, por seleccion de taxonomia local o texto libre. Supuesto a validar: existe una taxonomia cerrada de generos y estilos.
4. Solicita la generacion de `synopsis`. Sistema: encola el job asincronico `generate_synopsis` con contexto = braindump + genre + style.
5. El worker arma el prompt, invoca el LLM local (modelo configurable) y espera salida estructurada.
6. Sistema: valida la salida contra el esquema de synopsis (campos obligatorios, longitud) y la guarda como propuesta en `pending_review`.
7. El usuario acepta, edita o descarta la propuesta.
8. Al aceptar: persiste `synopsis.v1`, la fuente base queda completa (`base_ready`) y se dispara la indexacion.
9. Indexacion: chunking de braindump + genre + style + synopsis, generacion de embeddings y escritura en el indice vectorial local. Estado final: `indexed`, `index_version = 1`.

### Errores y recuperacion

- **LLM local no disponible o timeout.** El job pasa a `failed` con causa registrada. Estado final: `braindump_ok`, fuente base incompleta, proyecto no indexado. Reintento manual desde la UI; el braindump no se pierde.
- **Salida no parseable o fuera de esquema.** Hasta 2 reintentos con el error de validacion inyectado en el prompt (supuesto a validar). Si persiste, el job queda `failed` y se ofrece edicion manual. Estado final: `pending_review` con propuesta vacia editable.
- **Contexto insuficiente** (braindump por debajo del minimo de tokens). El sistema no invoca al LLM y devuelve `insufficient_context`. Estado final: `braindump_ok`, sin propuesta.
- **El usuario descarta la propuesta.** Estado final: `base_ready` sin synopsis; el proyecto puede indexarse con advertencia de cobertura parcial.
- **Falla la indexacion** (embeddings o escritura en el indice). Estado final: `base_ready` + `index_stale`; se reintenta sin regenerar contenido.

## Flujo 2: Alta de ficha (personaje, lugar, lore, objeto, faccion, evento)

1. El usuario elige el tipo de ficha y el modo: manual, generar con IA, o generar desde cero.
2. Modo manual: formulario vacio con el esquema del tipo. Salta al paso 6.
3. Modo generar con IA: el sistema arma el prompt con fuente base + fichas existentes del mismo tipo + fichas vinculadas + instruccion del usuario.
4. Modo generar desde cero: mismo prompt sin instruccion del usuario; el LLM decide el elemento a partir de los huecos detectados (ver Flujo 3).
5. El LLM devuelve la ficha como JSON contra el esquema del tipo. Sistema: valida esquema, campos obligatorios y coherencia con el lore existente.
6. Deteccion de duplicados: similitud semantica contra fichas del mismo tipo. Umbral 0.85 (supuesto a validar).
7. La ficha queda en `pending_review`. El usuario acepta, edita o descarta.
8. Al aceptar: persiste la ficha, crea los vinculos declarados (relacion, pertenencia, ubicacion) y encola reindexacion incremental.
9. Estado final: ficha `active`, `index_version` incrementada, vinculos bidireccionales creados.

### Errores y recuperacion

- **Esquema invalido.** Un reintento con el error de validacion en el prompt. Si falla, la ficha queda `draft` con los campos que si validaron. Estado final: ficha `draft`, no indexada.
- **Duplicado detectado.** El sistema no crea la ficha; muestra la existente y ofrece fusionar o editar. Estado final: sin cambios en el indice.
- **Contradiccion con el lore existente** (por ejemplo, personaje ya marcado como muerto). Se marca `conflict` con referencia a la ficha en conflicto. Estado final: ficha `pending_review` con bandera de conflicto; decide el usuario.
- **Vinculo a ficha inexistente.** El vinculo se guarda como `unresolved` y la ficha se persiste igual. Estado final: ficha `active` con vinculos pendientes listados en el panel de salud del mundo.
- **LLM no disponible.** Estado final: ficha `draft` vacia, editable manualmente.
- **Falla la reindexacion incremental.** Estado final: ficha `active`, `index_stale = true`; el RAG sigue sirviendo la version anterior de esa ficha hasta el reintento.

## Flujo 3: Deteccion de elementos faltantes

1. Disparador: manual desde la UI, o automatico al superar N fichas (supuesto a validar: N = 10) o al cerrar el outline.
2. Sistema: calcula la matriz de cobertura por tipo de ficha y por acto, region o arco.
3. Encola el job `gap_analysis` con la matriz y un resumen de la fuente base.
4. El LLM devuelve hasta K propuestas (supuesto a validar: K = 5), cada una con tipo, nombre tentativo, justificacion y ubicacion sugerida.
5. Sistema: filtra propuestas con similitud mayor al umbral contra fichas existentes y contra propuestas ya descartadas.
6. El usuario acepta una propuesta: se abre el Flujo 2 en modo generar con IA, con la propuesta como instruccion.
7. El usuario descarta: se registra el hash de la propuesta en la lista de descartes para no repetirla.
8. Estado final: propuestas en `pending_review`; las aceptadas pasan a fichas `active`.

### Errores y recuperacion

- **Sin fuente base.** El sistema rechaza el job con `base_missing`. Estado final: sin propuestas; se sugiere completar el Flujo 1.
- **Todas las propuestas son duplicados.** Estado final: lista vacia con motivo `no_gaps_found`; nada se registra como descartado.
- **Propuesta aceptada que genera contradiccion.** Se resuelve en el Flujo 2, paso 6. Estado final: ficha `pending_review` con bandera de conflicto.
- **LLM no disponible.** Estado final: job `failed`, matriz de cobertura calculada y visible igual.

## Flujo 4: Consumo RAG desde Kanam Writer

1. Kanam Writer envia una consulta: texto de escena o pregunta, mas filtros opcionales (tipos de ficha, arco, personajes presentes).
2. La API local valida el contrato y la version de esquema del consumidor.
3. Genera el embedding de la consulta con el mismo modelo usado en la indexacion.
4. Busqueda vectorial sobre el indice local con los filtros aplicados; recupera top-M candidatos (supuesto a validar: M = 20).
5. Re-ranking y armado del contexto bajo un presupuesto de tokens (supuesto a validar: 8k).
6. Devuelve el contexto con citas: id de ficha, version y fragmento.
7. Registra la consulta y los ids servidos, para trazabilidad y para detectar fichas nunca usadas.
8. Estado final: respuesta entregada, sin mutacion del Story Bible.

### Errores y recuperacion

- **Indice desactualizado** (`index_stale`). Responde con la version disponible y agrega `stale: true`. Estado final: sin cambios; se encola reindexacion.
- **Sin resultados.** Devuelve contexto vacio con `no_match` en vez de inventar contenido. Estado final: sin cambios.
- **Presupuesto de tokens excedido.** Trunca por prioridad (fuente base > fichas vinculadas a los personajes presentes > resto) y marca `truncated: true`. Estado final: sin cambios.
- **Version de esquema incompatible.** Rechaza con `schema_mismatch` y la version esperada. Estado final: sin cambios; requiere migracion.
- **Embeddings no disponibles** (modelo caido). Rechaza con `embedding_unavailable`. Estado final: sin cambios; v1 no tiene fallback a busqueda por texto (supuesto a validar).

## Flujo 5: Edicion, versionado y reindexacion

1. El usuario edita una ficha o un campo de la fuente base.
2. Sistema: calcula el impacto, es decir las fichas que referencian a la editada y los campos derivados.
3. Persiste la nueva version (conserva la anterior) y marca las dependientes como `review_suggested`.
4. Encola reindexacion incremental solo de los chunks afectados.
5. Al terminar, incrementa `index_version` y notifica a los consumidores suscritos.
6. Estado final: ficha en version n+1, indice consistente, dependientes marcadas.

### Errores y recuperacion

- **Conflicto de edicion concurrente.** Gana la primera escritura; la segunda recibe `version_conflict` con el diff. Estado final: version n+1 persistida, la otra edicion queda en `draft` local del usuario.
- **Reindexacion parcial.** Los chunks no actualizados quedan marcados y `index_version` no se incrementa hasta completar. Estado final: `index_stale` con la lista de chunks pendientes.
- **Edicion que rompe un vinculo** (ficha referenciada borrada). El vinculo pasa a `unresolved`. Estado final: ficha activa, vinculo listado en salud del mundo.
- **Falla de embeddings durante la reindexacion.** Reintento con backoff; tras el limite, `index_stale`. Estado final: contenido nuevo persistido, indice sirviendo la version previa.

## Modelo de datos

Supuestos de plataforma a validar: motor PostgreSQL 16 o superior con extensiones `pgvector` (busqueda vectorial) y `pg_trgm` (busqueda difusa); despliegue de un solo usuario sin tabla de cuentas; claves primarias UUIDv7 generadas en la aplicacion para preservar orden temporal sin depender de secuencias. Si el destino es SQLite embebido, `jsonb`, `vector` y `tsvector` se reemplazan por `TEXT` con JSON1, `sqlite-vec` y FTS5 respectivamente, y los indices GIN/HNSW por indices virtuales equivalentes.

## Entidades

### Entidad: story_bible

Raiz del agregado. Una fila por mundo literario. Todo el resto de las entidades cuelga de aca.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | uuid | no | PK. UUIDv7. |
| titulo | text | no | Nombre del mundo o proyecto. |
| idioma | char(5) | no | BCP-47 del contenido. Default `es`. Define el stemmer de busqueda full-text. |
| schema_version | smallint | no | Version del modelo de datos. Default 1. Habilita migraciones in-place. |
| notas | text | si | Campo libre del autor, fuera del alcance del RAG. |
| created_at | timestamptz | no | |
| updated_at | timestamptz | no | Se actualiza ante cualquier cambio en entidades hijas. |
| deleted_at | timestamptz | si | Soft delete. |

### Entidad: foundation_block

Contenido base que alimenta todo el conocimiento derivado: braindump, genero, estilo y sinopsis. Un bloque por tipo y por mundo.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | uuid | no | PK. UUIDv7. |
| bible_id | uuid | no | FK a `story_bible(id)`. |
| tipo | foundation_kind | no | Enum: `braindump`, `genre`, `style`, `synopsis`. |
| contenido | text | no | Markdown. |
| tokens | int | no | Conteo aproximado del tokenizador del modelo activo. Default 0. |
| orden | smallint | no | Orden de presentacion en la UI. Default 0. |
| updated_at | timestamptz | no | |
| deleted_at | timestamptz | si | Soft delete. |

Restriccion: `UNIQUE (bible_id, tipo)`. Un unico braindump por mundo. Si se requiere historial de braindump, se resuelve con `audit_log`, no con filas adicionales.

### Entidad: card_type_schema

Registro de tipos de ficha. Los tipos base (`character`, `place`, `lore`, `item`, `faction`, `event`) se insertan como `es_sistema = true`; el usuario puede agregar tipos propios sin migracion de esquema.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | text | no | PK. Slug del tipo, ej. `character`. |
| nombre | text | no | Etiqueta visible. |
| campos | jsonb | no | JSON Schema de los atributos validos para el tipo. |
| es_sistema | boolean | no | Default false. Los de sistema no se pueden borrar. |
| created_at | timestamptz | no | |

### Entidad: card

Ficha unica y polimorfica para personajes, lugares, lore, objetos, facciones y eventos. El tipo determina la validacion de `atributos` contra `card_type_schema.campos`.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | uuid | no | PK. UUIDv7. |
| bible_id | uuid | no | FK a `story_bible(id)`. |
| tipo | text | no | FK a `card_type_schema(id)`. |
| nombre | text | no | Nombre canonico. |
| slug | text | no | Nombre normalizado (minusculas, sin acentos, guion comun). Clave de negocio dentro del mundo. |
| alias | text[] | si | Variantes y apodos. Se indexan para resolucion de menciones. |
| resumen | text | si | Una o dos frases. Es el texto de mayor peso en la recuperacion RAG. |
| descripcion | text | si | Markdown completo. |
| atributos | jsonb | no | Default `{}`. Validado contra el schema del tipo. |
| etiquetas | text[] | si | Filtros de recuperacion. |
| estado | card_status | no | Enum: `canon`, `borrador`, `descartado`. Solo `canon` entra al contexto RAG por defecto. |
| origen | card_origin | no | Enum: `manual`, `ia`, `importado`. |
| generacion_id | uuid | si | FK a `generation_job(id)`. Trazabilidad cuando `origen = ia`. |
| confianza | numeric(3,2) | si | Rango 0.00 a 1.00. Solo para `origen = ia`. |
| bloqueado | boolean | no | Default false. Si es true, la IA no puede sobrescribir la ficha. |
| created_at | timestamptz | no | |
| updated_at | timestamptz | no | |
| deleted_at | timestamptz | si | Soft delete. |

### Entidad: card_relation

Aristas del grafo del mundo. Dirigidas por defecto; `simetrica` indica que la relacion se lee en ambos sentidos.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | uuid | no | PK. UUIDv7. |
| bible_id | uuid | no | FK a `story_bible(id)`. Denormalizado para filtrar sin join. |
| origen_id | uuid | no | FK a `card(id)`. |
| destino_id | uuid | no | FK a `card(id)`. |
| tipo | text | no | Ej. `padre_de`, `aliado_de`, `ubicado_en`, `miembro_de`. |
| simetrica | boolean | no | Default false. |
| notas | text | si | Contexto narrativo de la relacion. |
| created_at | timestamptz | no | |

Restricciones: `CHECK (origen_id <> destino_id)` y `UNIQUE (origen_id, destino_id, tipo)`.

### Entidad: outline_node

Estructura jerarquica del outline. Auto-referenciada para permitir actos, capitulos, escenas y beats con la misma tabla.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | uuid | no | PK. UUIDv7. |
| bible_id | uuid | no | FK a `story_bible(id)`. |
| padre_id | uuid | si | FK a `outline_node(id)`. Nulo en la raiz. |
| nivel | outline_level | no | Enum: `acto`, `capitulo`, `escena`, `beat`. |
| orden | numeric(10,4) | no | Orden fraccional. Permite reordenar insertando entre dos valores sin reescribir hermanos. |
| titulo | text | no | |
| resumen | text | si | |
| contenido | text | si | Markdown. |
| estado | outline_status | no | Enum: `idea`, `esbozado`, `aprobado`. |
| created_at | timestamptz | no | |
| updated_at | timestamptz | no | |
| deleted_at | timestamptz | si | Soft delete. |

### Entidad: chunk

Unidad de recuperacion RAG. Se regenera por trigger de aplicacion cuando cambia el texto de la fila origen. `fuente_id` es referencia polimorfica sin FK fisica, porque apunta a tres tablas distintas.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | uuid | no | PK. UUIDv7. |
| bible_id | uuid | no | FK a `story_bible(id)`. |
| fuente_tipo | chunk_source | no | Enum: `foundation_block`, `card`, `outline_node`. |
| fuente_id | uuid | no | Id de la fila origen. |
| campo | text | no | Campo de origen: `resumen`, `descripcion`, `contenido`. |
| orden | smallint | no | Posicion dentro de la fuente cuando el texto se parte en varios chunks. |
| texto | text | no | Fragmento indexable. |
| texto_tsv | tsvector | no | Columna generada: `to_tsvector(idioma, texto)`. |
| tokens | int | no | |
| hash | bytea | no | SHA-256 del texto. Evita re-embedding si el contenido no cambio. |
| embedding | vector(1024) | si | Nulo hasta que se calcule. Dimension segun modelo de embeddings. |
| modelo_embedding | text | si | Identificador del modelo que genero el vector. |
| created_at | timestamptz | no | |

### Entidad: generation_job

Registro de cada invocacion a IA: generacion de fichas, deteccion de elementos faltantes, sugerencias de mundo. Permite auditar, reproducir y descartar resultados.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | uuid | no | PK. UUIDv7. |
| bible_id | uuid | no | FK a `story_bible(id)`. |
| operacion | text | no | Ej. `generar_personaje`, `generar_lugar`, `sugerir_faltantes`, `expandir_lore`. |
| modelo | text | no | Identificador del modelo local. |
| parametros | jsonb | no | Temperatura, top_p, max_tokens y demas. |
| prompt | text | no | Prompt efectivo enviado. |
| contexto_refs | jsonb | no | Ids de chunks y cards inyectados como contexto. |
| resultado | jsonb | si | Salida cruda del modelo. |
| estado | job_status | no | Enum: `pendiente`, `corriendo`, `completado`, `fallido`, `descartado`. |
| aceptado | boolean | si | Nulo mientras el usuario no decide. |
| error | text | si | |
| duracion_ms | int | si | |
| created_at | timestamptz | no | |

### Entidad: audit_log

Bitacora append-only. No se actualiza ni se borra por operacion normal.

| Campo | Tipo | Nulo | Descripcion |
|---|---|---|---|
| id | bigserial | no | PK. |
| bible_id | uuid | si | FK a `story_bible(id)`. Nulo en eventos globales. |
| entidad | text | no | Nombre de la tabla afectada. |
| entidad_id | uuid | si | |
| accion | text | no | `crear`, `actualizar`, `borrar`, `restaurar`, `purgar`, `generar`. |
| actor | text | no | `usuario` o `ia`. |
| diff | jsonb | si | Campos modificados con valor anterior y nuevo. |
| created_at | timestamptz | no | |

## Relaciones

| Origen | Destino | Cardinalidad | FK | On delete |
|---|---|---|---|---|
| story_bible | foundation_block | 1:N | `foundation_block.bible_id` | CASCADE |
| story_bible | card | 1:N | `card.bible_id` | CASCADE |
| story_bible | card_relation | 1:N | `card_relation.bible_id` | CASCADE |
| story_bible | outline_node | 1:N | `outline_node.bible_id` | CASCADE |
| story_bible | chunk | 1:N | `chunk.bible_id` | CASCADE |
| story_bible | generation_job | 1:N | `generation_job.bible_id` | CASCADE |
| card_type_schema | card | 1:N | `card.tipo` | RESTRICT |
| card | card_relation | 1:N | `card_relation.origen_id` | CASCADE |
| card | card_relation | 1:N | `card_relation.destino_id` | CASCADE |
| card | chunk | 1:N polimorfica | `chunk.fuente_id` con `fuente_tipo = 'card'` | Sin FK fisica. Purga por aplicacion. |
| outline_node | outline_node | 1:N | `outline_node.padre_id` | CASCADE |
| generation_job | card | 1:N | `card.generacion_id` | SET NULL |
| story_bible | audit_log | 1:N | `audit_log.bible_id` | SET NULL |

Regla de integridad para `chunk`: al borrar fisicamente una fila de `card`, `foundation_block` u `outline_node`, la aplicacion borra los chunks con `(fuente_tipo, fuente_id)` coincidentes dentro de la misma transaccion. No se delega a trigger de base para mantener el borrado explicito y auditable.

## Indices

| Tabla | Indice | Tipo | Motivo |
|---|---|---|---|
| story_bible | `(updated_at DESC) WHERE deleted_at IS NULL` | B-tree parcial | Listado de mundos recientes. |
| foundation_block | `UNIQUE (bible_id, tipo)` | B-tree unico | Un bloque por tipo. |
| card | `UNIQUE (bible_id, tipo, slug) WHERE deleted_at IS NULL` | B-tree unico parcial | Evita fichas duplicadas sin bloquear el slug de una ficha borrada. |
| card | `(bible_id, tipo, estado)` | B-tree | Filtro principal de la vista de fichas y del contexto RAG. |
| card | `(atributos jsonb_path_ops)` | GIN | Consultas por atributo del schema de tipo. |
| card | `(etiquetas)` | GIN | Filtro por etiqueta. |
| card | `(nombre gin_trgm_ops)` | GIN trigram | Busqueda difusa y resolucion de menciones. |
| card_relation | `UNIQUE (origen_id, destino_id, tipo)` | B-tree unico | Evita aristas duplicadas. |
| card_relation | `(destino_id)` | B-tree | Recorrido inverso del grafo. |
| card_relation | `(bible_id, tipo)` | B-tree | Subgrafo por tipo de relacion. |
| outline_node | `(bible_id, padre_id, orden)` | B-tree | Carga ordenada del arbol. |
| chunk | `(fuente_tipo, fuente_id)` | B-tree | Purga y regeneracion por fuente. |
| chunk | `UNIQUE (fuente_tipo, fuente_id, campo, hash)` | B-tree unico | Idempotencia del re-embedding. |
| chunk | `(embedding vector_cosine_ops)` | HNSW | Busqueda por similitud coseno. |
| chunk | `(texto_tsv)` | GIN | Busqueda full-text combinada con la vectorial. |
| chunk | `(bible_id) WHERE embedding IS NULL` | B-tree parcial | Cola de trabajo de embeddings pendientes. |
| generation_job | `(bible_id, created_at DESC)` | B-tree | Historial de generaciones. |
| generation_job | `(estado) WHERE estado IN ('pendiente','corriendo')` | B-tree parcial | Recuperacion de jobs interrumpidos al reiniciar. |
| audit_log | `(entidad, entidad_id, created_at DESC)` | B-tree | Historial por entidad. |

## Retencion y borrado

### Politica general

- El contenido del mundo no caduca. No hay TTL sobre `story_bible`, `foundation_block`, `card`, `card_relation` ni `outline_node`.
- Borrado en dos fases: soft delete con `deleted_at`, luego purga fisica. Las consultas de la aplicacion filtran siempre `deleted_at IS NULL`.
- Ventana de recuperacion: 30 dias desde `deleted_at`. Supuesto a validar con el usuario; configurable por mundo.
- La purga corre como tarea programada diaria en el proceso local. No requiere scheduler externo.

### Cascada de purga

| Paso | Accion |
|---|---|
| 1 | Marcar `deleted_at` en la entidad raiz. Las entidades hijas no se marcan: quedan ocultas por el filtro del padre. |
| 2 | Excluir del contexto RAG todo chunk cuyo `bible_id` o fuente tenga `deleted_at` no nulo. |
| 3 | A los 30 dias, borrar fisicamente la fila raiz. El `ON DELETE CASCADE` elimina hijas. |
| 4 | Borrar los chunks asociados por `(fuente_tipo, fuente_id)` en la misma transaccion. |
| 5 | Registrar la purga en `audit_log` con `accion = 'purgar'`. |

### Casos particulares

- `generation_job`: se conserva 12 meses por defecto. Supuesto a validar. Los jobs `descartado` y `fallido` se purgan a los 90 dias. El `prompt` y el `resultado` se truncan a 64 KB en la purga para acotar el crecimiento del archivo local.
- `audit_log`: retencion de 12 meses. Supuesto a validar. Es la unica tabla que crece de forma monotona; se recomienda particionado mensual por `created_at` si supera los 5 millones de filas.
- `chunk.embedding`: se borra junto con el chunk. Al cambiar `modelo_embedding` activo, los vectores del modelo anterior se marcan como obsoletos y se recalculan en background; no se borran hasta que exista reemplazo.
- `card_type_schema`: los tipos de sistema no se borran. Un tipo de usuario con fichas asociadas no se puede borrar (`ON DELETE RESTRICT`); primero se reasignan o se borran las fichas.

### Exportacion y respaldo

- Export completo del mundo en JSON con `schema_version`, sin `chunk` ni `embedding` (se regeneran). Incluye `foundation_block`, `card`, `card_relation` y `outline_node`.
- El respaldo es responsabilidad del operador del despliegue local. La aplicacion no gestiona copias automaticas.
- Un mundo exportado e importado en otra instancia conserva los UUID, por lo que las referencias cruzadas entre fichas siguen siendo validas.

## Convenciones

**Base URL:** `http://127.0.0.1:8080/api/v1` (supuesto a validar: puerto y bind configurables por `KANAM_HOST` / `KANAM_PORT`).

| Aspecto | Regla |
|---|---|
| Transporte | HTTP/1.1 y HTTP/2 sobre loopback o LAN |
| Content-Type | `application/json; charset=utf-8` en request y response |
| Nombres de campo | `snake_case` |
| Fechas | ISO 8601 en UTC con sufijo `Z` (`2025-03-14T18:22:07Z`) |
| IDs | UUID v7, opacos para el cliente |
| Envelope de recurso | Todo recurso expone `id`, `created_at`, `updated_at`, `version` |
| Concurrencia | Optimista vía `If-Match: <version>` en `PATCH`/`PUT`/`DELETE`; desajuste devuelve `412` |
| Paginación | Por cursor: `?limit=<1..200>&cursor=<opaco>`; la respuesta incluye `next_cursor` (null si no hay más) |
| Filtros | Query params repetibles (`?type=character&type=lore`) |
| Errores | `application/problem+json` (RFC 9457) |
| Idempotencia | `Idempotency-Key` obligatorio en `POST` de generación; repetir la clave devuelve la misma respuesta |
| Operaciones largas | `202 Accepted` + recurso `job` consultable |
| Caché | `Cache-Control: no-store` en generación y retrieval |
| Tamaño máximo de body | 2 MB (supuesto a validar) |

### Formato de error

```json
{
  "type": "https://kanam.local/errors/validation",
  "title": "Validation failed",
  "status": 422,
  "detail": "field 'name' is required",
  "instance": "/api/v1/projects/0192f3a1-.../entities",
  "errors": [
    { "field": "name", "code": "required" }
  ]
}
```

### Modelo de ficha (entidad)

Toda ficha del mundo es una `entity` con un `type` que determina los atributos válidos. Esto unifica personajes, lugares y lore bajo un mismo contrato y permite que el retrieval RAG opere sobre una sola colección.

| `type` | Atributos propios (además de `name`, `aliases`, `summary`, `body`, `tags`) |
|---|---|
| `character` | `role`, `goal`, `conflict`, `arc`, `traits[]`, `voice` |
| `place` | `region`, `climate`, `inhabitants[]`, `significance` |
| `lore` | `category`, `rules[]`, `scope` |
| `faction` | `ideology`, `members[]`, `territory` |
| `item` | `origin`, `properties[]`, `owner_id` |
| `event` | `date_in_world`, `participants[]`, `outcome` |
| `creature` | `habitat`, `abilities[]`, `threat_level` |
| `concept` | `definition`, `domain` |

Campos comunes: `id`, `project_id`, `type`, `name`, `aliases[]`, `summary`, `body` (markdown), `attributes` (objeto libre validado contra el tipo), `tags[]`, `status` (`draft` \| `canon` \| `deprecated`), `source` (`manual` \| `ai_generated` \| `imported`), `version`, `created_at`, `updated_at`.

### Autenticación

Tres modos, seleccionables por configuración (`KANAM_AUTH_MODE`):

| Modo | Comportamiento | Uso |
|---|---|---|
| `none` | Sin credenciales. El servidor rechaza conexiones fuera de loopback | Instalación local de un solo usuario (default) |
| `token` | `Authorization: Bearer <token>` obligatorio en todo endpoint salvo `/health` | Kanam Writer u otros clientes en la misma máquina o LAN |
| `token+tls` | Igual que `token` con TLS terminado en el propio servicio | Exposición fuera de la máquina |

Reglas:

- Los tokens se emiten con `POST /tokens` (scope `bible:admin`) y se almacenan hasheados (Argon2id). El valor plano se muestra una sola vez.
- Cada token lleva scopes; la ausencia del scope requerido devuelve `403`, la ausencia de credencial devuelve `401`.
- Scopes: `bible:read`, `bible:write`, `bible:generate`, `bible:retrieve`, `bible:admin`.
- Kanam Writer se conecta con un token de servicio de solo lectura + retrieval: `bible:read`, `bible:retrieve`.
- Los tokens de servicio no pueden leer `braindump` si el proyecto lo marca como privado (`foundation.braindump_private = true`); en ese caso el campo se omite de la respuesta.
- Revocación inmediata: `DELETE /tokens/{token_id}`; no hay tokens de larga vida sin revocación.

## Endpoints

### POST /projects

Crea un Story Bible vacío.

**Request**

```json
{
  "title": "Los nombres del río",
  "language": "es",
  "schema_version": "1.0"
}
```

**Response 201**

```json
{
  "id": "0192f3a1-7c4e-7b21-9f30-2a1b3c4d5e6f",
  "title": "Los nombres del río",
  "language": "es",
  "schema_version": "1.0",
  "foundation": {
    "braindump": "",
    "genres": [],
    "styles": [],
    "synopsis": "",
    "tone": null,
    "pov": null,
    "audience": null,
    "braindump_private": false,
    "updated_at": "2025-03-14T18:22:07Z"
  },
  "counts": { "entities": 0, "relations": 0, "outline_nodes": 0 },
  "version": 1,
  "created_at": "2025-03-14T18:22:07Z",
  "updated_at": "2025-03-14T18:22:07Z"
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 400 | JSON malformado |
| 401 | Falta credencial en modo `token` |
| 403 | Token sin scope `bible:write` |
| 422 | `title` vacío o `schema_version` no soportada |
| 429 | Límite de proyectos alcanzado (supuesto a validar) |

### GET /projects/{project_id}

**Request**

```json
{}
```

**Response 200**

```json
{
  "id": "0192f3a1-7c4e-7b21-9f30-2a1b3c4d5e6f",
  "title": "Los nombres del río",
  "language": "es",
  "schema_version": "1.0",
  "foundation": {
    "braindump": "Una ciudad portuaria que olvida los nombres...",
    "genres": ["fantasía", "misterio"],
    "styles": ["prosa seca", "primera persona"],
    "synopsis": "Iria investiga por qué su ciudad pierde los nombres.",
    "tone": "melancólico",
    "pov": "primera_persona",
    "audience": "adulto",
    "braindump_private": false,
    "updated_at": "2025-03-14T18:40:11Z"
  },
  "counts": { "entities": 42, "relations": 17, "outline_nodes": 28 },
  "version": 7,
  "created_at": "2025-03-14T18:22:07Z",
  "updated_at": "2025-03-14T18:40:11Z"
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:read` |
| 404 | Proyecto inexistente |

### PUT /projects/{project_id}/foundation

Reemplaza el bloque base (braindump, género, estilo, sinopsis). Es la fuente primaria de contexto para toda generación y para el retrieval.

**Request**

```json
{
  "braindump": "Una ciudad portuaria que olvida los nombres...",
  "genres": ["fantasía", "misterio"],
  "styles": ["prosa seca", "primera persona"],
  "synopsis": "Iria investiga por qué su ciudad pierde los nombres.",
  "tone": "melancólico",
  "pov": "primera_persona",
  "audience": "adulto",
  "braindump_private": false
}
```

**Response 200**

```json
{
  "project_id": "0192f3a1-7c4e-7b21-9f30-2a1b3c4d5e6f",
  "foundation": {
    "braindump": "Una ciudad portuaria que olvida los nombres...",
    "genres": ["fantasía", "misterio"],
    "styles": ["prosa seca", "primera persona"],
    "synopsis": "Iria investiga por qué su ciudad pierde los nombres.",
    "tone": "melancólico",
    "pov": "primera_persona",
    "audience": "adulto",
    "braindump_private": false,
    "updated_at": "2025-03-14T18:40:11Z"
  },
  "reindex_required": true,
  "version": 8
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:write` |
| 404 | Proyecto inexistente |
| 412 | `If-Match` no coincide con la `version` actual |
| 422 | `pov` o `audience` fuera del enum; `genres` con más de 5 elementos |

### GET /projects/{project_id}/entities

**Request**

```json
{}
```

Query params: `type`, `status`, `tag`, `q` (búsqueda textual), `limit`, `cursor`, `sort` (`name` \| `updated_at`).

**Response 200**

```json
{
  "items": [
    {
      "id": "0192f3a1-1111-7b21-9f30-000000000001",
      "type": "character",
      "name": "Iria Vasto",
      "aliases": ["la Sin Nombre"],
      "summary": "Cartógrafa que recuerda lo que la ciudad olvida.",
      "tags": ["protagonista"],
      "status": "canon",
      "source": "manual",
      "version": 3,
      "updated_at": "2025-03-14T18:35:00Z"
    }
  ],
  "next_cursor": "eyJvZmZzZXQiOjUwfQ",
  "total_estimate": 42
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 400 | `cursor` inválido o `limit` fuera de rango |
| 401 | Falta credencial |
| 403 | Token sin scope `bible:read` |
| 404 | Proyecto inexistente |

### POST /projects/{project_id}/entities

Crea una ficha desde cero.

**Request**

```json
{
  "type": "character",
  "name": "Iria Vasto",
  "aliases": ["la Sin Nombre"],
  "summary": "Cartógrafa que recuerda lo que la ciudad olvida.",
  "body": "## Motivación\nRecuperar el nombre de su hermano.",
  "attributes": {
    "role": "protagonista",
    "goal": "recuperar el nombre de su hermano",
    "conflict": "cada nombre que recuerda le cuesta un recuerdo propio",
    "arc": "de archivista a testigo",
    "traits": ["obstinada", "solitaria"],
    "voice": "frases cortas, sin adjetivos"
  },
  "tags": ["protagonista"],
  "status": "draft"
}
```

**Response 201**

```json
{
  "id": "0192f3a1-1111-7b21-9f30-000000000001",
  "project_id": "0192f3a1-7c4e-7b21-9f30-2a1b3c4d5e6f",
  "type": "character",
  "name": "Iria Vasto",
  "aliases": ["la Sin Nombre"],
  "summary": "Cartógrafa que recuerda lo que la ciudad olvida.",
  "body": "## Motivación\nRecuperar el nombre de su hermano.",
  "attributes": {
    "role": "protagonista",
    "goal": "recuperar el nombre de su hermano",
    "conflict": "cada nombre que recuerda le cuesta un recuerdo propio",
    "arc": "de archivista a testigo",
    "traits": ["obstinada", "solitaria"],
    "voice": "frases cortas, sin adjetivos"
  },
  "tags": ["protagonista"],
  "status": "draft",
  "source": "manual",
  "version": 1,
  "created_at": "2025-03-14T18:45:02Z",
  "updated_at": "2025-03-14T18:45:02Z"
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 400 | JSON malformado |
| 401 | Falta credencial |
| 403 | Token sin scope `bible:write` |
| 409 | Ya existe una entidad con el mismo `name` y `type` en el proyecto |
| 422 | `type` desconocido o atributo no permitido para ese `type` |

### PATCH /projects/{project_id}/entities/{entity_id}

**Request**

```json
{
  "status": "canon",
  "attributes": { "arc": "de archivista a mártir" }
}
```

**Response 200**

```json
{
  "id": "0192f3a1-1111-7b21-9f30-000000000001",
  "type": "character",
  "name": "Iria Vasto",
  "status": "canon",
  "attributes": {
    "role": "protagonista",
    "goal": "recuperar el nombre de su hermano",
    "conflict": "cada nombre que recuerda le cuesta un recuerdo propio",
    "arc": "de archivista a mártir",
    "traits": ["obstinada", "solitaria"],
    "voice": "frases cortas, sin adjetivos"
  },
  "version": 4,
  "updated_at": "2025-03-14T19:02:44Z"
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:write` |
| 404 | Entidad inexistente en el proyecto |
| 409 | `name` resultante colisiona con otra entidad del mismo `type` |
| 412 | `If-Match` no coincide con la `version` actual |
| 422 | Valor inválido para un atributo del `type` |

### DELETE /projects/{project_id}/entities/{entity_id}

Borra la ficha y sus relaciones. Las referencias desde el outline quedan huérfanas y se reportan en `GET /projects/{project_id}/gaps`.

**Request**

```json
{}
```

**Response 204**

```json
{}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:write` |
| 404 | Entidad inexistente |
| 409 | La entidad está referenciada por un nodo de outline con `locked = true` |
| 412 | `If-Match` no coincide |

### POST /projects/{project_id}/relations

**Request**

```json
{
  "from_entity_id": "0192f3a1-1111-7b21-9f30-000000000001",
  "to_entity_id": "0192f3a1-2222-7b21-9f30-000000000002",
  "kind": "enemigo_de",
  "notes": "Se conocen desde el incendio del archivo.",
  "bidirectional": true
}
```

**Response 201**

```json
{
  "id": "0192f3a1-3333-7b21-9f30-000000000003",
  "from_entity_id": "0192f3a1-1111-7b21-9f30-000000000001",
  "to_entity_id": "0192f3a1-2222-7b21-9f30-000000000002",
  "kind": "enemigo_de",
  "notes": "Se conocen desde el incendio del archivo.",
  "bidirectional": true,
  "version": 1,
  "created_at": "2025-03-14T19:10:00Z"
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:write` |
| 404 | Alguna de las entidades no existe en el proyecto |
| 409 | Relación duplicada con el mismo `kind` y dirección |
| 422 | `kind` fuera del vocabulario controlado |

### PUT /projects/{project_id}/outline

Reemplaza el árbol de outline completo (actos, capítulos, beats, escenas).

**Request**

```json
{
  "nodes": [
    {
      "id": "0192f3a1-4444-7b21-9f30-000000000004",
      "parent_id": null,
      "kind": "act",
      "title": "Acto I",
      "summary": "La ciudad pierde el nombre de la protagonista.",
      "order": 1,
      "entity_refs": ["0192f3a1-1111-7b21-9f30-000000000001"],
      "locked": false
    }
  ]
}
```

**Response 200**

```json
{
  "project_id": "0192f3a1-7c4e-7b21-9f30-2a1b3c4d5e6f",
  "nodes": [
    {
      "id": "0192f3a1-4444-7b21-9f30-000000000004",
      "parent_id": null,
      "kind": "act",
      "title": "Acto I",
      "summary": "La ciudad pierde el nombre de la protagonista.",
      "order": 1,
      "entity_refs": ["0192f3a1-1111-7b21-9f30-000000000001"],
      "locked": false
    }
  ],
  "orphan_refs": [],
  "version": 5
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:write` |
| 404 | Proyecto inexistente |
| 409 | `parent_id` genera un ciclo |
| 412 | `If-Match` no coincide |
| 422 | `kind` inválido o `entity_refs` apunta a entidades inexistentes |

### POST /projects/{project_id}/generations

Lanza una generación asistida por IA. Es asíncrona: devuelve un `job`. Requiere `Idempotency-Key`.

**Request**

```json
{
  "kind": "entity",
  "entity_type": "character",
  "instruction": "un antagonista que se beneficie de que la ciudad olvide",
  "context": {
    "include_foundation": true,
    "entity_ids": ["0192f3a1-1111-7b21-9f30-000000000001"],
    "include_outline": true
  },
  "count": 3,
  "model": "local-default",
  "temperature": 0.8,
  "max_tokens": 1200
}
```

`kind` admitido: `entity`, `relation`, `outline_node`, `foundation_field`, `gap_analysis`.

**Response 202**

```json
{
  "id": "0192f3a1-5555-7b21-9f30-000000000005",
  "project_id": "0192f3a1-7c4e-7b21-9f30-2a1b3c4d5e6f",
  "kind": "entity",
  "status": "queued",
  "progress": 0.0,
  "generator_version": "kanam-gen/1.0.0+modelo-local-7b",
  "result": null,
  "error": null,
  "created_at": "2025-03-14T19:20:00Z",
  "finished_at": null
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 400 | Falta `Idempotency-Key` |
| 401 | Falta credencial |
| 403 | Token sin scope `bible:generate` |
| 409 | `Idempotency-Key` reutilizada con un body distinto |
| 422 | `kind` o `entity_type` inválidos; `count` fuera de `1..10` |
| 503 | Modelo local no cargado o sin memoria disponible |

### GET /generations/{job_id}

**Request**

```json
{}
```

**Response 200**

```json
{
  "id": "0192f3a1-5555-7b21-9f30-000000000005",
  "project_id": "0192f3a1-7c4e-7b21-9f30-2a1b3c4d5e6f",
  "kind": "entity",
  "status": "succeeded",
  "progress": 1.0,
  "generator_version": "kanam-gen/1.0.0+modelo-local-7b",
  "result": {
    "candidates": [
      {
        "candidate_id": "c1",
        "type": "character",
        "name": "El Cobrador de Nombres",
        "summary": "Funcionario que compra nombres olvidados y los revende.",
        "attributes": {
          "role": "antagonista",
          "goal": "monopolizar la memoria de la ciudad",
          "conflict": "necesita que la ciudad siga olvidando, pero él también olvida",
          "traits": ["cortés", "paciente"],
          "voice": "registro administrativo"
        },
        "rationale": "El outline no tiene aún una fuerza que se beneficie del olvido colectivo."
      }
    ]
  },
  "error": null,
  "created_at": "2025-03-14T19:20:00Z",
  "finished_at": "2025-03-14T19:20:41Z"
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:generate` |
| 404 | Job inexistente |

### POST /generations/{job_id}/apply

Persiste uno o más candidatos como fichas reales. Es el único punto donde una sugerencia de IA entra al canon.

**Request**

```json
{
  "candidates": [
    {
      "candidate_id": "c1",
      "status": "canon",
      "overrides": { "name": "Vasco el Cobrador" }
    }
  ]
}
```

**Response 201**

```json
{
  "created": [
    {
      "id": "0192f3a1-6666-7b21-9f30-000000000006",
      "type": "character",
      "name": "Vasco el Cobrador",
      "status": "canon",
      "source": "ai_generated",
      "version": 1
    }
  ],
  "reindex_required": true
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:write` |
| 404 | Job o `candidate_id` inexistente |
| 409 | El job ya fue aplicado (operación no repetible) |
| 422 | `overrides` viola el esquema del `type` |

### GET /projects/{project_id}/gaps

Devuelve los huecos detectados: tipos de entidad ausentes, referencias huérfanas, arcos sin conflicto. Alimenta la sugerencia de "qué falta".

**Request**

```json
{}
```

**Response 200**

```json
{
  "gaps": [
    {
      "id": "gap-001",
      "kind": "missing_entity",
      "entity_type": "faction",
      "rationale": "Hay dos bandos enfrentados pero ninguna organización que los agrupe.",
      "priority": "high",
      "related_entity_ids": ["0192f3a1-1111-7b21-9f30-000000000001"]
    },
    {
      "id": "gap-002",
      "kind": "orphan_reference",
      "entity_type": "place",
      "rationale": "El nodo 'Acto II' referencia una entidad borrada.",
      "priority": "medium",
      "related_entity_ids": []
    }
  ],
  "computed_at": "2025-03-14T19:25:00Z"
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:read` |
| 404 | Proyecto inexistente |

### POST /projects/{project_id}/retrieve

Interfaz RAG que consume Kanam Writer. Devuelve fragmentos del mundo con su origen, listos para inyectar en un prompt.

**Request**

```json
{
  "query": "quién traiciona a Iria y por qué",
  "top_k": 8,
  "filters": {
    "types": ["character", "lore", "event"],
    "status": ["canon"]
  },
  "max_tokens": 2000
}
```

**Response 200**

```json
{
  "chunks": [
    {
      "entity_id": "0192f3a1-6666-7b21-9f30-000000000006",
      "entity_type": "character",
      "title": "Vasco el Cobrador",
      "text": "Vasco compra nombres olvidados...",
      "score": 0.83,
      "source": "entity.body"
    }
  ],
  "index_version": "idx-2025-03-14T19-21-00Z",
  "truncated": false,
  "tokens_used": 1840
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:retrieve` |
| 404 | Proyecto inexistente |
| 409 | Índice desactualizado respecto de la última escritura (`reindex_required = true`) |
| 422 | `top_k` fuera de `1..50` o `max_tokens` fuera de `256..8000` |
| 503 | Índice vectorial no disponible |

### POST /projects/{project_id}/index/reindex

Reconstruye el índice de retrieval. Operación larga: devuelve `202` con un `job` de `kind = reindex`.

**Request**

```json
{
  "scope": "all",
  "entity_ids": []
}
```

**Response 202**

```json
{
  "id": "0192f3a1-7777-7b21-9f30-000000000007",
  "kind": "reindex",
  "status": "queued",
  "progress": 0.0,
  "created_at": "2025-03-14T19:30:00Z"
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:admin` |
| 404 | Proyecto inexistente |
| 409 | Ya hay un reindex en curso para el proyecto |
| 503 | Motor de embeddings no disponible |

### GET /projects/{project_id}/export

**Request**

```json
{}
```

Query params: `format` (`json` \| `markdown`), `include` (`foundation`, `entities`, `relations`, `outline`).

**Response 200**

```json
{
  "project_id": "0192f3a1-7c4e-7b21-9f30-2a1b3c4d5e6f",
  "format": "json",
  "schema_version": "1.0",
  "exported_at": "2025-03-14T19:35:00Z",
  "foundation": {},
  "entities": [],
  "relations": [],
  "outline": { "nodes": [] }
}
```

Con `format=markdown` la respuesta es `text/markdown; charset=utf-8` y el cuerpo es el documento plano.

**Errores**

| Codigo | Significado |
|---|---|
| 401 | Falta credencial |
| 403 | Token sin scope `bible:read` |
| 404 | Proyecto inexistente |
| 422 | `format` no soportado |

### GET /health

Sin autenticación. No expone datos del proyecto.

**Request**

```json
{}
```

**Response 200**

```json
{
  "status": "ok",
  "version": "1.0.0",
  "components": {
    "db": "ok",
    "index": "ok",
    "llm": "degraded"
  },
  "uptime_seconds": 8421
}
```

**Errores**

| Codigo | Significado |
|---|---|
| 503 | Al menos un componente en estado `down`; el cuerpo usa el mismo esquema con `status: "degraded"` |

## Versionado

### Versionado de la API

- El número de versión mayor vive en la ruta: `/api/v1`. No se usa header de versión.
- Cambios no rompientes no cambian la versión: nuevos endpoints, nuevos campos opcionales en response, nuevos valores de enum que el cliente deba tolerar, nuevos `kind` de job.
- Cambios rompientes exigen `/api/v2`: renombrar o quitar campos, cambiar tipos, volver obligatorio un campo opcional, cambiar el significado de un valor de enum.
- `v1` se mantiene soportada al menos dos releases menores posteriores a la publicación de `v2`.
- Un endpoint deprecado responde con `Deprecation: @1735689600` (RFC 9745) y `Sunset: Wed, 01 Jan 2026 00:00:00 GMT` (RFC 8594), y se documenta en el changelog.
- Los clientes deben ignorar campos desconocidos en las respuestas.

### Versionado del esquema de datos

- Cada proyecto declara `schema_version`. Al abrir un proyecto con una versión anterior, el servicio aplica migraciones automáticas y escribe un backup previo en `data/backups/` (supuesto a validar: ruta configurable).
- Las migraciones son unidireccionales. No hay downgrade automático.
- Si `schema_version` es mayor a la soportada por el binario, el proyecto se abre en modo solo lectura y todo `POST`/`PATCH`/`PUT` devuelve `409`.

### Versionado del índice y de la generación

- `POST /retrieve` devuelve `index_version`. Kanam Writer debe invalidar su caché de contexto cuando cambia.
- Cada `job` de generación registra `generator_version` (versión del pipeline + identificador del modelo). Dos jobs con la misma `generator_version`, mismo `instruction` y mismo contexto deben producir resultados comparables; un cambio de modelo o de plantilla de prompt incrementa esa cadena.
- Los candidatos generados no se persisten hasta `POST /generations/{job_id}/apply`, de modo que un cambio de versión del generador nunca altera el canon de forma implícita.

## Componentes

| Componente | Responsabilidad | Tecnologia |
|---|---|---|
| UI Web | Editar braindump, genero, estilo, sinopsis, outline; gestionar fichas de personajes, lugares y lore; disparar generacion asistida y revisar sugerencias antes de aceptarlas | React + TypeScript + Vite |
| API / BFF | Exponer el contrato HTTP, validar entrada, gestionar sesion local, emitir streaming de generacion | FastAPI + Pydantic |
| Nucleo Story Bible | Modelo de dominio de las fichas, reglas de consistencia, versionado de cambios, resolucion de referencias entre entidades | Python + SQLAlchemy 2.0 + Alembic |
| Orquestador de generacion | Armar el contexto RAG, componer prompts por tipo de ficha, invocar el LLM, parsear y validar la salida estructurada, proponer entidades faltantes | Python + plantillas Jinja + salida JSON schema |
| Indexador RAG | Trocear fichas, generar embeddings, mantener el indice vectorial sincronizado con la fuente de verdad | Python + pgvector |
| Almacen de verdad | Persistir fichas, relaciones, versiones y embeddings en una unica transaccion | PostgreSQL 16 + pgvector |
| Runtime de modelos | Servir el LLM y el modelo de embeddings en la maquina local, con gestion de VRAM y carga bajo demanda | Ollama |
| Cola de trabajos | Ejecutar generaciones e indexados fuera del ciclo de request, con reintentos y cancelacion | Redis + arq |
| Exportador RAG | Entregar contexto a Kanam Writer por consulta o por entidad, con presupuesto de tokens | FastAPI + endpoint MCP |
| Proxy y TLS | Terminar TLS, servir estaticos, enrutar a la API | Caddy |
| Observabilidad | Trazas de generacion, latencia por modelo, costo en tokens, errores de parseo | OpenTelemetry + Loki |

Supuestos a validar: despliegue mono usuario en una sola maquina; corpus de una story bible por debajo de 5.000 fichas; GPU con al menos 12 GB de VRAM para un modelo de 8B en cuantizacion Q4.

## Comunicacion entre componentes

**UI a API.** REST/JSON sobre HTTPS. Las operaciones de generacion usan Server-Sent Events para emitir tokens y el resultado parcial de la ficha; el resto de las llamadas son request/response. No hay estado de dominio en el cliente: la UI es una vista del backend.

**API a Nucleo.** Llamada en proceso. API, Nucleo, Orquestador e Indexador viven en el mismo servicio desplegable (monolito modular) y se comunican por interfaces internas, no por red. El limite es de modulo, no de proceso, para evitar serializacion y fallos parciales en una operacion que debe ser transaccional.

**Nucleo a Cola.** Patron outbox. Cada escritura de ficha persiste un evento `entity.created` / `entity.updated` / `entity.deleted` en la misma transaccion que el dato. Un worker lee el outbox y encola el trabajo de reindexado. Esto garantiza que el indice vectorial nunca quede por delante de la fuente de verdad y que un fallo del indexador sea reintentable sin perder el cambio.

**Orquestador a Runtime de modelos.** HTTP con contrato compatible OpenAI (`/v1/chat/completions`, `/v1/embeddings`). El orquestador no conoce el runtime concreto; cambiar Ollama por otro servidor local no toca el dominio.

**Orquestador a Indexador.** El orquestador pide contexto al Indexador antes de componer el prompt. La recuperacion combina busqueda vectorial sobre fichas y filtro por tipo de entidad y por relevancia declarada en el outline.

**Exportador a Kanam Writer.** Kanam Writer consume el endpoint `GET /v1/context` con una consulta y un presupuesto de tokens, o invoca la herramienta MCP equivalente. La respuesta incluye las fichas recuperadas con su identificador estable, para que las citas del texto generado apunten a la ficha de origen.

### Flujo de generacion asistida

1. La UI envia tipo de ficha, instruccion y entidades ancla opcionales.
2. La API valida y encola el trabajo; devuelve un identificador de job.
3. El worker recupera contexto del Indexador y lo recorta al presupuesto de tokens.
4. El Orquestador compone el prompt y llama al LLM con streaming.
5. La salida se parsea contra el esquema de la ficha. Si no valida, se reintenta una vez con el error como feedback.
6. El resultado se persiste como borrador, no como ficha activa.
7. La UI muestra el borrador y las entidades nuevas sugeridas; el usuario acepta, edita o descarta.
8. Al aceptar, el Nucleo escribe la ficha y emite el evento de reindexado.

La generacion nunca escribe directo sobre la fuente de verdad. El paso 7 es obligatorio y es lo que separa una sugerencia de un dato.

## Stack y justificacion

| Tecnologia | Rol | Por que se elige |
|---|---|---|
| PostgreSQL 16 + pgvector | Fuente de verdad y indice vectorial | Un solo motor cubre relacional y vectorial, permite escribir ficha y embedding en la misma transaccion, y evita sincronizar dos almacenes. Self-hosted sin dependencia de servicios gestionados. |
| SQLAlchemy 2.0 + Alembic | Acceso a datos y migraciones | Modelo de dominio tipado y migraciones versionadas, necesario porque el esquema de fichas va a cambiar con cada tipo de entidad nuevo. |
| FastAPI + Pydantic | API y validacion | Validacion declarativa reutilizable como esquema de salida del LLM, y soporte nativo de SSE para streaming. |
| React + TypeScript + Vite | UI | El editor de fichas tiene estado complejo (borradores, sugerencias, referencias cruzadas); el tipado compartido con los esquemas del backend evita divergencia de contratos. |
| Ollama | Runtime de LLM y embeddings | Corre local, gestiona carga y descarga de modelos en VRAM, y expone contrato compatible OpenAI, lo que desacopla el dominio del runtime. |
| Redis + arq | Cola de trabajos | Las generaciones duran mas que un request y deben sobrevivir a un reinicio del proceso. arq es asincronico y comparte el runtime de Python, sin sumar un lenguaje mas. |
| Caddy | Proxy y TLS | Certificados automaticos y configuracion minima para un despliegue de una sola maquina. |
| Docker Compose | Empaquetado y despliegue | Define el stack completo en un archivo reproducible, requisito de un producto auto alojado. |
| OpenTelemetry + Loki | Trazas y logs | Permite medir latencia por modelo y tasa de fallo de parseo, que son las dos metricas que gobiernan la calidad del RAG. |

Decisiones abiertas, a resolver antes de implementar:

- Motor de base de datos. PostgreSQL asume un despliegue con contenedor y recursos suficientes. Si el objetivo es una instalacion de escritorio sin servicios, SQLite con `sqlite-vec` cubre el mismo rol con menos piezas. La eleccion cambia el empaquetado, no el dominio.
- Modelo de embeddings. Depende del idioma de las historias y del presupuesto de VRAM. Candidatos a evaluar: `bge-m3` para multilingue, `nomic-embed-text` para menor consumo.
- Grafo de conocimiento. Las relaciones entre personajes, lugares y lore se modelan en v1 como tabla de aristas en PostgreSQL. Un motor de grafo dedicado solo se justifica si las consultas de traversal aparecen como cuello de botella medido.

## Deuda tecnica aceptada

| Deuda | Motivo de aceptarla | Condicion de pago |
|---|---|---|
| Sin multiusuario ni permisos | El producto es mono usuario local; agregar autenticacion y aislamiento ahora no valida ninguna hipotesis | Cuando exista un caso de uso colaborativo o despliegue compartido |
| Sin grafo dedicado | Las relaciones caben en tablas de aristas para el volumen supuesto | Cuando una consulta de traversal supere el presupuesto de latencia de la UI |
| Chunking por ficha, sin estrategia semantica | Las fichas ya son unidades coherentes; el chunking fino agrega complejidad sin ganancia medible al inicio | Cuando la recuperacion falle en fichas largas de worldbuilding |
| Sin versionado del indice vectorial | Reindexar es barato al volumen supuesto y el outbox garantiza consistencia eventual | Cuando el reindexado completo supere el minuto |
| Sin evaluacion automatica de calidad del RAG | Requiere un corpus de referencia que todavia no existe | Cuando haya story bibles reales de usuarios |
| Reintento unico ante salida invalida del LLM | Un segundo reintento rara vez corrige y duplica el costo en tokens | Si la tasa de fallo de parseo supera el umbral definido en operacion |
| Sin cache de embeddings | El volumen de fichas no lo justifica | Cuando el costo de reindexado por edicion sea perceptible |

## Autenticacion

Kanam Story Bible se despliega autoalojado. El modo por defecto es single-user local: el servicio escucha en `127.0.0.1` y no acepta conexiones externas.

### Modos de despliegue y requisito de autenticacion

| Modo | Binding | Autenticacion | Estado |
|---|---|---|---|
| Local single-user (default) | `127.0.0.1` | Sesion local; login opcional si el SO ya aisla la sesion | Soportado |
| LAN / self-host multiusuario | Interfaz explicita | Obligatoria, con TLS obligatorio | Soportado |
| Expuesto a Internet | - | - | No soportado: se bloquea por configuracion; requiere reverse proxy con TLS y rate limiting |

### Credenciales

- Hash de contrasena con Argon2id. Parametros de referencia: m=64 MiB, t=3, p=1 (supuesto a validar contra el hardware objetivo).
- Politica de contrasena: minimo 12 caracteres, sin rotacion forzada, bloqueo temporal tras 10 intentos fallidos en 15 minutos (supuesto a validar).
- Recuperacion de cuenta solo local, mediante token generado en la consola del servidor. No hay email saliente ni recuperacion remota.
- MFA TOTP opcional en modo local y obligatorio cuando el binding no es loopback.

### Sesiones y tokens

- Sesion de UI: cookie `HttpOnly`, `Secure` cuando hay TLS, `SameSite=Lax`, expiracion de 12 h con renovacion deslizante (supuesto a validar).
- Tokens de servicio para Kanam Writer y scripts: bearer token con hash almacenado, prefijo identificable, expiracion configurable y revocacion individual.
- Rotacion del secreto de firma de sesion al cambiar contrasena o revocar tokens.

## Autorizacion

### Roles

| Rol | Lectura de fichas | Escritura de fichas | Generacion IA | Gestion de miembros | Export / borrado |
|---|---|---|---|---|---|
| Owner | Si | Si | Si | Si | Si |
| Editor | Si | Si | Si | No | No |
| Reader | Si | No | No | No | No |
| Servicio (Kanam Writer) | Si | No por defecto | No | No | No |

### Reglas de control de acceso

- Toda entidad (proyecto, ficha de personaje, lugar, elemento de lore, outline) pertenece a un proyecto. La autorizacion se evalua siempre contra `project_id`, nunca contra el id de la ficha de forma aislada.
- El rol Servicio se emite con scope explicito `bible:read` por proyecto. La escritura desde Kanam Writer requiere el scope separado `bible:write` y esta deshabilitada por defecto.
- Deny by default: una ruta sin politica declarada devuelve 403.
- La verificacion ocurre en la capa de servicio, no solo en la UI.

### Aislamiento en la recuperacion RAG

- El indice vectorial se particiona por proyecto. Una consulta de Kanam Writer solo puede recuperar chunks del proyecto para el que su token tiene scope.
- El filtro por proyecto se aplica como pre-filtro en la busqueda, no como post-filtro sobre resultados.
- Las fichas marcadas como borrador o privadas quedan fuera del indice hasta su publicacion explicita.

## Datos sensibles

### Clasificacion

| Dato | Clase | Nunca sale del entorno | Notas |
|---|---|---|---|
| Braindump, genre, style, synopsis, outline | Confidencial | Si | Texto de autor; base de conocimiento del RAG |
| Fichas de personajes, lugares y lore | Confidencial | Si | Incluye campos generados por IA |
| Embeddings e indice vectorial | Confidencial | Si | Reconstruibles desde el texto, se tratan igual |
| Prompts y respuestas del modelo | Confidencial | Si, salvo proveedor externo con opt-in | Ver "Datos que nunca salen del entorno" |
| Credenciales de usuario y hashes | Secreto | Si | Nunca en logs ni en respuestas de API |
| API keys de proveedores LLM | Secreto | Si | Keyring del SO o variable de entorno |
| Logs y metadatos de uso | Interno | Si | Sin telemetria remota |

### Cifrado

- En transito: TLS obligatorio en cualquier binding distinto de loopback.
- En reposo: cifrado de volumen o filesystem recomendado; cifrado a nivel de columna para los campos de clase Secreto (supuesto a validar segun el motor de base de datos elegido).
- Backups cifrados con una clave distinta de la de la base.

### Manejo de secretos

- Las API keys de proveedores LLM no se persisten en la base ni se devuelven por API. Se leen del keyring del SO o de variables de entorno al iniciar.
- Los logs redactan por patron: claves, tokens, cookies y contenido de braindump.
- Los errores devueltos al cliente son genericos; el detalle queda solo en el log local.

### Retencion y borrado

- El borrado de un proyecto elimina fichas, chunks del indice y embeddings en la misma operacion. El borrado del indice no es diferido.
- El borrado de una cuenta elimina credenciales y revoca sus tokens de servicio.
- No hay retencion por defecto de prompts y respuestas mas alla de la sesion de generacion, salvo que el usuario guarde el resultado como ficha (supuesto a validar).

### Datos que nunca salen del entorno

- Texto de braindump, genre, style, synopsis y outline.
- Fichas de personajes, lugares y lore, en cualquier estado.
- Embeddings, consultas de recuperacion y resultados del RAG.
- Credenciales, tokens de sesion y API keys.
- Logs, metricas y telemetria: no se envia telemetria a ningun servicio.
- Unica excepcion: si el usuario configura un proveedor LLM externo, el prompt (que puede contener fragmentos de fichas recuperadas por RAG) se envia a ese proveedor. Requiere opt-in explicito por proyecto, aviso en la UI con la lista de campos enviados y registro de auditoria de cada llamada. Con modelo local (llama.cpp / Ollama) no hay salida de datos.

## Amenazas y mitigaciones

| Amenaza | Impacto | Mitigacion |
|---|---|---|
| Servicio accesible por red sin autenticacion | Alto | Binding a loopback por defecto; autenticacion obligatoria fuera de loopback; TLS; rate limiting |
| Fuga cruzada entre proyectos via RAG | Alto | Particion del indice por proyecto; pre-filtro por `project_id`; test de regresion que verifica que una consulta no devuelve chunks de otro proyecto |
| Prompt injection desde contenido ingerido o fichas | Alto | Todo contenido recuperado se trata como no confiable; el modelo no ejecuta escrituras; la ficha se persiste solo por accion explicita del usuario; delimitadores y etiquetado de procedencia en el prompt |
| Exfiltracion de secretos via logs o mensajes de error | Alto | Redaccion por patron; errores genericos al cliente; prohibicion de loguear cuerpos de request en rutas de autenticacion |
| Envio no intencional de contenido a un proveedor externo | Alto | Default a modelo local; opt-in explicito por proyecto; aviso con campos enviados; auditoria de llamadas externas |
| Robo de backup o del volumen de datos | Alto | Backup cifrado con clave separada; permisos de archivo restrictivos; API keys excluidas del backup |
| Inversion de embeddings para reconstruir texto | Medio | Embeddings tratados como confidenciales; acceso al indice con el mismo scope que el texto fuente |
| Escalada de privilegios entre usuarios del mismo host | Medio | Aislamiento por proceso o contenedor; el servidor no confia en el `project_id` enviado por el cliente; verificacion de rol en cada request |
| SSRF via ingesta de URLs de material de referencia | Medio | Allowlist de esquemas; bloqueo de rangos privados y endpoints de metadata; timeouts |
| DoS por import masivo o generacion concurrente | Medio | Limite de tamano de import; cola de generacion con concurrencia acotada; timeouts |
| Dependencia o modelo descargado de origen no verificado | Alto | Pin de versiones y hashes; descarga desde fuente declarada; verificacion de checksum antes de cargar |
| Borrado accidental de proyecto | Medio | Confirmacion explicita escribiendo el nombre del proyecto; soft-delete con ventana de recuperacion (supuesto a validar) |

## Niveles de prueba

| Nivel | Alcance | Herramienta | Cuando corre |
|---|---|---|---|
| Unitario | Funciones puras: validacion de esquemas de fichas, chunking, construccion de prompts, scoring de retrieval, parseo de salidas del modelo, migraciones de datos | Runner del stack (supuesto: pytest o Vitest, a validar) | Pre-commit y cada push |
| Integracion | Modulos contra DB local e indice vectorial reales, proveedor de IA sustituido por doble; API HTTP con cliente de prueba | Runner + cliente HTTP de test + DB temporal en disco | Cada PR |
| Contrato | Esquema del paquete que consume Kanam Writer (export RAG) y esquema de fichas | Validacion JSON Schema + tests de contrato versionados | Cada PR que toque el esquema |
| End-to-end | Flujo completo: UI, API, persistencia, indice, generacion con proveedor fake determinista | Playwright (supuesto, a validar) sobre instancia local | Nightly y pre-release |
| Evaluacion de IA (evals) | Calidad de generacion y de sugerencias sobre un golden set | Runner de evals + proveedor fake con respuestas grabadas | Nightly y ante cambio de prompt o modelo |
| Manual | Calidad literaria, coherencia narrativa, UX de generacion | Checklist humano | Pre-release |

### Dobles del proveedor de IA

- Modo replay: respuestas grabadas por caso, con semilla fija. Es el modo por defecto en unitario, integracion, contrato y e2e.
- Modo grabacion: corre contra el modelo local real y regenera fixtures. Se ejecuta a mano, nunca en el build.
- Modo caos: respuestas truncadas, JSON invalido, timeout y salida vacia, para verificar manejo de errores y reintentos.
- Ningun test del build depende de un modelo real ni de red saliente.

### Datos de prueba

- Mundo Semilla: proyecto versionado en el repo con fichas de personajes, lugares y lore, relaciones y cronologia. Base comun de integracion, e2e y evals. Tamano supuesto: 200 fichas (a validar).
- Segundo proyecto minimo para verificar aislamiento entre proyectos en retrieval y export.
- Fixtures de esquema: una ficha valida por tipo y una invalida por cada regla de validacion.

## Casos criticos

| ID | Caso | Nivel | Criterio de aceptacion |
|---|---|---|---|
| C-01 | Alta manual de ficha (personaje, lugar, lore) | Integracion + e2e | Se persiste con ID estable, campos obligatorios validados, sin duplicados por nombre o alias |
| C-02 | Generacion de ficha con IA desde contexto | Integracion | Salida valida contra el esquema; no se persiste hasta confirmacion del usuario; se registra origen (manual o generado) |
| C-03 | Sugerencia de elementos faltantes | Integracion + eval | No propone entidades ya existentes (dedupe por nombre, alias y similitud de embedding); incluye justificacion del aporte |
| C-04 | Consistencia del mundo | Integracion | Detecta contradicciones de atributos, relaciones y cronologia entre fichas del mismo proyecto |
| C-05 | Retrieval RAG | Integracion | Devuelve solo fichas del proyecto consultado, ordenadas por relevancia, sin fragmentos truncados |
| C-06 | Export para Kanam Writer | Contrato | El paquete valida contra el esquema versionado; un cambio incompatible rompe el build |
| C-07 | Determinismo con proveedor fake | Unitario | Misma entrada y semilla producen la misma salida byte a byte |
| C-08 | Migracion de DB | Integracion | Una base en version N-1 migra sin perdida ni duplicacion de fichas |
| C-09 | Operacion sin red | Integracion | Ninguna llamada saliente durante el uso normal; falla explicita si se intenta |
| C-10 | Mundo grande | Integracion | Con el Mundo Semilla, retrieval y generacion responden bajo el presupuesto de latencia (supuesto: p95 < 2 s en retrieval, a validar) |

## Criterio de calidad (definicion de verde)

Un build esta verde cuando se cumplen todas estas condiciones:

- Unitarios, integracion y contrato pasan al 100%.
- Cobertura de lineas en modulos criticos (persistencia, retrieval, validacion de esquemas, export) >= 80% (supuesto a validar). No hay umbral global.
- Evals: >= 90% de los casos del golden set cumplen su criterio y cero regresiones contra la linea base registrada (supuesto a validar).
- Cero tests flaky: un test intermitente se marca, se arregla o se elimina dentro de 48 h.
- El build corre sin red externa y sin modelo real, en menos de 10 min (supuesto a validar).
- El esquema de export es compatible hacia atras o sube version mayor con nota de migracion.

## Lo que no se automatiza

- Calidad literaria de la prosa: voz, estilo y ritmo se revisan a mano contra el genero y el estilo declarados en el proyecto.
- Coherencia narrativa de largo alcance: el arco completo se valida leyendo, no con asserts.
- Utilidad real de las sugerencias de IA: si un personaje o elemento "aporta" es juicio editorial.
- UX de la generacion: streaming, cancelacion y espera percibida se prueban a mano.
- Ajuste de prompts: se decide con evals mas revision humana; ningun assert fija el texto del prompt.
- Definicion de campos obligatorios y reglas de dominio del mundo.

## Entornos

Tres entornos sobre infraestructura auto alojada. No hay cloud: cada entorno es un host con Docker Engine y Docker Compose.

| Entorno | Proposito | Host | Base de datos | Modelos | Datos |
|---|---|---|---|---|---|
| `dev` | Desarrollo y pruebas unitarias | Notebook del desarrollador | Postgres + pgvector en contenedor | Modelo chico cuantizado (7B Q4) | Mundos sinteticos descartables |
| `staging` | Validacion de migraciones, prompts y pipeline RAG | Host dedicado o VM en la misma red | Postgres + pgvector | Mismos pesos que prod | Copia anonimizada de un mundo real |
| `prod` | Uso real del autor | Host unico (o 2 nodos: app + inferencia) | Postgres + pgvector con WAL archiving | Pesos fijos versionados | Mundos del autor, backup diario |

Convenciones:

- Puertos: `8080` API, `3000` UI, `9090` Prometheus, `3001` Grafana, `3100` Loki. Postgres (`5432`) y el servidor de inferencia (`8000`) no se exponen fuera de la red Docker.
- Configuracion por `.env` por entorno; nunca en la imagen. Variables minimas: `DATABASE_URL`, `MODEL_PATH`, `MODEL_VERSION`, `EMBEDDING_MODEL`, `IMAGE_TAG`, `SECRET_KEY`, `RAG_INDEX_PATH`.
- Pesos de modelos y snapshots del indice vectorial viven en volumenes (`/srv/kanam/models`, `/srv/kanam/index`), no dentro de la imagen. Se referencian por hash.
- `prod` es single node: cada despliegue implica una ventana de indisponibilidad de 20 a 40 s (supuesto a validar segun tiempo de carga de pesos en VRAM).

## Pipeline

Disparador: push a `main` (staging) y tag `v*` (prod). CI auto alojado (Gitea Actions o GitLab CE, supuesto a validar).

Etapas:

1. **Verificacion local** antes del push:
   ```bash
   make lint test          # ruff + mypy + pytest
   docker compose -f compose.dev.yml up -d
   ```
2. **Build y test en CI**: lint, tests unitarios, tests de contrato del RAG (retrieval sobre un mundo fixture), build de imagen.
3. **Publicacion**: imagen etiquetada con `sha-<short>` (inmutable) y `staging`. Nunca se reutiliza un tag.
   ```bash
   docker build -t registry.local/kanam/story-bible:sha-9f3c1a2 .
   docker push registry.local/kanam/story-bible:sha-9f3c1a2
   ```
4. **Deploy a staging** automatico al pasar los tests.
5. **Promocion a prod** manual, con tag semantico:
   ```bash
   git tag -a v0.4.0 -m "Story Bible 0.4.0"
   git push origin v0.4.0
   ```
6. **Migraciones** como job previo al arranque de la app, con lock para evitar ejecuciones concurrentes:
   ```bash
   docker compose run --rm api alembic upgrade head
   ```
7. **Reindexado RAG** solo si cambio el modelo de embeddings o el esquema de fichas:
   ```bash
   docker compose run --rm api python -m kanam.rag.reindex --world all --snapshot-before
   ```
8. **Arranque y smoke test**:
   ```bash
   export IMAGE_TAG=v0.4.0
   docker compose pull && docker compose up -d
   curl -fsS http://localhost:8080/healthz
   docker compose exec api python -m kanam.smoke --world demo --check rag,generation
   ```
9. **Cierre**: si el smoke test falla, el pipeline ejecuta el rollback automatico (seccion siguiente) y marca el tag como no desplegable.

Reglas:

- La app arranca solo si `alembic current` coincide con `head`; si no, el contenedor sale con codigo 1 y no sirve trafico.
- Los pesos de modelo se actualizan por separado del codigo: cambiar `MODEL_VERSION` en `.env` y reiniciar. No requiere rebuild de imagen.
- Un despliegue de codigo y uno de modelo no se ejecutan en la misma ventana.

## Observabilidad

Metricas expuestas en `/metrics` (formato Prometheus), recolectadas por Prometheus y visualizadas en Grafana. Logs en JSON a stdout, recolectados por Loki; si no hay Loki, `docker compose logs` con rotacion de 100 MB por servicio.

| Senal | Que mide | Umbral de alerta |
|---|---|---|
| `http_request_duration_seconds` p95 | Latencia de API sin inferencia | > 800 ms durante 5 min |
| `http_requests_total{status=~"5.."}` | Tasa de error 5xx | > 2% en 10 min |
| `llm_request_duration_seconds` p95 | Latencia de generacion completa | > 45 s en 10 min (supuesto a validar) |
| `llm_tokens_per_second` | Throughput de inferencia | < 8 tok/s en 10 min |
| `llm_queue_depth` | Trabajos de generacion en cola | > 20 en 5 min |
| `gpu_memory_used_bytes` | VRAM ocupada | > 92% del total en 5 min |
| `rag_retrieval_duration_seconds` p95 | Busqueda vectorial sobre el mundo | > 1.5 s en 10 min |
| `rag_index_lag_seconds` | Fichas modificadas sin reindexar | > 300 s |
| `postgres_connections` | Conexiones activas | > 80% de `max_connections` |
| `disk_free_bytes` | Espacio en volumenes de datos, modelos e indice | < 15% |
| `backup_last_success_timestamp` | Antiguedad del ultimo backup exitoso | > 26 h |
| `container_restarts_total` | Reinicios de contenedor | > 2 en 15 min |

Logs:

- Campos obligatorios: `ts`, `level`, `service`, `request_id`, `world_id`, `route`, `latency_ms`, `error`.
- Campos de inferencia: `model`, `model_version`, `tokens_in`, `tokens_out`, `retrieval_hits`.
- Prohibido loguear contenido de fichas, prompts completos o texto generado. Solo conteos y hashes. El mundo del autor es dato privado.
- Retencion: 14 dias en Loki, 7 dias en disco local (supuesto a validar).
- `request_id` se propaga desde la UI hasta la llamada al modelo para reconstruir una generacion completa.

Comandos de diagnostico:

```bash
docker compose logs -f --since 15m api
docker compose logs api | jq 'select(.level=="error") | {ts, route, error}'
docker compose logs api | jq 'select(.tokens_out != null) | .tokens_out' | awk '{s+=$1; n++} END {print s/n}'
curl -s localhost:9090/api/v1/query --data-urlencode 'query=histogram_quantile(0.95, rate(llm_request_duration_seconds_bucket[5m]))'
docker compose exec api python -m kanam.rag.stats --world <world_id>
```

## Rollback

Criterios de disparo (cualquiera alcanza):

- Tasa de error 5xx > 5% sostenida 10 min.
- Latencia p95 de generacion > 3x la linea base previa al despliegue.
- Corrupcion o perdida de fichas detectada en el smoke test o en reporte del autor.
- Migracion aplicada que no se puede revertir sin perdida de datos.

Procedimiento:

1. **Congelar escrituras** para evitar datos nuevos sobre un esquema en transicion:
   ```bash
   docker compose stop worker api
   ```
2. **Volver a la imagen anterior** (tag inmutable conocido):
   ```bash
   export IMAGE_TAG=v0.3.2
   docker compose pull && docker compose up -d
   ```
3. **Revertir migraciones** si la version nueva las aplico:
   ```bash
   docker compose exec api alembic current
   docker compose exec api alembic downgrade <revision_anterior>
   ```
   Si la migracion es destructiva (drop de columna o tabla), no usar `downgrade`: restaurar el dump previo (paso 4).
4. **Restaurar datos** solo si hubo corrupcion:
   ```bash
   docker compose stop postgres
   pg_restore -h localhost -U kanam -d kanam --clean /srv/kanam/backups/kanam-<fecha>.dump
   docker compose start postgres
   ```
5. **Restaurar el indice RAG** si cambio el esquema de embeddings:
   ```bash
   docker compose run --rm api python -m kanam.rag.restore --snapshot /srv/kanam/index/<snapshot_id>
   ```
6. **Verificar**:
   ```bash
   curl -fsS http://localhost:8080/healthz
   docker compose exec api alembic current
   docker compose exec api python -m kanam.smoke --world demo --check rag,generation
   ```
7. **Reabrir trafico** y registrar el incidente con el `request_id` o el rango temporal afectado.

Notas:

- El rollback de modelo es independiente: cambiar `MODEL_VERSION` en `.env` y `docker compose up -d api worker`. No requiere revertir la imagen.
- RTO objetivo: 30 min. RPO: 24 h con backup diario; 15 min si se habilita WAL archiving continuo (supuesto a validar).
- Todo rollback deja un snapshot del indice y un dump previo a la intervencion, aunque no se usen, para permitir un re-despliegue posterior sin reindexar desde cero.

## Riesgos

| Riesgo | Probabilidad | Impacto | Mitigacion |
|---|---|---|---|
| Kanam Writer no existe todavia: el contrato de consumo RAG se disena sin consumidor real y deriva antes de implementarse | Alta | Alto | Congelar un contrato minimo versionado (esquema de entidades + endpoint de recuperacion) y validarlo con un cliente de prueba propio; tratar el contrato como interfaz publica con tests de compatibilidad |
| El modelo local no alcanza la coherencia necesaria para generar fichas utiles (personajes, lugares, lore) | Media | Alto | Definir un set de evaluacion con 10-20 casos reales antes de construir la UI; permitir cambiar de modelo sin tocar la capa de dominio; degradar a generacion asistida (borrador editable) en vez de generacion directa |
| Deriva de canon: las fichas generadas contradicen el braindump, el genero o la sinopsis | Alta | Alto | Jerarquia de canon explicita y validacion post-generacion contra las secciones base; marcar toda ficha generada como "propuesta" hasta que el usuario la confirme |
| Duplicacion de entidades: el mismo personaje o lugar se crea dos veces con nombres distintos | Alta | Medio | Indice de entidades con busqueda por nombre y alias; deteccion de similitud por embeddings antes de crear; sugerir fusion en vez de crear |
| Recuperacion RAG imprecisa: el indice no devuelve el contexto relevante para la consulta de Kanam Writer | Media | Alto | Evaluar recuperacion con un set de consultas etiquetadas; combinar busqueda vectorial con filtros por tipo de entidad y por relevancia narrativa |
| El mundo completo no entra en la ventana de contexto del modelo local | Alta | Medio | Recuperacion por subgrafo (entidad + vecinos) en vez de volcado completo; resumen jerarquico por seccion; presupuesto de tokens por consulta |
| Indice de embeddings desactualizado tras editar una ficha | Media | Medio | Reindexado incremental disparado por evento de escritura; marca de version por entidad; verificacion de consistencia entre almacen y indice |
| Perdida de datos del worldbuilding sin backup ni versionado | Media | Critico | Persistencia en almacen transaccional con historial de cambios; export completo en formato abierto; snapshot automatico antes de cada operacion de generacion masiva |
| Costo y latencia de inferencia local por encima de lo tolerable en el hardware del usuario | Media | Medio | Medir latencia real en el hardware objetivo (supuesto a validar); generacion en background con progreso; cache de resultados por contexto identico |
| Acoplamiento al esquema de SudoWrite: se replican secciones sin validar que aportan al objetivo | Media | Medio | Mapear cada feature heredada a un caso de uso concreto; descartar explicitamente lo que no alimente la fuente de la verdad |
| Crecimiento no acotado del grafo de lore: entidades huerfanas, sin referencias ni uso | Media | Bajo | Vista de entidades huerfanas; sugerir conexiones al crear; limite blando de entidades por tipo con aviso |
| Inyeccion de prompt a traves de contenido importado o del braindump | Baja | Alto | Tratar todo contenido de usuario como dato, no como instruccion; separar system prompt de contexto recuperado; sanitizar en la capa de armado de prompt |
| Licencias de modelos y datasets incompatibles con uso local o redistribucion | Media | Alto | Fijar criterio de licencia antes de elegir modelo; registrar licencia por modelo en la configuracion |
| Encierro en formato propio sin export: el usuario no puede sacar su mundo | Media | Medio | Export a JSON y Markdown desde el primer release; el esquema de export es el mismo que el de la API |
| Concurrencia si el usuario accede desde varios dispositivos a la misma instancia | Baja | Medio | Definir hoy si el modelo de datos soporta escritura concurrente; si no, bloquear explicitamente el escenario |

## Supuestos

### Supuestos de producto

- Un solo usuario por instancia. No hay colaboracion en tiempo real ni control de acceso por rol en el alcance inicial.
- Las secciones base (braindump, genero, estilo, sinopsis) son la fuente de verdad de mayor jerarquia y prevalecen sobre cualquier ficha generada.
- Las fichas (personajes, lugares, lore) son entidades tipadas con identificador estable y relaciones explicitas entre ellas.
- El usuario revisa y confirma lo que la IA genera. La generacion produce propuestas, no canon automatico.
- El objetivo de Kanam Story Bible es ser fuente de la verdad para Kanam Writer, no un editor de prosa. La escritura queda fuera de alcance.
- El contenido del mundo es propiedad del usuario y no se envia a servicios de terceros.

### Supuestos tecnicos

- El despliegue es auto alojado y corre local, sin dependencia de APIs de modelos en la nube.
- El hardware objetivo puede ejecutar un modelo de generacion y un modelo de embeddings en simultaneo. Supuesto a validar: cuantizacion y tamano de modelo concretos.
- La latencia aceptable por operacion de generacion esta en el orden de segundos a minutos. Supuesto a validar con el usuario.
- El modelo no conserva memoria entre sesiones: todo el contexto se reconstruye por recuperacion en cada consulta.
- Los embeddings se calculan localmente y se persisten junto al almacen de entidades.
- El idioma de trabajo inicial es el espanol, con el ingles como caso secundario. Supuesto a validar.
- No hay requisito de sincronizacion con servicios externos ni de importacion desde SudoWrite.

## Decisiones abiertas

| Decision | Opciones consideradas | Bloquea a | Criterio de cierre |
|---|---|---|---|
| Modelo de generacion y de embeddings | Modelo local unico para ambas tareas; modelos separados y especializados | Generacion de fichas, calidad de recuperacion | Benchmark sobre el set de evaluacion en el hardware objetivo |
| Motor de almacenamiento vectorial | Embebido en el proceso (SQLite con extension vectorial, LanceDB) o servicio aparte (Qdrant, Weaviate) | Arquitectura de despliegue, backup | Prueba de recuperacion con el volumen de mundo esperado |
| Granularidad de indexado para RAG | Por ficha completa, por campo, por parrafo | Precision de recuperacion, costo de reindexado | Evaluacion de recuperacion con consultas etiquetadas |
| Esquema de entidades | Tipos fijos (personaje, lugar, lore) o tipos extensibles por el usuario | Modelo de datos, UI de fichas | Definir si el lore libre necesita tipo propio |
| Jerarquia de canon y resolucion de conflictos | Las secciones base siempre ganan; la ficha mas reciente gana; el usuario decide caso a caso | Validacion post-generacion | Regla unica escrita y testeada |
| Contrato con Kanam Writer | API HTTP, archivo exportado, protocolo de herramientas para modelos | Integracion futura, versionado | Contrato minimo congelado y cliente de prueba funcionando |
| Versionado del mundo | Historial lineal de cambios, snapshots, ramas alternativas | Persistencia, UI de historial | Definir si el usuario necesita explorar variantes del mundo |
| Deteccion de duplicados | Automatica con umbral de similitud o sugerida al usuario | Flujo de creacion de fichas | Umbral calibrado sobre casos reales |
| Generacion proactiva de lo que falta | Sugerir entidades faltantes al abrir el mundo o solo bajo demanda | UX, costo de inferencia | Definir tolerancia del usuario a sugerencias no pedidas |
| Persistencia | Archivo unico portable o base de datos local | Backup, export, concurrencia | Definir requisito de portabilidad del mundo |
| Modelo de datos multiusuario | Disenar con usuario desde el inicio o diferirlo | Costo de migracion futura | Definir si habra instancia compartida |
| Formatos de export e import | JSON, Markdown, ambos | Portabilidad, encierro de formato | Definir formato canonico de export |

## Plan de salida

| Frente | Accion de validacion | Criterio de cierre |
|---|---|---|
| Calidad de generacion | Set de 10-20 casos reales sobre un mundo de prueba | Las fichas generadas pasan revision manual sin correccion estructural en la mayoria de los casos |
| Recuperacion RAG | Consultas etiquetadas con contexto esperado | El contexto relevante aparece en el top de resultados en la mayoria de las consultas |
| Hardware y latencia | Medicion en el equipo objetivo con el modelo candidato | Latencia por operacion dentro del umbral acordado con el usuario |
| Contrato con Kanam Writer | Cliente de prueba que consume el esquema de entidades | Contrato versionado y test de compatibilidad en verde |
| Persistencia y backup | Prueba de export, import y restauracion de snapshot | Ciclo completo sin perdida de entidades ni relaciones |
| Licencias | Revision de licencia por modelo y dataset candidato | Ningun componente con licencia incompatible con el uso previsto |

Las decisiones de la tabla anterior se cierran antes de iniciar la construccion de la capa de generacion y de la capa de recuperacion. Las decisiones de esquema de entidades y de contrato con Kanam Writer se cierran antes de escribir el modelo de datos.
