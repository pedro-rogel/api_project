from flask import Blueprint, jsonify, request
from ..models.turmas_models import TurmaException, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, deletar_turma

turmas_bp = Blueprint("turmas", __name__)

@turmas_bp.route("/turmas", methods=['GET'])
def get_turmas():
    return jsonify(listar_turmas()), 200

@turmas_bp.route("/turmas/<int:id>", methods=['GET'])
def get_turma_id(id):
   try:
       return jsonify(data=turma_por_id(id)), 200
   except TurmaException as erro:
       return jsonify(erro=erro.msg), 400

@turmas_bp.route("/turmas", methods=['POST'])
def create_turma():
    data = request.json
    try:
        msg = adicionar_turma(data)
        return jsonify(data=data, mensagem=msg), 200
    except TurmaException as erro:
        return jsonify(erro=erro.msg), 400

@turmas_bp.route("/turmas/<int:id>", methods=['PUT'])
def update_turma(id):
    data = request.json
    try:
        msg = atualizar_turma(id, data)
        return jsonify(data=turma_por_id(id), mensagem=msg), 200
    except TurmaException as erro:
        return jsonify(erro=erro.msg), 400

@turmas_bp.route("/turmas/<int:id>", methods=['DELETE'])
def delete_turma(id):
    try:
        msg = deletar_turma(id)
        return jsonify(mensagem=msg), 200
    except TurmaException as erro:
        return jsonify(erro=erro.msg), 400
