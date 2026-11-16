<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Spec técnico — reservas de aeronave compartida

## 1. Alcance

Una aeronave, dos socios, N invitados habilitados. Fuera: costos, pilotos, mantenimiento técnico, charter.

**Modelo de comercialización:** producto enlatado. Un despliegue por cliente, infraestructura a nombre del cliente. No es servicio por hora.

## 2. Stack

| Capa | Elección | Motivo |
|---|---|---|
| App | Next.js (App Router) + TypeScript | Stack propio, deploy trivial |
| Base + auth | Supabase (Postgres, Auth, RLS) | Los permisos se hacen cumplir en la base, no en el front |
| UI | Tailwind + shadcn/ui | Componentes propios, sin dependencia pesada |
| Fechas | date-fns | Sin librería de calendario |
| Mail | Resend | Transactional, barato |
| Hosting | Vercel | Con el cliente como titular |

**Descartados:** Google Sheets (historial editable), Google Calendar (sin aprobación ni saldo), Calendly (SaaS cerrado, sin concepto de recurso compartido), Cal.com / cal.diy (edición comunitaria, no producción), Booked Scheduler (plan B para piloto express; sin saldo por socio ni camino a charter).

## 3. Modelo de datos

```
accounts      (id, name, created_at)
members       (id, account_id, email, display_name, role, invited_by, status)
              role: 'owner' | 'guest'
reservations  (id, asset_id, kind, requested_by, approved_by, starts_at, ends_at,
               origin, destination, state, hold_expires_at, decided_at, notes)
              kind:  'flight' | 'maintenance'
              state: 'requested' | 'confirmed' | 'cancelled' | 'expired'
assets        (id, account_id, name, base_location, status)
events        (id, reservation_id, actor_id, action, payload jsonb, created_at)  -- append-only
```

Dos decisiones que sostienen todo:

**a) No hay tabla `assets` con una sola fila por capricho.** Es la fila que hoy tiene la aeronave y mañana tiene la flota. El charter agrega `quotes`, `rates` y un rol `customer`; no rediseña esto.

**b) El no-solapamiento lo garantiza Postgres, no la aplicación.**

```sql
ALTER TABLE reservations
  ADD CONSTRAINT no_overlap
  EXCLUDE USING gist (asset_id WITH =, tstzrange(starts_at, ends_at) WITH &&)
  WHERE (state IN ('requested', 'confirmed'));
```

Dos pestañas abiertas, un doble clic, dos pedidos simultáneos: la segunda escritura falla en la base. Es el único lugar donde esto puede garantizarse de verdad.

**c) El mantenimiento es una reserva con `kind = 'maintenance'`.** Entra en la misma restricción, bloquea igual, y se ve igual en el calendario. Un solo mecanismo, cero casos especiales.

**d) Saldo de uso** es una vista, no una tabla:

```sql
create view usage_by_member as
select requested_by, date_trunc('quarter', starts_at) as period,
       count(*) as reservations,
       sum(extract(epoch from (ends_at - starts_at)) / 86400)::numeric(10,1) as days
from reservations where state = 'confirmed' and kind = 'flight'
group by 1, 2;
```

Derivado, siempre cuadra, no se puede editar.

## 4. Permisos (RLS)

| Rol | Base | Ven |
|---|---|---|
| owner | todas las filas de su account | todo |
| guest | solo sus propias reservas | disponibilidad vía vista, sin notas ni destino ajenos |

Los invitados **no** leen `reservations` completa: leen `v_availability`, que expone rango, estado y nada más. Si alguien reescribe el front, la base sigue negando.

## 5. Flujo

1. **Socio reserva** → `confirmed` al instante. Sin aprobación.
2. **Invitado solicita** → `requested`, con `hold_expires_at = now() + 48h`. **Retiene el lugar** (entra en la restricción).
3. **Socio aprueba** → `confirmed`, `approved_by` seteado.
4. **Socio rechaza** → `cancelled` con motivo; el lugar se libera al instante.
5. **Cron cada 15 min** → `requested` vencidas pasan a `expired` y notifican.
6. **Socio bloquea mantenimiento** → reserva `kind='maintenance'`, `state='confirmed'`.

**Regla anti-acaparamiento:** máximo 2 solicitudes activas por invitado. Sin esto, un invitado puede sentarse 48 h sobre cada fin de semana.

## 6. Acceso cerrado

Sin registro público. El socio invita por link con token de un solo uso; login por magic link. Todas las respuestas con `X-Robots-Tag: noindex` y `robots.txt` cerrado.

## 7. Despliegue: un cliente, un deploy

**Single-tenant.** Cada cliente tiene su proyecto Supabase y su proyecto Vercel, a su nombre y con su tarjeta.

- **A favor:** aislamiento total de datos, y "los datos son suyos" es un argumento real cuando el cliente son dos socios.
- **En contra:** N deploys. Se resuelve con un repo único, migraciones versionadas y un script que despliega a todos. No es multi-tenant, y no hace falta que lo sea hasta que haya decenas.

**Soporte:** el cliente invita a un usuario con rol de socio cuando necesita ayuda, y lo revoca después. Sin código especial.

## 8. Costos por cliente

**Fase piloto (30 días): costo cero.** Free tier de Supabase y de Vercel, cuentas del desarrollador. Al cierre de la prueba, los proyectos se transfieren a nombre de la sociedad y pasan a planes pagos.

| Ítem | Aprox. |
|---|---|
| Vercel Pro | USD 20/mes — **Hobby es non-commercial**, se tolera solo durante el piloto sin cobro |
| Supabase Pro | USD 25/mes — **el plan free pausa el proyecto por inactividad** |
| Dominio | USD 12/año |

≈ **USD 45/mes** ya en manos del cliente. Verificar precios al cotizar.

**Mitigaciones del free tier:** el cron diario de vencimientos consulta la base, así que mantiene el proyecto de Supabase despierto; el vencimiento de las 48 h además se evalúa de forma perezosa al leer, para no depender de la granularidad del cron.

## 9. Riesgos

1. **Adopción.** El único riesgo que importa. Si los socios siguen usando WhatsApp, todo lo demás es decorado.
2. **Mantenimiento técnico sin responsable.** Es el hueco que el propio cliente tiene hoy; el sistema lo expone.
3. **Datos personales.** El responsable del tratamiento es el cliente; hay que decirlo en el contrato.
4. **N deploys.** Barato al principio, molesto a los veinte clientes.
