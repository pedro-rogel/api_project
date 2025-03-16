from flask import Blueprint, jsonify, request
from apis.entities import api_entidades

professores_bp = Blueprint("professores", __name__)

professores = api_entidades["professores"]

@professores_bp.route("/professores", methods=['GET'])
def get_professores():
    return jsonify(professores)

@professores_bp.route("/professores/<int:id>", methods=['GET'])
def get_professor_id(id):
    for professor in professores:
        if professor["id"] == id:
            return jsonify(professor)
    return jsonify({"erro":"professor nao encontrado"}), 400

@professores_bp.route("/professores", methods=['POST'])
def create_professor():
    novo_professor = request.json
    if not novo_professor.get("nome"):
        return jsonify({"erro":"professor sem nome"}), 400
    if not any(professor["id"] == novo_professor["id"] for professor in professores):
        professores.append(novo_professor)
        return jsonify(message="criado com sucesso")
    return jsonify({"erro":"id ja utilizada"}), 400

@professores_bp.route("/professores/<int:id>", methods=['PUT'])
def update_professor(id):
    for professor in professores:
        if professor["id"] == id:
            atualizar_nome = request.json
            if not atualizar_nome.get("nome"):
                return jsonify({"erro":"professor sem nome"}), 400
            professor["nome"] = atualizar_nome["nome"]
            return jsonify(message="atualizado com sucesso")
    return jsonify({"erro":"professor nao encontrado"}), 400

@professores_bp.route("/professores/<int:id>", methods=['DELETE'])
def delete_professor(id):
    for professor in professores:
        if professor["id"] == id:
            professores.remove(professor)
            return jsonify(message="deletado com sucesso")
    return jsonify({"erro":"professor nao encontrado"}), 400
