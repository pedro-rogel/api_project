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
        self.__idade = atribuir_idade(self.data_nascimento)
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.__media_final = media_final(self.nota_primeiro_semestre, self.nota_segundo_semestre)
        self.turma_id = turma_id

    def get(self):
        return self.id, self.nome, self.__idade, self.data_nascimento, self.nota_primeiro_semestre, self.nota_segundo_semestre, self.__media_final, self.turma_id

class Professor(Pessoa):
    def __init__(self, id, nome, data_nascimento, disciplina, salario):
        super().__init__(id, nome, data_nascimento)
        self.id = id
        self.nome = nome
        self.__idade = atribuir_idade(self.data_nascimento)
        self.data_nascimento = data_nascimento
        self.disciplina = disciplina
        self.salario = salario

    def get(self):
        return self.id, self.nome, self.__idade, self.data_nascimento, self.disciplina, self.salario

class Turma():
    def __init__(self, id, nome, turno, professor_id):
        self.id = id
        self.nome = nome
        self.turno = turno
        self.professor_id = professor_id

    def get(self):
        return self.id, self.nome, self.turno, self.professor_id

def converter_aluno_dici(atribuir_aluno):
    aluno = {
        "id": atribuir_aluno[0],
        "nome": atribuir_aluno[1],
        "idade": atribuir_aluno[2],
        "data_nascimento": atribuir_aluno[3],
        "nota_primeiro_semestre": atribuir_aluno[4],
        "nota_segundo_semestre": atribuir_aluno[5],
        "media_final": atribuir_aluno[6],
        "turma_id": atribuir_aluno[7]
    }
    return aluno

def converter_professor_dici(atribuir_professor):
    professor = {
        "id": atribuir_professor[0],
        "nome": atribuir_professor[1],
        "idade": atribuir_professor[2],
        "data_nascimento": atribuir_professor[3],
        "disciplina": atribuir_professor[4],
        "salario": atribuir_professor[5]
    }
    return professor

def converter_turma_dici(atribuir_turma):
    turma = {
        "id": atribuir_turma[0],
        "nome": atribuir_turma[1],
        "turno": atribuir_turma[2],
        "professor_id": atribuir_turma[3],
    }
    return turma

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

def media_final(nota1, nota2):
    return (nota1 + nota2) / 2
