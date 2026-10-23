"""Campos del catálogo y adaptación de nutrientes anidados."""


NUTRIENTES = (
    "energia", "proteinas", "carbohidratos", "azucares", "grasas", "sodio"
)


def extraer_campos(registro):
    """Copiar una ficha plana o extraer nutrientes con valor y unidad."""
    plano = dict(registro)
    if "nutrientes" not in plano:
        return plano
    bloque = plano.pop("nutrientes")
    if not isinstance(bloque, dict):
        raise ValueError("El campo nutrientes debe ser un objeto.")
    for nombre in NUTRIENTES:
        if nombre in plano or f"{nombre}_unidad" in plano:
            raise ValueError("No mezcles nutrientes planos y anidados.")
    for nombre, detalle in bloque.items():
        if nombre not in NUTRIENTES:
            raise ValueError(f"Nutriente no admitido: {nombre}.")
        if not isinstance(detalle, dict):
            raise ValueError(f"{nombre}: se requiere un objeto valor/unidad.")
        if "valor" not in detalle or "unidad" not in detalle:
            raise ValueError(f"{nombre}: faltan las claves valor o unidad.")
        plano[nombre] = detalle["valor"]
        plano[f"{nombre}_unidad"] = detalle["unidad"]
    return plano
