<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Voz de Gonzo - Registro vivo (español)

Corpus de cómo Gonzo se expresa en español. Cada vez que edita un borrador mío, se agrega un caso acá. La skill `voz-gonzo` lee este archivo antes de redactar y actualiza las reglas cuando un patrón nuevo aparece.

**Alcance:** interacciones en español (LinkedIn, mails, mensajes directos, entrevistas, notas personales). **Fuera de alcance:** GitHub (issues, PRs, commits, READMEs) - ahí rige USER.md + AGENTS.md, en inglés.

**Estructura de cada caso:**
- Fecha y contexto (destinatario + objetivo).
- Mi borrador (extracto).
- Su edición final.
- Qué cambió y por qué.
- Patrón que refuerza o emerge.

---

## Casos

### 2026-09-11 - Respuesta a rechazo, OpenSistemas (Camila, LinkedIn)

**Contexto:** proceso cerrado con un "no" (avanzaron con otro candidato). Objetivo: agradecer el feedback, pedir reconsideración para un rol/esquema de entrada, adaptarse a lo que necesitan hoy.

**Mi borrador (extracto):** ofrecía "seguir en el radar para lo que venga", un rol "de otro alcance" a futuro, y cerraba con "Un abrazo grande".

**Su edición final:**

> Hola Camila, gracias por la respuesta y por la claridad. Entiendo la decisión, aunque no te voy a mentir: me hubiera gustado que fuera otra.
>
> Te agradezco cómo llevaste todo el proceso. Y te digo algo directo, porque prefiero ser claro: me interesó mucho el equipo y la empresa, y no me gustaría quedar afuera estando tan cerca. Si hoy no hay lugar para el rol que vimos, me gustaría que me consideren para otro puesto o esquema que necesiten cubrir ahora -un rol de otro nivel, contractor, part-time, o una entrada a prueba-, adaptándome a lo que busquen y con condiciones a conversar.
>
> Si me das una oportunidad, no te vas a arrepentir.
> 😊

**Qué cambió:**
- "a futuro" / "en el radar" -> **"ahora"**. Pide en presente. Si quiere algo, el texto lo pide ya.
- "proyecto" -> **"empresa"**. Amplía el alcance: no se cierra a un equipo ni a un rol puntual.
- Sacó "Estoy disponible para hablar cuando quieras, incluso esta semana" -> menos ansiedad, misma disponibilidad implícita.
- Cierre con **"Si me das una oportunidad, no te vas a arrepentir"** + emoji, sin despedida formal ("Un abrazo" afuera). Confianza con filo, no sumisión.
- Mantuvo "condiciones a conversar" - no puso número por escrito.

**Patrón que emerge:**
- Directo y honesto, incluso con la emoción ("no te voy a mentir", "no me gustaría quedar afuera estando tan cerca").
- Cálido pero sin adornos: sin epílogos decorativos, sin servilismo.
- Pide en presente y con alcance amplio. La flexibilidad se ofrece como posición, no como rebaja.
- La confianza cierra mejor que la cortesía.

---

## Reglas consolidadas

Estas son las que la skill aplica por defecto. Se actualizan cuando un caso nuevo las contradice.

1. **Presente, no futuro.** Si Gonzo quiere algo, el texto lo pide ahora. "En el radar" y "para lo que venga" son debilidad.
2. **Alcance amplio.** "Empresa" antes que "proyecto"; varios roles/esquemas antes que uno solo.
3. **Cálido sin adornos.** Sin "¡Gran pregunta!", sin cierres decorativos, sin servilismo. La calidez es precisión, no longitud.
4. **No exponer urgencia ni necesidad.** La urgencia propia debilita la posición. Se dice con disponibilidad, no con ansiedad.
5. **Sin números por escrito.** Ofrecer "condiciones a conversar". El número se negocia en la charla.
6. **Cerrar con confianza.** Frases con filo ("no te vas a arrepentir") están bien; la humildad excesiva, no.
7. **Honestidad emocional medida.** Reconocer el sentimiento ("me hubiera gustado que fuera otra") es válido y suena humano.
8. **Guion común (-) siempre.** Nunca em dash ni en dash. Validar con `scripts/check_em_dash.py`.

---

_Creado 2026-09-11. Última actualización: 2026-09-11._
