#!/usr/bin/env python3
"""Practica 0.1 del CPACC: los siete modelos de discapacidad.

Que hace: recibe una descripcion de un problema de accesibilidad y devuelve
como se lo diria cada uno de los siete modelos del BoK (Domain One A).

Para que sirve: es el primer artefacto ejecutable del curso. El ejercicio del
Modulo 1.1 es "contar un bug desde los siete modelos"; esto lo convierte en una
herramienta que se puede mejorar, testear y despues reusar en reviews reales:
cuando alguien describe un defecto, el sesgo del modelo aparece en la forma de
nombrarlo, no en el contenido.

Uso:
    python3 modelos.py --listar
    python3 modelos.py "<descripcion del problema>" [--modelo medico]
    python3 modelos.py --demo

Fuente: BoK v4.0, Domain One A (docs/cpacc/cpacc-bok.pdf, pp. 4-8).
Cada modelo lleva su fortaleza y su debilidad, que es lo que el examen pregunta.
"""

from __future__ import annotations

import argparse
import sys
import textwrap

MODELOS = {
    "medico": {
        "nombre": "Medico",
        "lente": "El problema esta en la persona: cuerpo, condicion, deficit.",
        "pregunta": "Que le pasa a esta persona y como se trata?",
        "ejemplo_pregunta": "Necesita que le recetemos algo?",
        "fortaleza": "Atiende la fuente biologica real; hay condiciones que requieren manejo clinico.",
        "debilidad": "Ignora el entorno inaccesible y las actitudes. Culpa al cuerpo.",
    },
    "social": {
        "nombre": "Social",
        "lente": "El problema esta en el entorno y en la sociedad, no en la persona.",
        "pregunta": "Que barrera construimos nosotros y podemos desarmar?",
        "ejemplo_pregunta": "El formulario no tiene labels o el edificio solo tiene escaleras?",
        "fortaleza": "Muestra que las barreras no son inevitables: se disenan hacia afuera.",
        "debilidad": "Puede minimizar el aspecto corporal de la discapacidad.",
    },
    "biopsicosocial": {
        "nombre": "Biopsychosocial",
        "lente": "Interseccion de biologico, psicologico y social. Base del ICF de la OMS.",
        "pregunta": "Como se combinan la condicion, la psiquis y el contexto?",
        "ejemplo_pregunta": "La ansiedad suma a la barrera fisica?",
        "fortaleza": "El mas completo; modelo de base para rehabilitacion.",
        "debilidad": "Complejo de implementar; puede diluir las necesidades medicas.",
    },
    "economico": {
        "nombre": "Economico",
        "lente": "Costo: productividad, soporte, impacto fiscal. Base de las politicas de benefits.",
        "pregunta": "Cuanto cuesta, quien lo paga y cuanto valor se pierde?",
        "ejemplo_pregunta": "Cuanto factura la empresa que no puede usar nuestra plataforma?",
        "fortaleza": "Pone el problema en la conversacion del negocio.",
        "debilidad": "Crea una categoria legal de 'necesitado' que estigmatiza; excluye a quien no cruza el umbral.",
    },
    "funcional": {
        "nombre": "Soluciones funcionales",
        "lente": "Resolver la limitacion con producto o tecnologia. Es el lente del profesional de a11y.",
        "pregunta": "Que solucion tecnica elimina la limitacion funcional?",
        "ejemplo_pregunta": "Que componente accesible reemplaza esto?",
        "fortaleza": "Orientado a resultados y a casos reales; el que mas mueve la aguja dia a dia.",
        "debilidad": "Puede producir tecnologia innovadora pero inutil, o cara, que beneficia al innovador y no al usuario.",
    },
    "identidad": {
        "nombre": "Identidad social / afiliacion cultural",
        "lente": "Pertenencia a una comunidad con experiencia compartida (la comunidad Sorda es el caso testigo).",
        "pregunta": "Como vive esto la comunidad de la que la persona forma parte?",
        "ejemplo_pregunta": "La comunidad espera 'Sordo' con mayuscula, no 'persona con sordera'?",
        "fortaleza": "Acepta la discapacidad como orgullo y punto de union.",
        "debilidad": "La pertenencia puede volverse exclusion para quien no encaja con la expectativa del grupo.",
    },
    "caridad": {
        "nombre": "Caridad",
        "lente": "Ver a la persona como desafortunada que necesita ayuda externa.",
        "pregunta": "Que podemos darle a esta persona?",
        "ejemplo_pregunta": "Le hacemos una excepcion manual en vez de arreglar el sistema?",
        "fortaleza": "Puede movilizar tiempo y recursos cuando la necesidad es genuina.",
        "debilidad": "Condescendiente; empuja soluciones de corto plazo en vez de estructurales.",
    },
}

ORDEN = list(MODELOS)


def leer(bug: str, clave: str) -> dict:
    m = MODELOS[clave]
    return {
        "modelo": m["nombre"],
        "clave": clave,
        "lente": m["lente"],
        "lectura": f"{m['pregunta']} -> {bug.strip()}",
        "ejemplo_aplicado": m["ejemplo_pregunta"],
        "fortaleza": m["fortaleza"],
        "debilidad": m["debilidad"],
    }


def render(resultado: dict, ancho: int = 88) -> str:
    out = [
        f"=== {resultado['modelo'].upper()} ===",
        textwrap.fill(f"Lente: {resultado['lente']}", ancho),
        textwrap.fill(f"Lectura: {resultado['lectura']}", ancho),
        textwrap.fill(f"La pregunta que hace: {resultado['ejemplo_aplicado']}", ancho),
        textwrap.fill(f"+ {resultado['fortaleza']}", ancho),
        textwrap.fill(f"- {resultado['debilidad']}", ancho),
    ]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Los siete modelos de discapacidad aplicados a un caso.")
    p.add_argument("bug", nargs="?", help="Descripcion del problema de accesibilidad")
    p.add_argument("--modelo", choices=ORDEN, help="Ver solo un modelo")
    p.add_argument("--listar", action="store_true", help="Listar los siete modelos")
    p.add_argument("--demo", action="store_true", help="Correr con un caso de ejemplo")
    args = p.parse_args(argv)

    if args.listar:
        for i, k in enumerate(ORDEN, 1):
            print(f"{i}. {MODELOS[k]['nombre']:<42} {MODELOS[k]['lente']}")
        return 0

    bug = args.bug
    if args.demo and not bug:
        # Caso real y acotado: es el ejercicio del Modulo 1.2 en miniatura.
        bug = "un formulario de alta sin etiquetas asociadas: el lector de pantalla lee 'cuadro de texto' cuatro veces"

    if not bug:
        p.print_help()
        return 2

    claves = [args.modelo] if args.modelo else ORDEN
    print(f"\nCaso: {bug}\n")
    for i, k in enumerate(claves):
        if i:
            print()
        print(render(leer(bug, k)))
    print(f"\n({len(claves)} de 7 modelos. El examen pregunta fortalezas y debilidades de cada uno.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
