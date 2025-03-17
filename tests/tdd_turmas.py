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
        r = requests.post('http://localhost:5002/turmas',json={'nome':'ADS2B','id':1})
        r = requests.post('http://localhost:5002/turmas',json={'nome':'ADS3A','id':2})
        r_lista = requests.get('http://localhost:5002/turmas')
        achei_ads2b = False
        achei_ads3a = False
        for turma in r_lista.json():
            if turma['nome'] == 'ADS2B':
                achei_ads2b = True
            if turma['nome'] == 'ADS3A':
                achei_ads3a = True
        if not achei_ads2b:
            self.fail('turma ADS2B nao apareceu na lista de turmas')
        if not achei_ads3a:
            self.fail('turma ADS3A nao apareceu na lista de turmas')


    def test_003_turmas_get_por_id(self):
        r = requests.post('http://localhost:5002/turmas',json={'nome':'ADS4C','id':20})
        r_lista = requests.get('http://localhost:5002/turmas/20')
        self.assertEqual(r_lista.json()['nome'],'ADS4C')


    def test_004_turmas_post_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/turmas',json={'nome':'ADS5D','id':29})
        r_lista = requests.get('http://localhost:5002/turmas')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/turmas')
        self.assertEqual(len(r_lista_depois.json()),0)


    def test_005_turmas_delete(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/turmas',json={'nome':'ADS6E','id':29})
        requests.post('http://localhost:5002/turmas',json={'nome':'ADS7F','id':28})
        r_lista = requests.get('http://localhost:5002/turmas')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/turmas/28')
        r_lista = requests.get('http://localhost:5002/turmas')
        self.assertEqual(len(r_lista.json()),1)
    

    def test_006_turmas_put_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/turmas',json={'nome':'ADS1A','id':28})
        r_antes = requests.get('http://localhost:5002/turmas/28')
        self.assertEqual(r_antes.json()['nome'],'ADS1A')
        requests.put('http://localhost:5002/turmas/28', json={'nome':'ADS2B'})
        r_depois = requests.get('http://localhost:5002/turmas/28')
        self.assertEqual(r_depois.json()['nome'],'ADS2B')


    def test_007_turmas_put_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/turmas/15',json={'nome':'ADS1A','id':15})
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'turma nao encontrada')
    
    
    def test_008_turmas_get_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.get('http://localhost:5002/turmas/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'turma nao encontrada')
        

    def test_009_turmas_delete_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/turmas/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'turma nao encontrada')


    def test_010_turmas_post_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/turmas',json={'nome':'ADS1A','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/turmas',json={'nome':'ADS2B','id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_011_turmas_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/turmas',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'turma sem nome')
    

    def test_012_turmas_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/turmas',json={'nome':'ADS1A','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/turmas/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'turma sem nome')


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
