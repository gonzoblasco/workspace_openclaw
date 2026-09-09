# LinkedIn Post: aria-posinset global en menús con secciones (react-spectrum)

**Nicho:** a11y (diferenciador)
**Proyecto:** adobe/react-spectrum
**PR:** #10554 (mergeado 2026-09-09 por yihuiliao)
**Fecha:** 2026-09-09

---

## Draft

No todos los bugs de accesibilidad rompen algo visible. Algunos simplemente desaparecen del test suite un día, sin que nadie se dé cuenta.

Hace unos días mergeé un PR en Adobe React Spectrum que ilustra este punto: es solo un test, y justamente por eso es interesante.

**El contexto**

En un menú con secciones (grupos de ítems), la especificación ARIA exige que `aria-posinset` sea **global**: si hay 4 ítems repartidos en 2 secciones, las posiciones van de 1 a 4 seguidas, consistente con `aria-setsize=4`. Si una sección reinicia el conteo, los screen readers anuncian posiciones que no corresponden ("elemento 1 de 2" cuando en realidad es "elemento 1 de 4"), y la navegación se vuelve confusa.

React Spectrum ya producía los valores correctos. El problema era que **nada lo garantizaba**: un refactor futuro del cálculo de índices podía reintroducir el reinicio por sección sin que ningún test fallara.

**La trampa del test**

Escribir el test parecía trivial: renderizar un menú con secciones y asertar que las posiciones son 1, 2, 3, 4. Pero la primera versión tenía una falla que yo mismo no vi: el helper que armaba el mock "aplanaba" las secciones en una lista plana de ítems. El DOM resultante nunca contenía la estructura de secciones que el test decía cubrir.

El test pasaba. Pero no estaba testeando lo que decía testear. Un maintainer lo detectó en segundos, y con razón: es exactamente el tipo de atajo que da falsa confianza.

**La corrección**

La versión final renderiza cada sección a través del hook real (`useMenuSection`), incluyendo los grupos con sus headings, y además cubre el caso de secciones sin heading (donde el nombre accesible viene por `aria-label`). Así, cualquier cambio futuro en la lógica de secciones -no solo en el cálculo de índices- queda ejercido por el test.

**El por qué importa**

Un test de accesibilidad solo vale lo que vale la estructura que ejercita. Si el setup simplifica el DOM hasta convertirlo en una lista plana, el test verde es decoración. La regla que me quedó: el test tiene que renderizar la estructura real del componente, fallar si el comportamiento se rompe, y verificar exactamente lo que el PR declara.

#Accessibility #ARIA #Testing #OpenSource #FrontendEngineering