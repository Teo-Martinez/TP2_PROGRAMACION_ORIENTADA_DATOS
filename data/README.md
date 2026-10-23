# Datos simulados

Responsable del trabajo: Teo Martinez. Elaboración: 23/10/2026.
Procedimiento preparado con asistencia de IA para fines educativos.

## Procedencia, uso y limitaciones

Las 500 fichas son ficticias y se generan con `scripts/crear_muestra.py`.
No se descargan datos externos: no corresponde atribuir esta muestra a Open
Food Facts ni asignarle su licencia. No hay marcas, datos personales ni
mediciones de alimentos reales. El responsable autoriza reutilizar la muestra
en actividades educativas.

Su utilidad es verificar el programa con cantidades conocidas. La distribución
es artificial y no representa el mercado ni una población. No es una fuente
para recomendar dietas ni afirmar propiedades de productos comerciales.
Los códigos son identificadores ficticios, sin garantía de dígito verificador.

## Reproducción

Desde la raíz del repositorio, con Python 3.10 o posterior:

```bash
python scripts/crear_muestra.py
python -m unittest discover -s tests -v
```

En Windows se puede usar `py`. El generador reemplaza `productos.csv` y
`productos.json` en esta carpeta. No usa azar, red ni paquetes externos y
produce los mismos archivos en ejecuciones sucesivas. Se conserva la muestra
completa porque es pequeña. Todavía no se implementó la aplicación de consulta.

## Unidad de análisis y variables

Cada fila representa la etiqueta ficticia de un producto. Sus cantidades
corresponden a la masa indicada en `base_g`, que puede ser 30, 50 o 100 g.
Por ejemplo, 3 g de proteínas por 50 g equivalen a 6 g por 100 g.

| Campo | Tipo lógico | Significado y unidad |
|---|---|---|
| codigo | Texto | Identificador de 13 dígitos, con ceros iniciales |
| nombre | Texto | Nombre ficticio del producto |
| categorias | Texto | Categorías separadas por `\|`; no son excluyentes |
| base_g | Número | Masa de referencia de la etiqueta, en g |
| energia | Número o ausencia | Energía para `base_g`, en kcal o kJ |
| proteinas | Número o ausencia | Proteínas para `base_g`, en g o mg |
| carbohidratos | Número o ausencia | Carbohidratos para `base_g`, en g o mg |
| azucares | Número o ausencia | Azúcares para `base_g`, en g o mg |
| grasas | Número o ausencia | Grasas para `base_g`, en g o mg |
| sodio | Número o ausencia | Sodio para `base_g`, en g o mg; no es sal |
| Cada campo terminado en _unidad | Texto | Unidad de la cantidad correspondiente |

Hay 16 columnas en total. CSV usa UTF-8, encabezado y separador coma. JSON es
una lista de objetos planos. CSV expresa los valores como texto al leerlos;
JSON conserva números y `null`. Los lectores entregan listas de diccionarios
con los mismos campos. La conversión de tipos se implementará al preparar
los productos.

## Procedimiento y controles conocidos

Se recorren 100 rondas de cinco plantillas: cereales, lácteos, legumbres,
snacks y untables. Cada ronda aumenta los valores de referencia de 100 g por
un factor `1 + ronda / 1000`, empezando por ronda 0. Se alternan masas y
unidades, y se redondean las cantidades de la etiqueta a seis decimales.

- Cada familia tiene 100 fichas; todas pertenecen también a `envasados`.
- Hay 167 etiquetas por 100 g, 167 por 50 g y 166 por 30 g.
- Hay 250 energías en kcal y 250 en kJ.
- Los códigos van de `0000000000001` a `0000000000500`, como texto.
- En los códigos cuyo número deja resto 1 al dividir por 7, el azúcar es
  desconocido: 72 ausencias. Se escribe celda vacía en CSV y `null` en JSON.
- El producto `0000000000002` tiene sodio cero conocido. Cero y ausencia
  conservan significados diferentes.

Las plantillas de base son inventadas: no se exige que su energía coincida
exactamente con la suma de macronutrientes. No permiten conclusiones dietarias.
La conversión kJ/kcal utiliza 4,184 kJ por kcal; 1000 mg equivalen a 1 g.

Las pruebas comprueban cantidad, esquema, códigos, categorías, masas,
conversiones conocidas del generador, ausencias y equivalencia de los archivos.
Los lectores ya tienen pruebas con archivos deliberadamente incorrectos en
carpetas temporales. Los casos numéricos inválidos se añadirán junto con sus
reglas de validación.

## Ejemplo con nutrientes anidados

`ejemplo_anidado.json` conserva las dos primeras fichas del catálogo, pero
agrupa cada cantidad y unidad dentro de `nutrientes`. Se preparó a partir de
esas fichas para demostrar la adaptación de estructura; no agrega productos
al catálogo de 500. El generador regenera los dos archivos principales.
Las pruebas verifican que este ejemplo siga siendo equivalente a esas fichas.

Contrato de los lectores, formatos y errores: [docs/fuentes.md](../docs/fuentes.md).
