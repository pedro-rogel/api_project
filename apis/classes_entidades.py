import datetime

class Pessoa:
    def __init__(self, id, nome, data_de_nascimento):
        self.nome = nome
        self.data_nascimento = data_de_nascimento
        self.id = id

class Aluno(Pessoa):
    def __init__(self, id, nome, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, turma_id):
        super().__init__(id, nome, data_nascimento)
        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.idade = atribuir_idade(self.data_nascimento)
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = media(self.nota_primeiro_semestre, self.nota_segundo_semestre)
        self.turma_id = turma_id
    
    def converter_aluno_dici(self):
        atribuir_aluno = self.id, self.nome, self.idade, self.data_nascimento, self.nota_primeiro_semestre, self.nota_segundo_semestre, self.media_final, self.turma_id
        dados_alunos = ["id", "nome", "idade", "data_nascimento", "nota_primeiro_semestre", "nota_segundo_semestre", "media_final", "turma_id"]
        return dict(zip(dados_alunos, atribuir_aluno))

class Professor(Pessoa):
    def __init__(self, id, nome, data_nascimento, disciplina, salario, descricao):
        super().__init__(id, nome, data_nascimento)
        self.id = id
        self.nome = nome
        self.idade = atribuir_idade(self.data_nascimento)
        self.data_nascimento = data_nascimento
        self.disciplina = disciplina
        self.salario = salario
        self.descricao = descricao

    def converter_professor_dici(self):
        atribuir_professor = self.id, self.nome, self.idade, self.data_nascimento, self.disciplina, self.salario, self.descricao
        dados_professores = ["id", "nome", "idade", "data_nascimento", "disciplina", "salario", "descricao"]
        return dict(zip(dados_professores, atribuir_professor))

class Turma():
    def __init__(self, id, nome, turno, professor_id, descricao, status):
        self.id = id
        self.nome = nome
        self.turno = turno
        self.professor_id = professor_id
        self.descricao = descricao
        self.status = status

    def converter_turma_dici(self):
        atribuir_turma = self.id, self.nome, self.turno, self.professor_id, self.descricao, self.status
        dados_turmas = ["id", "nome", "turno", "professor_id", "descricao", "status"]
        return dict(zip(dados_turmas, atribuir_turma))

def atribuir_idade(birthDate):
    data = birthDate.split("/")
    if not len(data[0]) == 4:
        return 
    ano = int(data[0])
    mes = int(data[1])
    dia = int(data[2])
    data_atual = datetime.date.today()
    if mes < int(data_atual.month):
        idade = data_atual.year - ano
    elif mes == data_atual.month:
        if dia <= data_atual.day:
            idade = data_atual.year - ano
        else:
            idade = (data_atual.year - ano) - 1
    else:
        idade = (data_atual.year - ano) - 1
    return idade

def media(nota1, nota2):
    return (nota1 + nota2) / 2
