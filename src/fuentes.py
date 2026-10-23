"""Fuentes que entregan fichas como una lista de diccionarios planos."""

from abc import ABC, abstractmethod
import csv
import json
from pathlib import Path

from src.esquema import extraer_campos


class ErrorLectura(ValueError):
    """Archivo ilegible o estructura incompatible con el formato acordado."""


class FuenteDatos(ABC):
    """Compartir apertura y errores; delegar la lectura del formato."""

    def cargar(self, ruta):
        """Leer UTF-8, con o sin BOM, sin convertir cantidades ni códigos."""
        ruta = Path(ruta)
        try:
            with ruta.open(encoding="utf-8-sig", newline="") as archivo:
                registros = self._leer(archivo)
        except UnicodeDecodeError as error:
            raise ErrorLectura(
                f"El archivo '{ruta}' debe estar codificado en UTF-8."
            ) from error
        except OSError as error:
            raise ErrorLectura(
                f"No se pudo abrir o leer '{ruta}': {error.strerror}."
            ) from error
        except csv.Error as error:
            raise ErrorLectura(
                f"No se pudo interpretar el CSV '{ruta}': {error}. "
                "Revisá las comillas y el tamaño de sus campos."
            ) from error
        except json.JSONDecodeError as error:
            raise ErrorLectura(
                f"JSON inválido en '{ruta}', línea {error.lineno}, "
                f"columna {error.colno}: {error.msg}."
            ) from error
        if not registros:
            raise ErrorLectura("La entrada no contiene registros.")
        return registros

    @abstractmethod
    def _leer(self, archivo):
        """Entregar una lista de diccionarios desde el archivo abierto."""


class FuenteCSV(FuenteDatos):
    """Leer encabezado y filas CSV separados por coma, sin inferir tipos."""

    def _leer(self, archivo):
        lector = csv.DictReader(archivo, strict=True)
        encabezado = lector.fieldnames
        if not encabezado:
            raise ErrorLectura("El CSV está vacío o no tiene encabezado.")
        if any(not campo.strip() for campo in encabezado):
            raise ErrorLectura("El CSV tiene nombres de columnas vacíos.")
        if len(encabezado) != len(set(encabezado)):
            raise ErrorLectura("El CSV tiene nombres de columnas repetidos.")
        registros = []
        for numero, registro in enumerate(lector, start=1):
            if None in registro or None in registro.values():
                raise ErrorLectura(
                    f"Registro {numero}: cantidad de campos CSV incorrecta."
                )
            registros.append(registro)
        return registros


class FuenteJSON(FuenteDatos):
    """Leer una lista de fichas planas o con un objeto nutrientes."""

    def _leer(self, archivo):
        registros = json.load(archivo)
        if not isinstance(registros, list):
            raise ErrorLectura("El JSON debe contener una lista de fichas.")
        planos = []
        for numero, registro in enumerate(registros, start=1):
            if not isinstance(registro, dict):
                raise ErrorLectura(
                    f"Registro {numero}: la ficha JSON debe ser un objeto."
                )
            try:
                planos.append(extraer_campos(registro))
            except ValueError as error:
                raise ErrorLectura(f"Registro {numero}: {error}") from error
        return planos


def fuente_para(ruta):
    """Elegir el lector por extensión sin cambiar la lógica que lo utiliza."""
    extension = Path(ruta).suffix.casefold()
    if extension == ".csv":
        return FuenteCSV()
    if extension == ".json":
        return FuenteJSON()
    raise ErrorLectura("El archivo debe tener extensión .csv o .json.")
