from flask import Blueprint, jsonify, request
from apis.entidades import *

professores_bp = Blueprint("professores", __name__)

professores = api_entidades["professores"]

class ProfessorNaoEncontrado(Exception):
    pass

def listar_professores():
    return professores

def professor_por_id(id_professor):
    for professor in professores:
        if professor['id'] == id_professor:
            return professor
        raise ProfessorNaoEncontrado
    
def adicionar_professor(novo_professor):
    if not novo_professor.get('id'):
        novo_professor['id'] = professores[-1]["id"] + 1 if professores else 1
    if not novo_professor.get("nome"):
        return "professor sem nome", 
    if not novo_professor.get("data_nascimento"):
        return "professor sem data de nascimento", 
    if not novo_professor.get("disciplina"):
        return "professor sem disciplina", 
    if not novo_professor.get("descricao"):
        return "professor sem descrição", 
    if not novo_professor.get("salario"):
        return "professor sem salario", 
    if not any(professor["id"] == novo_professor["id"] for professor in professores):
        obj_professor = Professor(novo_professor["id"], novo_professor['nome'], novo_professor['data_nascimento'], novo_professor['disciplina'], novo_professor['salario'], novo_professor['descricao'])
        professores.append(obj_professor.converter_professor_dici())
        return "criado com sucesso"
    return "id ja utilizada"

def update_professor(id, novos_dados):
    professor = professor_por_id(id)
    if not novos_dados.get("nome"):
        return "professor sem nome"
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
    return "professor nao encontrado"

def delete_professor(id):
    for professor in professores:
        if professor["id"] == id:
            professores.remove(professor)
            return "deletado com sucesso"
    return "professor nao encontrado"

