from flask import Blueprint, jsonify, request
from ..models.alunos_models import AlunoException, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, deletar_aluno

alunos_bp = Blueprint("alunos", __name__)

@alunos_bp.route("/alunos", methods=['GET'])
def get_alunos():
    return jsonify(listar_alunos()), 200

@alunos_bp.route("/alunos/<int:id>", methods=['GET'])
def get_aluno_id(id):
    try:
        return jsonify(data=aluno_por_id(id)), 200
    except AlunoException as erro:
        return jsonify(erro=erro.msg), 400

@alunos_bp.route("/alunos", methods=['POST'])
def create_aluno():
    data = request.json
    try:
        msg = adicionar_aluno(data)
        return jsonify(data=data, mensagem=msg), 200
    except AlunoException as erro:
        return jsonify(erro=erro.msg), 400

@alunos_bp.route("/alunos/<int:id>", methods=['PUT'])
def update_aluno(id):
    data = request.json
    try:
        msg = atualizar_aluno(id, data)
        return jsonify(data=aluno_por_id(id), mensagem=msg), 200
    except AlunoException as erro:
        return jsonify(erro=erro.msg), 400

@alunos_bp.route("/alunos/<int:id>", methods=['DELETE'])
def delete_aluno(id):
    try:
        msg = deletar_aluno(id)
        return jsonify(mensagem=msg), 200
    except AlunoException as erro:
        return jsonify(erro=erro.msg), 400
