"""Adaptación de nutrientes anidados sin alterar la ficha original."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.crear_muestra import generar_productos
from src.esquema import NUTRIENTES, extraer_campos
from src.fuentes import ErrorLectura, FuenteJSON


def anidar(ficha):
    """Preparar un JSON equivalente para verificar el adaptador."""
    copia = dict(ficha)
    copia["nutrientes"] = {}
    for nombre in NUTRIENTES:
        copia["nutrientes"][nombre] = {
            "valor": copia.pop(nombre),
            "unidad": copia.pop(f"{nombre}_unidad"),
        }
    return copia


class TestEsquema(unittest.TestCase):
    """Contrastar fichas planas, anidadas e incompatibles."""

    def test_extraccion_equivalente_para_500_fichas(self):
        for ficha in generar_productos():
            with self.subTest(codigo=ficha["codigo"]):
                self.assertEqual(extraer_campos(anidar(ficha)), ficha)

    def test_no_modifica_la_entrada(self):
        for ficha in (generar_productos()[0], anidar(generar_productos()[0])):
            original = deepcopy(ficha)
            extraer_campos(ficha)
            self.assertEqual(ficha, original)

    def test_faltante_y_cero_se_conservan(self):
        primero, segundo = generar_productos()[:2]
        self.assertIsNone(extraer_campos(anidar(primero))["azucares"])
        self.assertEqual(extraer_campos(anidar(segundo))["sodio"], 0)

    def test_estructuras_invalidas(self):
        casos = (
            {"nutrientes": []},
            {"nutrientes": {"proteinas": 6}},
            {"nutrientes": {"proteinas": {"valor": 6}}},
            {"nutrientes": {"proteinas": {"unidad": "g"}}},
            {"nutrientes": {"inventado": {"valor": 1, "unidad": "g"}}},
            {"proteinas": 6, "nutrientes": {}},
            {"proteinas_unidad": "g", "nutrientes": {}},
        )
        for ficha in casos:
            with self.subTest(ficha=ficha):
                with self.assertRaises(ValueError):
                    extraer_campos(ficha)

    def test_lector_identifica_registro_anidado_incorrecto(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "anidado.json"
            ruta.write_text(
                '[{"codigo": "00000001"}, {"nutrientes": []}]',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ErrorLectura, "Registro 2"):
                FuenteJSON().cargar(ruta)

    def test_ejemplo_versionado_equivale_a_dos_fichas(self):
        datos = Path(__file__).resolve().parents[1] / "data"
        ruta = datos / "ejemplo_anidado.json"
        original = json.loads(ruta.read_text(encoding="utf-8"))
        self.assertIn("nutrientes", original[0])
        self.assertEqual(FuenteJSON().cargar(ruta), generar_productos()[:2])


if __name__ == "__main__":
    unittest.main()
