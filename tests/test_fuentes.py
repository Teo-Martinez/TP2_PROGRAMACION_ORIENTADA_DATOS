"""Lectura normal, estructuras inválidas y errores comprensibles."""

import csv
import json
from pathlib import Path
import tempfile
import unittest

from src.fuentes import (
    ErrorLectura, FuenteCSV, FuenteDatos, FuenteJSON, fuente_para,
)


class TestFuentes(unittest.TestCase):
    """Probar ambos formatos con archivos aislados y con la muestra."""

    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.carpeta = Path(self.temporal.name)

    def escribir(self, nombre, texto):
        ruta = self.carpeta / nombre
        ruta.write_text(texto, encoding="utf-8")
        return ruta

    def test_fuente_abstracta_y_seleccion_por_extension(self):
        with self.assertRaises(TypeError):
            FuenteDatos()
        self.assertIsInstance(fuente_para("ejemplo.CSV"), FuenteCSV)
        self.assertIsInstance(fuente_para("ejemplo.JSON"), FuenteJSON)
        with self.assertRaisesRegex(ErrorLectura, "extensión"):
            fuente_para("ejemplo.txt")

    def test_muestra_conserva_esquema_codigos_y_ausencias(self):
        datos = Path(__file__).resolve().parents[1] / "data"
        csv_leido = FuenteCSV().cargar(datos / "productos.csv")
        json_leido = FuenteJSON().cargar(datos / "productos.json")
        self.assertEqual(len(csv_leido), 500)
        self.assertEqual(len(json_leido), 500)
        for fila_csv, fila_json in zip(csv_leido, json_leido):
            self.assertEqual(set(fila_csv), set(fila_json))
            self.assertEqual(fila_csv["codigo"], fila_json["codigo"])
            self.assertEqual(fila_csv["nombre"], fila_json["nombre"])
        self.assertEqual(csv_leido[0]["codigo"], "0000000000001")
        self.assertEqual(csv_leido[0]["azucares"], "")
        self.assertIsNone(json_leido[0]["azucares"])
        self.assertEqual(csv_leido[1]["sodio"], "0")
        self.assertEqual(json_leido[1]["sodio"], 0)

    def test_archivo_inexistente_y_directorio(self):
        for fuente in (FuenteCSV(), FuenteJSON()):
            for ruta in (self.carpeta / "ausente", self.carpeta):
                with self.subTest(fuente=type(fuente).__name__, ruta=ruta):
                    with self.assertRaisesRegex(ErrorLectura, "abrir o leer"):
                        fuente.cargar(ruta)

    def test_codificacion_invalida(self):
        ruta = self.carpeta / "incorrecto"
        ruta.write_bytes(b"\xff\xfe\x00")
        for fuente in (FuenteCSV(), FuenteJSON()):
            with self.assertRaisesRegex(ErrorLectura, "UTF-8"):
                fuente.cargar(ruta)

    def test_bom_utf8_en_ambos_formatos(self):
        csv_ruta = self.escribir("bom.csv", '\ufeffcodigo\n00000001\n')
        json_ruta = self.escribir(
            "bom.json", '\ufeff[{"codigo": "00000001"}]'
        )
        esperado = [{"codigo": "00000001"}]
        self.assertEqual(FuenteCSV().cargar(csv_ruta), esperado)
        self.assertEqual(FuenteJSON().cargar(json_ruta), esperado)

    def test_csv_encabezados_invalidos(self):
        casos = ("", "codigo,codigo\n1,2\n", "codigo, \n1,2\n")
        for contenido in casos:
            with self.subTest(contenido=contenido):
                ruta = self.escribir("encabezado.csv", contenido)
                with self.assertRaises(ErrorLectura):
                    FuenteCSV().cargar(ruta)

    def test_csv_filas_con_campos_de_mas_o_de_menos(self):
        for fila in ("00000001", "00000001,Producto,Extra"):
            ruta = self.escribir("fila.csv", f"codigo,nombre\n{fila}\n")
            with self.assertRaisesRegex(ErrorLectura, "Registro 1"):
                FuenteCSV().cargar(ruta)

    def test_csv_comillas_sin_cerrar(self):
        ruta = self.escribir("comillas.csv", 'codigo,nombre\n1,"Producto\n')
        with self.assertRaisesRegex(ErrorLectura, "interpretar el CSV"):
            FuenteCSV().cargar(ruta)

    def test_csv_campo_supera_limite_del_lector(self):
        campo = "x" * (csv.field_size_limit() + 1)
        ruta = self.escribir("largo.csv", f"codigo,nombre\n1,{campo}\n")
        with self.assertRaisesRegex(ErrorLectura, "tamaño de sus campos"):
            FuenteCSV().cargar(ruta)

    def test_json_malformado_informa_ubicacion(self):
        ruta = self.escribir("malformado.json", '[\n{"codigo": ]')
        with self.assertRaisesRegex(ErrorLectura, r"línea 2, columna"):
            FuenteJSON().cargar(ruta)

    def test_json_necesita_lista_de_objetos(self):
        for contenido in ('{"codigo": "00000001"}', '[42]', '[null]'):
            with self.subTest(contenido=contenido):
                ruta = self.escribir("estructura.json", contenido)
                with self.assertRaises(ErrorLectura):
                    FuenteJSON().cargar(ruta)

    def test_entradas_sin_registros(self):
        csv_ruta = self.escribir("vacio.csv", "codigo,nombre\n")
        json_ruta = self.escribir("vacio.json", "[]")
        for ruta in (csv_ruta, json_ruta):
            with self.assertRaisesRegex(ErrorLectura, "no contiene registros"):
                fuente_para(ruta).cargar(ruta)

    def test_la_lectura_no_altera_los_archivos(self):
        for nombre, contenido in (
            ("original.csv", "codigo,nombre\n00000001,Producto\n"),
            ("original.json", json.dumps([{"codigo": "00000001"}])),
        ):
            ruta = self.escribir(nombre, contenido)
            original = ruta.read_bytes()
            fuente_para(ruta).cargar(ruta)
            self.assertEqual(ruta.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
