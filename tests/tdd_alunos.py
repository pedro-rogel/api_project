import requests
import unittest

class TestStringMethods(unittest.TestCase):

    def test_001_alunos_get_retorna_lista(self):
        r = requests.get('http://localhost:5002/alunos')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")
        self.assertEqual(type(obj_retornado),type([]))


    def test_002_alunos_post_adiciona(self):
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 1,
            "nome": "Pedro",
            "data_nascimento": "2006/06/01",
            "nota_primeiro_semestre": 5,
            "nota_segundo_semestre": 8,
            "turma_id": 1
            })
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 2,
            "nome": "Gustavo",
            "data_nascimento": "2003/03/11",
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10,
            "turma_id": 1
            })
        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()
        achei_pedro = False
        achei_gustavo = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'Pedro':
                achei_pedro = True
            if aluno['nome'] == 'Gustavo':
                achei_gustavo = True
        if not achei_pedro:
            self.fail('aluno Pedro nao apareceu na lista de alunos')
        if not achei_gustavo:
            self.fail('aluno Gustavo nao apareceu na lista de alunos')


    def test_003_alunos_get_por_id(self):
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 10,
            "nome": "Renan Nunes",
            "data_nascimento": "2004/09/02",
            "nota_primeiro_semestre": 5,
            "nota_segundo_semestre": 5,
            "turma_id": 1
            })
        resposta = requests.get('http://localhost:5002/alunos/10')
        dict_retornado = resposta.json()
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome',dict_retornado)
        self.assertEqual(dict_retornado['nome'],'Renan Nunes')


    def test_004_alunos_post_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 20,
            "nome": "Fernando Barril",
            "data_nascimento": "2004/06/18",
            "nota_primeiro_semestre": 6.5,
            "nota_segundo_semestre": 8.5,
            "turma_id": 1
            })
        r_lista = requests.get('http://localhost:5002/alunos')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_depois.json()),0)


    def test_005_alunos_delete(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/alunos',json={
            "id": 1,
            "nome": "Felippe",
            "data_nascimento": "2001/10/25",
            "nota_primeiro_semestre": 7.5,
            "nota_segundo_semestre": 10,
            "turma_id": 1
            })
        requests.post('http://localhost:5002/alunos',json={
            "id": 2,
            "nome": "Murillo",
            "data_nascimento": "2006/11/10",
            "nota_primeiro_semestre": 3,
            "nota_segundo_semestre": 7.5,
            "turma_id": 1
            })
        requests.post('http://localhost:5002/alunos',json={
            "id": 3,
            "nome": "Vinicius",
            "data_nascimento": "2002/07/24",
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": 9,
            "turma_id": 1
            })
        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()
        self.assertEqual(len(lista_retornada),3)
        requests.delete('http://localhost:5002/alunos/2')
        r_lista2 = requests.get('http://localhost:5002/alunos')
        lista_retornada2 = r_lista2.json()
        self.assertEqual(len(lista_retornada2),2) 
        acheiFelippe = False
        acheiVinicius = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'Felippe':
                acheiFelippe=True
            if aluno['nome'] == 'Vinicius':
                acheiVinicius=True
        if not acheiFelippe or not acheiVinicius:
            self.fail("voce parece ter deletado o aluno errado!")
        requests.delete('http://localhost:5002/alunos/1')
        r_lista3 = requests.get('http://localhost:5002/alunos')
        lista_retornada3 = r_lista3.json()
        self.assertEqual(len(lista_retornada3),1)
        if lista_retornada3[0]['nome'] == 'Vinicius':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")


    def test_006_alunos_put_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/alunos',json={
            "id": 1,
            "nome": "Gustavo",
            "data_nascimento": "2003/03/24",
            "nota_primeiro_semestre": 7,
            "nota_segundo_semestre": 7,
            "turma_id": 1
            })
        r_antes = requests.get('http://localhost:5002/alunos/1')
        self.assertEqual(r_antes.json()['nome'],'Gustavo')
        requests.put('http://localhost:5002/alunos/1', json={'nome':'Gustavo Santos'})
        r_depois = requests.get('http://localhost:5002/alunos/1')
        self.assertEqual(r_depois.json()['nome'],'Gustavo Santos')
        self.assertEqual(r_depois.json()['id'],1)


    def test_007_alunos_put_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/alunos/15',json={
            "id": 1,
            "nome": "Fernando",
            "data_nascimento": "2007/08/07",
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 9.5,
            "turma_id": 1
            })
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
    
    
    def test_008_alunos_get_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.get('http://localhost:5002/alunos/1')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
        

    def test_009_alunos_delete_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/alunos/1')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')


    def test_010_alunos_post_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 1,
            "nome": "Fabricio",
            "data_nascimento": "2001/09/06",
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": 9,
            "turma_id": 1
            })
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 1,
            "nome": "Marcelo",
            "data_nascimento": "2002/06/13",
            "nota_primeiro_semestre": 9.5,
            "nota_segundo_semestre": 5.5,
            "turma_id": 1
            })
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')


    def test_011_alunos_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'id':1})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
    

    def test_012_alunos_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 1,
            "nome": "Maycon",
            "data_nascimento": "2005/10/22",
            "nota_primeiro_semestre": 7,
            "nota_segundo_semestre": 2,
            "turma_id": 1
            })
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/alunos/1',json={'id':1})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
