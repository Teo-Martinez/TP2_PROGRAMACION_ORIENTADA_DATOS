"""Conversiones conocidas y propiedades del modelo nutricional."""

from copy import deepcopy
import unittest

from src.productos import ProductoNutricional


def nutrientes_ejemplo():
    """Etiqueta conocida por 50 g, con cantidades en distintas unidades."""
    return {
        "energia": (209.2, "kj"), "proteinas": (3000, "mg"),
        "carbohidratos": (10, "g"), "azucares": (None, "g"),
        "grasas": (2, "g"), "sodio": (0.025, "g"),
    }


class TestProductos(unittest.TestCase):
    """Verificar base, unidades, ausencias y cantidades incompatibles."""

    def crear(self, base=50, nutrientes=None):
        if nutrientes is None:
            nutrientes = nutrientes_ejemplo()
        return ProductoNutricional(
            "00000001", "Producto", ["prueba"], base, nutrientes
        )

    def test_conversiones_conocidas(self):
        producto = self.crear()
        self.assertAlmostEqual(producto.obtener_nutriente("energia"), 100)
        self.assertEqual(producto.obtener_nutriente("proteinas"), 6)
        self.assertEqual(producto.obtener_nutriente("sodio"), 50)
        self.assertEqual(producto.obtener_nutriente("grasas"), 4)

    def test_treinta_gramos_y_base_cien(self):
        valores = nutrientes_ejemplo()
        valores["proteinas"] = (3, "g")
        self.assertEqual(self.crear(30, valores).obtener_nutriente(
            "proteinas"), 10)
        self.assertEqual(self.crear(100, valores).obtener_nutriente(
            "proteinas"), 3)

    def test_misma_composicion_distinta_base(self):
        primero = nutrientes_ejemplo()
        segundo = {
            campo: (None if valor is None else valor * 2, unidad)
            for campo, (valor, unidad) in primero.items()
        }
        por_50 = self.crear(50, primero)
        por_100 = self.crear(100, segundo)
        for campo in primero:
            self.assertEqual(por_50.obtener_nutriente(campo),
                             por_100.obtener_nutriente(campo))

    def test_faltante_distinto_de_cero(self):
        valores = nutrientes_ejemplo()
        valores["sodio"] = (0, "mg")
        producto = self.crear(nutrientes=valores)
        self.assertIsNone(producto.obtener_nutriente("azucares"))
        self.assertEqual(producto.obtener_nutriente("sodio"), 0)

    def test_bases_invalidas(self):
        for base in (0, -1, float("nan"), float("inf"), True, "50"):
            with self.subTest(base=base):
                with self.assertRaises(ValueError):
                    self.crear(base)

    def test_cantidades_invalidas(self):
        for valor in (-1, float("inf"), float("nan"), True, "3"):
            valores = nutrientes_ejemplo()
            valores["proteinas"] = (valor, "g")
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    self.crear(nutrientes=valores)

    def test_nutrientes_y_unidades_invalidos(self):
        producto = self.crear()
        with self.assertRaises(ValueError):
            producto.obtener_nutriente("sal")
        for unidad in ("ml", "kcal", None):
            valores = nutrientes_ejemplo()
            valores["proteinas"] = (None, unidad)
            with self.assertRaises(ValueError):
                self.crear(nutrientes=valores)
        with self.assertRaises(ValueError):
            self.crear(nutrientes={})

    def test_no_modifica_la_etiqueta_original(self):
        valores = nutrientes_ejemplo()
        original = deepcopy(valores)
        categorias = ["prueba"]
        producto = ProductoNutricional(
            "00000001", "Producto", categorias, 50, valores
        )
        producto.obtener_nutriente("energia")
        categorias.append("otra")
        valores["grasas"] = (20, "g")
        self.assertEqual(producto.categorias, ["prueba"])
        self.assertEqual(producto.nutrientes, original)

    def test_conversion_de_entero_extremo_informa_value_error(self):
        valores = nutrientes_ejemplo()
        valores["sodio"] = (10 ** 308, "g")
        with self.assertRaisesRegex(ValueError, "fuera de rango"):
            self.crear(nutrientes=valores)


if __name__ == "__main__":
    unittest.main()
