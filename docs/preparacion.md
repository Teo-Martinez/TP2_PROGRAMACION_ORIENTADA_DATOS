# Diagnóstico, validación y trazabilidad

La inspección describe la tabla adaptada al esquema común antes de convertir
cantidades: filas, columnas, tipos observados, campos ausentes, ejemplos y
frecuencias de categorías, bases y unidades. También cuenta ausencias y códigos
repetidos. No se altera la entrada.

La preparación exige los 16 campos del esquema. Una columna ausente es un error
estructural que detiene la entrada. Un valor inválido en una ficha completa se
registra como rechazo y permite procesar las demás fichas.

Reglas aplicadas:

1. Código de texto, con espacios externos removidos. `re.fullmatch` y el patrón
   `(?:[0-9]{8}|[0-9]{13})` comprueban ocho o trece dígitos ASCII. Se conservan
   ceros iniciales; no se verifica el dígito de control ni existencia comercial.
2. Nombre no vacío y categorías separadas por `|`. Se normalizan espacios y
   mayúsculas, se quitan categorías repetidas y se exige al menos una.
3. Cantidades con punto o coma decimal; no se admiten booleanos, negativos,
   NaN ni infinito. La base debe ser positiva y las unidades compatibles.
4. Ausencias: `null`, celda vacía y textos NA, N/A, null o None, sin distinguir
   mayúsculas. Se conservan como `None`. Las unidades siguen siendo necesarias.
5. Se convierten unidades y masa de referencia a 100 g antes de validar rangos:
   hasta 1000 kcal, 100 g por macronutriente y 100000 mg de sodio. Son límites
   técnicos, no recomendaciones nutricionales. Los extremos dentro de rango
   se conservan. Los azúcares no pueden superar los carbohidratos conocidos,
   con tolerancia de coma flotante de 1e-6 y la tolerancia relativa de isclose.
6. Se conserva la primera ficha válida por código y se rechazan duplicados
   posteriores. Una ficha inválida previa no bloquea otra válida del mismo código.

`preparar_productos` devuelve productos, rechazos y cambios. Cada rechazo tiene
número de registro, código y primer motivo. Los cambios conservan el valor
original y el equivalente normalizado por 100 g, también para `base_g`.
Los números de registro empiezan en 1, sin contar el encabezado CSV.

Las estadísticas usan el catálogo válido completo, valores convertidos y solo
cantidades conocidas. Incluyen cobertura, mínimo, máximo y media. Cero participa
en la media; una ausencia no se sustituye por cero. Sin valores conocidos, las
estadísticas son `None`; sin productos, la cobertura también es `None`.
Como las categorías no son excluyentes, sus conteos no se suman como productos.

En la muestra se esperan 500 válidos, cero rechazados y 72 azúcares desconocidos:
428 conocidos y cobertura de 85,6 %. La consola exporta este diagnóstico.
