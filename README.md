# Evaluación 3 de Programación Web

Estudiante: **Ignacio Garcia**

Aplicación Python con Flask para los dos ejercicios de TA_6 (2).docx.
El menú y los formularios siguen la referencia visual del documento y del
[video de la evaluación](https://www.youtube.com/watch?v=fjreh4bIoIQ).

## Ejecutar en Windows

Necesitas Python 3.9 o superior. Extrae el ZIP y abre una terminal dentro de la
carpeta IGNACIO_GARCIA, donde está main.py. Ejecuta:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

Abre http://127.0.0.1:5000 en tu navegador. Detén el servidor con Ctrl+C.
Si `py` no está disponible, usa `python -m venv .venv`.
Si el puerto 5000 está ocupado, usa:

```powershell
.venv\Scripts\python.exe -m flask --app main run --port 5001
```

En ese caso, abre http://127.0.0.1:5001. El servidor incluido es para uso local.

## Organización

```text
IGNACIO_GARCIA/
  main.py
  requirements.txt
  templates/
    base.html
    index.html
    ejercicio1.html
    ejercicio2.html
    acerca.html
  static/
    style.css
  tests/
    test_main.py
  README.md
  ENLACE_GITHUB.txt
  .gitignore
```

Hay cuatro páginas: menú, notas, nombres e información del trabajo. Esta última
se abre desde el nombre del estudiante en el pie de página. Así se cubren las
cuatro páginas mencionadas en la pauta, conservando los dos botones del menú.
La quinta plantilla, base.html, permite reutilizar sus bloques.

## Funcionamiento

- `/`: menú principal con los botones Ejercicio 1 y Ejercicio 2.
- `/acerca`: información del trabajo y nombre del estudiante.
- `/ejercicio1`: GET muestra el formulario; POST valida tres notas de 10 a 70
  y asistencia de 0 a 100. Aprueba si el promedio es >= 40 **y** asistencia >= 75.
  El promedio se muestra con dos decimales; el estado se decide sin redondear.
- `/ejercicio2`: GET muestra el formulario; POST recibe tres nombres diferentes,
  selecciona el que tiene más letras y muestra su longitud. Felipe, Juan, Gustavo
  devuelve Gustavo, 7 caracteres. Acepta tildes, ñ y nombres compuestos; no cuenta
  espacios. Normaliza espacios y Unicode. En empate elige el primero ingresado.
  Los nombres repetidos no se distinguen por mayúsculas.
- `/ejercicio/1` y `/ejercicio/2`: rutas con parámetro que redirigen al formulario.
  Otros números responden con 404.

Las funciones `calcular_notas` y `comparar_nombres` separan la lógica de las rutas.
Los datos viven en variables durante cada solicitud; no se necesita base de datos.
Se validan los datos en HTML y nuevamente en Python. Los errores conservan los
valores para corregirlos. Jinja escapa los valores al renderizar las plantillas.

## Pruebas

Desde la carpeta del proyecto:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas comprueban los ejemplos, límites de aprobación, rangos inválidos,
campos vacíos, valores no finitos, nombres repetidos, tildes, empates y rutas.

## Entrega y GitHub

El ZIP es el proyecto para Blackboard. La entrega también requiere publicar el
código en tu cuenta de GitHub y adjuntar su URL real en ENLACE_GITHUB.txt.
El proyecto aún no se ha publicado. No entregues ese TXT con el aviso pendiente.

1. Crea un repositorio vacío en tu cuenta, por ejemplo `evaluacion3-flask`.
2. Desde esta carpeta ejecuta (reemplaza TU_USUARIO por tu usuario real):

```text
git init
git add .
git commit -m "Evaluacion 3 Flask - Ignacio Garcia"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/evaluacion3-flask.git
git push -u origin main
```

3. Reemplaza el contenido de ENLACE_GITHUB.txt por la URL del repositorio creado.
4. Actualiza el archivo en GitHub y comprime la carpeta sin `.venv`, `.git` ni
   `__pycache__`. Entrega el ZIP y el TXT del enlace; no solo el enlace.

Documentación: [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
y [entornos virtuales e instalación](https://flask.palletsprojects.com/en/stable/installation/).
