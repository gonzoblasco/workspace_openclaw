# Pipeline ABC - casos extremos

Tres casos, cada uno con un spec, un artefacto A debe producir, y un vector de ataque concreto
que B (revisión) y C (tests) deben cubrir. El objetivo del ABC no es "que A escriba bien":
es que la cadena completa **detecte y neutralice** lo que A NO va a detectar solo.

## Caso 1 - `resilient_cache` : TTL +Invalidación + concurrencia
**Spec**: caché LRU con TTL, con invalidación explícita y safe con reentrada (misma clave pedida dos veces).
**Trampa esperada**: A implementa `dict` + timestamp sin Newport de reentrada ni invalidación real.
**Lo que C debe testear**:
- TTL vencido con reloj inyectado (nada de `time.time()` hardcodeado).
- Invalidación durante un fetch en vuelo.
- Dos threads pidiendo la misma clave miss → **una sola** llamada upstream.
- `KeyboardInterrupt` a mitad de fetch no deja la clave " envenenada".

## Caso 2 - `date_range` : aritmética de fechas y DST
**Spec**: parser que genera rangos `[start, end)` desde fechas ISO, con fin de mes y años bisiestos.
**Trampa esperada**: A usa `timedelta(days=30)` para "un mes" y no maneja bisiesto ni fin de mes.
**Lo que C debe testear**:
- 29/02 en año bisiesto, 28/02 en no bisiesto, 31→30 días.
- Rango con `start == end` → vacío (no un día).
- DST: un día con 23 o 25 horas.
- Orden inverso `start > end` → error explícito, no lista vacía silenciosa.

## Caso 3 - `rate_limiter` : token bucket + reloj + overflow
**Spec**: limitador de tasa token-bucket con capacidad, refill por segundo y decisión de "permitir o no".
**Trampa esperada**: A usa contador simple en vez de bucket, y `refill` no es monótono.
**Lo que C debe testear**:
- Ráfaga: 1 token por request, capacidad N → exactamente N permitidos.
- Refill fraccionario (0.5 token/s, pedir a los 0.5s).
- Burst sobre capacidad → `False`, no excepción.
- Reloj que retrocede → no debe crear tokens infinitos.
