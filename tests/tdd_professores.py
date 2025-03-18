import requests
import unittest

class TestStringMethods(unittest.TestCase):

    def test_001_professores_get_retorna_lista(self):
        r = requests.get('http://localhost:5002/professores')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /professores no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")
        self.assertEqual(type(obj_retornado),type([]))
    

    def test_002_professores_post_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 101,
            "nome": "Pedro",
            "data_nascimento": "2006/06/01",
            "nota_primeiro_semestre": 5,
            "nota_segundo_semestre": 8,
            "turma_id": 1
            })
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={
            "id": 102,
            "nome": "Gustavo",
            "data_nascimento": "2003/03/11",
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10,
            "turma_id": 1
            })
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),0)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),2)


    def test_003_professores_post_adiciona(self):
        r = requests.post('http://localhost:5002/professores',json={
            "id": 1,
            "nome": "João",
            "data_nascimento": "1979/03/11",
            "disciplina": "Dev Mobile",
            "salario": 5000.0
            })
        r = requests.post('http://localhost:5002/professores',json={
            "id": 2,
            "nome": "Marcelo",
            "data_nascimento": "1988/04/14",
            "disciplina": "Dev Web",
            "salario": 6300.0
            })
        r_lista = requests.get('http://localhost:5002/professores')
        achei_joao = False
        achei_marcelo = False
        for professor in r_lista.json():
            if professor['nome'] == 'João':
                achei_joao = True
            if professor['nome'] == 'Marcelo':
                achei_marcelo = True
        if not achei_joao:
            self.fail('professor joao nao apareceu na lista de professores')
        if not achei_marcelo:
            self.fail('professor marcelo nao apareceu na lista de professores')


    def test_004_professores_get_por_id(self):
        r = requests.post('http://localhost:5002/professores',json={
            "id": 3,
            "nome": "Mario",
            "data_nascimento": "1960/10/18",
            "disciplina": "Linguagem SQL",
            "salario": 6550.0
            })
        r_lista = requests.get('http://localhost:5002/professores/3')
        self.assertEqual(r_lista.json()['nome'],'Mario')


    def test_005_professores_post_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/professores',json={
            "id": 4,
            "nome": "Cicero",
            "data_nascimento": "1966/11/20",
            "disciplina": "Linguagem Python",
            "salario": 3730.0
            })
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista_depois.json()),0)


    def test_006_professores_delete(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={
            "id": 1,
            "nome": "Cicero",
            "data_nascimento": "1966/11/20",
            "disciplina": "Linguagem Python",
            "salario": 3730.0
            })
        requests.post('http://localhost:5002/professores',json={
            "id": 2,
            "nome": "Jagunço",
            "data_nascimento": "1976/10/26",
            "disciplina": "Linguagem Python",
            "salario": 4000.0
            })
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/professores/1')
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),1)
    

    def test_007_professores_put_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={
            "id": 1,
            "nome": "Lucas",
            "data_nascimento": "1990/10/10",
            "disciplina": "Dev API",
            "salario": 4500.0
            })
        r_antes = requests.get('http://localhost:5002/professores/1')
        self.assertEqual(r_antes.json()['nome'],'Lucas')
        requests.put('http://localhost:5002/professores/1', json={'nome':'Lucas Morellos'})
        r_depois = requests.get('http://localhost:5002/professores/1')
        self.assertEqual(r_depois.json()['nome'],'Lucas Morellos')


    def test_008_professores_put_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/professores/1',json={
            "id": 1,
            "nome": "Matias Fernandes",
            "data_nascimento": "1989/01/07",
            "disciplina": "Ambientes Operacionais",
            "salario": 6500.0
            })
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
    
    
    def test_009_professores_get_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.get('http://localhost:5002/professores/1')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        

    def test_010_professores_delete_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/professores/1')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'professor nao encontrado')


    def test_011_professores_post_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={
            "id": 1,
            "nome": "James Bonde",
            "data_nascimento": "1973/08/20",
            "disciplina": "DevOps",
            "salario": 8000.0
            })
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={
            "id": 1,
            "nome": "Guilherme Antonio",
            "data_nascimento": "1991/01/20",
            "disciplina": "Engenharia de Software",
            "salario": 8700.0
            })
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_012_professores_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':1})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')
    

    def test_013_professores_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={
            "id": 1,
            "nome": "Matheus Bontempo",
            "data_nascimento": "1957/02/21",
            "disciplina": "Automoção Robótica de Processos",
            "salario": 7500.0
            })
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/professores/1',json={'id':1})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')


    def test_014_professores_post_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/professores',json={
            "id": 1,
            "nome": "Maria Guilhermina",
            "data_nascimento": "1957/11/12",
            "disciplina": "Soft Skills",
            "salario": 3500.0
            })
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={
            "id": 1,
            "nome": "Fernanda Santos",
            "data_nascimento": "1993/10/02",
            "disciplina": "Lógica de Programação",
            "salario": 6620.0
            })
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
