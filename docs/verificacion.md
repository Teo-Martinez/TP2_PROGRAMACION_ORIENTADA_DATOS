# Verificación de la entrega

Se ejecutaron 66 pruebas con unittest, sin fallas, y pycodestyle sobre src,
scripts y tests, sin observaciones. La sintaxis se comprueba con la gramática
de Python 3.10; la ejecución de esta revisión utilizó Python 3.12.

Las pruebas incluyen:

- Regeneración determinista y equivalencia de las 500 fichas CSV/JSON.
- Lectores, estructura incorrecta, UTF-8, campos CSV excesivos y errores JSON.
- Extracción de nutrientes anidados, sin modificar datos originales.
- Conversión mg/g, kJ/kcal y masas de referencia de 30, 50 y 100 g.
- Validación, ausencias, cero, códigos con ceros iniciales y duplicados.
- Diagnóstico, cobertura, estadísticas y conciliación de registros.
- Búsquedas, categorías múltiples, ordenamiento estable y desconocidos al final.
- Ejecución de consola, exportaciones, repetición y protección de las entradas.
- Equivalencia de resultados con otra masa de referencia y JSON anidado.
- Muestra de nueve registros: dos aceptados y siete rechazados.

La cantidad de pruebas describe esta versión, no una garantía de ausencia de
errores para cualquier entrada imaginable. Las limitaciones funcionales y de
escritura están documentadas en propuesta.md y uso.md.
