"""Demostración de rechazos y tratamiento del error CSV en la consola."""

import csv
import json
from pathlib import Path
import tempfile
import unittest

from tests.test_consola import correr


class TestErroresConsola(unittest.TestCase):
    """Probar errores reales sin modificar el catálogo de demostración."""

    def test_csv_error_se_informa_sin_traceback(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "largo.csv"
            campo = "x" * (csv.field_size_limit() + 1)
            ruta.write_text(f"codigo,nombre\n1,{campo}\n", encoding="utf-8")
            salida = Path(temporal) / "salidas"
            resultado = correr("--archivo", str(ruta), "--salida", str(salida))
            self.assertEqual(resultado.returncode, 1)
            self.assertIn("Error:", resultado.stderr)
            self.assertIn("tamaño de sus campos", resultado.stderr)
            self.assertNotIn("Traceback", resultado.stderr)
            self.assertFalse(salida.exists())

    def test_muestra_con_errores_concilia_conteos(self):
        for extension in ("csv", "json"):
            with self.subTest(extension=extension):
                with tempfile.TemporaryDirectory() as salida:
                    archivo = "data/demo_errores/productos_con_errores."
                    resultado = correr("--archivo", archivo + extension,
                                       "--salida", salida)
                    self.assertEqual(resultado.returncode, 0, resultado.stderr)
                    diagnostico = json.loads(
                        (Path(salida) / "diagnostico.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    self.assertEqual(diagnostico["total_entrada"], 9)
                    self.assertEqual(diagnostico["validos"], 2)
                    self.assertEqual(diagnostico["rechazados"], 7)


if __name__ == "__main__":
    unittest.main()
