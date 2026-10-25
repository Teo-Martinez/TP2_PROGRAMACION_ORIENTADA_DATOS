# Guía de defensa individual

El objetivo es explicar el código y sus decisiones con ejemplos propios.

## Demostración breve

```bash
python -m src.main --codigos 0000000000001 0000000000002
python -m src.main --archivo data/ejemplo_anidado.json --salida outputs/anidado
python -m src.main --archivo data/demo_errores/productos_con_errores.csv --salida outputs/demo
python -m unittest discover -s tests -v
```

El primer producto tiene 10 g de proteínas por 100 g. El segundo informa 3 g
por 50 g: su comparación muestra 6 g por 100 g. También informa 146,44 kJ
por 50 g, que corresponden a 70 kcal por 100 g. El azúcar del primero es
desconocido y el sodio del segundo es cero conocido. Son datos simulados.

## Preguntas para preparar

- ¿Para quién sirve el catálogo y qué queda fuera de su alcance?
- ¿Cómo se generan los 500 productos y por qué no representan alimentos reales?
- ¿Qué representa una fila y por qué sus cantidades dependen de base_g?
- ¿Por qué el código se conserva como texto y qué comprueba la regex?
- ¿Qué comparten las fuentes y qué resuelve cada implementación?
- ¿Qué hace ProductoNutricional que no sería solo almacenar atributos?
- ¿Cómo se convierte 3000 mg por 50 g en 6 g por 100 g?
- ¿Por qué una ausencia no puede convertirse en cero para calcular una media?
- ¿Qué diferencia hay entre un campo ausente y un campo con valor null?
- ¿Qué ocurre con códigos duplicados y con una categoría sin coincidencias?
- ¿Cómo se relacionan entradas, válidos y rechazados en el diagnóstico?
- ¿Qué prueba detectaría que la conversión de bases dejó de funcionar?
- ¿Qué cambió en cada commit y qué asistencia se utilizó?

La defensa corresponde a la consigna de esta materia. Si se debe recuperar
la exposición del TP1 por nota inferior a 50, preparar también sus preguntas,
según las indicaciones de la cátedra.
