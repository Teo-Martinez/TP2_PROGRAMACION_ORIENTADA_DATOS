"""Generar 500 etiquetas ficticias equivalentes en CSV y JSON."""

import csv
import json
from pathlib import Path


NUTRIENTES = (
    "energia", "proteinas", "carbohidratos", "azucares", "grasas", "sodio"
)
BASES_G = (100, 50, 30)

# Los valores de cada plantilla corresponden a 100 g: energía en kcal,
# sodio en mg y los demás nutrientes en g. Son valores inventados.
FAMILIAS = (
    {
        "nombre": "Cereal", "categoria": "cereales", "energia": 320,
        "proteinas": 10, "carbohidratos": 60, "azucares": 8,
        "grasas": 5, "sodio": 120,
    },
    {
        "nombre": "Lácteo", "categoria": "lacteos", "energia": 70,
        "proteinas": 6, "carbohidratos": 8, "azucares": 8,
        "grasas": 1.5, "sodio": 45,
    },
    {
        "nombre": "Legumbre", "categoria": "legumbres", "energia": 110,
        "proteinas": 8, "carbohidratos": 15, "azucares": 1,
        "grasas": 0.5, "sodio": 20,
    },
    {
        "nombre": "Snack", "categoria": "snacks", "energia": 500,
        "proteinas": 6, "carbohidratos": 50, "azucares": 20,
        "grasas": 25, "sodio": 600,
    },
    {
        "nombre": "Untable", "categoria": "untables", "energia": 250,
        "proteinas": 4, "carbohidratos": 20, "azucares": 15,
        "grasas": 18, "sodio": 300,
    },
)


def elegir_unidad(nutriente, numero, posicion):
    """Alternar unidades compatibles para ejercitar sus conversiones."""
    if nutriente == "energia":
        return "kcal" if numero % 2 == 1 else "kj"
    if nutriente == "sodio":
        return "mg" if numero % 2 == 0 else "g"
    return "mg" if (numero + posicion) % 2 == 0 else "g"


def crear_ficha(numero, ronda, familia):
    """Expresar una plantilla en la masa y las unidades de la etiqueta."""
    base_g = BASES_G[(numero - 1) % len(BASES_G)]
    factor = 1 + ronda / 1000
    ficha = {
        "codigo": f"{numero:013d}",
        "nombre": f"{familia['nombre']} simulado {ronda + 1:03d}",
        "categorias": f"{familia['categoria']}|envasados",
        "base_g": base_g,
    }
    for posicion, nutriente in enumerate(NUTRIENTES):
        unidad = elegir_unidad(nutriente, numero, posicion)
        valor = familia[nutriente] * factor * base_g / 100
        if nutriente == "energia" and unidad == "kj":
            valor *= 4.184
        elif nutriente == "sodio" and unidad == "g":
            valor /= 1000
        elif nutriente not in {"energia", "sodio"} and unidad == "mg":
            valor *= 1000
        valor = round(valor, 6)
        if nutriente == "azucares" and numero % 7 == 1:
            valor = None
        if nutriente == "sodio" and numero == 2:
            valor = 0
        ficha[nutriente] = valor
        ficha[f"{nutriente}_unidad"] = unidad
    return ficha


def generar_productos():
    """Crear 100 rondas de cinco familias, sin utilizar números aleatorios."""
    productos = []
    for ronda in range(100):
        for familia in FAMILIAS:
            numero = len(productos) + 1
            productos.append(crear_ficha(numero, ronda, familia))
    return productos


def guardar_muestra(carpeta):
    """Reemplazar ambos archivos con las mismas fichas y orden estable."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    productos = generar_productos()
    with (carpeta / "productos.csv").open(
        "w", encoding="utf-8", newline=""
    ) as archivo:
        escritor = csv.DictWriter(
            archivo, fieldnames=list(productos[0]), lineterminator="\n"
        )
        escritor.writeheader()
        escritor.writerows(productos)
    contenido = json.dumps(
        productos, ensure_ascii=False, indent=2, allow_nan=False
    )
    (carpeta / "productos.json").write_text(
        contenido + "\n", encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    destino = Path(__file__).resolve().parents[1] / "data"
    guardar_muestra(destino)
    print("Se generaron 500 fichas en data/productos.csv "
          "y data/productos.json.")
