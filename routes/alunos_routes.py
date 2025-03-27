from flask import Blueprint, jsonify, request
from models.alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno

alunos_bp = Blueprint("alunos", __name__)

@alunos_bp.route("/alunos", methods=['GET'])
def get_student():
    return jsonify(listar_alunos())

@alunos_bp.route("/alunos/<int:id>", methods=['GET'])
def get_student_id(id):
    try:
        aluno = aluno_por_id(id)
        return jsonify(aluno)
    except AlunoNaoEncontrado as erro:
        return jsonify(erro=erro.msg), 400

@alunos_bp.route("/alunos", methods=['POST'])
def create_student():
    data = request.json
    try:
        adicionar_aluno(data)
        return jsonify(data)
    except AlunoNaoEncontrado as erro:
        return jsonify(erro=erro.msg), 400

@alunos_bp.route("/alunos/<int:id>", methods=['PUT'])
def update_student(id):
    data = request.json
    try:
        atualizar_aluno(id, data)
        return jsonify(aluno_por_id(id))
    except AlunoNaoEncontrado as erro:
        return jsonify(erro=erro.msg), 400

@alunos_bp.route("/alunos/<int:id>", methods=['DELETE'])
def delete_student(id):
    try:
        excluir_aluno(id)
        return jsonify(message="deletado com sucesso")
    except AlunoNaoEncontrado as erro:
        return jsonify(erro=erro.msg), 400
