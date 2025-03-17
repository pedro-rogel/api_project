import json
from entities_test import *

api_entidades = {
    "Alunos": [

    ],
    "Professores": [

    ],
    "Turmas": [

    ]
}

def output_json(entidades):
    return json.dumps(entidades, indent=4, ensure_ascii=False)

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

api_entidades["Alunos"].append(converter_aluno_dici(aluno_test.get()))
api_entidades["Professores"].append(converter_professor_dici(professor_test.get()))
api_entidades["Turmas"].append(converter_turma_dici(aluno_test.get()))

print(output_json(api_entidades))
