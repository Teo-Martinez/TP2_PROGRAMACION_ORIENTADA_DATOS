# Lectura de CSV y JSON

`FuenteDatos` es una clase abstracta con una operación pública `cargar(ruta)`.
Comparte la apertura del archivo, la codificación y los mensajes de error.
El método abstracto `_leer(archivo)` delega la interpretación del formato en
`FuenteCSV` y `FuenteJSON`. Esta herencia evita repetir controles comunes.

`fuente_para(ruta)` selecciona una implementación por extensión, sin distinguir
mayúsculas. Ambas entregan una lista no vacía de diccionarios planos.

CSV conserva cantidades como texto y JSON conserva sus tipos originales.
Todavía no se convierten cantidades, unidades ni masas de referencia: esas
responsabilidades pertenecen al modelo y a la preparación de datos.
Los códigos no se convierten a números. Ningún lector escribe en las entradas.

## Errores explícitos

`ErrorLectura` deriva de `ValueError` y contiene un mensaje comprensible.
Se informa un error ante archivos inexistentes, directorios, permisos o fallas
de lectura, codificación incompatible, CSV mal formado y JSON inválido.
Se admite UTF-8 con o sin marca inicial BOM en ambos formatos.

CSV necesita encabezados no vacíos y únicos, y el mismo número de campos en
cada fila. `strict=True` detecta, entre otros casos, comillas sin cerrar.
Un `csv.Error`, incluido un campo que supera el límite del lector, se convierte
en `ErrorLectura` con una indicación para revisar comillas y tamaño de campos.
No se cambia el límite global del módulo CSV. Los errores JSON incluyen su
línea y columna. Una entrada sin registros también produce un error explícito.

La validación del esquema completo, los rangos, los duplicados y los rechazos
por ficha se implementarán en la etapa de preparación. Un error estructural
de lectura detiene el archivo completo; no se omiten filas silenciosamente.

## JSON anidado

Una ficha puede incluir las cantidades y unidades como campos planos, o usar
un objeto `nutrientes`. Dentro de ese objeto, cada nutriente se representa con
un objeto que contiene `valor` y `unidad`. El archivo
`data/ejemplo_anidado.json` contiene dos fichas completas de demostración.

`extraer_campos`, en `src/esquema.py`, copia la ficha y adapta esa estructura
sin modificar el original. Se rechazan los nutrientes desconocidos, los
objetos mal formados y la mezcla de campos planos y anidados de nutrientes.
Un valor `null` se conserva como desconocido, y cero permanece como cero.
Un campo no proporcionado sigue ausente: el lector no inventa sus valores.
La preparación posterior comprobará que estén todos los campos obligatorios.

Esta adaptación implementa el esquema acordado del TP. Otras estructuras,
incluidas las de una API externa, requieren su propio adaptador.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Se prueban el contrato abstracto, los archivos normales, los errores de ambos
formatos, el límite de campos CSV, los códigos con ceros, las ausencias, el
cero conocido y la conservación de archivos originales. Las 500 fichas también
se adaptan a anidado y se contrastan con sus versiones planas.
