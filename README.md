# Comparador de etiquetas nutricionales

Autor: Teo Martinez. TP2 de Programación Orientada a Datos, opción 9.

Proyecto en desarrollo. Requiere Python 3.10 o posterior y su biblioteca
estándar, sin dependencias externas. Ya incluye el generador y 500 fichas;
el comparador se implementará en las próximas etapas.

El programa permitirá buscar productos por código, seleccionar categorías y
comparar nutrientes por cada 100 g a partir de archivos CSV y JSON. Incluirá
500 productos simulados y conservará los valores desconocidos como ausencias.

Desde la raíz del proyecto, para regenerar los datos y ejecutar las pruebas:

```bash
python scripts/crear_muestra.py
python -m unittest discover -s tests -v
```

En Windows podés usar `py` en lugar de `python`.

Alcance y etapas previstas: [docs/propuesta.md](docs/propuesta.md).
Datos, variables y limitaciones: [data/README.md](data/README.md).
