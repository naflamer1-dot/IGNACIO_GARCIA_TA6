"""Pruebas funcionales ejecutables sin dependencias de desarrollo adicionales."""
import unittest

from main import app


class AplicacionTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def notas(self, n1='55', n2='65', n3='45', asistencia='86'):
        return self.client.post('/ejercicio1', data={
            'nota1': n1, 'nota2': n2, 'nota3': n3, 'asistencia': asistencia})

    def nombres(self, a='Felipe', b='Juan', c='Gustavo'):
        return self.client.post('/ejercicio2', data={
            'nombre1': a, 'nombre2': b, 'nombre3': c})

    def test_paginas_y_autor(self):
        for url in ['/', '/ejercicio1', '/ejercicio2', '/acerca']:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Ignacio Garcia', response.data)

    def test_menu_y_css(self):
        text = self.client.get('/').get_data(as_text=True)
        self.assertIn('href="/ejercicio1"', text)
        self.assertIn('href="/ejercicio2"', text)
        with self.client.get('/static/style.css') as response:
            self.assertEqual(response.status_code, 200)

    def test_ejemplo_notas(self):
        response = self.notas()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'55.00', response.data)
        self.assertIn(b'>APROBADO<', response.data)

    def test_umbral_exacto(self):
        self.assertIn(b'>APROBADO<', self.notas('40','40','40','75').data)

    def test_notas_bajas(self):
        self.assertIn(b'>REPROBADO<', self.notas('39','39','39','100').data)

    def test_asistencia_baja(self):
        self.assertIn(b'>REPROBADO<', self.notas('70','70','70','74.99').data)

    def test_no_aprobar_por_redondeo(self):
        self.assertIn(b'>REPROBADO<', self.notas('39.999','40','40','100').data)

    def test_limites_validos(self):
        for nota, asistencia in [('10','0'), ('70','100')]:
            self.assertEqual(self.notas(nota,nota,nota,asistencia).status_code,200)

    def test_numeros_invalidos(self):
        for nota in ['', 'abc', '9', '71', 'NaN', 'Infinity', '-Infinity', '1e999']:
            with self.subTest(nota=nota):
                self.assertEqual(self.notas(n1=nota).status_code,400)

    def test_asistencia_invalida(self):
        for asistencia in ['-1','101','','NaN']:
            self.assertEqual(self.notas(asistencia=asistencia).status_code,400)

    def test_formularios_vacios(self):
        for url in ['/ejercicio1','/ejercicio2']:
            self.assertEqual(self.client.post(url,data={}).status_code,400)

    def test_ejemplo_nombres(self):
        response = self.nombres()
        self.assertEqual(response.status_code,200)
        self.assertIn(b'<strong>Gustavo</strong>',response.data)
        self.assertIn(b'<strong>7</strong>',response.data)

    def test_nombres_duplicados(self):
        for segundo in ['ANA',' Ana ','Ana']:
            self.assertEqual(self.nombres('Ana',segundo,'Juan').status_code,400)

    def test_nombre_invalido(self):
        for nombre in ['','   ','123','<script>alert(1)</script>','A'*101]:
            self.assertEqual(self.nombres(a=nombre).status_code,400)

    def test_empate(self):
        response=self.nombres('Juan','Luis','Ana').get_data(as_text=True)
        self.assertIn('<strong>Juan</strong>',response)
        self.assertIn('Hay un empate',response)

    def test_unicode_y_compuestos(self):
        response=self.nombres('Mari\u0301a Jose\u0301','Ana','Luis').get_data(as_text=True)
        self.assertIn('<strong>María José</strong>',response)
        self.assertIn('<strong>9</strong>',response)

    def test_escape_html(self):
        text=self.nombres(a='<script>').get_data(as_text=True)
        self.assertNotIn('value="<script>"',text)
        self.assertIn('&lt;script&gt;',text)

    def test_redireccion_y_error_404(self):
        for numero in (1,2):
            response=self.client.get(f'/ejercicio/{numero}')
            self.assertEqual(response.status_code,302)
            self.assertTrue(response.headers['Location'].endswith(f'/ejercicio{numero}'))
        self.assertEqual(self.client.get('/ejercicio/3').status_code,404)


if __name__ == '__main__':
    unittest.main()
