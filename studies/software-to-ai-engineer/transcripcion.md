# Transcripción (ASR): De Software Engineer a AI Engineer — El Roadmap Más Realista

- Fuente: https://www.youtube.com/watch?v=qLobAfve9b0
- Canal: Fazt (@FaztTech)
- Título en YouTube: «De Software Engineer a AI Engineer: El Roadmap Más Realista»
- Ponente: Fazt
- Publicado: 2026-07-30
- Duración: 32:47 (1967s medidos en el reproductor; el último cue ASR cierra en 1951.8s)
- Idioma: español (subtítulos automáticos / ASR)
- Nota: el bloque 0:53–1:59 es un anuncio del patrocinador (**seenode**, `seenode.link/fazt`); se incluye como se escuchó, pero NO es contenido del roadmap. El ASR lo escribió «Cynote».

Timestamps en segundos, tal como los devolvió el ASR. Cada línea es un cue; líneas consecutivas pueden corresponder al mismo bloque. **No se editaron los cues**: las correcciones de términos van en el glosario, al final de este encabezado.

## Capítulos oficiales (descripción del video)

```
00:00 Intro: de Software Engineer a AI Engineer
00:53 Patrocinado
01:59 Para quién es este roadmap
02:37 Las bases del desarrollo
04:07 AI Engineer vs MLE vs AI Researcher
06:31 ¿Qué hace realmente un AI Engineer?
07:41 Checklist previo: lenguaje, SQL, Git, redes, Docker
09:07 System Design
11:17 Bases de los modelos: tokens, contexto, temperatura, roles
12:48 APIs de IA: Anthropic y OpenAI
13:58 Costos: API vs suscripción (y modelos chinos)
16:58 Trabajar con la API y casos de uso reales
19:40 Prompt engineering y function calling
22:04 RAG y bases de datos vectoriales
24:18 CLI, Skills y MCP
26:46 Repaso del roadmap
28:21 LLMOps: desplegar modelos y optimizar costos
30:23 Resumen de roles y por dónde empezar
32:20 Cierre
```

## Glosario de errores del ASR

| ASR | Correcto |
|---|---|
| Cynote | seenode |
| Note 10 | .NET 10 |
| Postres / Postre SQL | PostgreSQL |
| Maya SQL | MySQL |
| ASIS | ACID |
| IPI | API |
| EA engineer | AI Engineer |
| CBS | CVs |
| pr the engineering / PR engineer | prompt engineering |
| RAC / RAS | RAG |
| Cloud / Sonate / output | Claude / Sonnet / Opus |
| LlM OS | LLM Ops |
| Lane Shain / Laraf / Injes | LangChain / LlamaIndex / Inngest |
| Pinecon | Pinecone |
| fast.de | fazt.dev |

## Recursos reales de la descripción

- System Design Primer: https://github.com/karanpratapsingh/system-design
- Video de RAG: https://youtu.be/_B4jGz0JEGE
- Patrocinador: https://seenode.link/fazt

Los videos de CLI y de modelos locales que el ponente anuncia «en la descripción» no figuran en ella.

[0.1s] Si eres un desarrollador de software o
[2.0s] software engineer y has escuchado el
[3.6s] término AI engineer o ingeniero de
[5.8s] inteligencia artificial, probablemente
[7.2s] puedas pensar que es un rol algo
[8.6s] complicado y que es una nueva área que
[10.4s] no podrías continuar o quizás es muy
[12.4s] complicada de poder cambiar de rol.
[14.2s] Bueno, el día de hoy te voy a mostrar
[15.4s] justamente un roadmap bastante sencillo
[17.4s] para aquellos que son software engineer
[18.9s] o son desarrolladores de software y
[20.4s] quieren entrar en este rol de ingeniero
[22.4s] IA. Porque en la práctica podríamos
[24.2s] pensar que se tratan de estos que crean
[25.7s] modelos inteligentes o que están
[27.4s] haciendo investigación de modelos
[28.5s] inteligentes y no, en realidad es como
[30.3s] una continuación del desarrollo de
[31.6s] software y que en realidad cualquiera
[33.0s] puede aprender si ya sabe el desarrollo
[34.7s] de software básico. Así que en este
[36.1s] video les voy a dar un paso a paso de
[37.6s] qué temas aprender y sobre todo entender
[39.6s] algunos conceptos que deberían dominar
[41.3s] si quieren actualizarse o quieren
[43.1s] colocar en esos nuevos currículums o CBS
[45.5s] o en su perfil que ahora son EA engineer
[47.8s] y no tan solamente software engineer.
[49.7s] Pero bueno, vamos a ver de qué se trata
[51.0s] paso a paso. Coders, antes de empezar,
[54.1s] si quieren desplegar una web completa
[55.6s] que quizás han desarrollado con Note 10,
[57.6s] Python, Go o incluso Elixir, más una
[60.3s] base de datos, quizás Postres o My SQL y
[63.1s] quieren subirlo todo a un buen precio,
[64.7s] deben conocer Cynote. Esta es una
[66.4s] plataforma que te permite subir
[67.7s] proyectos web de una forma muy simple y
[69.3s] a un buen precio. Usarlo es muy fácil,
[71.1s] solo conectas tu repositorio de GitHub o
[73.1s] Gitlab, eliges tu proyecto y en segundos
[75.1s] tu aplicación ya está en línea con una
[77.0s] URL pública lista para usarse. Además,
[79.6s] la plataforma ya incluye el esencial
[81.3s] como permitirte añadir un dominio
[82.8s] personalizado. Ya le añade https y
[85.4s] también te da lo en tiempo real. Tiene
[87.3s] soporte también para wet sockets y
[89.0s] http2. Añadir variables de entorno y
[91.4s] tiene un soporte 247. Y en cuanto a
[93.6s] precios puedes desplegar base de datos
[95.2s] de Postres o MySQL desde $4 al mes y
[98.0s] servidores backend desde $ al mes. Con
[100.2s] esto ya tendrías tanto tu frontend y
[102.0s] backen funcionando en producción. Así
[104.1s] que para proyectos pequeños, MVPs o
[106.2s] clientes con bajo presupuesto, esta es
[107.8s] una opción rápida, simple y económica. Y
[111.0s] si en caso quieres probar la plataforma
[112.6s] antes, también tienes un trial gratuito
[114.2s] de 7 días para que puedas subir tu
[115.8s] proyecto. Para saber más de Cynote, te
[117.8s] dejo un enlace en la descripción. Muy
[119.3s] bien, antes de empezar primero vamos a
[120.6s] dejar en claro que este roadmap no es
[122.9s] tanto como para personas que no saben
[125.3s] desarrollar, sino es más para aquellos
[127.0s] que ya han estudiado quizás algunos años
[128.8s] o ya han creado algunas aplicaciones y
[130.4s] podríamos definirlos como software
[131.7s] engineer, pero quieren ahora migrar o
[134.2s] continuar con su aprendizaje. Entonces,
[136.1s] digamos que para aquellas personas que
[137.4s] ya sea que estén estudiando o recién
[139.0s] estén empezando o ya conocen algo del
[141.0s] desarrollo base, es decir, escribir
[142.6s] código, leer código o crear software en
[144.6s] general, este roadmand es más enfocado
[146.4s] en ese estilo. Luego voy a crear uno
[148.0s] desde cero donde les voy a explicar
[149.4s] justamente cómo también aprender esas
[151.4s] cosas, pero este video es más que todo
[152.8s] para aquellas personas que quieren
[154.0s] continuar con su aprendizaje o mejor
[155.6s] dicho quieren actualizarse. Ahora, en
[157.4s] cuanto a las bases del desarrollo, por
[159.3s] lo general siempre hablamos de estas
[160.7s] tres partes de sistemas que por lo
[162.3s] general todas las aplicaciones los
[163.7s] llevan de alguna forma. Es decir,
[165.1s] estamos hablando de base de datos aquí
[166.8s] de forma en general, es decir, hablamos
[168.7s] de base de datos SQL, no SQL e incluso
[171.5s] base de datos nuevas que podrían estar
[173.0s] surgiendo. Luego podríamos estar
[174.4s] hablando también de API, específicamente
[176.3s] de frameworks backend y lenguajes del
[178.2s] backend. Aquí podríamos mencionar a
[180.0s] lenguajes como Go, como Python o
[182.3s] JavaScript o TypeScript con Node y así.
[184.6s] En realidad es bastante amplio el
[186.1s] desarrollo backend, pero digamos que por
[187.9s] lo general hay lenguajes que son muy
[189.4s] comunes. Aquí también podría entrar
[190.8s] Java.net y muchos otros más. Ahora, para
[193.2s] desarrollar allí también están los
[194.2s] frameworks y digamos que estos facilitan
[196.0s] mucho más el trabajo y es una de las
[197.6s] bases que sabría cualquier
[198.6s] desarrollador. Y la otra base que
[200.2s] también se debería saber es el
[201.5s] desarrollo de aplicaciones frontend, es
[203.1s] decir, el poder crear interfaces o poder
[205.0s] generar alguna UI que consuma la API. Y
[207.2s] bueno, a partir de aquí es donde
[208.2s] realmente obtenemos lo que serían las
[210.0s] bases que les menciono. Es decir,
[211.5s] cualquier desarrollador sabe alguna de
[213.1s] estas áreas o incluso la combinación de
[214.9s] estas. Pero bueno, esto puede extenderse
[216.4s] mucho más porque dependiendo de lo que
[217.8s] hagan aquí podríamos estar hablando de
[219.4s] API que básicamente pueden comunicar
[221.6s] distintas aplicaciones. Luego también
[223.0s] podríamos estar hablando de protocolos
[224.4s] de seguridad para que básicamente
[226.3s] solamente usuarios autorizados puedan
[227.8s] acceder a cierto tipo de secciones o
[230.2s] datos, por ejemplo, de la base de datos
[231.7s] y así y en general varios tipos de
[233.2s] herramientas que acompañan tanto al
[234.8s] desarrollo de lo que sería el modelo de
[236.6s] datos, la API y el frontend. Es decir,
[238.7s] hay herramientas para poder debuguear,
[240.1s] para poder hacer testing y demás. Todo
[241.7s] esto es básicamente el desarrollo web
[243.1s] normal. Entonces, a partir de esta base
[244.4s] es donde yo voy a considerar los
[245.4s] siguientes temas que podrían aprender.
[247.0s] De hecho, hablando de esto, cuando me
[248.5s] refiero a engineer, en este caso, me
[250.3s] estoy refiriendo a un rol que estos días
[251.9s] es mucho más sencillo de lo que podría
[253.4s] parecer y es que no se confunden con el
[255.1s] término machine learning engineer, que
[256.8s] en este caso es otro tipo de rol y es
[259.0s] mucho más avanzado. Es decir, en años
[261.4s] anteriores, si ustedes han estado,
[262.9s] digamos, un poco atentos a cómo variaba
[264.8s] esta área de desarrollo de inteligencia
[266.6s] artificial, era como mucho más teórico,
[268.3s] es decir, podías ver alguno que otro
[270.0s] modelo o alguna que otra biblioteca que
[271.9s] realmente podía ser algo, pero no estaba
[273.6s] tan desarrollado como lo tenemos hoy en
[275.0s] día, que es prácticamente usable por
[277.0s] casi todas las personas al día de hoy.
[278.9s] Entonces, el Machine Learning Engineer
[280.3s] en este caso es un rol que por lo
[282.2s] general hace tareas mucho más complejas,
[284.4s] por ejemplo, entrena modelos o los puede
[286.6s] ir adaptando, es decir, hacer tuning. Y
[288.7s] bueno, en teoría también podría
[290.0s] implementar lo que son algunos research
[291.9s] o investigaciones a partir de cosas
[294.1s] nuevas que van surgiendo, es decir, sale
[295.8s] alguna optimización para algún modelo,
[297.2s] lo puede implementar, aunque no en
[298.7s] profundidad, pero digamos que sí puede
[300.4s] entender la mayoría de papers. Es decir,
[302.0s] es un trabajo mucho más especializado,
[303.7s] mientras que aquí hablamos de un trabajo
[305.2s] más práctico. Esto se trata de crear
[306.8s] aplicaciones. Aquí hablamos de
[308.2s] básicamente alterar un modelo, generar
[310.4s] un modelo o ir adaptándolo para que
[312.4s] otras aplicaciones encima de esta
[313.9s] funcionen. De hecho, aquí también se
[315.2s] combinan otras áreas. Por ejemplo, los
[317.4s] DevOBS por lo general también están
[319.2s] entrando en esta área, principalmente
[320.5s] porque los modelos también se tienen que
[322.0s] desplegar, también se tienen que subir
[323.4s] en una nube. Entonces están surgiendo
[324.9s] nuevas áreas como ML Ops, por ejemplo,
[327.2s] que es básicamente el poder desplegar
[328.7s] modelos, el poder adaptar herramientas
[330.5s] que funcionen como modelos inteligentes
[332.0s] y así. Pero bueno, eso lo voy a abarcar
[333.2s] en otro video porque también es un área
[334.7s] por aparte, pero digamos que muchos
[336.1s] creen que el eyer se trata de esto y sí,
[338.6s] en años anteriores posiblemente
[339.8s] podríamos estar enfocándonos en esta
[341.9s] área, pero en ese caso en la práctica,
[343.4s] el e engineer es incluso mucho más
[345.0s] sencillo de lo que podríamos pensar.
[346.8s] Ahora, aparte del machine learning
[348.2s] engineer, también hay otro rol que es
[349.8s] incluso mucho más complicado, que es el
[351.6s] EA Research o el investigador de IA, que
[353.9s] es básicamente una persona que ya no
[355.5s] solamente entrena modelos o hace fine
[357.5s] tuning o lo descarga, sino que
[359.3s] básicamente puede diseñar modelos, es
[361.6s] decir, estos ya no leen investigaciones,
[363.8s] sino que básicamente las crean. Y para
[365.6s] poder hacer eso, pues sí necesitan
[367.0s] conocer matemática avanzada. Por lo
[368.6s] general también tienen uno que otro PhD
[370.6s] o también incluso hasta tienen
[372.2s] financiación por parte de laboratorios
[374.2s] de IA. Es decir, este es como uno de los
[375.6s] roles más avanzados en IA y por lo
[377.5s] general se requiere cierto grado de
[378.9s] experiencia y pasar por todo esto o al
[380.8s] menos incluso enfocarse simplemente en
[382.8s] la parte teórica, porque en este caso no
[384.4s] se trata solamente de crear un modelo,
[385.7s] sino se trata de básicamente definir
[387.5s] cómo funciona, incluso a un nivel
[389.1s] estructural o teórico podríamos decir.
[390.8s] Pero bueno, después de todo esto, la
[391.8s] gran mayoría va a decir, "Okay, ¿cómo
[393.2s] entro a esta área?" O básicamente cómo
[394.6s] puedo empezar a aprender de todo esto
[396.8s] sabiendo que ya tengo algunas bases, ya
[398.9s] sé algunos lenguajes de programación y
[400.6s] demás. Bueno, lo primero es saber de qué
[401.9s] se trata este rol y de forma muy simple,
[403.8s] esto es básicamente la suma de lo que es
[405.6s] un desarrollo típico, es decir, lo que
[407.5s] puede saber de base de datos, API,
[409.1s] frontend, framework, frontend, full stag
[411.0s] y todo lo que conoces más lo que serían
[412.7s] herramientas y términos de IA. Y bueno,
[415.0s] si ya sabes desarrollo básico, esto no
[417.0s] lo voy a enfocar en este video,
[418.2s] simplemente me voy a enfocar en esta
[419.4s] parte de IA. Es decir, yo voy a asumir
[421.0s] que ya sabes de algún lenguaje, ya sabes
[422.6s] una base de datos y demás, pero lo que
[424.3s] quieres aprender es ahora esta parte. Y
[426.0s] bueno, aquí en realidad no es tan
[427.2s] sencillo como solamente escoger un
[428.9s] modelo o al menos es un inicio pero no
[431.0s] se queda allí, sino que a partir de
[432.6s] estos en realidad surgen nuevos tipos de
[434.2s] aplicaciones o digamos implementaciones
[436.1s] que vas a tener que ir conociendo a
[437.7s] medida que vas a ir ahondando en ese
[439.0s] tema. Y bueno, aquí podríamos hablar de
[440.4s] MCPs, RCXI o modelos locales y así, pero
[443.1s] esto se los voy a mencionar paso a paso.
[444.7s] El tema es que en este caso me voy a
[446.0s] enfocar en esta parte, así que tengan en
[447.8s] claro que cuando hablo de un AI engineer
[449.3s] es básicamente una persona que crea
[451.1s] aplicaciones de toda la vida, pero
[452.8s] utiliza modelos de IA y llega a generar
[454.8s] estas aplicaciones de aquí, solamente
[456.3s] que obviamente necesita esta base para
[458.5s] poder lograrlo. Pero bueno, solamente
[459.9s] para darles un resumen de qué cosas
[461.4s] deberían saber aquí, simplemente
[462.9s] listándolas, lo más básico sería
[464.4s] obviamente saber algún lenguaje de
[465.9s] programación, es decir, no solamente
[467.6s] verlo o que una lo genere, sino
[469.3s] realmente entender sus sintaxis o al
[471.0s] menos saber para qué funciona y qué
[472.8s] otras alternativas de lenguajes hay.
[474.3s] Esto aprenderlo en estos días es incluso
[476.0s] mucho más simple que otras veces porque
[477.7s] obviamente ya tienes modelos
[478.6s] inteligentes que pueden responderte
[480.2s] cualquier tipo de duda. Lo otro es
[481.8s] también aprender una base de datos.
[483.4s] Principalmente les diría cualquier SQL
[485.2s] sirve, aunque en mi sugerencia les diría
[486.9s] aprendan postre SQL o uno similar. Y con
[489.0s] esto pues van a empezar a implementar lo
[490.4s] que serían APIs y luego también saber
[492.4s] algo de desarrollo frontend como les
[493.7s] comenté, pero entre algunas de las
[495.1s] herramientas que todo desarrollador
[496.3s] utiliza, no importa qué lenguaje o
[497.9s] framework utilice, está Git, por
[499.5s] ejemplo, que es básicamente para poder
[501.0s] controlar software o controlar las
[502.5s] versiones de este. Lo otro es también
[504.0s] saber conceptos básicos de redes, es
[505.7s] decir, aquí no estoy hablando de
[506.6s] conceptos en profundidad, simplemente de
[508.4s] forma práctica. Es decir, aquí hablamos
[509.8s] de HTTP, estamos hablando de UDP, FTP o
[513.2s] cosas de ese estilo, que es básicamente
[514.8s] la forma de poder transferir archivos o
[516.6s] comunicarnos con sistemas externos y
[518.5s] así. Entonces, estas bases de cómo
[520.0s] comunicarse entre computadores es
[521.5s] bastante necesario y de nuevo también es
[523.4s] bastante fácil de aprender estos días. Y
[524.9s] lo otro que también deberían saber es
[526.2s] Docker, que es básicamente la forma de
[527.8s] poder crear contenedores o digamos como
[529.9s] empaquetar aplicaciones para que puedan
[531.6s] mantenerse de forma aislada. También
[533.2s] está relacionado con la nube, así que
[535.0s] digamos que es otro concepto que
[536.2s] deberían saber, pero con esto ya
[537.5s] estaría. Entonces, si ya tenemos alguna
[539.1s] idea de esto, es decir, ya eres como un
[540.8s] desarrollador que crea aplicaciones
[542.4s] utilizando estos programas o estos
[544.1s] conceptos, lo único que te faltaría es
[545.7s] este modelo IA. Pero antes de que entres
[547.4s] en esta área de IA, algo que sí te
[548.8s] recomendaría que aprendas, incluso antes
[550.3s] de que puedas dominar cualquiera de
[551.7s] estos conceptos o desarrollo de
[552.8s] aplicaciones, es algo llamado System
[554.7s] Design. El System Design se trata
[556.5s] justamente de que nosotros podamos
[558.0s] diseñar, como su nombre indica, lo que
[559.8s] sería un sistema. Esto quiere decir que
[561.7s] nosotros no pensamos solamente en
[563.7s] lenguajes o frameworks, sino básicamente
[565.8s] en los servicios, en la forma en la que
[567.8s] se desplan las aplicaciones y cómo estas
[569.6s] se conectan. Este es, digamos, como el
[571.4s] mapa de toda la aplicación y cómo
[573.2s] funciona junto con todos los servicios
[575.0s] que utiliza. Y por ejemplo, si buscan en
[576.8s] internet, van a encontrar muchos
[577.9s] recursos o muchas explicaciones, por
[579.8s] ejemplo, de cómo funcionan sistemas como
[581.6s] los de Instagram o los de Facebook o los
[583.6s] de YouTube y así. Y bueno, esos son
[585.2s] proyectos de hecho bastante grandes, es
[586.9s] decir, podrían pensar que solamente va
[588.3s] Ken y Fronén y ya está, pero en realidad
[589.8s] hay sistemas bastante complejos por
[591.1s] detrás e incluso algunos hasta tienen
[592.6s] sus propios sistemas internos o
[594.4s] propietarios. Pero bueno, si estás
[595.6s] creando un sistema, por lo general esta
[597.2s] es una forma de practicar, de saber todo
[599.1s] lo que conlleva tu aplicación y esta es
[600.5s] una forma de verlo bastante resumido
[602.0s] cualquier tipo de sistema que
[603.5s] implementes. Incluso pueden encontrar
[605.0s] muchos repos de este estilo, por
[606.2s] ejemplo, System Design, que es un repo
[608.1s] donde te explican algunos protocolos de
[609.8s] internet o algunos servicios para poder
[611.5s] almacenar algo o para poder comunicar
[613.7s] múltiples servicios y hacer que
[614.8s] funcionen como uno solo, como puede ser
[616.2s] un proxy, diseño de base de datos y lo
[618.7s] que importa dentro de una base de datos,
[620.2s] como pueden ser, por ejemplo, principios
[621.8s] ASIS, CAP y demás y bueno, temas en
[624.0s] general de cómo tomar datos y encolar,
[626.3s] por ejemplo, o tener sistemas publish
[628.4s] and subscribe y así. Es decir, es una
[630.4s] forma bastante genérica de poder diseñar
[632.8s] algo sin siquiera tocar lo que sería
[634.9s] algún tipo de lenguaje de programación o
[636.8s] framework aún. Entonces, esos gráficos
[638.2s] que acabamos de ver justamente se crean
[639.8s] de esta forma. Luego también tenemos
[641.0s] este otro que se llama System Design
[643.0s] Primer, que también lo que permite es
[644.9s] justamente lo mismo. También te explican
[646.7s] lo que son conceptos de forma en general
[649.1s] acerca de API, de cómo se comunican con
[651.2s] servicios de la nube y demás. Y bueno,
[652.7s] esto de aquí vale la pena que lo
[653.8s] estudien porque cuando ven algún tipo de
[655.7s] desarrollo con IA, por lo general esto
[657.5s] de aquí va a ser exactamente igual. Es
[658.9s] decir, igual se va a tener que
[659.9s] implementar una IPI, igual una base de
[661.6s] datos, una aplicación web, pero lo que
[663.9s] quizás van a encontrar de todo esto es
[665.6s] que van a aparecer un nuevo recuadro o
[667.4s] unos cuantos recuadros nuevos en su
[669.3s] diseño. Y esos son básicamente las
[671.0s] aplicaciones de IA. Así que esto de aquí
[672.8s] yo les recomendaría que no se lo salten
[674.4s] e incluso se los recomendaría que
[675.7s] aprendan mucho más a fondo. Pero bueno,
[677.2s] ya sabiendo eso, entonces, ¿de qué se
[678.8s] trata o cuáles son los conceptos que
[680.1s] debería dominar aquí en el área de IA? Y
[682.6s] bueno, el principal o el más básico es
[684.8s] justamente entender lo que son los
[686.5s] modelos inteligentes. Es decir, todo el
[688.2s] mundo puede llegar a utilizar algún
[689.4s] modelo de IA, pero lo importante es
[691.1s] conocer algunas bases, sobre todo al
[692.7s] momento de integrarlo con sistemas ya
[694.5s] existentes o sistemas incluso que pueden
[696.6s] estar desarrollando. Es decir, aquí
[697.8s] hablamos de poder entender, al menos de
[699.1s] forma básica cómo es que funcionan los
[701.1s] tokens, que es básicamente, digamos, el
[703.4s] streaming de datos que hacen estas sí o
[705.6s] las respuestas que te dan estas sillas.
[707.0s] Luego también entender el contexto que
[708.6s] es justamente para saber cuánto podemos
[710.6s] conversar con una que ya se empieza a
[713.0s] inventar cosas. Incluso relacionado a
[714.7s] eso también está lo que se conoce como
[716.4s] temperatura, que es básicamente el poder
[718.5s] decirle a una, "Okay, tienes temperatura
[720.7s] cero, no te inventes nada si no sabes
[722.5s] algo, simplemente responde que no sabes
[724.4s] y suficiente." Y bueno, todos estos
[725.8s] términos son las bases porque luego se
[727.7s] van a utilizar en sistemas un poco más
[729.6s] grandes y ya deberías saber esto.
[731.6s] Incluso luego también al momento de
[733.2s] chatear con una hay roles, es decir, no
[735.4s] solamente es tener como alguien que
[736.8s] envía un mensaje y alguien que recibe,
[738.3s] sino que hay varios tipos de formas de
[740.1s] poder configurar una conversación. Por
[741.9s] ejemplo, está el system, que es como el
[743.6s] prom que ya viene incluido dentro del
[745.2s] chat, por así decirlo. Luego está el
[746.7s] user, que es obviamente lo que el
[748.0s] usuario empieza a enviarte los mensajes.
[749.7s] Y luego está el modelo de IA, que es lo
[751.3s] que va respondiendo, que es el
[752.7s] asistente. Y bueno, estos son tan
[754.0s] solamente términos y es básicamente leer
[756.3s] un poco nada más de esto, incluso pueden
[758.4s] encontrar términos adicionales por allí,
[760.2s] pero esto es simplemente para que se den
[761.7s] una idea. Entonces, las bases de los
[763.6s] modelos de es lo más principal o al
[765.9s] menos lo que podrían empezar. Pero
[767.8s] bueno, a partir de aquí lo siguiente
[769.0s] sería empezar a utilizarlos de forma
[770.6s] práctica y aquí es donde entran las API
[772.6s] de IA, es decir, el poder utilizar estos
[775.2s] modelos inteligentes dentro de
[776.5s] aplicaciones propias. No hablamos de
[778.2s] utilizar, de hecho, una suscripción y
[779.9s] que se genere la aplicación, sino de que
[782.0s] cuando creamos algo, dentro de lo que
[783.9s] creamos, por ejemplo, una aplicación
[785.1s] web, puede haber algún tipo de chat que
[786.9s] consulte a los datos de la base de
[788.2s] datos. O por ejemplo, si creas algún
[790.3s] tipo de aplicación backend y quieres que
[792.3s] cada vez que llegue un mensaje una IA
[794.4s] empieza a procesarlo, bueno, eso también
[796.0s] se hace con una API de una IA. Y bueno,
[797.8s] allí hay dos proveedores que deben
[799.1s] conocer o que todo el mundo llega a
[800.7s] utilizar en algún punto y son las API,
[802.8s] que serían The Antropic y las de Open
[804.5s] AI. Las de Antropic porque básicamente
[806.0s] ellas ofrecen los modelos de cloud, es
[808.2s] decir, cloud en cualquier versión, cloud
[809.8s] output, cloud Sonate, Fable y muchos
[811.6s] otros más. y las de Open AI porque
[813.4s] también ellos son su competencia y
[815.0s] ofrecen lo que es GPT, es decir, en sus
[817.4s] múltiples variaciones 5.5, 5.6 o GPT
[820.6s] image, que es básicamente para poder
[822.0s] generar imágenes. Antropic no tiene para
[823.6s] generar imágenes, pero es justamente
[825.4s] algo que deben ir conociendo a medida
[827.1s] que van investigando de modelos. Es
[828.8s] decir, al final los modelos inteligentes
[830.2s] son como la IA que nosotros queremos
[832.0s] utilizar, pero para poder hacerlo
[833.7s] tenemos que utilizar una API y pagar por
[836.2s] uso. De hecho, aquí viene otro tema y es
[837.8s] que justamente las API que nosotros
[839.6s] vamos a estar utilizando, de hecho, por
[841.0s] lo general lo cobran por millón de
[842.4s] token, por así decirlo. Y bueno, esto
[844.2s] hay que tenerlo muy en cuenta porque he
[845.9s] visto, por ejemplo, algunos clientes que
[847.2s] por lo general te piden la idea de, "OK,
[849.0s] quisiera tener un chat dentro de mi
[850.4s] proyecto y creen que es algo muy simple
[852.6s] y algo muy barato, porque hay muchos
[854.7s] clientes, por ejemplo, que piensan que
[856.0s] solamente pagando $100 o $200 ya tienes
[858.4s] tu IA de forma ilimitada." Y no, hay
[860.0s] algo muy importante a tener en cuenta y
[861.8s] es que una cosa son el uso por API y
[864.1s] otra cosa es una suscripción de IA. La
[865.8s] suscripción de IA es de hecho lo que
[867.8s] ustedes quizás están utilizando para
[869.2s] desarrollar, quizás Cloud Code, quizás
[871.2s] Open Code, es decir, la suscripción de
[872.9s] Open Code o quizás GPT Codex con Chat
[875.7s] GPT. Y aquí ustedes pueden estar
[877.3s] pagando, por ejemplo, $100, $20, $200 y
[880.7s] así con cada una de las suscripciones.
[882.4s] Es decir, estos no sirven para poder
[883.6s] utilizarte dentro de aplicaciones, por
[885.3s] lo general solamente es para que puedas
[887.0s] crear aplicaciones. Es decir, eso está
[888.8s] más enfocado en que lo uses para
[890.3s] desarrollar. Y la razón es que
[891.8s] justamente ellos lo que hacen es que te
[894.1s] subsidian los gastos. Es decir, una
[895.6s] suscripción de $200 no cubre todo el
[897.9s] gasto que estás haciendo por parte de
[899.6s] esos modelos inteligentes. Es como si te
[901.6s] regalaran mucho más uso del que deberían
[903.6s] realmente. Pero bueno, la razón de que
[905.6s] funciona de esta forma es porque, bueno,
[906.9s] estas empresas grandes están subsidiadas
[908.6s] y modelos como Open Code como que te
[910.2s] combinan varios modelos, te dan modelos
[911.8s] baratos, otros modelos que son mucho más
[913.2s] caros que otros y ahí es como que se
[914.7s] compensa, pero de forma resumida, lo que
[916.5s] tú pagas como suscripción no se puede
[918.0s] utilizar para desarrollar aplicaciones
[919.9s] en general o por lo general. Así que
[921.6s] tarde o temprano vas a llegar a utilizar
[923.2s] lo que son las API de IA y vas a tener
[925.0s] que pagar por uso. Y bueno, esto es muy
[926.5s] importante tener en cuenta porque de
[927.6s] esta forma puedes decir a tu cliente,
[929.2s] "Okay, qué tanto estás dispuesto a pagar
[931.1s] por tener esa característica
[932.2s] inteligente." Y bueno, allí es donde
[933.5s] entra el tema y es que honestamente la
[935.2s] gran mayoría de personas que tienen
[937.0s] algún proyecto no quieren pagar por el
[938.7s] uso de este realmente. Y es que
[940.2s] justamente este último año también ha
[941.7s] habido muchas empresas que han estado
[943.1s] teniendo gasto por uso y se han dado
[945.1s] cuenta que es muy caro tener modelos de
[946.9s] funcionando constantemente. Pero bueno,
[948.6s] esta es justamente la razón de que los
[950.2s] modelos chinos también sean una
[951.9s] alternativa porque son API que por lo
[954.0s] general es mucho más barato de utilizar
[955.6s] que estas otras dos. Entonces si es
[957.4s] posible también que puedas tener
[958.9s] alternativas que son mucho más baratas,
[960.8s] pero también algo importante es que no
[962.8s] son exactamente iguales a estas de aquí.
[964.7s] Es decir, hay cierto grupo de personas
[966.2s] que por lo general son muy activos de
[968.4s] sugerir modelos chinos porque para cosas
[970.0s] básicas puede que te sirvan, pero
[971.2s] digamos que si tienes algún tipo de
[972.7s] aplicación compleja donde estás
[974.1s] interpretando, por ejemplo, una imagen
[976.0s] con pocos detalles o un archivo muy
[978.1s] grande donde quieres que realmente el
[979.7s] modelo sea lo más preciso posible, estas
[981.8s] dos de aquí por lo general son las que
[983.4s] mejor responden. Pero bueno, si
[985.0s] solamente quieres un chat y que te
[986.4s] responda y que entienda las cosas
[987.6s] básicas de un lenguaje y sobre todo no
[989.8s] es algo tan complejo, es posible que
[991.3s] también los modelos chinos te puedan
[992.4s] ofrecer lo mismo grado de calidad, al
[994.4s] menos en ese tipo de aspectos. Entonces,
[996.0s] aquí ya entrarían de forma general
[997.4s] muchos modelos y en realidad la gran
[999.0s] mayoría lo utiliza porque uno se puede
[1001.1s] incluso hasta alojar localmente, pero
[1003.2s] eso ya se los voy a mencionar en breve.
[1004.6s] El tema es que sí o sí van a tener que
[1006.2s] pagar, ya sea si utilizan un modelo
[1007.7s] chino o un modelo de estos populares,
[1009.7s] igual van a tener que pagar por uso para
[1011.4s] el desarrollo de su aplicación. Entonces
[1012.8s] es muy importante el manejo de precios
[1014.8s] porque de esta forma incluso podrían
[1016.0s] decidir si implementar una
[1017.0s] característica inteligente o no. Y
[1018.4s] bueno, una vez ya escojan su API,
[1019.6s] obviamente van a tener que conocer
[1020.7s] algunos temas. Por ejemplo, van a tener
[1022.1s] que aprender cómo funcionan las llamadas
[1023.6s] de API, es decir, cómo envías tu mensaje
[1025.5s] a esta API y este API te responde. Y de
[1027.6s] hecho, estas respuestas también pueden
[1029.0s] variar en formatos. Por lo general,
[1030.6s] estas se responden en marnow como texto.
[1032.6s] También podrías formatearlo para que te
[1034.0s] respondan un Jason o un HTML y así.
[1036.8s] Incluso si estás generando un chat para
[1038.9s] múltiples usuarios, es posible que
[1040.4s] múltiples usuarios estén consultando a
[1042.0s] la vez una misma llamada o hasta o hasta
[1043.9s] podrías tener un chat con múltiples
[1045.4s] conversaciones. Pero bueno, todo esto es
[1047.2s] normal que no siempre funcione siempre.
[1049.2s] Entonces, también tienes que considerar
[1050.6s] lo que son el soporte a fallos, es
[1053.1s] decir, el manejo de errores, que es algo
[1054.8s] típico de API. Así que si han
[1056.3s] desarrollado antes algún IPI normal,
[1058.2s] pues saben que todo lo que les estoy
[1059.2s] mencionando aquí es básicamente lo
[1060.7s] mismo. Ahora, una vez sepan esto, no
[1062.5s] solamente pueden crear chats, que es
[1064.4s] algo que la gran mayoría siempre tiene
[1066.0s] en mente cuando recién empiezan, pues
[1067.8s] obviamente creen que todo lo que se hace
[1069.3s] con es solamente puro chat que le envías
[1071.4s] un mensaje y responden, pero no
[1072.7s] necesariamente necesitas enviar un
[1074.3s] mensaje a una para esperar que te
[1076.2s] responda. Por lo general también se
[1078.0s] pueden desarrollar otro tipo de sistemas
[1079.4s] que no requieran que incluso estés
[1081.3s] conversando directamente con una. Y
[1083.0s] bueno, si colocamos un ejemplo muy
[1084.8s] básico y sencillo, por lo general si
[1086.8s] tienes algún tipo de interfaz donde
[1088.3s] necesitas, por ejemplo, generar texto,
[1090.3s] tú puedes crear algún tipo de UI donde
[1092.6s] solamente al dar un clic este ya
[1094.0s] rellena, por ejemplo, el campo de texto.
[1096.3s] Y por lo general, esta es una llamada de
[1097.7s] API también, solamente que aquí estamos
[1099.5s] integrando una UI, una interfaz gráfica
[1101.8s] con características inteligentes, aunque
[1103.8s] eso también podría funcionar para el
[1105.2s] backend. Es decir, si tú, por ejemplo,
[1107.0s] tienes alguna ruta del backend y quieres
[1109.2s] procesar algo con IA, a, supongamos que
[1111.0s] tú tienes un correo electrónico donde
[1112.4s] tus clientes te envían datos o correos
[1114.7s] electrónicos a esa dirección. Bueno, lo
[1116.4s] que podrías hacer, por ejemplo, es que
[1117.5s] cuando te envían un correo tu backend,
[1119.0s] el backend lo recibe. Pero antes de
[1120.5s] guardarlo, simplemente en la base de
[1121.8s] datos, tú puedes procesarlo con alguno
[1123.6s] de estos llamadas de API de IA y puedes,
[1126.1s] por ejemplo, resumir el correo, puedes
[1128.0s] ver si es válido o no y a partir de allí
[1129.8s] puedes guardarlo si tú quieres en una
[1131.1s] base de datos o simplemente también
[1133.0s] puedes clasificarlos si quieres saber de
[1135.1s] qué se trata el correo y si vale la pena
[1136.8s] procesarlo. o incluso esto también se
[1138.8s] está utilizando en despliegue, es decir,
[1140.8s] al momento de tener el despliegue de una
[1143.0s] aplicación, si una aplicación llega a
[1144.5s] fallar, esto se lo pasa a una API de IA.
[1147.6s] La IA lo procesa, corrige el código, es
[1150.0s] decir, el código que se ha subido a la
[1151.8s] nube y luego vuelve a hacer el
[1153.5s] despliegue. Nuevamente vuelve a hacer un
[1155.2s] push a GitHub y el despliegue se vuelve
[1157.1s] a disparar y si ocurre otro error ahí lo
[1158.9s] vuelve a procesar y así. Obviamente
[1160.2s] estos son procesos mucho más complejos
[1161.8s] porque incluso no solamente estamos
[1163.7s] hablando de que se repare algo, sino
[1165.4s] también del gasto, como les digo. Y es
[1167.0s] que justamente el poder tener en cuenta
[1168.8s] cuánto se está gastando por una o si el
[1170.5s] modelo es capaz de hacerlo es muy
[1172.1s] importante al momento de implementarlo
[1173.8s] en la realidad. Aunque bueno, para poder
[1175.5s] lograr todo esto dentro también ustedes
[1177.3s] van a aprender otros conceptos, es
[1178.8s] decir, cuando empiecen a implementar ese
[1180.6s] tipo de proyectos que pueden ser muy
[1182.4s] sencillos, adentro se va a encontrar con
[1184.0s] lo que se conocen como pr the
[1185.4s] engineering. Y bueno, en realidad este
[1186.7s] término tiene mala reputación,
[1187.9s] principalmente porque cuando salió como
[1189.8s] que sobreexplotaron mucho esta idea de
[1192.1s] que necesitabas aprender pron
[1193.5s] engineering y demás como para poder
[1195.0s] aprovechar los modelos inteligentes. Y
[1196.4s] bueno, para aquel que no sepa de qué se
[1197.6s] trata esto, es básicamente el poder
[1199.3s] saber cómo pedirle algo a una es la
[1202.7s] consulta, cómo qué términos utilizar o
[1204.8s] qué tan complejo debe ser y demás. El
[1206.9s] tema es que a este punto los modelos
[1208.6s] inteligentes ya entienden muy bien
[1210.4s] muchas de las instrucciones y, incluso
[1212.3s] no necesitas darle muchas. Incluso hace
[1214.0s] poco se publicó un post de algunos de
[1216.0s] los trabajadores de Cloud Code, por
[1217.3s] ejemplo, y básicamente estab quitando
[1219.1s] una enorme cantidad de prs que tenía
[1220.5s] internamente la herramienta, porque
[1221.7s] ahora el modelo, es decir, los modelos
[1223.3s] actuales, como por ejemplo Cloud 5, ya
[1225.2s] puede interpretar mucho mejor el
[1226.4s] contexto y no necesita que le des tantas
[1228.1s] instrucciones en sí. Pero bueno, esto sí
[1229.7s] es importante sobre todo cuando
[1230.7s] desarrollamos aplicaciones propias
[1232.0s] porque obviamente nosotros no estamos
[1233.5s] dependiendo de herramientas externas,
[1235.0s] entonces obviamente tu chat tiene que
[1236.6s] tener en claro cómo es que tiene que
[1238.2s] responder. Lo mismo si vas a crear una
[1239.6s] aplicación backend que va a recibir
[1240.8s] algún tipo de mensaje y la lo tiene que
[1242.4s] procesar y en el despliegue igual. De
[1243.8s] hecho, el PR engineer es tan sencillo
[1245.0s] como colocar un texto y decirle cómo se
[1247.2s] tiene que comportar el sistema o cómo se
[1248.8s] tiene que comportar en realidad la IA al
[1250.3s] momento de recibir cierto mensaje.
[1251.6s] Entonces aquí, por ejemplo, en el
[1252.9s] despliegue le dirías, "Eres un sistema
[1254.6s] de manejador de errores de despliegue."
[1256.6s] En el backend le podrías decir, "Eres un
[1258.0s] clasificador de correos y así." Ahora,
[1259.9s] mucho más importante incluso que el PR
[1261.3s] engineering, es decir, de saber qué
[1262.7s] pedir a la IA, a es algo llamado
[1264.1s] function calling, que es básicamente el
[1265.9s] poder hacer que una IA pueda ejecutar
[1268.4s] algún tipo de código adicional para
[1270.3s] poder hacer algo. Es decir, supongamos
[1272.0s] que aquí en el backend decidió que tiene
[1273.8s] que clasificar un correo o tiene que
[1275.8s] eliminarlo. Bueno, ¿de qué forma podría
[1277.5s] ser eso? Y bueno, ahí es donde entra
[1278.6s] justamente el function calling, que es
[1280.1s] una función de toda la vida en código.
[1282.0s] Digamos que puede ser un script que la
[1283.7s] puede ejecutar y de esa forma puede
[1285.2s] eliminar el correo o puede mover el
[1287.0s] correo y así. Y bueno, eso depende mucho
[1288.8s] de lo que estés implementando en tu
[1290.0s] backend, porque por ahí quizás ya tienes
[1291.8s] Python disponible o el lenguaje que
[1294.0s] utilices y la simplemente puede llamar
[1296.0s] esa función y ejecutarla por ti. De
[1297.6s] hecho, aquí también solo modo de
[1299.0s] detalles, hay algunas herramientas que
[1301.5s] llaman esto de varias formas. Por
[1303.0s] ejemplo, hay quien también lo llama
[1304.3s] tools, que es justamente la forma de
[1305.9s] poder darle a la Igunas herramientas
[1308.4s] para que haga algo. Es decir, ya no
[1309.8s] solamente responde o te dice, "Bueno,
[1311.8s] podrías hacer esto, esto, esto,", sino
[1313.2s] que básicamente el mismo modelo de día
[1314.6s] puede ejecutar ese código y es donde
[1316.6s] realmente puede hacerlo él mismo. Pero
[1318.0s] bueno, el conocer todo esto nos lleva
[1319.2s] justamente el poder crear aplicaciones
[1321.1s] que van a utilizar todos esos conceptos
[1322.7s] por debajo. Es decir, aquí finalmente
[1324.3s] vamos a llegar a crear aplicaciones que
[1326.4s] realmente utilicen todo esto y uno de
[1328.3s] los más populares actuales es justamente
[1330.5s] el RAC y las bases de datos vectoriales.
[1332.8s] Ahora, el término RAC viene de retrieval
[1334.6s] augmented generation, que es básicamente
[1336.2s] la forma en la que muchas empresas están
[1338.2s] permitiendo comunicar a una IA con sus
[1340.4s] datos. Es decir, si por ejemplo
[1342.2s] planteamos la idea de que hay alguna
[1343.7s] empresa que tiene ventas, registro de
[1345.8s] recursos humanos, pagos, inventario y
[1348.4s] todo aquello, por lo general quieren que
[1350.0s] alguna simplemente al consultarle pueda
[1351.8s] leer estos datos y pueda darle o
[1353.5s] reportes o predicciones o simplemente
[1356.1s] hacer algunas tareas que por lo general
[1358.2s] requerirían de varios pasos. Y bueno, el
[1360.0s] RAS justamente trata de eso, de que una
[1362.0s] puede acceder a tus datos, que puedes
[1363.9s] estar en una base de datos o pueden ser
[1365.7s] documentos o Excels o cualquier tipo de
[1368.1s] origen de datos. es solamente una forma
[1370.2s] en la que va a poder leer por sí mismo y
[1372.8s] va a poder entenderlos. Ahora, esto
[1374.2s] suena muy simple, pero en la práctica
[1375.8s] conlleva varios tipos de herramientas. Y
[1377.5s] bueno, en este video no voy a andar en
[1378.6s] detalles de cómo crear uno, pero sí les
[1380.7s] voy a dejar un video en la descripción
[1381.6s] de cómo poder crearlos y entrar en
[1383.3s] detalle en qué es lo que usan
[1384.3s] internamente. Y bueno, aquí también hay
[1385.7s] otro término que les mencioné que se
[1386.8s] llama vector database o base de datos
[1389.0s] vectorial. Y en realidad es como una
[1391.1s] base de datos alternativa a la base de
[1393.1s] datos de tu negocio o proyecto que estés
[1395.3s] creando. Es decir, la gran mayoría de
[1396.6s] nosotros cuando hablamos de dónde se
[1398.2s] almacenan los datos quizás te viene a la
[1399.9s] mente una base de datos SQL. Bueno, por
[1401.8s] lo general una no puede entender los
[1404.2s] datos de una base de datos SQL. Podría
[1406.4s] parecer que sí porque por lo general
[1408.2s] procesa datos de texto, es decir,
[1410.5s] simplemente textos escritos. Pero en
[1412.5s] realidad para poder entender lo que está
[1414.2s] allí, en lugar de simplemente cargarle
[1416.4s] texto, porque tu base de datos puede ser
[1417.7s] muy grande, necesitas convertir tus
[1419.3s] datos a un formato especial que se le
[1420.7s] llama vector. Y cuando se habla que la
[1422.5s] puede entender tus datos, en realidad va
[1424.0s] a estar consultando esa base de datos
[1426.0s] realmente que tiene como una versión
[1427.8s] alternativa de lo que ya tenías antes.
[1429.8s] Incluso estos vectores también se pueden
[1431.1s] guardar en la misma base de datos, pero
[1433.2s] digamos que para entendimiento al menos
[1434.8s] de esta explicación, digamos que es una
[1436.2s] base de datos por aparte. Y esta base de
[1437.8s] datos por aparte, al igual que aquí
[1439.2s] podrías utilizar por ejemplo Postre SQL,
[1441.9s] Maya SQL y muchas otras más. Bueno,
[1443.8s] también hay bases de datos
[1444.7s] especializadas simplemente en este tipo
[1446.4s] de formato. Aquí entra, por ejemplo,
[1448.2s] Pinecon, entra Chroma y muchas otras
[1450.8s] bases de datos vectoriales similares,
[1452.5s] aunque bueno, en la realidad no es la
[1454.4s] única forma de lograr que una IA pueda
[1456.2s] interpretar tus datos. Así que aquí
[1458.0s] también simplemente a modo de mención y
[1460.2s] que vale la pena que también lo estudies
[1461.8s] si quieres enfocarte en esto de AI
[1463.3s] Engineer. Es básicamente el poder
[1464.9s] desarrollar un CLI. Y es que como
[1466.8s] justamente hay muchas aplicaciones que
[1468.2s] ofrecen algún tipo de API, esta API se
[1470.2s] comunica con tu base de datos, pues
[1471.6s] también puedes crear un CLI que funciona
[1473.1s] como cliente que consulta tu API y de
[1475.3s] esta forma puedes llegar a tener como
[1476.6s] una especie de IA que pueda utilizar tu
[1478.5s] API. Esto es mucho más avanzado, pero
[1480.0s] les dejo un video ahí en la descripción
[1481.4s] demostrativo de cómo funciona esto y
[1483.3s] cómo una puede utilizar justamente ese
[1485.1s] tipo de herramientas de consola para
[1486.6s] poder contestar tus datos o manipular tu
[1488.8s] sistema. De hecho, esto de aquí se
[1490.1s] combina también con lo que se le llaman
[1491.4s] los skills, que es otro tema también
[1493.3s] aprender, pero es bastante ligero. De
[1495.1s] hecho, los skills es una forma
[1496.4s] simplemente de definir como un pront y
[1498.2s] poder reutilizarlo de forma muy
[1499.8s] resumida. Y bueno, básicamente eso lo
[1501.8s] pueden aprender en simplemente unos
[1503.2s] cuantos minutos y lo estudien más que
[1505.6s] suficiente incluso. Ahora, muy aparte de
[1507.4s] esto, también hay otra forma de hacer
[1508.8s] que tus usuarios consulten tus datos de
[1511.0s] tu sistema y es a través de otro
[1512.6s] concepto también que vale la pena
[1513.9s] mencionar aquí que se llama MCP. El MCP
[1516.3s] es básicamente como una API adicional.
[1519.2s] De hecho, el MCP consulta tu API, pero
[1521.6s] este permite ser como un conector para
[1523.6s] aplicaciones ya existentes o chats ya
[1526.2s] existentes. Es decir, si tienes usuarios
[1528.3s] que utilizan, por ejemplo, Chat GPT o
[1530.8s] Cloud Desktop o cualquier otra interfaz
[1533.3s] que permita tener un chat, por lo
[1535.2s] general esas interfaces permiten
[1536.9s] conectar a un MCP. El MCP es un programa
[1539.3s] que se mantiene escuchando y digamos que
[1541.4s] es como un traductor, es decir, tu
[1543.2s] usuario puede pedir algo como, "¿Cuáles
[1545.2s] son mis ventas de este año?" Y lo que va
[1548.6s] a hacer es que este mensaje va a llegar
[1550.0s] al MCP y el MSP lo va a traducir en una
[1552.3s] llamada de API, algo así como
[1554.1s] slashventas con un parámetro desde 2026
[1557.2s] o algo así. Entonces, esto de aquí
[1558.8s] justamente para que funcione, obviamente
[1560.6s] el MSP tiene que conocer tu API y
[1562.8s] obviamente también tiene que traducir el
[1564.5s] texto del usuario. Entonces, entonces
[1566.2s] esta es una forma de poder comunicar lo
[1567.9s] que hace, por ejemplo, aplicaciones como
[1569.3s] chat GPT, Cloud Desktop y demás. Y
[1571.5s] también se alimenta de los datos, pero
[1573.5s] básicamente la suscripción la paga el
[1575.1s] usuario porque el usuario ya está
[1576.3s] suscrito en estas plataformas y el MCP
[1578.3s] se utiliza desde su aplicación.
[1579.8s] Entonces, como que no tienes que pagar
[1580.9s] ninguna IPI externa, solamente tendrías
[1582.9s] que desplegar tu traductor, por así
[1584.9s] decirlo, del MCP y con eso ya estaría.
[1587.0s] Pero bueno, con esto básicamente ya
[1588.7s] tienen una idea de que este tipo de
[1590.4s] aplicaciones se pueden desarrollar, mps,
[1592.2s] CI y Skills y RA. Y de nuevo, este no es
[1594.4s] un video a detalle de cada uno de estos,
[1596.1s] pero digamos que son como
[1597.0s] implementaciones prácticas encima de
[1598.8s] todos esos términos que ya hemos visto
[1600.2s] antes, solamente que eso es una forma en
[1602.1s] la que básicamente podrías desarrollar
[1604.2s] algo para el usuario. Y bueno, si le
[1605.9s] damos una revisión rápida, hablamos de
[1607.6s] modelos inteligentes. Esto es como la
[1609.1s] base que todo el mundo debería saber si
[1610.6s] va a iniciar en esto. Luego hablamos de
[1612.2s] la teoría, por así decirlo, en conocer
[1614.5s] todos estos temas de aquí para poder
[1616.1s] entender de qué se tratan los sistemas
[1617.8s] basados en IA. Y eso ya sería lo
[1619.2s] práctico, lo que podrías vender a un
[1620.8s] usuario, lo que podrías implementar
[1622.4s] dentro de un sistema real. Pero bueno,
[1623.9s] dentro de cada una de estas
[1624.8s] implementaciones van a haber muchos más
[1626.2s] temas que van a tener que ir
[1627.4s] aprendiendo, principalmente porque aquí
[1629.2s] está sobre simplificado, pero por
[1631.1s] ejemplo dentro de las bases de datos
[1632.6s] vectoriales, pues tienen que aprender
[1634.0s] algunos tipos de herramientas que van a
[1635.3s] permitir poder vectorizar grandes
[1637.0s] cantidades de datos o cómo van llegando
[1638.8s] incluso. Luego en cuanto a los MCPs,
[1640.4s] pues que tengan uno que otro trabajo al
[1642.3s] momento de documentar y saber qué
[1643.7s] funciones son las capaces de poder
[1645.4s] llamar, porque básicamente estos chats
[1647.2s] pueden utilizar este MCP para poder
[1648.8s] acceder a datos que quizás no deberían.
[1650.7s] Entonces es como diseñar una API al
[1652.4s] final del día y con el CLI es
[1653.8s] básicamente otra forma o otro cliente
[1655.6s] que también consulta la IPI y también
[1657.6s] requiere que conozcas qué es lo que es
[1659.0s] capaz de hacer el CLI o permitirle a la
[1661.3s] gente hacer con el CLI porque de otra
[1663.0s] forma también podrías reescribir el
[1664.4s] código allí. Entonces también si tienes
[1666.2s] que aprender cómo desplegar la
[1667.6s] herramienta para que la no simplemente
[1669.3s] acceda al código y lo reescriba. Y
[1670.7s] bueno, básicamente son algunos temas
[1672.0s] allí soltados al aire, pero no es lo
[1674.0s] único. Es decir, a medida que vayan
[1675.3s] aprendiendo, pues pueden ir encontrando
[1676.6s] proyectos como Lane Shain, Laraf, por
[1678.9s] ejemplo, Temporal, Injes y muchos otros
[1681.2s] más que básicamente lo que hacen es que
[1682.8s] te permiten poder vectorizar datos o te
[1685.1s] permiten poder incluso ingresar datos
[1687.1s] dentro de un modelo que ya esté
[1688.2s] desplegado y empezar a procesarlo. Y
[1689.8s] bueno, en realidad implementar cada uno
[1691.1s] de estos depende del proyecto que estén
[1692.6s] desarrollando, así que tampoco vale la
[1693.9s] pena aprender todo esto, pero
[1695.2s] simplemente modo de comentario pueden
[1696.4s] que se lo encuentren tarde o temprano. Y
[1698.0s] bueno, aquí es donde realmente está la
[1699.3s] mayor parte del trabajo, pero hay
[1701.0s] ocasiones en las que también pueden que
[1702.5s] les pidan que desplieguen estos
[1704.5s] proyectos e incluso hasta que alojen un
[1706.5s] modelo en local, que es tarde o temprano
[1708.6s] se va a encontrar con alguna empresa que
[1710.2s] va a querer, por ejemplo, no pagar por
[1712.1s] un API porque se preocupan de que sus
[1713.9s] datos no salgan fuera de su sistema. Y
[1716.1s] bueno, allí justamente se van a topar
[1717.6s] con el término de Llm OS, que es
[1720.1s] básicamente mandar a producción modelos
[1721.8s] inteligentes o aplicaciones que utilicen
[1723.3s] modelos inteligentes. Y aquí, de hecho,
[1725.0s] entran varios temas. En realidad, este
[1726.6s] también es un tema amplio porque
[1728.2s] hablamos de modelos que puedes desplegar
[1729.6s] dentro de tu propio hardware o incluso
[1731.6s] también puedes utilizar modelos
[1733.0s] desplegados en una nube. Es decir, así
[1735.1s] como desplegas una aplicación en una
[1736.9s] nube de terceros, como puede ser AWS,
[1738.9s] Google Cloud o Asure, también puedes
[1740.7s] desplegar un modelo inteligente en una
[1742.8s] nube y pagar por uso, sabiendo que todo
[1744.9s] lo que se procesa está dentro de tu
[1746.5s] nube. Es decir, puedes llegar a
[1747.7s] utilizar, por ejemplo, un GPT open
[1749.4s] source y este va a estar desplegado en
[1750.7s] tu nube y vas a pagar por el uso de tu
[1752.3s] nube en lugar de pagar una suscripción.
[1754.2s] Y bueno, esto es un poco extraño que una
[1756.0s] persona lo use, pero empresas por lo
[1757.4s] general de nuevo dependiendo del grado
[1759.1s] de privacidad que quieran, pues pueden
[1760.5s] que lo implementen. Y ahí entran temas,
[1762.2s] por ejemplo, de colocar un ray limiting
[1764.2s] como para que no estén saturando la IA
[1766.6s] solamente ir consultando todos al mismo
[1768.4s] tiempo, sino que como que hay un
[1769.7s] intervalo de tiempo. Luego también
[1771.1s] hablamos de costos al momento de
[1773.1s] optimizar, por ejemplo, consultas. O
[1775.4s] incluso puede que en algún momento
[1777.2s] necesites enrutar de un modelo a otro
[1780.0s] porque quizás te están enviando un audio
[1782.0s] o una imagen o quizás quieres que el
[1783.9s] modelo responda de cierta forma y sabes
[1785.5s] que otro modelo lo hace mejor. Entonces
[1787.0s] allí también podríamos hablar de model
[1788.3s] routing, es decir, también hay modelos
[1789.6s] inteligentes que al momento que le haces
[1790.9s] la duda, este dice, "Okay, le voy a
[1792.4s] pasar esta pregunta a otro modelo."
[1794.4s] Luego también está el caching, que es
[1795.8s] básicamente el guardar en memoria
[1797.5s] algunas respuestas que ya ha generado la
[1799.4s] para que si alguien pregunta exactamente
[1800.8s] lo mismo, no se vuelva a generar. Y
[1802.6s] básicamente hablamos también del
[1803.9s] escalado, que es cuánto nosotros podemos
[1805.7s] soportar o cuántos usuarios concurrentes
[1807.4s] podríamos soportar o consultas
[1809.0s] concurrentes dentro de un modelo
[1810.3s] inteligente. Y de nuevo, este es
[1811.5s] simplemente hablando de que se despliega
[1813.1s] una nueva propia. Eh, si hablamos, por
[1815.0s] ejemplo, de que tenemos un hardware
[1816.4s] propio, ya allí cambia la cosa. Ahí
[1818.0s] estaremos hablando de i en local y es
[1819.6s] otro tema que también he abarcado que
[1820.8s] les voy a dejar algunos videos en la
[1821.8s] descripción. Entonces, de forma
[1822.9s] resumida, de esto se trata el engineer
[1824.8s] de forma práctica. Como pueden ver, si
[1826.9s] ustedes ya saben de desarrollo básico,
[1828.5s] ya se están saltando la mayoría de temas
[1830.0s] a aprender, entonces no es como que
[1832.0s] tienen que empezar desde cero una nueva
[1833.5s] carrera o algo así, simplemente es una
[1835.1s] continuación, es una actualización de
[1836.8s] estos días, básicamente. Y de nuevo,
[1838.2s] pueden ver que aquí no estoy hablando de
[1839.6s] cosas técnicas, no estoy hablando de
[1841.7s] matemáticas o modelos de inferencia o
[1844.1s] básicamente de cosas teóricas, sino que
[1845.9s] todo tiene un uso práctico y la idea es
[1848.0s] generar aplicaciones que utilicen estos
[1849.9s] modelos actuales que ya están
[1851.3s] funcionando. Y bueno, a partir de aquí,
[1852.6s] obviamente, si les interesa más esto,
[1854.0s] pues podrían ir subiendo el nivel y
[1855.8s] pueden ir entrando mucho más en generar
[1857.9s] sus primeros modelos, en el hacer tuning
[1860.4s] o pueden entrar un poco más en detalle
[1861.9s] del funcionamiento interno de estos
[1863.2s] modelos, pero allí justamente ya entran
[1865.2s] temas de machine learning y no tanto de
[1867.4s] desarrollar una aplicación. Entonces, de
[1868.9s] forma resumida, como que el AI Engineer
[1871.2s] pues genera aplicaciones, entonces un
[1873.0s] desarrollador de software está mucho más
[1874.3s] cercano a un AI engineer. Luego el MLS
[1876.8s] trabaja con modelos o o puede
[1878.4s] desplegarlos o incluso poder hacer una
[1880.2s] que otra configuración más avanzada. Y
[1881.8s] bueno, el AI Research pues puede hacer
[1883.1s] básicamente lo que quiera porque es
[1884.4s] solamente diseñar un modelo y ya está en
[1886.6s] la parte más básica. Entonces es como el
[1888.4s] fundamento de todo lo que utilizamos en
[1890.2s] realidad. Y bueno, espero que este video
[1891.5s] les haya dado una idea justamente. Y si
[1893.5s] se preguntan, "Okay, ¿con cuál empiezo o
[1895.2s] qué programa empiezo o qué aplicación me
[1897.1s] gustaría desarrollar?", Yo les diría,
[1898.3s] empiecen con el rag. Es básicamente la
[1900.0s] forma más básica de entender cómo una
[1901.8s] puede responder datos y a partir de allí
[1903.8s] ya pueden ir probando otras cosas como
[1905.6s] pueden ser el MCP. Y bueno, a medida que
[1907.4s] van desarrollando esto, pues allí van a
[1909.0s] ir encontrándose más herramientas. De
[1910.9s] nuevo, en este caso yo he resumido
[1912.0s] algunas, pero en la práctica van a ver
[1913.8s] que van a haber más framework, van a ir
[1915.4s] surgiendo nuevas herramientas e incluso
[1917.0s] estos días se habla del graph engineer,
[1919.0s] que es como para poder generar grafos a
[1920.6s] partir de tu información y todo esos son
[1922.2s] conceptos nuevos que van surgiendo, pero
[1923.7s] de forma resumida empiecen con el RAG,
[1925.4s] es muy fácil de implementar y si quieren
[1927.2s] crear uno o quieren saber de qué se
[1928.5s] trata, les voy a dejar también un video
[1929.5s] en la descripción y luego a partir de
[1930.8s] allí ya pueden ir saltando con otros
[1932.2s] temas. En fin, espero que este video les
[1933.6s] haya dado una idea y si tienen una duda
[1935.2s] o algo no se les haya quedado claro,
[1936.6s] también pueden dejarlo en los
[1937.6s] comentarios. Nos vemos en un siguiente
[1939.0s] video. Y eso ha sido todo por el video
[1940.4s] del día de hoy. Si quieres conocer más,
[1942.1s] te dejo en pantalla mis enlaces sociales
[1943.8s] y mi web fast.de, en donde puedes
[1945.6s] reservar asesorías personalizadas de
[1947.2s] cualquier tema. Y no te olvides de
[1948.8s] dejarme un comentario, ya sea de una
[1950.2s] duda o una sugerencia para el siguiente
[1951.8s] video. Nos vemos en un próximo
