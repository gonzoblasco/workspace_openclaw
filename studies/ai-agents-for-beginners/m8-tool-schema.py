#!/usr/bin/env python3
"""M8 - Schema de una tool + handler + dispatcher.

Consigna: definir el schema de `search_flights(origin, destination, date,
max_price)` y escribir el handler + dispatcher.

Puntos del curso que este script demuestra:
  - Una tool tiene TRES partes: nombre, descripcion, parametros (00:53:05).
  - "The LLM never runs the tools itself" (00:54:23). El schema es lo que el
    modelo ve; el handler es TU codigo.
  - El loop: el modelo emite el tool call, tu codigo lo ejecuta, el resultado
    vuelve como mensaje `tool`, el modelo decide el siguiente paso.
  - La descripcion no es decoracion: es lo que el modelo lee para elegir la
    tool y para llenar los argumentos.

Corre offline: el handler tiene un dataset mock, no llama a ninguna API.
"""
import json
from datetime import date as date_cls

# --------------------------------------------------------------- 1. SCHEMA
# Esto es lo unico que el modelo ve. Si falta la descripcion de un parametro,
# el modelo adivina ese parametro.

SEARCH_FLIGHTS_SCHEMA = {
    "name": "search_flights",
    "description": (
        "Busca vuelos disponibles entre dos ciudades en una fecha. "
        "Devuelve opciones con precio en USD y escalas. "
        "Usala cuando el usuario pregunte por vuelos, tarifas o disponibilidad. "
        "NO la uses para hoteles ni autos."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "Codigo IATA de la ciudad de origen (ej. 'EZE').",
            },
            "destination": {
                "type": "string",
                "description": "Codigo IATA de la ciudad de destino (ej. 'MAD').",
            },
            "date": {
                "type": "string",
                "description": "Fecha de salida en formato YYYY-MM-DD.",
            },
            "max_price": {
                "type": "number",
                "description": "Precio maximo en USD. Omitilo si no hay tope.",
            },
        },
        "required": ["origin", "destination", "date"],
    },
}

# --------------------------------------------------------------- 2. HANDLER
# El dataset es mock a proposito: el ejercicio es el contrato, no la API real.

VUELOS = [
    {"id": "AR1130", "origin": "EZE", "destination": "MAD", "date": "2026-12-01",
     "price": 890, "stops": 0},
    {"id": "IB6842", "origin": "EZE", "destination": "MAD", "date": "2026-12-01",
     "price": 745, "stops": 1},
    {"id": "AR1132", "origin": "EZE", "destination": "MAD", "date": "2026-12-02",
     "price": 980, "stops": 0},
    {"id": "UX042", "origin": "EZE", "destination": "MAD", "date": "2026-12-01",
     "price": 1290, "stops": 0},
]


def search_flights(origin=None, destination=None, date=None, max_price=None):
    """Handler real. Valida, ejecuta y devuelve un dict serializable.

    Tres reglas que todo handler deberia cumplir:
      1. Valida los argumentos: el modelo puede mandar basura.
      2. No explota: devuelve un error estructurado, no una excepcion.
      3. Devuelve algo que quepa en un mensaje (JSON serializable).
    """
    errores = []
    if not origin:
        errores.append("origin es obligatorio")
    if not destination:
        errores.append("destination es obligatorio")
    if not date:
        errores.append("date es obligatorio")
    else:
        try:
            date_cls.fromisoformat(date)
        except ValueError:
            errores.append(f"date invalida: {date!r} (se espera YYYY-MM-DD)")
    if origin and len(origin) != 3:
        errores.append(f"origin debe ser IATA de 3 letras, recibi {origin!r}")
    if destination and len(destination) != 3:
        errores.append(f"destination debe ser IATA de 3 letras, recibi {destination!r}")
    # max_price negativo no es un tope, es un error del llamador. Sin esta
    # validacion el handler devolvia "ok, 0 resultados bajo USD -10", que
    # parece exito. Detectado en review.
    if max_price is not None:
        if not isinstance(max_price, (int, float)):
            errores.append(f"max_price debe ser numerico, recibi {max_price!r}")
        elif max_price < 0:
            errores.append(f"max_price no puede ser negativo, recibi {max_price}")

    if errores:
        return {"ok": False, "error": "; ".join(errores), "results": []}

    encontrados = [
        v for v in VUELOS
        if v["origin"] == origin.upper()
        and v["destination"] == destination.upper()
        and v["date"] == date
        and (max_price is None or v["price"] <= max_price)
    ]
    encontrados.sort(key=lambda v: v["price"])

    if not encontrados:
        return {"ok": True, "results": [],
                "nota": f"sin vuelos {origin}->{destination} el {date}"
                        + (f" bajo USD {max_price}" if max_price else "")}

    return {"ok": True, "count": len(encontrados), "results": encontrados}


# --------------------------------------------------------------- 3. DISPATCHER
# El dispatcher es la frontera de seguridad: traduce nombre -> funcion.

REGISTRY = {
    "search_flights": search_flights,
}


def dispatch(tool_name, arguments):
    """Ejecuta un tool call que vino del modelo.

    Esta funcion es la frontera: el modelo NO ejecuta nada. Solo propone un
    nombre y unos argumentos; aca se decide si ese nombre existe y se llama
    (o no) a la funcion.
    """
    fn = REGISTRY.get(tool_name)
    if fn is None:
        return {"ok": False, "error": f"tool desconocida: {tool_name!r}"}
    if not isinstance(arguments, dict):
        return {"ok": False, "error": "arguments debe ser un objeto"}
    try:
        return fn(**arguments)
    except TypeError as e:
        # Argumento que el schema no declara.
        return {"ok": False, "error": f"argumentos invalidos: {e}"}
    except Exception as e:
        # El handler nunca deberia tirar, pero si tira, no tumba el loop.
        return {"ok": False, "error": f"fallo el handler: {type(e).__name__}: {e}"}


# --------------------------------------------------------------- 4. LOOP
# Lo que haria el agente: el modelo propone, el codigo ejecuta, el resultado
# vuelve. Aca simulo las propuestas del modelo para probar el dispatcher.

TOOL_CALLS_SIMULADOS = [
    ("caso feliz", "search_flights",
     {"origin": "EZE", "destination": "MAD", "date": "2026-12-01"}),
    ("con tope de precio", "search_flights",
     {"origin": "EZE", "destination": "MAD", "date": "2026-12-01",
      "max_price": 800}),
    ("sin resultados", "search_flights",
     {"origin": "EZE", "destination": "MAD", "date": "2027-06-01"}),
    ("fecha invalida", "search_flights",
     {"origin": "EZE", "destination": "MAD", "date": "el mes que viene"}),
    ("falta un obligatorio", "search_flights",
     {"origin": "EZE", "date": "2026-12-01"}),
    ("tool inexistente", "book_hotel",
     {"city": "MAD"}),
    ("argumento no declarado", "search_flights",
     {"origin": "EZE", "destination": "MAD", "date": "2026-12-01",
      "clase": "business"}),
]


def main():
    print("=" * 68)
    print("SCHEMA QUE VE EL MODELO")
    print("=" * 68)
    print(f"  name:        {SEARCH_FLIGHTS_SCHEMA['name']}")
    print(f"  description: {SEARCH_FLIGHTS_SCHEMA['description'][:70]}...")
    print(f"  parametros:  {list(SEARCH_FLIGHTS_SCHEMA['parameters']['properties'])}")
    print(f"  requeridos:  {SEARCH_FLIGHTS_SCHEMA['parameters']['required']}")

    print()
    print("=" * 68)
    print("DISPATCHER: lo que pasa con cada tool call")
    print("=" * 68)
    for label, name, args in TOOL_CALLS_SIMULADOS:
        r = dispatch(name, args)
        if r.get("ok"):
            n = r.get("count", 0)
            resumen = f"ok, {n} vuelo(s)" if n else f"ok, 0 resultados ({r.get('nota','')})"
        else:
            resumen = f"ERROR: {r['error']}"
        print(f"  {label:24} -> {resumen}")

    print()
    print("=" * 68)
    print("El mensaje `tool` que vuelve al modelo (caso feliz)")
    print("=" * 68)
    r = dispatch("search_flights",
                 {"origin": "EZE", "destination": "MAD", "date": "2026-12-01"})
    print(json.dumps({"role": "tool", "content": json.dumps(r)}, indent=2)[:600])


if __name__ == "__main__":
    main()
