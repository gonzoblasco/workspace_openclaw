#!/usr/bin/env python3
"""Tests de la practica 01: los siete modelos.

Que prueban de verdad (no decorativo):
- que esten los SIETE modelos del BoK, por nombre, sin que falte ni sobre ninguno;
- que cada uno tenga fortaleza Y debilidad (el examen pregunta ambas);
- que el CLI devuelva 0 con un caso, 2 sin caso, y que --demo no requiera argumentos;
- que --modelo filtre a uno solo;
- que el texto del caso aparezca en la lectura (no se pierda la entrada).

Correr: python3 test_modelos.py
"""

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import modelos  # noqa: E402


class TestCatalogo(unittest.TestCase):
    def test_siete_modelos(self):
        self.assertEqual(len(modelos.MODELOS), 7)
        self.assertEqual(len(modelos.ORDEN), 7)

    def test_nombres_del_bok(self):
        esperados = {
            "medico",
            "social",
            "biopsicosocial",
            "economico",
            "funcional",
            "identidad",
            "caridad",
        }
        self.assertEqual(set(modelos.MODELOS), esperados)
        # el BoK los llama asi; el orden tambien importa para estudiarlos
        self.assertEqual(modelos.ORDEN, list(modelos.MODELOS))

    def test_cada_modelo_completo(self):
        campos = {"nombre", "lente", "pregunta", "ejemplo_pregunta", "fortaleza", "debilidad"}
        for clave, m in modelos.MODELOS.items():
            with self.subTest(modelo=clave):
                faltan = campos - set(m)
                self.assertFalse(faltan, f"a {clave} le falta {faltan}")
                for campo in campos:
                    self.assertTrue(str(m[campo]).strip(), f"{clave}.{campo} vacio")


class TestLectura(unittest.TestCase):
    def test_la_lectura_conserva_el_caso(self):
        bug = "un boton que solo responde al mouse"
        for clave in modelos.ORDEN:
            with self.subTest(modelo=clave):
                r = modelos.leer(bug, clave)
                self.assertIn(bug, r["lectura"])

    def test_la_lectura_cambia_por_modelo(self):
        bug = "un video sin subtitulos"
        lecturas = {modelos.leer(bug, k)["lente"] for k in modelos.ORDEN}
        # siete lentes distintas: si dos coinciden, el modelo esta duplicado
        self.assertEqual(len(lecturas), 7)

    def test_render_incluye_fortaleza_y_debilidad(self):
        texto = modelos.render(modelos.leer("x", "social"))
        self.assertIn("+", texto)
        self.assertIn("-", texto)


class TestCLI(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "modelos.py"), *args],
            capture_output=True,
            text=True,
        )

    def test_sin_argumentos_devuelve_2(self):
        r = self.run_cli()
        self.assertEqual(r.returncode, 2)

    def test_listar_devuelve_7_lineas(self):
        r = self.run_cli("--listar")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(len([l for l in r.stdout.splitlines() if l.strip()]), 7)

    def test_demo_funciona_sin_bug(self):
        r = self.run_cli("--demo")
        self.assertEqual(r.returncode, 0)
        self.assertIn("7 de 7 modelos", r.stdout)

    def test_modelo_unico(self):
        r = self.run_cli("un caso cualquiera", "--modelo", "caridad")
        self.assertEqual(r.returncode, 0)
        self.assertIn("1 de 7 modelos", r.stdout)
        self.assertNotIn("SOCIAL", r.stdout.upper().replace("SOCIAL ES", ""))

    def test_caso_propio(self):
        caso = "el menu colapsado atrapa el foco y no deja salir con teclado"
        r = self.run_cli(caso)
        self.assertEqual(r.returncode, 0)
        # el caso se refleja en las SIETE lecturas + 1 en el encabezado "Caso:".
        # Ojo: textwrap puede partir la frase en dos lineas, asi que se cuenta
        # sobre el texto con los saltos normalizados, no sobre el stdout crudo.
        plano = " ".join(r.stdout.split())
        self.assertEqual(plano.count(caso), 8)
        # y hay una lectura por modelo, no una sola repetida
        self.assertEqual(r.stdout.count("Lectura:"), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
