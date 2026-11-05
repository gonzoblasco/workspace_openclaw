#!/usr/bin/env python3
"""review-check.py - Chequeo mecanico de un borrador de resena de modelo.

No juzga la prosa. Ataja los errores que un script SI puede ver y que igual
se publican: cifras sin condicion, veredictos que faltan, citas ausentes,
adjetivos prohibidos, secciones de mas.

El que lee decide. Este script solo avisa: exit 0 siempre, salvo error de uso.

Uso:
    review-check.py <archivo.md> [--tipo articulo|informe] [--json]

Salida: una linea por hallazgo, con severidad.
Exit: 0 sin hallazgos o con hallazgos; 2 uso invalido.
"""
import json
import re
import sys

# Adjetivos que el estandar de la skill prohibe.
PROHIBIDAS = [
    "poderoso", "poderosa", "revolucionario", "revolucionaria",
    "impresionante", "vertiginoso", "vertiginosa",
]

# Muletillas que no aportan una decision.
MULETILLAS = [
    "en el vertiginoso mundo",
    "es importante destacar",
    "cabe destacar",
    "en conclusion",
    "en definitiva",
    "sin lugar a dudas",
]

# Una cifra con unidad de tiempo o volumen pero sin condicion cerca.
RE_CIFRA = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:s|seg|segundos|GB|MB|tokens|tok)\b")
RE_CONDICION = re.compile(r"contexto|ctx|num_ctx|tokens|declarad|medido|a \d|con \d", re.I)
RE_CITA = re.compile(r"[\"“][^\"”]{25,}[\"”]")
# Solo las cifras de TIEMPO exigen condicion de corrida. Las de capacidad o
# tamano son propiedades del artefacto, no del experimento.
RE_CIFRA_TIEMPO = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:s|seg|segundos|min)\b")
RE_FICHA = re.compile(r"par[aá]metros|millones|GB|MB|n[uú]cleos|disco|RAM|tokens declarados", re.I)


def sin_tildes(s):
    return s.translate(str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN"))


def tablas_ajenas(texto):
    """Filas de tabla cuya condicion esta en el TITULO que las precede.

    La tabla de "siete pruebas" no repite "contexto 32768" en cada fila: lo dice
    el titulo de la seccion. Una fila de tabla sin condicion en su cabecera pero
    bajo un titulo que la menciona esta condicionada igual.
    """
    dentro = set()
    contexto_ok = False
    bloque = []
    for linea in texto.splitlines():
        if linea.startswith("#"):
            contexto_ok = bool(RE_CONDICION.search(linea))
            bloque = []
        elif linea.lstrip().startswith("|"):
            bloque.append(linea)
        else:
            if bloque and contexto_ok:
                dentro.update(bloque)
            bloque = []
    if bloque and contexto_ok:
        dentro.update(bloque)
    return dentro


def filas_condicionadas(texto):
    """Lineas de tabla cuya cabecera menciona la condicion.

    Una cifra dentro de una tabla hereda la condicion de su encabezado: la
    columna se llama "Contexto" o la tabla entera esta bajo un titulo que la
    explica. Revisar fila por fila produce falsos positivos en masa: la primera
    version marco 14 de 16 hallazgos falsos sobre un articulo ya validado.
    """
    dentro = set()
    bloque = []

    def cerrar(b):
        if b and RE_CONDICION.search(" ".join(b[:2])):
            dentro.update(b)

    for linea in texto.splitlines():
        if linea.lstrip().startswith("|"):
            bloque.append(linea)
        else:
            cerrar(bloque)
            bloque = []
    cerrar(bloque)
    return dentro


def leer(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def secciones(texto):
    return [sin_tildes(l.strip("# ").strip()).lower()
            for l in texto.splitlines() if l.startswith("#")]


def chequear_articulo(texto):
    h = []
    secs = secciones(texto)

    if not RE_CITA.search(texto):
        h.append(("alta", "sin citas literales: el estandar pide al menos 3 citas del modelo entre comillas"))

    palabras = len(texto.split())
    if palabras < 900:
        h.append(("media", f"{palabras} palabras: el estandar pide 1.200-1.800"))

    for m in MULETILLAS:
        if m in texto.lower():
            h.append(("media", f'muletilla: "{m}"'))

    for p in PROHIBIDAS:
        if re.search(rf"\b{p}\b", texto, re.I):
            h.append(("alta", f'adjetivo prohibido: "{p}"'))

    # Las cifras sin condicion NO se chequean aca. Saber si "469 s" necesita decir
    # "a 163.840 tokens" depende del parrafo, del titulo de la tabla y de lo que el
    # lector ya leyo: tres intentos de heuristica dieron 14, 10 y 6 falsos positivos
    # sobre un articulo correcto. Un check que grita sobre originales valida se ignora,
    # y ese es peor que no tener check. Se revisa leyendo: regla 3 de la skill.

    # El subtitulo tiene que decir una tesis, no un topic. Heuristica grosera:
    # un subtitulo de mas de 14 palabras probablemente sea una frase, no un tema.
    subs = [l for l in texto.splitlines() if l.startswith("## ") and not l.startswith("###")]
    if subs:
        primero = subs[0].lstrip("# ").strip()
        if len(primero.split()) > 14:
            h.append(("baja", f"subtitulo muy largo, revisar si es tesis o tema: {primero[:60]}"))

    # Se acepta cualquiera de las variantes: el estandar fija el sentido, no el titulo.
    grupos = [("conclusion",), ("falla",), ("funciona", "brilla", "logra")]
    for grupo in grupos:
        if not any(any(v in sec for v in grupo) for sec in secs):
            h.append(("media", f"falta una seccion esperada: {grupo[0]}"))

    return h


def chequear_informe(texto):
    h = []
    primeras = [l for l in texto.splitlines() if l.strip()][:12]
    cabeza = "\n".join(primeras)

    if "Veredicto" not in cabeza and "veredicto" not in cabeza:
        h.append(("alta", "el veredicto no esta en las primeras lineas: el lector no puede decidir sin scrollear"))

    if not re.search(r"ADOPTAR|NO ADOPTAR|ESPECIALISTA", texto):
        h.append(("alta", "no hay veredicto de adopcion explicito (ADOPTAR / ADOPTAR COMO ESPECIALISTA / NO ADOPTAR)"))

    if not re.search(r"\bdeclarado\b", texto, re.I):
        h.append(("media", 'falta la columna o el termino "declarado": sin eso no se distingue medido de prometido'))

    if not re.search(r"\bmedido\b", texto, re.I):
        h.append(("media", 'falta la columna o el termino "medido"'))

    if "NO_VERIFICABLE" in texto and not re.search(r"NO_VERIFICABLE.{0,200}fallo|fallo.{0,200}NO_VERIFICABLE", texto, re.I | re.S):
        h.append(("baja", "NO_VERIFICABLE aparece sin declarar que cuenta como fallo"))

    for p in PROHIBIDAS:
        if re.search(rf"\b{p}\b", texto, re.I):
            h.append(("alta", f'adjetivo prohibido: "{p}"'))

    return h


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    path = argv[1]
    tipo = "articulo"
    as_json = False
    i = 2
    while i < len(argv):
        if argv[i] == "--tipo" and i + 1 < len(argv):
            tipo = argv[i + 1]
            i += 2
        elif argv[i] == "--json":
            as_json = True
            i += 1
        else:
            print(f"review-check.py: flag invalida: {argv[i]}", file=sys.stderr)
            return 2

    texto = leer(path)
    hallazgos = chequear_informe(texto) if tipo == "informe" else chequear_articulo(texto)

    if as_json:
        print(json.dumps([{"severidad": s, "hallazgo": h} for s, h in hallazgos],
                         ensure_ascii=False, indent=1))
        return 0

    if not hallazgos:
        print(f"review-check: {path} — sin hallazgos mecanicos")
        return 0

    orden = {"alta": 0, "media": 1, "baja": 2}
    for s, msg in sorted(hallazgos, key=lambda x: orden[x[0]]):
        print(f"[{s:5}] {msg}")
    print(f"\nreview-check: {len(hallazgos)} hallazgo(s) en {path}")
    print("Avisa, no bloquea: el que lee decide.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
