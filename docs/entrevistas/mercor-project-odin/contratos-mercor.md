<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Contratos de Mercor - lo que firmaste y lo que no

> Registro del proceso Odin (29/10/2026). Los PDF firmados viven en el mail / media store.
> Esto es el resumen de las cláusulas con consecuencia real, no el contrato.

## Los tres documentos

| Documento | Qué es | Firmado |
|---|---|---|
| Offer Letter | Puesto, tarifa base, at-will, background check | Sí (29/10) |
| Worker Agreement (TOW) | Contractor, IP, confidencialidad, arbitraje | Sí (29/10) |
| CIIAA | Cesión de invenciones | Sí (29/10) |

## Lo que te protege

**Excluded IP (§2(a)(iii) del CIIAA, §9(a)(iii) del TOW)** - tres condiciones **acumulativas**:
- (A) creado fuera de la relación y no en conexión con los Servicios;
- (B) en tiempo propio, sin equipos, instalaciones ni Confidencial de Mercor;
- (C) que no se relacione con el negocio de Mercor ni su research.

**SoporteML, Kanam OnWheels, kanam-pulse, kanam-fixer: quedan tuyos.** No hay cesión
general ni "todas las invenciones durante el término". Ese era el riesgo real y no está.

**§5(b) TOW** - podés irte con 7 días de aviso y te pagan lo trabajado. Mercor puede
cortar sin aviso. Asimétrico, pero normal.

**§8(b) TOW** - confidencialidad dura 2 años post-contrato, solo sobre info de Mercor.

**§4(e) CIIAA** - cláusula de reconversión: si un tribunal dice que sos empleado, el
acuerdo se lee como empleo. Protege el acuerdo, no te crea obligaciones nuevas.

## Lo que tiene filo

### §2(c) CIIAA - Background IP y la licencia perpetua
Define Background IP como lo que ya creaste **que se relacione de cualquier modo** con los
negocios, productos, servicios o I+D de Mercor. Si **lo usás o incorporás** en el trabajo,
Mercor obtiene licencia **perpetua, irrevocable, mundial, libre de regalías, sublicenciable**.

- **La licencia se dispara solo si lo usás** ("If in the course of the Relationship I use or
  incorporate...").
- Si no lo tocás, no aplica.
- Tenés obligación de **avisar por escrito** si incorporás Background IP.

**Regla operativa: en las grabaciones, entorno neutro. Nada de kanam-fixer, ni el AI
Engineering OS, ni repos propios.**

### §13 TOW - uso de IA
Prohíbe (i) meter Confidencial de Mercor en IA de terceros, y (ii) **usar IA o su output
en el desarrollo de Developed IP**.

- Autocompletado del editor (IntelliSense): no es IA.
- AI Assistant de JetBrains: zona gris, preguntar.
- Pedirle a Claude/GPT que escriba el código que grabás: prohibido.

### §2 Non-Circumvention (TOW)
No trabajar para **el cliente de Mercor** por fuera, mientras dure el contrato.
No prohíbe tener **varios proyectos de Mercor en paralelo**. Esa es la diferencia clave.

### §11 Non-Solicit (TOW)
2 años sin reclutar empleados o contractors de Mercor. Bajo impacto.

### §9(b)(iii) CIIAA - power of attorney
Si no cooperás con la cesión de Developed IP, Mercor firma por vos. Irrevocable.
Solo aplica a Developed IP.

### §14 Indemnification (TOW)
Si tu trabajo causa daño, lo pagás vos, incluidos honorarios. Con $40/h y sin seguro,
es un riesgo asimétrico pero de baja probabilidad.

## Lo que NO está en ningún documento

- **No hay cláusula de exclusividad.**
- **No hay non-compete.**
- **No hay prohibición de trabajar para otros.**
- **No hay obligación de dedicación exclusiva.**

§6 del TOW dice lo contrario: *"Worker shall have sole direction, control and
responsibility for determining the method, details and means of performing the Services."*

## Preguntas pendientes (por escrito, no por interpretación)

1. **Uso de IA en los workflows** - preguntar a `@Maven` en Slack, citando §13.
2. **El cap de 3 h** - no está en el Offer Letter ni en el TOW; vive en la plataforma.
   Confirmar si es por proyecto y si los caps de varios proyectos se suman.
3. **Background IP** - si en algún momento hay que usar algo propio, mandar el aviso
   por escrito que exige §2(c).

## Datos del contrato

- Puesto: **Odin - Writer**
- Tarifa base contractual: **$40/h** (Offer Letter).
- **Lo que realmente cobrás: el tier multiplica la base.** Fuente: mail de bienvenida a Odin.

| Tier | % de la base | Tarifa sobre $40 | Horas permitidas |
|---|---|---|---|
| Writer (inicial) | **137,5 %** | **$55/h** | hasta 60 h/semana |
| Super Writer | **187,5 %** | **$75/h** | hasta 80 h/semana |
| Throttled Writer | 100 % | $40/h | hasta 40 h/semana |

- **El "Weekly Cap: 3 hours" del certificado NO es un límite de trabajo.** El mail lo aclara
  textualmente: *"The 3-hour cap is not a time limit. It's only how many setup hours are paid
  hourly."* O sea: 3 h de **setup pagas**, y el trabajo real va aparte, hasta 60 h/semana.
- Bono de onboarding: **$150 al enviar la primera tarea + $250 al aprobarla** (= $400), más las
  3 h de setup. Efectivo ~$80-120/h en la primera tarea.
- Gate real: **aprobar la primera tarea** habilita más horas y más tareas.
- Jurisdicción: Delaware, arbitraje JAMS. Para montos chicos el arbitraje es prohibitivo, así que
  la protección real es no entrar en conflicto: guardar registros de horas y aprobaciones.
- Start date: 29/10/2026.

## Corrección de un cálculo previo (29/10)

En la primera lectura del certificado de contratista se concluyó que el cap era 3 h/semana y que
el techo eran ~$520/mes. **Era falso, y por un factor de ~10.** El certificado dice *"Hours
allowed: Up to 3 hrs/wk"* pero el mail de bienvenida reinterpreta ese número como horas de
**setup pago**, no como límite de trabajo. Con el tier de 137,5 % y 20 h/semana, el ingreso real
ronda **$4.400/mes**, y sube con el tier de Super Writer.
