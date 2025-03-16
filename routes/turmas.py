from flask import Blueprint, jsonify, request
from apis.entities import api_entidades

turmas_bp = Blueprint("turmas", __name__)

turmas = api_entidades["turmas"]

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
    nova_turma = request.json
    if not nova_turma.get("nome"):
        return jsonify(erro="turma sem nome"), 400
    if not any(turma["id"] == nova_turma["id"] for turma in turmas):
        turmas.append(nova_turma)
        return jsonify(message="criado com sucesso")
    return jsonify(erro="id ja utilizada"), 400

@turmas_bp.route("/turmas/<int:id>", methods=['PUT'])
def update_turma(id):
    for turma in turmas:
        if turma["id"] == id:
            atualizacao = request.json
            if not atualizacao.get("nome"):
                return jsonify(erro="turma sem nome"), 400
            turma["nome"] = atualizacao["nome"]
            return jsonify(message="atualizado com sucesso")
    return jsonify(erro="turma nao encontrada"), 400

@turmas_bp.route("/turmas/<int:id>", methods=['DELETE'])
def delete_turma(id):
    for turma in turmas:
        if turma["id"] == id:
            turmas.remove(turma)
            return jsonify(message="deletado com sucesso")
    return jsonify(erro="turma nao encontrada"), 400
