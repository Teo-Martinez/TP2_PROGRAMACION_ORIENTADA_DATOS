"""Validación, diagnóstico y trazabilidad con casos conocidos."""

from copy import deepcopy
from pathlib import Path
import unittest

from scripts.crear_muestra import generar_productos
from src.diagnostico import resumir_estructura, resumir_validos
from src.fuentes import FuenteCSV, FuenteJSON
from src.preparacion import diagnosticar, preparar_productos


class TestPreparacion(unittest.TestCase):
    """Verificar controles antes y después de convertir a 100 g."""

    def test_muestra_y_cobertura_conocidas(self):
        registros = generar_productos()
        diagnostico = diagnosticar(registros)
        productos, rechazos, cambios = preparar_productos(registros)
        self.assertEqual(len(productos), 500)
        self.assertEqual(rechazos, [])
        self.assertTrue(cambios)
        self.assertEqual(diagnostico["faltantes"]["azucares"], 72)
        self.assertEqual(diagnostico["estructura_entrada"]["filas"], 500)
        self.assertEqual(diagnostico["estructura_entrada"][
            "cantidad_columnas"], 16)
        resumen = resumir_validos(productos)
        azucar = resumen["nutrientes"]["azucares"]
        self.assertEqual(azucar["conocidos"], 428)
        self.assertAlmostEqual(azucar["cobertura_porcentaje"], 85.6)

    def test_conversion_y_trazabilidad_por_cincuenta_gramos(self):
        ficha = dict(generar_productos()[1], nombre=" Prueba ")
        productos, rechazos, cambios = preparar_productos([ficha])
        self.assertEqual(rechazos, [])
        producto = productos[0]
        self.assertEqual(producto.base_g, 50)
        self.assertEqual(producto.obtener_nutriente("proteinas"), 6)
        self.assertAlmostEqual(producto.obtener_nutriente("energia"), 70)
        self.assertEqual(producto.obtener_nutriente("sodio"), 0)
        indice = {c["campo"]: c for c in cambios}
        self.assertEqual(indice["base_g"]["original"], 50)
        self.assertEqual(indice["base_g"]["normalizado"], 100)
        self.assertEqual(indice["nombre"]["normalizado"], "Prueba")

    def test_invalidos_y_controles_sobre_cantidades_convertidas(self):
        casos = [
            {"codigo": "12"}, {"codigo": 12345678},
            {"codigo": "１２３４５６７８"}, {"nombre": ""},
            {"categorias": "|"}, {"base_g": 0}, {"base_g": -50},
            {"base_g": True}, {"base_g": "nan"},
            {"proteinas": -1}, {"proteinas": True},
            {"proteinas": "inf"}, {"grasas": 60, "base_g": 50},
            {"energia_unidad": "g"}, {"sodio_unidad": "ml"},
            {"azucares": 90, "azucares_unidad": "g"},
        ]
        for cambio in casos:
            with self.subTest(cambio=cambio):
                fila = dict(generar_productos()[0], **cambio)
                productos, rechazos, _ = preparar_productos([fila])
                self.assertEqual(productos, [])
                self.assertEqual(len(rechazos), 1)

    def test_duplicados_y_entrada_intacta(self):
        fila = generar_productos()[0]
        filas = [dict(fila, nombre=""), fila, dict(fila)]
        original = deepcopy(filas)
        productos, rechazos, _ = preparar_productos(filas)
        self.assertEqual(len(productos), 1)
        self.assertEqual(len(productos) + len(rechazos), len(filas))
        self.assertIn("duplicado", rechazos[1]["motivo"])
        self.assertEqual(filas, original)

    def test_categorias_y_ausencias_normalizadas(self):
        ficha = dict(generar_productos()[0],
                     categorias=" Cereales | ENVASADOS |cereales",
                     proteinas="10000,0", proteinas_unidad=" MG ",
                     azucares=" N/A ")
        productos, rechazos, _ = preparar_productos([ficha])
        self.assertEqual(rechazos, [])
        self.assertEqual(productos[0].categorias, ["cereales", "envasados"])
        self.assertEqual(productos[0].obtener_nutriente("proteinas"), 10)
        self.assertIsNone(productos[0].obtener_nutriente("azucares"))

    def test_csv_y_json_producen_las_mismas_cantidades(self):
        datos = Path(__file__).resolve().parents[1] / "data"
        resultados = []
        for fuente, nombre in ((FuenteCSV(), "productos.csv"),
                               (FuenteJSON(), "productos.json")):
            productos, rechazos, _ = preparar_productos(
                fuente.cargar(datos / nombre)
            )
            self.assertEqual(rechazos, [])
            resultados.append([
                (p.codigo, p.categorias, p.obtener_nutriente("energia"),
                 p.obtener_nutriente("proteinas")) for p in productos
            ])
        self.assertEqual(resultados[0], resultados[1])

    def test_esquema_y_entrada_vacia(self):
        for registros in ([], [{"codigo": "00000001"}]):
            with self.assertRaises(ValueError):
                preparar_productos(registros)

    def test_estadisticas_sin_imputar_y_catalogo_vacio(self):
        filas = generar_productos()[:2]
        filas[0]["sodio"] = 0
        filas[1]["sodio"] = None
        productos, rechazos, _ = preparar_productos(filas)
        self.assertEqual(rechazos, [])
        resumen = resumir_validos(productos)["nutrientes"]["sodio"]
        self.assertEqual(resumen["media"], 0)
        self.assertEqual(resumen["conocidos"], 1)
        self.assertEqual(resumen["cobertura_porcentaje"], 50)
        vacio = resumir_validos([])["nutrientes"]["sodio"]
        self.assertIsNone(vacio["media"])
        self.assertIsNone(vacio["cobertura_porcentaje"])

    def test_diagnostico_de_campos_ausentes_y_tipos(self):
        resumen = resumir_estructura([{"codigo": "00000001"},
                                     {"codigo": 12, "base_g": 50}])
        self.assertEqual(resumen["campos_ausentes"]["base_g"], 1)
        self.assertEqual(resumen["tipos_observados"]["codigo"],
                         {"str": 1, "int": 1})


if __name__ == "__main__":
    unittest.main()
