from flask import Blueprint, jsonify, request
from models.professores_model import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor_post, update_professor_put,delete_professor_delete

professores_bp = Blueprint("professores", __name__)
  
@professores_bp.route("/professores", methods=['GET'])
def get_professores():
    return jsonify(listar_professores()), 200

@professores_bp.route("/professores/<int:id>", methods=['GET'])
def get_professor_id(id):
    try: 
        return jsonify(professor_por_id(id)), 200
    except ProfessorNaoEncontrado as erro:
        return jsonify(erro=erro.msg), 400

@professores_bp.route("/professores", methods=['POST'])
def create_professor():
    novo_professor = request.json
    try:
        adicionar_professor_post(novo_professor)
        return jsonify(novo_professor), 200
    except ProfessorNaoEncontrado as erro:
        return jsonify(erro=erro.msg), 400

@professores_bp.route("/professores/<int:id>", methods=['PUT'])
def atualizar_professor(id):
    atualizacao = request.json
    try:
        update_professor_put(id, atualizacao)
        return jsonify(professor_por_id(id)), 200
    except ProfessorNaoEncontrado as erro:
        return jsonify(erro=erro.msg), 400

@professores_bp.route("/professores/<int:id>", methods=['DELETE'])
def deletar_professor(id):
    try:
        delete_professor_delete(id)
        return jsonify(message="Deletado com sucesso"), 200
    except ProfessorNaoEncontrado as erro:
        return jsonify(erro=erro.msg), 400
