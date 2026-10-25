# Comparador de etiquetas nutricionales

Autor: Teo Martinez. TP2 de Programación Orientada a Datos, opción 9.

[Repositorio](https://github.com/Teo-Martinez/TP2_PROGRAMACION_ORIENTADA_DATOS)

Consulta y compara nutrientes por cada 100 g, a partir de 500 productos
simulados en CSV o JSON. Admite distintas masas de referencia y unidades.
Requiere Python 3.10 o posterior; no hay paquetes externos que instalar.

Abrí una terminal en la raíz del repositorio:

```bash
python -m src.main --listar-categorias
python -m src.main --codigos 0000000000001 0000000000002
python -m src.main --categoria cereales --ordenar proteinas --descendente
python -m src.main --archivo data/productos.json --categoria lacteos
python -m src.main --archivo data/ejemplo_anidado.json
```

En Windows podés usar `py` en lugar de `python`. Sin filtros compara todo el
catálogo; `--help` muestra las opciones. Cada comparación reemplaza cuatro
archivos en `outputs/`: `comparacion.csv`, `rechazos.csv`, `cambios.csv` y
`diagnostico.json`. Usá `--salida otra_carpeta` para conservar otra ejecución.
Los faltantes aparecen como "No disponible". Listar categorías no escribe
archivos y avisa si rechaza fichas. Los errores terminan con código distinto de 0.

Pruebas y regeneración de los datos:

```bash
python -m unittest discover -s tests -v
python scripts/crear_muestra.py
```

Alcance y etapas previstas: [docs/propuesta.md](docs/propuesta.md).
Datos, variables y limitaciones: [data/README.md](data/README.md).
Lectores y manejo de errores: [docs/fuentes.md](docs/fuentes.md).
Modelo y conversiones: [docs/modelo.md](docs/modelo.md).
Limpieza y diagnóstico: [docs/preparacion.md](docs/preparacion.md).
Selección y ordenamiento: [docs/consultas.md](docs/consultas.md).
Consola y demostración: [docs/uso.md](docs/uso.md).
Entrega e historial: [docs/entrega.md](docs/entrega.md).
Defensa: [docs/defensa.md](docs/defensa.md).
Verificación: [docs/verificacion.md](docs/verificacion.md).
