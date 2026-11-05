#!/usr/bin/env python3
"""Chequeos de un cuento generado: fidelidad al outline y ritmo de la prosa.

Uso: cuento-check.py <outline.md> <cuento.md>

Salida: lineas de aviso por stderr-equivalente (stdout, el wrapper lo redirige).
Nunca falla el proceso por contenido: avisa. Solo exit 2 si faltan argumentos.

Por que existe (2026-11-05): muse redacto bien desde un outline de glm pero
renombro el elenco entero (Joaquin -> Lautaro, San Cayetano -> San Jorge,
Mar de Gloria -> Mar Azul II). Si el redactor renombra, el outline dejo de ser
la decision y la planificacion no vale nada. Y medido: los dos modelos escriben
parrafos de 113-155 palabras promedio, uno detras del otro, sin aire.
"""

import re
import sys

# Palabras capitalizadas que NO son nombres propios: vocabulario de consigna.
STOP = {
    "PREMISA", "PERSONAJE", "OFICIO", "EL", "LAS", "LOS", "ESCENAS", "LA",
    "VUELTA", "TUERCA", "ULTIMO", "ULTIMA", "OBJETO", "IMAGEN", "FINAL",
    "REGLAS", "RITMO", "VOZ", "NOMBRE", "RELOJ", "PROCEDIMIENTO", "EXTENSION",
    "ESQUELETO", "DESPUES", "CUENTO", "TRES", "CUATRO", "CINCO", "SEIS",
    "SIETE", "DOS", "UNA", "UNO", "ESCENA", "NOTA", "SUMA", "AJUSTAR",
    "PROTAGONISTA", "ANTECESOR",
}

# Nombres propios de una sola aparicion en el outline que pueden desaparecer
# legitimamente (toponimos de paso, referencias de una linea).
MIN_MENCIONES = 1

RITMO = {
    "palabras_min": 1900,
    "parrafos_min": 30,
    "parrafos_max": 70,
    "promedio_min": 35,
    "promedio_max": 90,
    "cortos_max_pct": 60,
    "oracion_max": 60,
}


def nombres_propios(texto):
    """Nombres propios de verdad: capitalizados en medio de una oracion.

    Un capitalizado despues de un punto, de dos puntos, de un bullet o al inicio
    de linea es una palabra cualquiera ("Descubre", "Toca", "Casa"). Solo cuenta
    lo que aparece capitalizado EN MEDIO de una oracion ya empezada: eso es lo
    que distingue "Renzo" de "Revisa".
    """
    cands = set()
    for m in re.finditer(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{2,}", texto):
        antes = texto[max(0, m.start() - 3):m.start()]
        # inicio de texto, de linea, de oracion, de bullet o de campo
        if (m.start() == 0
                or antes.endswith("\n")
                or antes.rstrip().endswith((".", ":", "?", "!", ";", "—", "-", "*", "|"))):
            continue
        w = m.group(0)
        if w.upper() in STOP:
            continue
        cands.add(w)
    return cands


def main():
    if len(sys.argv) < 3:
        print("uso: cuento-check.py <outline.md> <cuento.md>", file=sys.stderr)
        return 2

    outline = open(sys.argv[1], encoding="utf-8").read()
    cuento = open(sys.argv[2], encoding="utf-8").read()
    avisos = []

    # --- fidelidad: nombres propios del outline que no sobrevivieron ---
    cands = nombres_propios(outline)
    perdidos = sorted(w for w in cands if w not in cuento)
    if perdidos:
        pct = 100 * len(perdidos) // max(len(cands), 1)
        avisos.append(
            f"FIDELIDAD: {len(perdidos)}/{len(cands)} nombres del esqueleto no aparecen "
            f"en el cuento ({pct}%): {', '.join(perdidos[:10])}"
        )
        if pct >= 40:
            avisos.append(
                "FIDELIDAD: revisar si es renombre (muse cambio un nombre que el outline "
                "ya habia fijado) o invencion (el outline no nombro esa entidad y muse la "
                "bautizo: eso es correcto y se acepta). Comparar a mano."
            )

    # --- ritmo ---
    parrafos = [p.strip() for p in re.split(r"\n\s*\n", cuento) if p.strip()]
    if not parrafos:
        print("RITMO: el cuento no tiene parrafos", file=sys.stderr)
        return 0

    lens = [len(p.split()) for p in parrafos]
    palabras = sum(lens)
    promedio = palabras // len(parrafos)
    cortos = sum(1 for x in lens if x <= 25)
    pct_cortos = 100 * cortos // len(parrafos)

    if palabras < RITMO["palabras_min"]:
        avisos.append(f"EXTENSION: {palabras} palabras, por debajo de {RITMO['palabras_min']}")
    if len(parrafos) < RITMO["parrafos_min"]:
        avisos.append(
            f"RITMO: {len(parrafos)} parrafos, pocos (<{RITMO['parrafos_min']}): "
            "probablemente sean bloques sin aire"
        )
    if len(parrafos) > RITMO["parrafos_max"]:
        avisos.append(
            f"RITMO: {len(parrafos)} parrafos, demasiados (>{RITMO['parrafos_max']}): "
            "metralleta, no hay cuerpo"
        )
    if promedio < RITMO["promedio_min"]:
        avisos.append(f"RITMO: promedio {promedio} palabras/parrafo, demasiado corto")
    if promedio > RITMO["promedio_max"]:
        avisos.append(f"RITMO: promedio {promedio} palabras/parrafo, muro de texto")
    if pct_cortos > RITMO["cortos_max_pct"]:
        avisos.append(f"RITMO: {pct_cortos}% de parrafos cortos, ninguno golpea si son todos")

    # racha de parrafos muy cortos seguidos
    run = best = 0
    for x in lens:
        run = run + 1 if x <= 12 else 0
        best = max(best, run)
    if best > 3:
        avisos.append(f"RITMO: {best} parrafos muy cortos seguidos (max recomendado 3)")

    oraciones = [s for s in re.split(r"(?<=[.!?])\s+", cuento) if s.strip()]
    slens = [len(s.split()) for s in oraciones]
    largas = sum(1 for x in slens if x > RITMO["oracion_max"])
    if largas:
        avisos.append(
            f"SINTAXIS: {largas} oraciones de mas de {RITMO['oracion_max']} palabras "
            "(el error tipico de glm: encadenar con 'y')"
        )

    # --- tell: etiquetas emocionales ---
    TELL = re.compile(
        r"(sinti[oó] miedo|el p[aá]nico|la tensi[oó]n creci[oó]|estaba aterrorizad|"
        r"el terror lo|la invadi[oó]|sinti[oó] un escalofr[ií]o|se le hel[oó] la sangre)",
        re.I,
    )
    tells = TELL.findall(cuento)
    if tells:
        avisos.append(f"TELL: {len(tells)} etiquetas emocionales: {', '.join(set(tells))}")

    # --- reporte ---
    print(
        f"cuento.sh: metricas -> {palabras} palabras | {len(parrafos)} parrafos | "
        f"medio {promedio} | cortos {cortos} ({pct_cortos}%) | "
        f"largos {sum(1 for x in lens if x > 60)} | max oracion {max(slens)}",
        file=sys.stderr,
    )
    for a in avisos:
        print(f"cuento.sh: AVISO: {a}", file=sys.stderr)
    if not avisos:
        print("cuento.sh: sin avisos", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
