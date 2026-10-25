# Modelo nutricional

`ProductoNutricional` reúne código, nombre, categorías, masa de referencia
`base_g` y los seis nutrientes como pares cantidad/unidad. Conserva la etiqueta
de origen y ofrece `obtener_nutriente(campo)` para compararla por 100 g.

Las unidades de comparación son kcal para energía, mg para sodio y g para el
resto. Se usan 4,184 kJ por kcal y 1000 mg por g. Después de convertir la unidad,
se calcula `cantidad / base_g * 100`. Así, 3 g por 50 g dan 6 g por 100 g.
Se admiten otras masas positivas y finitas, incluidos 30 g y 100 g.

Una cantidad desconocida se representa con `None`; cero es conocido. La unidad
debe ser compatible incluso cuando no hay una cantidad disponible. Se excluyen
booleanos, números negativos, NaN e infinito, y conversiones no finitas.
La base no puede ser cero. No se convierte volumen a masa ni sal a sodio.

Las cantidades no se redondean durante la conversión. La muestra redondea sus
etiquetas a seis decimales; puede haber pequeñas diferencias de coma flotante.
El modelo copia categorías y nutrientes para no alterar los datos recibidos.

Los controles de códigos, nombres, categorías y rangos por 100 g se incorporarán
en la preparación de fichas. Los lectores siguen conservando tipos originales;
el modelo recibe cantidades numéricas ya interpretadas.
