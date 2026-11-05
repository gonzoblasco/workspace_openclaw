Bateria de evaluacion: modelo de CODIGO

Evaluado: {{modelo}}
Fecha: {{fecha}}

Corres siete pruebas, una por bloque. Cada bloque empieza con la linea "### id".
No sumes pruebas, no omitas ninguna, no avises que vas a empezar.

==================================================================
### p1_funcion_simple
Escribe una funcion Python `es_par(n)` que devuelva True si n es par.
==================================================================
### p2_explicacion
Explica en castellano rioplatense, en 4 lineas, que hace un context manager
en Python y cuando lo usarias. Directo, sin vueltas.
==================================================================
### p3_debug
Este codigo falla en el ultimo caso. Encontra el bug y escribi la version corregida.

```python
def suma_total(items):
    total = 0
    for i in items:
        total += i['precio'] * i['cantidad']
    return total

print(suma_total([{'precio': 10, 'cantidad': 2}]))   # 20 ok
print(suma_total([]))                                 # 0 ok
print(suma_total([{'precio': 5}]))                    # KeyError: 'cantidad'
```
==================================================================
### p4_refactor
Refactoriza esta funcion para que sea testeable (inyectar dependencia de
tiempo), sin cambiar su comportamiento exterior:

```python
import datetime, smtplib

def enviar_recordatorio(email):
    ahora = datetime.datetime.now()
    if ahora.hour < 18:
        return None
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail('bot@x.com', email, 'Recordatorio: cerra el dia')
    smtp.quit()
    return 'enviado'
```
==================================================================
### p5_complejo
Implementa `resolve_deps(packages)` que recibe un dict
{paquete: [dependencias]} y devuelve una lista con el orden de instalacion
valido (dependencias antes que el paquete). Si hay un ciclo, devuelve None.
Sin recursion (iterativo). O(n+m).
==================================================================
### p6_trampa
Tengo 3 servidores y quiero tolerar la caida de 1 sin perder datos.
Que consenso uso? Y por que NO deberia usar Raft en mi caso si solo tengo
3 servidores? Responde concreto.
==================================================================
### p7_local
Un usuario argentino me dice que el sistema "no le anda". Le pedi el log y
dice `ECONNREFUSED 127.0.0.1:5432`. Que le contesto, en 3 lineas, sin
tecnicismos innecesarios?
==================================================================
