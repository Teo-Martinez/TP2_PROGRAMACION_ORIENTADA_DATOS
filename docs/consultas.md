# Consultas y comparación

El índice es un diccionario que conserva códigos de texto como claves.
`buscar_producto` devuelve la ficha o `None` si no existe. La selección admite
códigos o categoría; no se combinan ambos filtros. Un código solicitado que no
existe produce un error; los códigos repetidos en una selección se toman una
sola vez. Sin filtros se selecciona el catálogo completo.

Las categorías se comparan por coincidencia exacta después de quitar espacios
y unificar mayúsculas. Un producto coincide si cualquiera de sus categorías
coincide con la solicitada. Una categoría sin coincidencias genera una tabla
vacía. Sus frecuencias representan pertenencias y no categorías excluyentes.

`comparar_etiquetas` genera una fila por producto seleccionado. Las columnas
incluyen código, nombre y cantidades con unidad y base explícitas, por ejemplo
`proteinas_g_100g`. Se utiliza el método del modelo para convertir cada valor.
Una cantidad desconocida sigue siendo `None` hasta su presentación.

El ordenamiento usa cantidades convertidas. Los desconocidos quedan al final,
tanto en orden ascendente como descendente. A igual cantidad se conserva el
orden de selección; no se modifica la lista original.

La muestra permite comprobar que el primer producto tiene 10 g de proteínas
por 100 g y el segundo tiene 6 g, aunque su etiqueta informa 3 g por 50 g.
El primero tiene azúcar desconocido; el segundo tiene sodio cero conocido.
Estos resultados describen productos simulados.
