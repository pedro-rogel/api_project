from flask import Blueprint
from apis.entidades import *

professores_bp = Blueprint("professores", __name__)

professores = api_entidades["professores"]

class ProfessorNaoEncontrado(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

def listar_professores():
    return professores

def professor_por_id(id_professor):
    for professor in professores:
        if professor['id'] == id_professor:
            return professor
        raise ProfessorNaoEncontrado("Professor não foi criado")
    
def adicionar_professor_post(novo_professor):
    if not novo_professor.get('id'):
        novo_professor['id'] = professores[-1]["id"] + 1 if professores else 1
    if not novo_professor.get("nome"):
        raise ProfessorNaoEncontrado("Professor sem nome") 
    if not novo_professor.get("data_nascimento"):
        raise ProfessorNaoEncontrado("Professor sem data de nascimento") 
    if not novo_professor.get("disciplina"):
        raise ProfessorNaoEncontrado("Professor sem disciplina")
    if not novo_professor.get("descricao"):
        raise ProfessorNaoEncontrado("Professor sem descrição") 
    if not novo_professor.get("salario"):
        raise ProfessorNaoEncontrado("Professor sem salario") 
    if not any(professor["id"] == novo_professor["id"] for professor in professores):
        obj_professor = Professor(novo_professor["id"], novo_professor['nome'], novo_professor['data_nascimento'], novo_professor['disciplina'], novo_professor['salario'], novo_professor['descricao'])
        professores.append(obj_professor.converter_professor_dici())
        return "criado com sucesso"
    raise ProfessorNaoEncontrado("Id já utilizado")

def update_professor_put(id, novos_dados):
    professor = professor_por_id(id)
    if not professor:
        raise ProfessorNaoEncontrado("Professor nao criado")
    if not novos_dados.get("nome"):
        raise ProfessorNaoEncontrado("Professor sem nome")
    professor["nome"] = novos_dados["nome"]
    if novos_dados.get("id"):
        professor['id'] = novos_dados['id']
    if novos_dados.get("data_nascimento"):
        professor["data_nascimento"] = novos_dados['data_nascimento']
        professor["idade"] = atribuir_idade(professor['data_nascimento'])
    if novos_dados.get("salario"):
        professor["salario"] = novos_dados["salario"]
    if novos_dados.get("discipina"):
        professor["disciplina"] = novos_dados["disciplina"]
    if novos_dados.get("descricao"):
        professor["descricao"] = novos_dados["descricao"]
        return "atualizado com sucesso"
    

def delete_professor_delete(id):
    professor = professor_por_id(id)
    if not professor:
        raise ProfessorNaoEncontrado("Professor não criado")
    professores.remove(professor)
    return "deletado com sucesso"

