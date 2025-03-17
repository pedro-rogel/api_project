import json
import datetime


class Pessoa:
    def __init__(self, id, nome, data_de_nascimento):
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
        self.id = id

    def dateAge(self, birthDate):
        date = birthDate.split("/")
        if not len(date[0]) == 4:
            return
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        dateToday = datetime.date.today()
        if month < int(dateToday.month):
            idade = dateToday.year - year
        elif month == dateToday.month:
            if day <= dateToday.day:
                idade = dateToday.year - year
            else:
                idade = (dateToday.year - year) - 1
        else:
            idade = (dateToday.year - year) - 1
        return idade


class Aluno(Pessoa):
    def __init__(self, id, nome, data_de_nascimento, nota_primeiro_semestre, nota_segundo_semestre, turma_id):
        super().__init__(id, nome, data_de_nascimento)
        self.id = id
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
        self.__idade = self.dateAge(self.data_de_nascimento)
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.__media = (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2
        self.turma_id = turma_id

    def get(self):
        return [self.id, self.nome, self.__idade, self.data_de_nascimento, self.nota_primeiro_semestre, self.nota_segundo_semestre, self.__media, self.turma_id]


class Professor(Pessoa):
    def __init__(self, id, nome, data_de_nascimento, disciplina, salario):
        super().__init__(id, nome, data_de_nascimento)
        self.id = id
        self.nome = nome
        self.idade = self.dateAge(self.data_de_nascimento)
        self.data_de_nascimento = data_de_nascimento
        self.disciplina = disciplina
        self.salario = salario

    def get(self):
        return [self.id, self.nome, self.idade, self.data_de_nascimento, self.disciplina, self.salario]


class Turma():
    def __init__(self, id, nome, turno, professor_id):
        self.id = id
        self.nome = nome
        self.turno = turno
        self.professor_id = professor_id

    def get(self):
        return [self.id, self.nome, self.turno, self.professor_id]


api_entidades = {
    "Alunos": [

    ],
    "Professores": [

    ],
    "Turmas": [

    ]
}


aluno_test = Aluno(
    100,
    "Felipe Santos",
    "2003/03/18", 
    7.5, 
    10.0, 
    100,
)

professor_test = Professor(
    100,
    "João Augusto",
    "1975/10/20",
    "Desenvolvimento Web",
    5000.0
)

turma_test = Turma(
    100,
    "ADS",
    "Noite",
    100
)


def converter_aluno_dici(descompactando):
    aluno = {
        "id": descompactando[0],
        "nome": descompactando[1],
        "idade": descompactando[2],
        "data_nascimento": descompactando[3],
        "nota_primeiro_semestre": descompactando[4],
        "nota_segundo_semestre": descompactando[5],
        "media_final": descompactando[6],
        "turma_id": descompactando[7]
    }
    return aluno

def converter_professor_dici(descompactando):
    professor = {
        "id": descompactando[0],
        "nome": descompactando[1],
        "idade": descompactando[2],
        "data_nascimento": descompactando[3],
        "disciplina": descompactando[4],
        "salario": descompactando[5]
    }
    return professor

def converter_turma_dici(descompactando):
    turma = {
        "id": descompactando[0],
        "nome": descompactando[1],
        "turma": descompactando[2],
        "professor_id": descompactando[3],
    }
    return turma


def output_json(entidades):
    return json.dumps(entidades, indent=4, ensure_ascii=False)


api_entidades["Alunos"].append(converter_aluno_dici(aluno_test.get()))
api_entidades["Professores"].append(converter_professor_dici(professor_test.get()))
api_entidades["Turmas"].append(converter_turma_dici(aluno_test.get()))

print(output_json(api_entidades))
