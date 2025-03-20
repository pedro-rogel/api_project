import requests
import unittest


class TestStringMethods(unittest.TestCase):
    

    def test_001_alunos_get_existe_rota(self):
        r = requests.get('http://localhost:5002/alunos')
        if r.status_code == 404:
            self.fail("Rota '/alunos' não definida")


    def test_002_professores_get_existe_rota(self):
        r = requests.get('http://localhost:5002/professores')
        if r.status_code == 404:
            self.fail("Rota '/professores' não definida")


    def test_003_turmas_get_existe_rota(self):
        r = requests.get('http://localhost:5002/turmas')
        if r.status_code == 404:
            self.fail("Rota '/turmas' não definida")


    def test_004_alunos_get_retorna_nada(self):
        r = requests.get('http://localhost:5002/alunos')
        try:
            obj_retornado = r.json()
        except:
            self.fail("Retorno diferente de 'json' na rota '/alunos'")
        self.assertEqual(type(obj_retornado), type([]))


    def test_005_professores_get_retorna_nada(self):
        r = requests.get('http://localhost:5002/professores')
        try:
            obj_retornado = r.json()
        except:
            self.fail("Retorno diferente de 'json' na rota '/professores'")
        self.assertEqual(type(obj_retornado), type([]))


    def test_006_turmas_get_retorna_nada(self):
        r = requests.get('http://localhost:5002/turmas')
        try:
            obj_retornado = r.json()
        except:
            self.fail("Retorno diferente de 'json' na rota '/turmas'")
        self.assertEqual(type(obj_retornado), type([]))


    def test_007_alunos_post_sem_turmas(self):
        r = requests.post('http://localhost:5002/alunos',json={
        "id": 1,
        "nome": "Pedro",
        "data_nascimento": "2006/06/01",
        "nota_primeiro_semestre": 5,
        "nota_segundo_semestre": 8,
        "turma_id": 1
        })
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'Não há turmas criadas')


    def test_008_turmas_post_sem_professores(self):
        r = requests.post('http://localhost:5002/turmas',json={
            'id':1, 
            'nome':'ADS', 
            'turno':'Diurno', 
            'professor_id': 1
            })
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'Não há professores criados')


    def test_009_professores_post_criar_professor(self):
        r = requests.post('http://localhost:5002/professores',json={
            "nome": "João",
            "data_nascimento": "1979/03/11",
            "disciplina": "Dev Mobile",
            "salario": 5000.0,
            "descricao": "Alguma coisa"
            })
        r = requests.post('http://localhost:5002/professores',json={
            "nome": "Marcelo",
            "data_nascimento": "1988/04/14",
            "disciplina": "Dev Web",
            "salario": 6300.0,
            "descricao": "Coisa alguma"
            })
        r_lista = requests.get('http://localhost:5002/professores')
        if not any(professor["nome"] == "João" for professor in r_lista.json()):
            self.fail('professor João nao apareceu na lista de professores')
        if not any(professor["nome"] == "Marcelo" for professor in r_lista.json()):
            self.fail('professor Marcelo nao apareceu na lista de professores')


    def test_010_turmas_post_criar_turmas(self):
        r = requests.post('http://localhost:5002/turmas',json={ 
            'nome': 'ADS', 
            'turno': 'Dia', 
            'professor_id': 1,
            'descricao': "Qualquer coisa",
            'status': True
            })
        r = requests.post('http://localhost:5002/turmas',json={ 
            'nome': 'SI', 
            'turno': 'Noite', 
            'professor_id': 1,
            'descricao': "Coisa qualquer",
            'status': True
            })
        r_lista = requests.get('http://localhost:5002/turmas')
        if not any(turma["nome"] == "ADS" for turma in r_lista.json()):
            self.fail('Turma ADS não apareceu na lista de turmas')
        if not any(turma["nome"] == "SI" for turma in r_lista.json()):
            self.fail('Turma SI não apareceu na lista de turmas')


    def test_011_alunos_post_criar_alunos(self):
        r = requests.post('http://localhost:5002/alunos',json={
            "nome": "Renan Nunes",
            "data_nascimento": "2004/09/02",
            "nota_primeiro_semestre": 5,
            "nota_segundo_semestre": 5,
            "turma_id": 1
            })
        r = requests.post('http://localhost:5002/alunos',json={
            "nome": "Fernando Barril",
            "data_nascimento": "2004/06/18",
            "nota_primeiro_semestre": 6.5,
            "nota_segundo_semestre": 8.5,
            "turma_id": 1
            })
        r_lista = requests.get('http://localhost:5002/alunos')
        if not any(aluno["nome"] == "Renan Nunes" for aluno in r_lista.json()):
            self.fail('Nome Renan Nunes não encontrado na lista de alunos')
        if not any(aluno["nome"] == "Fernando Barril" for aluno in r_lista.json()):
            self.fail('Nome Fernando Barril não encontrado na lista de alunos')


    def test_012_alunos_get_id(self):
        r_lista = requests.get('http://localhost:5002/alunos/2')
        self.assertEqual(r_lista.json()['nome'],'Fernando Barril')


    def test_013_professores_get_id(self):
        r_lista = requests.get('http://localhost:5002/professores/2')
        self.assertEqual(r_lista.json()['nome'],'Marcelo')


    def test_014_turmas_get_id(self):
        r_lista = requests.get('http://localhost:5002/turmas/2')
        self.assertEqual(r_lista.json()['nome'],'SI')


    def test_015_alunos_put_edita(self):
        r = requests.get('http://localhost:5002/alunos/2')
        self.assertEqual(r.json()['nome'],'Fernando Barril')
        requests.put('http://localhost:5002/alunos/2', json={'nome':'Felippe Fodase'})
        r_depois = requests.get('http://localhost:5002/alunos/2')
        self.assertEqual(r_depois.json()['nome'],'Felippe Fodase')


    def test_016_professores_put_edita(self):
        r = requests.get('http://localhost:5002/professores/1')
        self.assertEqual(r.json()['nome'],'João')
        requests.put('http://localhost:5002/professores/1', json={'nome':'Gustavo Santos'})
        r_depois = requests.get('http://localhost:5002/professores/1')
        self.assertEqual(r_depois.json()['nome'],'Gustavo Santos')


    def test_017_turmas_put_edita(self):
        r = requests.get('http://localhost:5002/turmas/1')
        self.assertEqual(r.json()['nome'],'ADS')
        requests.put('http://localhost:5002/turmas/1', json={'nome':'ADS 2B'})
        r_depois = requests.get('http://localhost:5002/turmas/1')
        self.assertEqual(r_depois.json()['nome'],'ADS 2B')


    def test_018_alunos_delete(self):
        r_lista = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/alunos/1')
        r_lista = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista.json()),1)


    def test_019_turmas_delete(self):
        r_lista = requests.get('http://localhost:5002/turmas')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/turmas/1')
        r_lista = requests.get('http://localhost:5002/turmas')
        self.assertEqual(len(r_lista.json()),1)


    def test_020_professores_delete(self):
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/professores/1')
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),1)


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
