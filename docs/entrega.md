# Entrega y reproducción

Autor: Teo Martinez. Opción 9: comparador de etiquetas nutricionales.

Repositorio: https://github.com/Teo-Martinez/TP2_PROGRAMACION_ORIENTADA_DATOS

La entrega debe indicar ese enlace y el identificador del último commit que
se desea evaluar. Después de publicar los cambios se obtiene con:

```bash
git rev-parse HEAD
git status
git log --oneline
```

El identificador se copia en el mensaje de entrega; no se intenta escribir el
hash de un commit dentro de ese mismo commit. El repositorio debe permanecer
accesible a la cátedra. Fechas y medio de entrega: los indicados en EVA.

Para reproducir desde otra carpeta:

```bash
git clone https://github.com/Teo-Martinez/TP2_PROGRAMACION_ORIENTADA_DATOS.git
cd TP2_PROGRAMACION_ORIENTADA_DATOS
python -m unittest discover -s tests -v
python -m src.main --codigos 0000000000001 0000000000002
```

Requiere Python 3.10 o posterior. En Windows se puede usar `py`. El archivo
requirements.txt indica que no hay paquetes externos que instalar.

## Historial y asistencia

El repositorio de este reinicio se creó en GitHub antes de implementar código.
Los primeros tres commits fueron realizados por Teo: alcance, muestra y lectores.
Ante problemas de conexión durante el push, el estudiante autorizó a Codex a
preparar los avances restantes. El código se elaboró con asistencia de IA y
retoma partes del prototipo anterior. No se presenta como un trabajo realizado
sin asistencia. Los cinco avances siguientes corresponden a modelo, preparación,
consultas, consola y verificación final, con pruebas junto a cada cambio.

La cantidad de commits no reemplaza comprender y defender el trabajo.

## Evidencias según la consigna

| Paso | Evidencia |
|---|---|
| 1. Problema y alcance | docs/propuesta.md y docs/consultas.md |
| 2. Datos y procedencia | data/README.md, generador y 500 fichas CSV/JSON |
| 3. Flujo reproducible | src/main.py, diagnóstico, limpieza y cuatro salidas |
| 4. Programación | FuenteDatos, dos lectores, ProductoNutricional, regex y funciones |
| 5. Verificación | tests/, casos conocidos, inválidos y propiedades |
| 6. Git/GitHub | Historial, .gitignore, repositorio creado antes del código |
| 7. Documentación y defensa | README, docs/, enlace y commit en la entrega |

De la rúbrica de Exploración de Datos se adaptan los criterios de procedencia,
diagnóstico, reglas justificadas, trazabilidad, pruebas e interpretación. Los
requisitos de R, SQLite, JOIN, gráficos y presentación de esa otra materia no
se trasladan automáticamente a esta consigna de Python.
