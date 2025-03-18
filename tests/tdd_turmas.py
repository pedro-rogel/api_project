import requests
import unittest

class TestStringMethods(unittest.TestCase):
    
    def test_001_turmas_get_retorna_lista(self):
        r = requests.get('http://localhost:5002/turmas')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")
        self.assertEqual(type(obj_retornado),type([]))


    def test_002_turmas_post_adiciona(self):
        r = requests.post('http://localhost:5002/turmas',json={
            'id':1, 
            'nome':'ADS', 
            'turno':'Diurno', 
            'professor_id':1
            })
        r = requests.post('http://localhost:5002/turmas',json={
            'id':2, 
            'nome':'SI', 
            'turno':'Noturno', 
            'professor_id':1
            })
        r_lista = requests.get('http://localhost:5002/turmas')
        achei_ads = False
        achei_si = False
        for turma in r_lista.json():
            if turma['nome'] == 'ADS':
                achei_ads = True
            if turma['nome'] == 'SI':
                achei_si = True
        if not achei_ads:
            self.fail('turma ADS nao apareceu na lista de turmas')
        if not achei_si:
            self.fail('turma SI nao apareceu na lista de turmas')


    def test_003_turmas_get_por_id(self):
        r = requests.post('http://localhost:5002/turmas',json={
            'id':3, 
            'nome':'SI3B', 
            'turno':'integral', 
            'professor_id':1
            })
        r_lista = requests.get('http://localhost:5002/turmas/3')
        self.assertEqual(r_lista.json()['nome'],'SI3B')


    def test_004_turmas_post_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/turmas',json={
            'id':1, 
            'nome':'Engenharia de Software', 
            'turno':'Diurno', 
            'professor_id':1
            })
        r_lista = requests.get('http://localhost:5002/turmas')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/turmas')
        self.assertEqual(len(r_lista_depois.json()),0)


    def test_005_turmas_delete(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/turmas',json={
            'id':1, 
            'nome':'ADS1A', 
            'turno':'Diurno', 
            'professor_id':1
            })
        requests.post('http://localhost:5002/turmas',json={
            'id':2, 
            'nome':'SI1B', 
            'turno':'Integral', 
            'professor_id':1
            })
        r_lista = requests.get('http://localhost:5002/turmas')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/turmas/2')
        r_lista = requests.get('http://localhost:5002/turmas')
        self.assertEqual(len(r_lista.json()),1)
    

    def test_006_turmas_put_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/turmas',json={
            'id':1, 
            'nome':'ADS1A', 
            'turno':'Noturno', 
            'professor_id':1
            })
        r_antes = requests.get('http://localhost:5002/turmas/1')
        self.assertEqual(r_antes.json()['nome'],'ADS1A')
        requests.put('http://localhost:5002/turmas/1', json={
            'id':1, 
            'nome':'ADS4D', 
            'turno':'Diurno', 
            'professor_id':1
            })
        r_depois = requests.get('http://localhost:5002/turmas/1')
        self.assertEqual(r_depois.json()['nome'],'ADS4D')


    def test_007_turmas_put_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/turmas/1',json={
            'id':1, 
            'nome':'ADS3C', 
            'turno':'Diurno', 
            'professor_id':1
            })
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'turma nao encontrada')
    
    
    def test_008_turmas_get_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.get('http://localhost:5002/turmas/1')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'turma nao encontrada')
        

    def test_009_turmas_delete_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/turmas/1')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'turma nao encontrada')


    def test_010_turmas_post_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/turmas',json={
            'id':1, 
            'nome':'ADS', 
            'turno':'Diurno', 
            'professor_id':1
            })
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/turmas',json={
            'id':1, 
            'nome':'Ciência da Computação', 
            'turno':'Noturno', 
            'professor_id':1
            })
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_011_turmas_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/turmas',json={'id':1})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'turma sem nome')
    

    def test_012_turmas_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/turmas',json={
            'id':1, 
            'nome':'ADS2B', 
            'turno':'Integral', 
            'professor_id':1
            })
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/turmas/1',json={'id':1})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'turma sem nome')


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
