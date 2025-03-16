import requests
import unittest

class TestStringMethods(unittest.TestCase):

    def test_000_alunos_retorna_lista(self):
        r = requests.get('http://localhost:5002/alunos')

        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_001_adiciona_alunos(self):
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5002/alunos',json={'nome':'roberto','id':2})
        
        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()

        achei_fernando = False
        achei_roberto = False

        for aluno in lista_retornada:
            if aluno['nome'] == 'fernando':
                achei_fernando = True
            if aluno['nome'] == 'roberto':
                achei_roberto = True
        
        if not achei_fernando:
            self.fail('aluno fernando nao apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('aluno roberto nao apareceu na lista de alunos')

    def test_002_aluno_por_id(self):
        r = requests.post('http://localhost:5002/alunos',json={'nome':'mario','id':20})

        resposta = requests.get('http://localhost:5002/alunos/20')
        dict_retornado = resposta.json()
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome',dict_retornado)
        self.assertEqual(dict_retornado['nome'],'mario')

    def test_003_reseta(self):
        r = requests.post('http://localhost:5002/alunos',json={'nome':'cicero','id':29})

        r_lista = requests.get('http://localhost:5002/alunos')

        self.assertTrue(len(r_lista.json()) > 0)

        r_reset = requests.post('http://localhost:5002/reseta')

        self.assertEqual(r_reset.status_code,200)

        r_lista_depois = requests.get('http://localhost:5002/alunos')
        
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_004_deleta(self):

        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5002/alunos',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5002/alunos',json={'nome':'lucas','id':28})
        requests.post('http://localhost:5002/alunos',json={'nome':'marta','id':27})

        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()

        self.assertEqual(len(lista_retornada),3)

        requests.delete('http://localhost:5002/alunos/28')

        r_lista2 = requests.get('http://localhost:5002/alunos')
        lista_retornada2 = r_lista2.json()

        self.assertEqual(len(lista_retornada2),2) 

        acheiMarta = False
        acheiCicero = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'marta':
                acheiMarta=True
            if aluno['nome'] == 'cicero':
                acheiCicero=True
        if not acheiMarta or not acheiCicero:
            self.fail("voce parece ter deletado o aluno errado!")

        requests.delete('http://localhost:5002/alunos/27')

        r_lista3 = requests.get('http://localhost:5002/alunos')
        lista_retornada3 = r_lista3.json()

        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'cicero':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")

    def test_005_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')

        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5002/alunos',json={'nome':'lucas','id':28})

        r_antes = requests.get('http://localhost:5002/alunos/28')

        self.assertEqual(r_antes.json()['nome'],'lucas')

        requests.put('http://localhost:5002/alunos/28', json={'nome':'lucas mendes'})

        r_depois = requests.get('http://localhost:5002/alunos/28')

        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

        self.assertEqual(r_depois.json()['id'],28)

    def test_006a_id_inexistente_no_put(self):

        r_reset = requests.post('http://localhost:5002/reseta')

        self.assertEqual(r_reset.status_code,200)

        r = requests.put('http://localhost:5002/alunos/15',json={'nome':'bowser','id':15})

        self.assertIn(r.status_code,[400,404])

        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
    
    def test_006b_id_inexistente_no_get(self):

        r_reset = requests.post('http://localhost:5002/reseta')

        self.assertEqual(r_reset.status_code,200)

        r = requests.get('http://localhost:5002/alunos/15')
        self.assertIn(r.status_code,[400,404])

        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
        
    def test_006c_id_inexistente_no_delete(self):
        r_reset = requests.post('http://localhost:5002/reseta')

        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/alunos/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')

    def test_007_criar_com_id_ja_existente(self):

        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        r = requests.post('http://localhost:5002/alunos',json={'nome':'bond','id':7})
        self.assertEqual(r.status_code,200)

        r = requests.post('http://localhost:5002/alunos',json={'nome':'james','id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_008a_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        r = requests.post('http://localhost:5002/alunos',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
    
    def test_008b_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        r = requests.post('http://localhost:5002/alunos',json={'nome':'maximus','id':7})
        self.assertEqual(r.status_code,200)

        r = requests.put('http://localhost:5002/alunos/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
    
    def test_100_professores_retorna_lista(self):
        r = requests.get('http://localhost:5002/professores')
        self.assertEqual(type(r.json()),type([]))
    
    def test_100b_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),0)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),2)

    def test_101_adiciona_professores(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        r_lista = requests.get('http://localhost:5002/professores')
        achei_fernando = False
        achei_roberto = False
        for professor in r_lista.json():
            if professor['nome'] == 'fernando':
                achei_fernando = True
            if professor['nome'] == 'roberto':
                achei_roberto = True
        if not achei_fernando:
            self.fail('professor fernando nao apareceu na lista de professores')
        if not achei_roberto:
            self.fail('professor roberto nao apareceu na lista de professores')

    def test_102_professores_por_id(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'mario','id':20})
        r_lista = requests.get('http://localhost:5002/professores/20')
        self.assertEqual(r_lista.json()['nome'],'mario')

    def test_103_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'cicero','id':29})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_104_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':28})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/professores/28')
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_105_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':28})
        r_antes = requests.get('http://localhost:5002/professores/28')
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5002/professores/28', json={'nome':'lucas mendes'})
        r_depois = requests.get('http://localhost:5002/professores/28')
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    def test_106_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/professores/15',json={'nome':'bowser','id':15})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.get('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.delete('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')

    def test_107_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'bond','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'james','id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_108_post_ou_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')
        r = requests.post('http://localhost:5002/professores',json={'nome':'maximus','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/professores/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')

    def test_109_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/professores',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),0)

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
