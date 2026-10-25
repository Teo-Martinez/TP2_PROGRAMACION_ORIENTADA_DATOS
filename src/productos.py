"""Ficha nutricional y conversión de cantidades a una base de 100 g."""

import math


UNIDADES = {
    "energia": "kcal", "proteinas": "g", "carbohidratos": "g",
    "azucares": "g", "grasas": "g", "sodio": "mg",
}


def validar_numero(valor, campo, positivo=False):
    """Exigir números finitos; excluir booleanos y cantidades negativas."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{campo}: se requiere una cantidad numérica.")
    try:
        finito = math.isfinite(valor)
    except OverflowError:
        finito = False
    if not finito or valor < 0 or (positivo and valor == 0):
        condicion = "positivo" if positivo else "no negativo"
        raise ValueError(f"{campo}: debe ser finito y {condicion}.")


class ProductoNutricional:
    """Conservar la etiqueta original y obtener cantidades comparables."""

    def __init__(self, codigo, nombre, categorias, base_g, nutrientes):
        validar_numero(base_g, "base_g", positivo=True)
        if set(nutrientes) != set(UNIDADES):
            raise ValueError("La ficha debe incluir los seis nutrientes.")
        self.codigo = codigo
        self.nombre = nombre
        self.categorias = list(categorias)
        self.base_g = base_g
        self.nutrientes = {}
        for campo, detalle in nutrientes.items():
            if not isinstance(detalle, (tuple, list)) or len(detalle) != 2:
                raise ValueError(f"{campo}: se requiere cantidad y unidad.")
            valor, unidad = detalle
            permitidas = {"kcal", "kj"} if campo == "energia" else {"g", "mg"}
            if not isinstance(unidad, str) or unidad not in permitidas:
                raise ValueError(f"{campo}: unidad incompatible.")
            if valor is not None:
                validar_numero(valor, campo)
            self.nutrientes[campo] = (valor, unidad)
        for campo in UNIDADES:
            self.obtener_nutriente(campo)

    def obtener_nutriente(self, campo):
        """Obtener kcal, g o mg por 100 g; devolver None si se desconoce."""
        if campo not in UNIDADES:
            raise ValueError(f"Nutriente no admitido: {campo}.")
        valor, unidad = self.nutrientes[campo]
        if valor is None:
            return None
        destino = UNIDADES[campo]
        if unidad != destino:
            if destino == "kcal":
                valor /= 4.184
            elif destino == "g":
                valor /= 1000
            else:
                valor *= 1000
        comparable = valor / self.base_g * 100
        validar_numero(comparable, campo)
        return comparable
