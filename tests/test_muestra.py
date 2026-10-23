"""Verificar identidad, unidades, ausencias y reproducción de la muestra."""

from collections import Counter
import csv
import json
import math
from pathlib import Path
import re
import tempfile
import unittest

from scripts.crear_muestra import generar_productos, guardar_muestra


class TestMuestra(unittest.TestCase):
    """Comprobar los datos sin depender del futuro comparador."""

    def test_cantidad_esquema_y_codigos(self):
        productos = generar_productos()
        campos = {
            "codigo", "nombre", "categorias", "base_g", "energia",
            "energia_unidad", "proteinas", "proteinas_unidad",
            "carbohidratos", "carbohidratos_unidad", "azucares",
            "azucares_unidad", "grasas", "grasas_unidad", "sodio",
            "sodio_unidad",
        }
        self.assertEqual(len(productos), 500)
        self.assertEqual(len({p["codigo"] for p in productos}), 500)
        self.assertEqual(productos[0]["codigo"], "0000000000001")
        self.assertEqual(productos[-1]["codigo"], "0000000000500")
        for producto in productos:
            self.assertEqual(set(producto), campos)
            self.assertIsInstance(producto["codigo"], str)
            coincidencia = re.fullmatch(r"[0-9]{13}", producto["codigo"])
            self.assertIsNotNone(coincidencia)

    def test_categorias_y_bases_de_referencia(self):
        productos = generar_productos()
        categorias = Counter()
        for producto in productos:
            categorias.update(producto["categorias"].split("|"))
        self.assertEqual(categorias, {
            "cereales": 100, "lacteos": 100, "legumbres": 100,
            "snacks": 100, "untables": 100, "envasados": 500,
        })
        self.assertEqual(Counter(p["base_g"] for p in productos), {
            100: 167, 50: 167, 30: 166,
        })

    def test_ausencias_y_cero_conocido(self):
        productos = generar_productos()
        faltantes = sum(p["azucares"] is None for p in productos)
        self.assertEqual(faltantes, 72)
        self.assertIsNone(productos[0]["azucares"])
        self.assertEqual(productos[1]["sodio"], 0)
        self.assertIsNotNone(productos[1]["sodio"])
        for producto in productos:
            for campo in ("energia", "proteinas", "carbohidratos",
                          "azucares", "grasas", "sodio"):
                valor = producto[campo]
                if valor is not None:
                    self.assertTrue(math.isfinite(valor))
                    self.assertGreaterEqual(valor, 0)

    def test_cantidades_conocidas_por_masa_y_unidad(self):
        primero, segundo, tercero = generar_productos()[:3]
        self.assertEqual(primero["energia"], 320)
        self.assertEqual(primero["energia_unidad"], "kcal")
        self.assertEqual(primero["proteinas"], 10000)
        self.assertEqual(primero["proteinas_unidad"], "mg")
        self.assertEqual(segundo["base_g"], 50)
        self.assertAlmostEqual(segundo["energia"], 146.44)
        self.assertEqual(segundo["energia_unidad"], "kj")
        self.assertEqual(segundo["proteinas"], 3)
        self.assertEqual(segundo["proteinas_unidad"], "g")
        self.assertEqual(tercero["base_g"], 30)
        self.assertEqual(tercero["energia"], 33)

    def test_archivos_equivalentes_y_repetibles(self):
        with tempfile.TemporaryDirectory() as temporal:
            carpeta = Path(temporal)
            guardar_muestra(carpeta)
            csv_original = (carpeta / "productos.csv").read_bytes()
            json_original = (carpeta / "productos.json").read_bytes()
            with (carpeta / "productos.csv").open(
                encoding="utf-8", newline=""
            ) as archivo:
                filas_csv = list(csv.DictReader(archivo))
            filas_json = json.loads(json_original)
            self.assertEqual(filas_json, generar_productos())
            self.assertEqual(len(filas_csv), len(filas_json))
            for fila_csv, fila_json in zip(filas_csv, filas_json):
                for campo, valor in fila_json.items():
                    if valor is None:
                        self.assertEqual(fila_csv[campo], "")
                    elif isinstance(valor, (int, float)):
                        self.assertEqual(float(fila_csv[campo]), valor)
                    else:
                        self.assertEqual(fila_csv[campo], valor)
            guardar_muestra(carpeta)
            self.assertEqual(
                (carpeta / "productos.csv").read_bytes(), csv_original
            )
            self.assertEqual(
                (carpeta / "productos.json").read_bytes(), json_original
            )

    def test_archivos_versionados_corresponden_al_generador(self):
        datos = Path(__file__).resolve().parents[1] / "data"
        with tempfile.TemporaryDirectory() as temporal:
            guardar_muestra(temporal)
            for nombre in ("productos.csv", "productos.json"):
                self.assertEqual(
                    (datos / nombre).read_bytes(),
                    (Path(temporal) / nombre).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
