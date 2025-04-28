from flask import Blueprint, jsonify, request
from ..models.professores_models import ProfessorException, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, deletar_professor

professores_bp = Blueprint("professores", __name__)
  
@professores_bp.route("/professores", methods=['GET'])
def get_professores():
    return jsonify(listar_professores()), 200

@professores_bp.route("/professores/<int:id>", methods=['GET'])
def get_professor_id(id):
    try: 
        return jsonify(professor_por_id(id)), 200
    except ProfessorException as erro:
        return jsonify(erro.msg), 400

@professores_bp.route("/professores", methods=['POST'])
def create_professor():
    data = request.json
    try:
        msg = adicionar_professor(data)
        return jsonify(data, mensagem=msg), 200
    except ProfessorException as erro:
        return jsonify(erro=erro.msg), 400

@professores_bp.route("/professores/<int:id>", methods=['PUT'])
def update_professor(id):
    data = request.json
    try:
        msg = atualizar_professor(id, data)
        return jsonify(professor_por_id(id), mensagem=msg), 200
    except ProfessorException as erro:
        return jsonify(erro=erro.msg), 400

@professores_bp.route("/professores/<int:id>", methods=['DELETE'])
def delete_professor(id):
    try:
        msg = deletar_professor(id)
        return jsonify(mensagem=msg), 200
    except ProfessorException as erro:
        return jsonify(erro=erro.msg), 400
