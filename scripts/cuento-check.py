#!/usr/bin/env python3
"""Chequeos de un cuento generado: fidelidad al outline, ritmo por genero y cabos sueltos.

Uso: cuento-check.py <outline.md> <cuento.md> [--genero terror|thriller-psicologico|...]

Salida: lineas de aviso por stderr. Nunca falla el proceso por contenido: avisa.
Solo exit 2 si faltan argumentos.

Por que existe (2026-11-05):
1. muse redacto bien desde un outline de glm pero invento nombres para lo que el
   esqueleto dejo sin nombrar. Eso esta BIEN (es lo que se le pide al redactor);
   lo que no puede pasar es que RENOMBRE algo que el outline ya fijo.
2. Los dos modelos escriben parrafos de 113-155 palabras promedio, uno detras del
   otro, sin aire. El ritmo se gobierna con numeros, no con adjetivos.
3. Los umbrales de ritmo NO son universales: un thriller judicial con 11 lineas de
   dialogo tiene promedio 26 palabras/parrafo y esta bien; el mismo numero en
   terror es metralleta. Medido el 2026-11-05 con el thriller de La Plata.
4. Un detalle plantado que no vuelve es un error, no una ambiguedad: el "residente
   joven que no le pidio documento" del thriller paso todas las metricas y es un
   cabo suelto. Se detecta por hapax (aparece una sola vez) y se reporta para
   revisar a mano, porque distinguir "sembrado para volver" de "olvidado" no lo
   hace un script.
"""

import re
import sys

STOP = {
    "PREMISA", "PERSONAJE", "OFICIO", "EL", "LAS", "LOS", "ESCENAS", "LA",
    "VUELTA", "TUERCA", "ULTIMO", "ULTIMA", "OBJETO", "IMAGEN", "FINAL",
    "REGLAS", "RITMO", "VOZ", "NOMBRE", "RELOJ", "PROCEDIMIENTO", "EXTENSION",
    "ESQUELETO", "DESPUES", "CUENTO", "TRES", "CUATRO", "CINCO", "SEIS",
    "SIETE", "DOS", "UNA", "UNO", "ESCENA", "NOTA", "SUMA", "AJUSTAR",
    "PROTAGONISTA", "ANTECESOR", "ADVERSARIO", "MECANISMO", "PRUEBA", "FALSA",
    "REVELACI", "COSTO", "IMAGEN", "TRASTORNO", "DIAGN", "TAMBI", "SIN",
}

# Perfiles de ritmo por genero. Los numeros salen de medir los cuentos del
# 2026-11-05, no de una regla general.
PERFILES = {
    "terror": {
        "parrafos_min": 30, "parrafos_max": 70,
        "promedio_min": 35, "promedio_max": 90,
        "cortos_max_pct": 60,
    },
    # El thriller psicologico se construye con intercambios y beats procedurales:
    # parrafos mas cortos y mas numerosos son el genero, no un defecto.
    "thriller-psicologico": {
        "parrafos_min": 40, "parrafos_max": 95,
        "promedio_min": 20, "promedio_max": 60,
        "cortos_max_pct": 70,
    },
    "highsmith": {
        "parrafos_min": 35, "parrafos_max": 85,
        "promedio_min": 25, "promedio_max": 70,
        "cortos_max_pct": 65,
    },
    "default": {
        "parrafos_min": 30, "parrafos_max": 80,
        "promedio_min": 25, "promedio_max": 80,
        "cortos_max_pct": 65,
    },
}

PALABRAS_MIN = 1900
ORACION_MAX = 60


def nombres_propios(texto):
    """Capitalizados en medio de una oracion: distingue 'Renzo' de 'Revisa'."""
    cands = set()
    for m in re.finditer(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{2,}", texto):
        antes = texto[max(0, m.start() - 3):m.start()]
        if (m.start() == 0
                or antes.endswith("\n")
                or antes.rstrip().endswith((".", ":", "?", "!", ";", "—", "-", "*", "|"))):
            continue
        w = m.group(0)
        if w.upper() in STOP:
            continue
        cands.add(w)
    return cands


def hapax_detalles(cuento):
    """Sustantivos concretos con modificador que aparecen UNA sola vez.

    No es un veredicto: es la lista de candidatos a cabo suelto. Un detalle
    sembrado para volver aparece dos veces como minimo (una al plantar, otra al
    cobrar). Si aparece una sola, o es decoracion o es un olvido - y decidir cual
    es trabajo de quien lee, no de un regex.
    """
    # frases sustantivas: 2-4 palabras con al menos un sustantivo "cosificable"
    cands = {}
    for m in re.finditer(r"\b([a-záéíóúñ]{4,})\s+(?:de\s+)?([a-záéíóúñ]{4,})\b", cuento):
        frase = m.group(0)
        cands[frase] = cands.get(frase, 0) + 1
    return cands


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    genero = "default"
    for i, a in enumerate(sys.argv):
        if a == "--genero" and i + 1 < len(sys.argv):
            genero = sys.argv[i + 1]
    if len(args) < 2:
        print("uso: cuento-check.py <outline.md> <cuento.md> [--genero X]", file=sys.stderr)
        return 2

    outline = open(args[0], encoding="utf-8").read()
    cuento = open(args[1], encoding="utf-8").read()
    perfil = PERFILES.get(genero, PERFILES["default"])
    avisos = []

    # --- fidelidad ---
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
                "FIDELIDAD: revisar a mano si es renombre (muse cambio un nombre que el "
                "outline ya habia fijado: error) o invencion (el outline no nombro esa "
                "entidad y muse la bautizo: correcto). El script no distingue las dos."
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

    if palabras < PALABRAS_MIN:
        avisos.append(f"EXTENSION: {palabras} palabras, por debajo de {PALABRAS_MIN}")
    if len(parrafos) < perfil["parrafos_min"]:
        avisos.append(
            f"RITMO: {len(parrafos)} parrafos, pocos para {genero} "
            f"(<{perfil['parrafos_min']}): bloques sin aire"
        )
    if len(parrafos) > perfil["parrafos_max"]:
        avisos.append(
            f"RITMO: {len(parrafos)} parrafos, demasiados para {genero} "
            f"(>{perfil['parrafos_max']}): metralleta, no hay cuerpo"
        )
    if promedio < perfil["promedio_min"]:
        avisos.append(
            f"RITMO: promedio {promedio} palabras/parrafo, corto para {genero} "
            f"(min {perfil['promedio_min']})"
        )
    if promedio > perfil["promedio_max"]:
        avisos.append(
            f"RITMO: promedio {promedio} palabras/parrafo, muro de texto para {genero} "
            f"(max {perfil['promedio_max']})"
        )
    if pct_cortos > perfil["cortos_max_pct"]:
        avisos.append(
            f"RITMO: {pct_cortos}% de parrafos cortos, ninguno golpea si son todos "
            f"(max {perfil['cortos_max_pct']}% para {genero})"
        )

    run = best = 0
    for x in lens:
        run = run + 1 if x <= 12 else 0
        best = max(best, run)
    if best > 3:
        avisos.append(f"RITMO: {best} parrafos muy cortos seguidos (max recomendado 3)")

    oraciones = [s for s in re.split(r"(?<=[.!?])\s+", cuento) if s.strip()]
    slens = [len(s.split()) for s in oraciones]
    largas = sum(1 for x in slens if x > ORACION_MAX)
    if largas:
        avisos.append(
            f"SINTAXIS: {largas} oraciones de mas de {ORACION_MAX} palabras "
            "(error tipico de glm: encadenar con 'y')"
        )

    # --- tell ---
    TELL = re.compile(
        r"(sinti[oó] miedo|el p[aá]nico|la tensi[oó]n creci[oó]|estaba aterrorizad|"
        r"el terror lo|la invadi[oó]|sinti[oó] un escalofr[ií]o|se le hel[oó] la sangre|"
        r"el miedo le|una ola de p[aá]nico)",
        re.I,
    )
    tells = TELL.findall(cuento)
    if tells:
        avisos.append(f"TELL: {len(tells)} etiquetas emocionales: {', '.join(set(tells))}")

    # --- cabos sueltos: personas introducidas una sola vez ---
    # Un objeto decorativo que aparece una vez no es un cabo suelto. Una PERSONA
    # introducida con un detalle y que nunca vuelve, si lo es: el lector la
    # recuerda y espera que vuelva. El caso medido: "un residente joven que no le
    # pidio documento" en el thriller de La Plata, que insinuaba una suplantacion
    # y el cuento nunca retomo.
    PERSONAS = (
        r"residente|m[eé]dico|enfermer[oa]|sereno|vigilante|abogad[oa]|defensor|"
        r"emplead[oa]|secretari[oa]|escriban[oa]|archivista|juez|jueza|perito|"
        r"vecin[oa]|portero|taxista|chofer|polic[ií]a|agente|testigo|paciente|"
        r"muchach[oa]|hombre|mujer|chico|chica|se[nñ]or|se[nñ]ora"
    )
    persona_re = re.compile(
        r"\b(?:un|una|el|la)\s+(" + PERSONAS + r")\s+([a-záéíóúñ]{4,})",
        re.I,
    )
    menciones = {}
    for m in persona_re.finditer(cuento):
        clave = f"{m.group(1).lower()} {m.group(2).lower()}"
        menciones[clave] = menciones.get(clave, 0) + 1
        # contar tambien el sustantivo solo, para no marcar a alguien que vuelve
        # con otro adjetivo o sin adjetivo
    sustantivos = {}
    for m in persona_re.finditer(cuento):
        sust = m.group(1).lower()
        sustantivos[sust] = sustantivos.get(sust, 0) + 1

    sueltos = []
    for clave, n in menciones.items():
        sust = clave.split(" ", 1)[0]
        if n == 1 and sustantivos.get(sust, 0) == 1:
            sueltos.append(clave)
    if sueltos:
        avisos.append(
            f"CABOS SUELTOS: personas presentadas una sola vez y nunca retomadas: "
            f"{', '.join(sorted(sueltos)[:6])}. Si alguna insinua algo (una suplantacion, "
            "un testigo), el lector espera que vuelva: o vuelve o sobra."
        )

    # --- fuga de vocabulario del outline a la prosa ---
    # El esqueleto tiene encabezados ("EL OBJETO", "EL MECANISMO", "LA PRUEBA FALSA",
    # "EL ADVERSARIO"). Si esa palabra aparece en el cuento como parte de una frase,
    # el redactor esta narrando con el metalenguaje del plan. Caso medido 2026-11-05:
    # "El objeto viajaba en el sobre".
    FUGA = re.compile(
        r"\b(el|la|los|las)\s+(objeto|mecanismo|adversario|prueba falsa|premisa|"
        r"vuelta de tuerca|imagen final|esqueleto|arco)\b",
        re.I,
    )
    fugas = [m.group(0) for m in FUGA.finditer(cuento)]
    if fugas:
        avisos.append(
            f"FUGA DE OUTLINE: el metalenguaje del plan aparece en la prosa "
            f"({', '.join(set(f.lower() for f in fugas))}). El redactor esta narrando "
            "con los nombres de las secciones, no con los de la historia."
        )

    # --- reporte ---
    print(
        f"cuento.sh: metricas ({genero}) -> {palabras} palabras | {len(parrafos)} parrafos | "
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
