"""Propiedades nutricionales del flujo completo con masas diferentes."""

import json
from pathlib import Path
import tempfile
import unittest

from scripts.crear_muestra import generar_productos
from src.consultas import comparar_etiquetas
from src.preparacion import preparar_productos
from tests.test_consola import correr


class TestPropiedades(unittest.TestCase):
    """Contrastar resultados equivalentes, sin alterar archivos originales."""

    def test_misma_etiqueta_en_dos_masas(self):
        ficha = generar_productos()[1]
        doble = dict(ficha, base_g=ficha["base_g"] * 2)
        for campo in ("energia", "proteinas", "carbohidratos",
                      "azucares", "grasas", "sodio"):
            if doble[campo] is not None:
                doble[campo] *= 2
        primero, _, _ = preparar_productos([ficha])
        segundo, _, _ = preparar_productos([doble])
        self.assertEqual(comparar_etiquetas(primero),
                         comparar_etiquetas(segundo))

    def test_exportacion_plana_y_anidada_equivalente(self):
        with tempfile.TemporaryDirectory() as temporal:
            salidas = []
            for nombre, archivo, opciones in (
                ("plano", "data/productos.json",
                 ["--codigos", "0000000000001", "0000000000002"]),
                ("anidado", "data/ejemplo_anidado.json", []),
            ):
                carpeta = Path(temporal) / nombre
                resultado = correr("--archivo", archivo, "--salida",
                                   str(carpeta), *opciones)
                self.assertEqual(resultado.returncode, 0, resultado.stderr)
                salidas.append((carpeta / "comparacion.csv").read_bytes())
            self.assertEqual(salidas[0], salidas[1])

    def test_diagnostico_describe_catalogo_completo(self):
        with tempfile.TemporaryDirectory() as temporal:
            resultado = correr("--salida", temporal, "--codigos",
                               "0000000000001")
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            ruta = Path(temporal) / "diagnostico.json"
            informe = json.loads(ruta.read_text(encoding="utf-8"))
            self.assertEqual(informe["seleccionados"], 1)
            resumen = informe["resumen_validos"]
            self.assertEqual(resumen["total_productos"], 500)
            self.assertEqual(informe["resumen_validos"]["nutrientes"][
                "azucares"]["desconocidos"], 72)


if __name__ == "__main__":
    unittest.main()
