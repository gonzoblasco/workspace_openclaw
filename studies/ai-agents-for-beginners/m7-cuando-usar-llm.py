#!/usr/bin/env python3
"""M7 - Traductor de fechas (codigo) + resumen de resenas (LLM).

Consigna: implementar un traductor de fechas y un resumen de reseñas en el
mismo script, usando codigo para lo deterministico y LLM solo para el juicio.

Regla del curso (00:46:08): "If the answer is always the same for the same
input, use code."

Que demuestra este script:
  - La fecha es 100% deterministica -> codigo. Un LLM aca es costo y riesgo.
  - El resumen de resenas requiere juicio (que destaca, que omite) -> LLM.
  - El LLM solo recibe lo que el codigo ya limpio, no la tarea entera.

Corre contra Ollama local. Si no esta disponible, cae a un resumen
extractivo por codigo para que el script no falle.
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta

OLLAMA = "http://127.0.0.1:11434/api/generate"
MODEL = "gemma4:12b-mlx"

# ---------------------------------------------------------------- CODIGO
# Decision 1: la fecha es deterministica. Codigo, no LLM.

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}
DIAS = {
    "lunes": 0, "martes": 1, "miercoles": 2, "miércoles": 2, "jueves": 3,
    "viernes": 4, "sabado": 5, "sábado": 5, "domingo": 6,
}


def parse_fecha(texto, hoy=None):
    """Traduce una fecha en lenguaje natural a ISO. Deterministico.

    Soporta: 'hoy', 'mañana', 'ayer', 'en N dias', 'el proximo lunes',
    '15 de marzo', '2026-11-16'. Cualquier otra cosa -> None (no adivina).
    """
    hoy = hoy or datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    t = texto.lower().strip()

    if t == "hoy":
        return hoy.date()
    if t in ("mañana", "manana"):
        return (hoy + timedelta(days=1)).date()
    if t == "ayer":
        return (hoy - timedelta(days=1)).date()

    m = re.fullmatch(r"en (\d+) d[íi]as?", t)
    if m:
        return (hoy + timedelta(days=int(m.group(1)))).date()

    # Anclado a los nombres de dias: un regex con (\w+) suelto matchea
    # cualquier palabra ("hola") y desperdicia el paso. Detectado en review.
    m = re.fullmatch(r"(?:el )?(?:pr[oó]ximo |proximo )?(%s)" % "|".join(DIAS), t)
    if m:
        objetivo = DIAS[m.group(1)]
        delta = (objetivo - hoy.weekday()) % 7
        return (hoy + timedelta(days=delta or 7)).date()

    m = re.fullmatch(r"(\d{1,2}) de (\w+)(?: de (\d{4}))?", t)
    if m and m.group(2) in MESES:
        anio = int(m.group(3)) if m.group(3) else hoy.year
        try:
            fecha = datetime(anio, MESES[m.group(2)], int(m.group(1))).date()
        except ValueError:
            # Fecha que no existe: '29 de febrero' en un año no bisiesto.
            # Devolver None es coherente con el contrato: si no puede, no adivina.
            return None
        # Sin año explicito, una fecha ya pasada se interpreta como el año
        # siguiente: '15 de marzo' dicho en noviembre es marzo proximo, no
        # marzo de hace ocho meses. Nadie agenda hacia atras.
        if not m.group(3) and fecha < hoy.date():
            try:
                fecha = fecha.replace(year=fecha.year + 1)
            except ValueError:
                # 29 de febrero corrido a un año no bisiesto.
                return None
        return fecha

    try:
        return datetime.strptime(t, "%Y-%m-%d").date()
    except ValueError:
        return None


# ---------------------------------------------------------------- LLM
# Decision 2: resumir resenas requiere juicio. LLM.

RESENAS = [
    "El producto llego rapido y funciona perfecto. 5 estrellas.",
    "Pesima experiencia: el envio tardo 3 semanas y la caja vino rota.",
    "Esta bien por el precio. Nada del otro mundo.",
    "La atencion al cliente me resolvio el problema en 10 minutos. Excelente.",
    "No lo recomiendo. Dejo de funcionar al mes y no me devolvieron el dinero.",
    "Me encanto el diseno, pero el manual no se entiende nada.",
    "Lo compre dos veces, la segunda para regalo. Nunca falla.",
    "Esperaba mas. Cumple, pero no sorprende.",
]


def clasificar(resena):
    """Clasificacion por senales. CODIGO, no LLM.

    Esta funcion existe por un hallazgo real: al pedirle al LLM 'cuantos
    estan a favor y cuantos en contra', conto 4/3 sobre 8 resenas (se
    comio una) y clasifico una mixta como positiva. Contar no es juicio:
    es aritmetica. La aritmetica va en codigo.
    """
    r = resena.lower()
    negativas = ("pesima", "no lo recomiendo", "dejo de funcionar", "rota",
                 "no me devolvieron", "tardo 3 semanas")
    positivas = ("perfecto", "excelente", "encanto", "nunca falla",
                 "resolvio el problema")
    tiene_neg = any(p in r for p in negativas)
    tiene_pos = any(p in r for p in positivas)
    if tiene_neg and not tiene_pos:
        return "en contra"
    if tiene_pos and not tiene_neg:
        return "a favor"
    return "mixta"


def conteo_por_codigo(resenas):
    """Conteo determinista. El LLM NUNCA hace esta cuenta."""
    cuenta = {"a favor": 0, "en contra": 0, "mixta": 0}
    detalle = []
    for r in resenas:
        c = clasificar(r)
        cuenta[c] += 1
        detalle.append(c)
    assert sum(cuenta.values()) == len(resenas), "el conteo tiene que cerrar"
    return cuenta, detalle


def resumen_llm(resenas, cuenta):
    prompt = (
        "Resumi estas resenas de producto en 3 lineas: cual es la queja mas "
        "repetida y que rescatan los que estan conformes. "
        "Los conteos YA estan calculados: no los recalcules ni los cambies. "
        "No inventes datos que no esten en las resenas.\n\n"
        f"Conteos (dato, no los toques): {cuenta}\n\n"
        + "\n".join(f"- {r}" for r in resenas)
    )
    body = json.dumps({
        "model": MODEL, "prompt": prompt, "stream": False, "think": False,
        "options": {"temperature": 0, "num_predict": 200},
    }).encode()
    req = urllib.request.Request(
        OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["response"].strip()


def resumen_fallback(resenas):
    """Si no hay LLM: extractivo por codigo. Peor, pero no bloquea.

    Reusa `conteo_por_codigo` en vez de repetir listas de senales: tener dos
    juegos de senales distintas daba conteos distintos para las mismas resenas.
    Detectado en review.
    """
    cuenta, _ = conteo_por_codigo(resenas)
    return (f"[fallback codigo] {len(resenas)} resenas: "
            f"{cuenta['a favor']} a favor, {cuenta['en contra']} en contra, "
            f"{cuenta['mixta']} mixtas.")


# ---------------------------------------------------------------- MAIN

def main():
    print("=" * 62)
    print("PARTE 1 - Traductor de fechas (CODIGO, sin LLM)")
    print("=" * 62)
    casos = ["hoy", "mañana", "ayer", "en 10 dias", "el proximo lunes",
             "15 de marzo", "2026-12-25", "el dia del juicio final"]
    for c in casos:
        r = parse_fecha(c, hoy=datetime(2026, 11, 16))
        print(f"  {c!r:28} -> {r if r else 'None (no adivina)'}")

    print()
    print("=" * 62)
    print("PARTE 2 - Resumen de resenas (CODIGO cuenta, LLM juzga)")
    print("=" * 62)
    cuenta, detalle = conteo_por_codigo(RESENAS)
    print(f"  conteo por codigo (determinista): {cuenta}")
    print(f"  total: {len(RESENAS)} resenas, cierra: {sum(cuenta.values()) == len(RESENAS)}")
    try:
        out = resumen_llm(RESENAS, cuenta)
        motor = "LLM"
    except Exception as e:
        out = resumen_fallback(RESENAS)
        motor = f"fallback ({type(e).__name__})"
    print(f"  juicio del {motor}:")
    for linea in out.splitlines():
        if linea.strip():
            print(f"    {linea}")


if __name__ == "__main__":
    main()
