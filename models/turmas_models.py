from flask import Blueprint
from apis.entidades import *

turmas_bp = Blueprint("turmas", __name__)

turmas = api_entidades["turmas"]
professores = api_entidades["professores"]
class TurmaNaoEncontrada(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

def listar_turmas():
    return turmas

def get_turmas_id(id):
    for turma in turmas:
        if turma["id"] == id:
            return turma
    raise TurmaNaoEncontrada("Turma não encontrada")
    
def create_turma(nova_turma):
    if not professores:
        raise TurmaNaoEncontrada("Não há professores")
    if not nova_turma.get('id'):
         nova_turma['id'] = turmas[-1]["id"] + 1 if turmas else 1   
    if not nova_turma.get("nome"):
        raise TurmaNaoEncontrada("Turma sem nome") 
    if not nova_turma.get("turno"):
        raise TurmaNaoEncontrada("Turma sem turno") 
    if not nova_turma.get("descricao"):
        raise TurmaNaoEncontrada("Turma sem descrição")
    if not nova_turma.get("status"):
        raise TurmaNaoEncontrada("Turma sem status")
    if not nova_turma.get("professor_id"):
        raise TurmaNaoEncontrada("Turma sem id do professor") 
    else:
        if not any(professor["id"] == nova_turma["professor_id"] for professor in professores):
            raise TurmaNaoEncontrada("Id do professor não encontrado")
    if not any(turma["id"] == nova_turma["id"] for turma in turmas):
        obj_turma = Turma(nova_turma["id"], nova_turma['nome'], nova_turma['turno'], nova_turma['professor_id'], nova_turma['descricao'], nova_turma['status'])
        turmas.append(obj_turma.converter_turma_dici())
        return "criado com sucesso"
    raise TurmaNaoEncontrada("id turma já existente")
        
def update_turma_put(id, novos_dados):
    turma = get_turmas_id(id)
    if not turma:
        raise TurmaNaoEncontrada("Turma não criada")
    if not novos_dados.get("nome"):
        raise TurmaNaoEncontrada("Turma sem nome")
    if novos_dados.get("descricao"):
            turma['descricao'] = novos_dados['descricao']
    if novos_dados.get("status"):
        turma['status'] = novos_dados['status']
    turma["nome"] = novos_dados["nome"]
    if novos_dados.get("turno"):
        turma["turno"] = novos_dados["turno"]
    if novos_dados.get("professor_id"):
        if not any(professor["id"] == novos_dados["professor_id"] for professor in professores):
            raise TurmaNaoEncontrada("Id do professor não existente")
        turma["professor_id"] = novos_dados["professor_id"]
    if novos_dados.get("id"):
        turma['id'] = novos_dados['id']
    return "atualizado com sucesso"

def deletar_turma(id):
    turma = get_turmas_id(id)
    if not turma:
        raise TurmaNaoEncontrada("Turma não encontrada")
    turmas.remove(turma)