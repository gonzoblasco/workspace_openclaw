<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Sistema de reservas del avión — propuesta para los socios

**Qué se pide:** aprobar las reglas de uso y una prueba de 30 días con una versión mínima, terminada en dos semanas.

---

## El problema

Hoy la reserva del avión vive en un grupo de WhatsApp y en la memoria de cada uno. Funciona porque son dos y se conocen. Deja de funcionar en tres situaciones concretas:

- Se suma un invitado y nadie recuerda quién lo autorizó.
- Se cruzan dos reservas y alguien se entera en la pista.
- Nadie sabe con números cuánto voló cada socio este trimestre.

Ninguna de las tres es un problema técnico. Es que no hay registro.

## Qué es

Un calendario del avión, desde el teléfono, donde cada reserva queda pedida, aprobada y visible para los dos. No reemplaza al piloto, ni al operador, ni al mantenimiento: reemplaza al grupo de WhatsApp.

## Qué hace

- Muestra la disponibilidad real del avión.
- Un socio reserva y queda confirmado en el acto.
- Un invitado ve los huecos y pide; un socio aprueba.
- El mantenimiento se bloquea como una reserva y no se puede pisar.
- Lleva el saldo de uso de cada socio: reservas y días por trimestre.
- Guarda el historial completo: quién reservó, quién aprobó, cuándo.

## Las reglas que se proponen

1. Los socios reservan y queda confirmado al instante. **Ninguno aprueba al otro.**
2. Un invitado ve la disponibilidad y pide. Un socio aprueba.
3. Si el socio no responde en **48 horas**, la solicitud vence y el lugar se libera. Mientras espera, el lugar queda retenido, para que nadie lo tome por atrás.
4. Un invitado puede tener como máximo **dos solicitudes abiertas** a la vez.
5. El mantenimiento lo bloquea un socio y no se puede pisar.
6. Todo cambio queda registrado: quién, qué, cuándo.

## Qué no hace

- No gestiona pilotos, combustible, costos ni tareas de mantenimiento.
- No reemplaza al operador ni a ningún sistema de vuelo.
- No deja que un invitado vuele sin que un socio lo apruebe.

## Por qué no alcanza con un Google Calendar

Un calendario compartido muestra la disponibilidad y deja anotar. Le faltan las cuatro cosas que resuelven el problema: la aprobación del invitado, el mantenimiento como bloqueo con responsable, el historial que no se puede editar, y el saldo de uso. Con un Google Calendar, el 70/30 sigue siendo invisible hasta que alguien se enoja.

## Quién puede entrar

Nadie de afuera. No hay registro público: los socios dan de alta a cada invitado con un link personal, y el sistema no aparece en buscadores. Un invitado ve la disponibilidad y sus propias reservas; no ve las notas ni los destinos de los demás.

## Qué cuesta

- **Durante la prueba, nada.** La versión mínima se desarrolla sin costo para la sociedad y corre en planes gratuitos de hosting y base de datos.
- **Al terminar la prueba**, los proyectos se transfieren a nombre de la sociedad. Desde ahí el costo es la infraestructura: alrededor de USD 45 por mes.
- El mantenimiento y las mejoras se acuerdan aparte.
- No hay costo por usuario ni por reserva.

## Cómo medimos si sirvió

- Cero reservas cruzadas.
- Cero consultas de disponibilidad por WhatsApp.
- Tiempo promedio de aprobación de un invitado, menor a 24 horas.
- Los dos socios entran al menos una vez por semana.
- El saldo de uso de los dos, disponible a un clic.

## Propuesta de arranque

Versión mínima en dos semanas: un avión, dos socios, invitados. Treinta días de uso real con los invitados de siempre. Si las métricas se cumplen, se mantiene y se amplía: los proyectos pasan a nombre de la sociedad, con sus cuentas y sus datos. Si no, se apaga y no queda deuda.
