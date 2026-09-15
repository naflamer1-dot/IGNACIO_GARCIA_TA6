"""Evaluación 3 de Programación Web. Autor: Ignacio Garcia."""

from decimal import Decimal, InvalidOperation
import unicodedata

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024


def leer_numero(texto, etiqueta, minimo, maximo):
    """Convierte un número y valida el rango también en el servidor."""
    try:
        numero = Decimal(texto.strip().replace(',', '.'))
    except (InvalidOperation, ValueError):
        raise ValueError(f'{etiqueta}: ingresa un número válido.') from None
    if not numero.is_finite() or not minimo <= numero <= maximo:
        raise ValueError(f'{etiqueta}: debe estar entre {minimo} y {maximo}.')
    return numero


def calcular_notas(datos):
    notas = [leer_numero(datos[f'nota{i}'], f'Nota {i}', 10, 70)
             for i in range(1, 4)]
    asistencia = leer_numero(datos['asistencia'], 'Asistencia', 0, 100)
    promedio = sum(notas) / 3
    # Comparar la suma evita que el redondeo del promedio cambie el estado.
    aprobado = sum(notas) >= 120 and asistencia >= 75
    return {'promedio': f'{promedio:.2f}',
            'estado': 'APROBADO' if aprobado else 'REPROBADO',
            'aprobado': aprobado}


def comparar_nombres(datos):
    nombres = [unicodedata.normalize('NFC', ' '.join(datos[f'nombre{i}'].split()))
               for i in range(1, 4)]
    for i, nombre in enumerate(nombres, 1):
        if not nombre or len(nombre) > 100:
            raise ValueError(f'Nombre {i}: ingresa entre 1 y 100 caracteres.')
        if not all(letra.isalpha() or letra == ' ' for letra in nombre):
            raise ValueError(f'Nombre {i}: utiliza solo letras y espacios.')
    if len({nombre.casefold() for nombre in nombres}) != 3:
        raise ValueError('Ingresa tres nombres diferentes.')
    cantidades = [sum(letra.isalpha() for letra in nombre) for nombre in nombres]
    mayor = max(cantidades)
    indice = cantidades.index(mayor)  # En empate se conserva el primer ingreso.
    return {'nombre': nombres[indice], 'cantidad': mayor,
            'empate': cantidades.count(mayor) > 1}


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/acerca')
def acerca():
    return render_template('acerca.html')


@app.route('/ejercicio1', methods=['GET', 'POST'])
def ejercicio1():
    campos = ['nota1', 'nota2', 'nota3', 'asistencia']
    datos = {campo: request.form.get(campo, '') for campo in campos}
    resultado, error = None, None
    if request.method == 'POST':
        try:
            resultado = calcular_notas(datos)
        except ValueError as exc:
            error = str(exc)
    return render_template('ejercicio1.html', datos=datos,
                           resultado=resultado, error=error), 400 if error else 200


@app.route('/ejercicio2', methods=['GET', 'POST'])
def ejercicio2():
    datos = {f'nombre{i}': request.form.get(f'nombre{i}', '') for i in range(1, 4)}
    resultado, error = None, None
    if request.method == 'POST':
        try:
            resultado = comparar_nombres(datos)
        except ValueError as exc:
            error = str(exc)
    return render_template('ejercicio2.html', datos=datos,
                           resultado=resultado, error=error), 400 if error else 200


@app.get('/ejercicio/<int:numero>')
def abrir_ejercicio(numero):
    """Ruta con parámetro y redirección a las páginas de los ejercicios."""
    if numero not in (1, 2):
        abort(404)
    return redirect(url_for(f'ejercicio{numero}'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
