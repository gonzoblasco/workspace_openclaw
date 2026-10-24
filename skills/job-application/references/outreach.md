# Outreach - primer contacto y preguntas de screening

> Fuente: la tanda del 2026-10-22/23. Lo que funcionó y lo que no.
> **Fecha de relevancia: 2026-10-23.**

---

## 1. La regla del filtro de idioma

**El filtro de idioma se paga tarde.** Los dos cierres recientes (Staffy 20/10, Sol 21/10) llegaron
cuando el CV ya estaba armado, el screening hecho, y la prep de call lista: el cliente pidió "C1
conversacional" y se terminó el proceso. El mismo patrón, dos veces.

Por eso la **primera** pregunta de screening es el nivel de inglés conversacional, y va en el **primer
mensaje**. No como repasse, sino como información que Gonzo necesita antes de invertir un CV.

Y el corollary: la pregunta se hace **operacionalmente** ("¿con qué equipos se comunica el rol a
diario y en qué horario?"), no como "¿exigen C1?". Preguntar "¿el cliente exige C1?" es
auto-sabotaje: es el caso Staffy provocado a mano.

## 2. Cuándo NO preguntar el idioma

**En un puesto local.** Mercado Pago (Buenos Aires, híbrido) no lleva esa pregunta: no hay filtro que
descubrir, y preguntarla proyecta una duda que no hace falta.

La regla: **el idioma es filtro de elegibilidad en las agencies/nearshore (comunicación diaria con
clientes US) y es ruido de fondo en las empresas de producto con equipo propio.** Preguntá solo
cuando el rol realmente se comunica con US en el día a día.

## 3. Estructura del mensaje (130-200 palabras)

1. **Hook específico del rol** - una frase que demuestre que leíste la oferta. Mencioná el mecanismo
   del rol, no el título.
2. **El hecho que encaja** - un hecho real y verificable del corpus, conectado al hook.
3. **El diferenciador** - lo que no tiene el resto de los candidatos.
4. **Las preguntas de screening** - una o dos, con la del idioma al final.
5. **El paso siguiente** - "20 minutos" es concreto y fácil de aceptar.

### Qué NO va

- El nivel de inglés declarado. Se **pregunta**, no se anuncia. Declarar "Advanced" compra una
  conversación que se cae en la primera call.
- "N years of accessibility". No existe ese número. Se nombran los roles.
- Adjetivos de CV: *passionate*, *results-driven*, *proven track record*, *dynamic*.
- El "Success!" del parseo del CV ni el CV en sí. El mensaje es para **conseguir una conversación**,
  no para reemplazar el CV.
- Una URL larga de tracking.

### Longitud y límites de la plataforma

| Canal | Límite | Nota |
|---|---|---|
| LinkedIn DM (1° grado) | 800 caracteres | |
| LinkedIn DM (2° grado) | **bloqueado** | El botón dice "Message top connections". Usar la **invitación con nota** |
| LinkedIn invitación con nota | 300 caracteres, **ilimitado con Premium** | Fue lo que funcionó con RYZ (833 chars) |
| Email | sin límite | |

**El grado de conexión manda:** las cuatro recruiters de RYZ (Sonia Langone, Valentina Magni,
Valentina Tellechea, María Belén Giordano) eran 2° grado. Con Premium, la nota de la invitación no
tiene límite de caracteres, y ahí cabe el mensaje entero con las dos preguntas.

## 4. Las dos preguntas que hacen falta

Para un puesto de empresa de producto en LATAM:

1. **"¿Con qué equipos se comunica el rol en el día a día y en qué horario?"**
   Costo: bajo. Descarta de entrada lo que exige overlap full con US.
2. **"¿Qué nivel de inglés conversacional espera el rol?"**
   Costo: medio. Si es C1 y el nivel es B2, el proceso se frena ahí.

Una tercera, solo si el JD la pide explícitamente:

3. **"¿El puesto requiere certificación IAAP (CPACC, CPWA)?"**
   Costo: máximo. El corpus no tiene certificación IAAP, y se verifica en el registro público: un
   reclamo de más es un descargo de credibilidad completo. Si la exigen, se agradece y se sigue con
   otra vacante.

## 5. Angulos por tipo de empresa

### Startup studio / empresa de producto (RYZ Labs)

El gancho es el **método de trabajo con IA**, no el uso de IA:
- Sistema propio: sesiones por proyecto, memoria persistente, handoffs, subagentes, skills.
- Método de verificación: nada entra sin leerse, analizarse y verificarse.
- **Servidor MCP propio**: que un agente consult qué anuncia un lector de pantalla sobre un
  fragmento de HTML. Es respuesta directa a un requisito del JD y casi nadie lo tiene.
- 11 PRs mergeados en librerías de componentes de producción.

### Empresa de producto mediana (Mural)

El gancho es el **ciclo completo**: correr experimentos y entenderlos resultados, y ser dueño del
producto de punta a punta.
- Experimentos A/B reales en producción con Adobe Target, con variantes implementadas a mano.
- Ownership end-to-end: del problema ambiguo al producto facturado.
- **Gaps declarados**: no hay servicio de feature flags, ni pipeline de instrumentación. Decirlo en
  el mensaje convierte un gap en criterio. Un gap declarado se discute; un gap callado se descubre
  tarde, y tarde es como se cerraron los dos procesos.

### Empresa grande local (Mercado Pago)

El gancho es el **perfil híbrido diseño↔ingeniería**:
- Revisión de diseño antes de implementar, con requisitos técnicos y guía de código para las historias
  de UI.
- Design system propio: tokens semánticos, mapa token-componente, WCAG AA como criterio.
- Mismo dominio: un CRM para vendedores de Mercado Libre, cuando el rol es de Mercado Pago.

Acá el riesgo real no es el idioma: es que el puesto sea **más de diseño que de ingeniería**. Se
entiere antes de invertir.

## 6. Verificación antes de enviar

Todo mensaje sale con un chequeo de la lista de `docs/learnings/metodologia.md`:

- [ ] ¿Declara un nivel de inglés? (no debe)
- [ ] ¿Dice "N years of accessibility"? (no debe)
- [ ] ¿Cita un hecho que no está en `memory/career-facts.md`?
- [ ] ¿Tiene guiones largos (- o -) o caracteres de modelo (U+2011)? **No**: son huellas de
      salida de IA y hay un gate (`scripts/check_em_dash.py`).
- [ ] ¿Suena a folleto? (leelo en voz alta: si suena a CV, no va)
- [ ] ¿La pregunta de idioma va al final?
- [ ] ¿El largo está en el límite del canal?

El primer version de la cover letter de Mural pasó con 12 guiones no separables (U+2011) y un cierre
formulaico ("I look forward to contributing"). **Se detecta con `scripts/check_em_dash.py`.**
