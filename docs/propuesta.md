# Propuesta y alcance inicial

Autor del trabajo: Teo Martinez.

## Problema, usuario y resultado

Una persona que compara etiquetas necesita localizar productos y expresar sus
nutrientes en unidades y bases equivalentes. Un valor desconocido no equivale
a cero y no debe presentarse como tal.

Se propone una aplicación de consola que lea un catálogo CSV o JSON, busque
códigos, seleccione una categoría o varios productos y exporte una comparación
por cada 100 gramos. Un producto podrá pertenecer a varias categorías.

Preguntas previstas:

1. ¿Qué nutrientes tiene el producto identificado por un código?
2. ¿Cómo se comparan productos con distintas unidades o masas de referencia?
3. ¿Qué productos de una categoría tienen información disponible o faltante?

## Datos previstos

Se generarán 500 fichas ficticias mediante un procedimiento determinista, en
CSV y JSON equivalentes. Las simulaciones están admitidas por la consigna.
Se documentarán el procedimiento, las variables, las condiciones de uso y sus
limitaciones. No se utilizarán marcas ni mediciones nutricionales reales.

Cada fila representará una ficha de producto. Se conservarán los códigos como
texto. Campos previstos: código, nombre, categorías, masa de referencia en g,
energía, proteínas, carbohidratos, azúcares, grasas, sodio y sus unidades.
La muestra incluirá ausencias, ceros, unidades mixtas y distintas masas de
referencia para ejercitar las conversiones. Los casos deliberadamente inválidos
se prepararán por separado para pruebas y demostración.

## Decisiones funcionales previstas

- Admitir masas de referencia positivas y finitas, por ejemplo 30, 50 o 100 g.
  Convertir cada cantidad con la fórmula cantidad * 100 / masa de referencia.
- Convertir energía entre kJ y kcal, y masas de nutrientes entre g y mg.
- Aplicar controles de rango sobre las cantidades convertidas por cada 100 g.
- Distinguir ausencias de ceros, sin imputar cantidades desconocidas.
- Validar códigos de 8 o 13 dígitos ASCII con una expresión regular. Ese control
  no comprobará el dígito verificador ni la existencia comercial del producto.
- Leer JSON con nutrientes planos o anidados, con un esquema documentado.
- Registrar normalizaciones y rechazos, conservando los archivos de entrada.
- Informar fallas de lectura y errores del lector CSV con mensajes comprensibles.
- Separar fuentes, modelo, preparación, consultas y presentación de resultados.

Quedan fuera: interfaz web, APIs, productos definidos solo por volumen sin masa
conocida, prescripción de dietas y recomendaciones clínicas. Las comparaciones
serán demostrativas: no permitirán concluir qué alimento real conviene consumir.

## Desarrollo y publicaciones previstas

Este reinicio se realizará en un repositorio nuevo creado en GitHub antes de
implementar el programa. El trabajo anterior es un prototipo separado; no se
reutilizará su historial como si fuera el de este desarrollo.

Se prevén ocho commits con cambios reales. Cada etapa se revisará y publicará
antes de iniciar la siguiente. Teo realizará los commits y las publicaciones.
La implementación y la documentación se elaborarán con asistencia de IA.

| Etapa | Cambio que debe quedar implementado |
|---|---|
| 1 | Propuesta, alcance y configuración inicial |
| 2 | Generador determinista, 500 fichas CSV/JSON y documentación de datos |
| 3 | Fuente abstracta, lectores CSV/JSON, errores comprensibles y pruebas |
| 4 | Producto nutricional, conversión de unidades y bases, y pruebas |
| 5 | Diagnóstico, validación, limpieza, trazabilidad y pruebas |
| 6 | Índice, búsquedas, categorías, comparación, ordenamiento y pruebas |
| 7 | Consola, exportaciones, muestra de errores y pruebas de ejecución |
| 8 | Verificación integral, revisión PEP 8 y documentación final |

Las pruebas se incorporarán junto con cada comportamiento, no solo al final.
Se comprobarán casos conocidos, inválidos y propiedades: equivalencia CSV/JSON,
conservación de ceros iniciales, ausencias distintas de cero, conversiones
conocidas, repetibilidad y conciliación de registros válidos y rechazados.

El README final será breve e incluirá los comandos para ejecutar y probar;
la documentación ampliada quedará enlazada. La entrega identificará el enlace
al repositorio y el commit evaluado.
