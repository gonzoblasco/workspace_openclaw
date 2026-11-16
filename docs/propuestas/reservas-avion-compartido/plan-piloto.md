<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Plan del piloto — 30 días

## Fases

| # | Trabajo | Días |
|---|---|---|
| 1 | Repo, proyecto Supabase, proyecto Vercel, dominio | 0,5 |
| 2 | Auth por magic link, invitaciones con token, roles | 1 |
| 3 | Modelo de datos, RLS, restricción de no-solapamiento | 1 |
| 4 | Calendario semanal y creación de reserva | 2 |
| 5 | Aprobación, rechazo, vencimiento 48 h, log de eventos | 1 |
| 6 | Bloqueo de mantenimiento | 0,5 |
| 7 | Saldo de uso por socio | 0,5 |
| 8 | Notificaciones por email | 0,5 |
| 9 | QA en iPhone y Android, casos borde | 1 |
| 10 | Alta de los tres usuarios y arranque de la prueba | 0,5 |

**Total: 8,5 días de trabajo**, más los 30 días de uso real.

## Herramientas de desarrollo

MCP para acelerar, con una condición: los servidores MCP son código de terceros y se revisan y fijan de versión antes de correrlos. Los útiles acá: Supabase, Vercel y Playwright para probar el flujo en un browser real.

## Criterios de aceptación

1. Dos reservas simultáneas sobre el mismo rango: la segunda **falla**. Probado con dos pestañas.
2. Un invitado **no ve** notas ni destinos de otros invitados.
3. Una solicitud sin respuesta **vence sola** a las 48 h y el lugar queda libre.
4. El saldo de uso **cuadra** con las reservas confirmadas del trimestre.
5. Funciona en iPhone y Android, sin app que instalar.

## Qué necesitamos del cliente para arrancar

1. Nombre del avión y aeropuerto base (hangar de Federico).
2. Los tres usuarios iniciales, con email.
3. Confirmación de las reglas: sin límite entre socios, aprobación solo para invitados, 48 h para responder.

## Cómo se mide el piloto

| Métrica | Umbral |
|---|---|
| Reservas cruzadas | 0 |
| Consultas de disponibilidad por WhatsApp | 0 en la segunda quincena |
| Uso | ambos socios entran al menos 1 vez por semana |
| Aprobaciones | promedio menor a 24 h |

## Criterio de fracaso, escrito antes

Si al día 30 los socios siguen reservando por WhatsApp, el producto no resolvió el problema: se apaga, no se cobra mantenimiento y no queda deuda. Escribirlo antes es lo que evita discutirlo después.

## Después del piloto

Si las métricas se cumplen, el orden importa:

1. **Día 20:** se acuerda el mantenimiento — soporte y actualizaciones, alcance y precio.
2. **Día 30:** se transfiere la titularidad de los proyectos.

Al revés no. Entregar la titularidad antes de acordar el mantenimiento deja al cliente con sus datos, ya instalado, y sin motivo para pagar nada.

Después, se ofrece el mismo paquete a otra sociedad. El segundo cliente es el que dice si esto es un producto o un trabajo puntual.
