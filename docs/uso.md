# Consola y salidas

Los comandos se ejecutan desde la raíz. `python -m src.main --help` describe
las opciones. En Windows se puede usar `py`.

Se puede seleccionar una categoría, varios códigos o listar categorías.
`--ordenar` acepta energia, proteinas, carbohidratos, azucares, grasas o sodio.
`--descendente` requiere `--ordenar`. Listar categorías no admite ordenamiento
nutricional ni escribe archivos; informa por stderr los rechazos encontrados.

Una comparación guarda cuatro archivos en la carpeta elegida con `--salida`:

- `comparacion.csv`: productos seleccionados y nutrientes por 100 g.
- `rechazos.csv`: número de registro, código y primer motivo de cada rechazo.
- `cambios.csv`: campo, valor original y normalizado de cada cambio aceptado.
- `diagnostico.json`: dimensiones, tipos, cobertura, estadísticas del catálogo
  completo, conteos, decisiones y SHA-256 del archivo de entrada.

Los archivos se reemplazan, sin acumular filas. La aplicación protege la entrada
si coincide con una ruta de salida. Una consulta inválida no modifica las salidas
anteriores. La escritura de los cuatro archivos no es una transacción atómica
frente a un fallo de disco; para conservar otra ejecución se usa otra carpeta.
La consola muestra dos decimales y los archivos conservan la precisión interna.

## Demostración con errores

```bash
python -m src.main --archivo data/demo_errores/productos_con_errores.csv --salida outputs/demo
```

La muestra tiene nueve registros: dos aceptados y siete rechazados. Incluye un
duplicado, un código inválido, una base cero, una cantidad negativa, proteínas
por encima de 100 g al convertir la base, azúcares mayores que carbohidratos y
una unidad incompatible. Existe un JSON equivalente. Los casos son inventados
a propósito y están separados de los 500 productos del catálogo principal.

## Códigos de salida

Una comparación válida, incluso sin coincidencias, devuelve 0. Si todas las
fichas se rechazan, se guardan los motivos y se devuelve 1. Los errores de
lectura o de la consulta se muestran como `Error: ...` y devuelven 1.
Argumentos que argparse no reconoce o combinaciones mutuamente excluyentes
devuelven 2. Un `csv.Error` se comunica sin mostrar un traceback técnico.
