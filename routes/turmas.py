from flask import Blueprint, jsonify, request
from apis.entidades import api_entidades
from apis.classes_entidades import *

turmas_bp = Blueprint("turmas", __name__)

turmas = api_entidades["turmas"]
professores = api_entidades["professores"]

@turmas_bp.route("/turmas", methods=['GET'])
def get_turmas():
    return jsonify(turmas)

@turmas_bp.route("/turmas/<int:id>", methods=['GET'])
def get_turmas_id(id):
    for turma in turmas:
        if turma["id"] == id:
            return jsonify(turma)
    return jsonify(erro="turma nao encontrada"), 400

@turmas_bp.route("/turmas", methods=['POST'])
def create_turma():
    if not api_entidades['professores']:
        return jsonify(erro="Não há professores criados"),400
    nova_turma = request.json
    if not nova_turma.get('id'):
        nova_turma['id'] = turmas[-1]["id"] + 1 if turmas else 1   
    if not nova_turma.get("nome"):
        return jsonify(erro="turma sem nome"), 400
    if not nova_turma.get("turno"):
        return jsonify(erro="turma sem turno"), 400
    if not nova_turma.get("descricao"):
        return jsonify(erro="Turma sem descrição"),400
    if not nova_turma.get("status"):
        return jsonify(erro="turma sem status"), 400
    if not nova_turma.get("professor_id"):
        return jsonify(erro="turma sem professor"), 400
    else:
        if not any(professor["id"] == nova_turma["professor_id"] for professor in professores):
            return jsonify(erro="Id do professor não encontrado"), 400
    if not any(turma["id"] == nova_turma["id"] for turma in turmas):
        obj_turma = Turma(nova_turma["id"], nova_turma['nome'], nova_turma['turno'], nova_turma['professor_id'], nova_turma['descricao'], nova_turma['status'])
        turmas.append(obj_turma.converter_turma_dici())
        return jsonify(message="criado com sucesso")
    return jsonify(erro="id ja utilizada"), 400

@turmas_bp.route("/turmas/<int:id>", methods=['PUT'])
def update_turma(id):
    for turma in turmas:
        if turma["id"] == id:
            atualizacao = request.json
            if not atualizacao.get("nome"):
                return jsonify(erro="turma sem nome"), 400
            if atualizacao.get("descricao"):
                turma['descricao'] = atualizacao['descricao']
            if atualizacao.get("status"):
                turma['status'] = atualizacao['status']
            turma["nome"] = atualizacao["nome"]
            if atualizacao.get("turno"):
                turma["turno"] = atualizacao["turno"]
            if atualizacao.get("professor_id"):
                if not any(professor["id"] == atualizacao["professor_id"] for professor in professores):
                    return jsonify(erro="Id do professor não encontrado"), 400
                turma["professor_id"] = atualizacao["professor_id"]
            if atualizacao.get("id"):
                turma['id'] = atualizacao['id']
            return jsonify(message="atualizado com sucesso")
    return jsonify(erro="turma nao encontrada"), 400

@turmas_bp.route("/turmas/<int:id>", methods=['DELETE'])
def delete_turma(id):
    for turma in turmas:
        if turma["id"] == id:
            turmas.remove(turma)
            return jsonify(message="deletado com sucesso")
    return jsonify(erro="turma nao encontrada"), 400
