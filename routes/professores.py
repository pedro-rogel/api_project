from flask import Blueprint, jsonify, request
from apis.entidades import api_entidades
from apis.classes_entidades import *

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
    return jsonify(erro="professor nao encontrado"), 400

@professores_bp.route("/professores", methods=['POST'])
def create_professor():
    novo_professor = request.json
    if not novo_professor.get("id"):
        return jsonify(erro="professor sem id"), 400
    if not novo_professor.get("nome"):
        return jsonify(erro="professor sem nome"), 400
    if not novo_professor.get("data_nascimento"):
        return jsonify(erro="professor sem data de nascimento"), 400
    if not novo_professor.get("disciplina"):
        return jsonify(erro="professor sem disciplina"), 400
    if not novo_professor.get("salario"):
        return jsonify(erro="professor sem salario"), 400
    if not any(professor["id"] == novo_professor["id"] for professor in professores):
        obj_professor = Professor(novo_professor["id"], novo_professor['nome'], novo_professor['data_nascimento'], novo_professor['disciplina'], novo_professor['salario'])
        professores.append(converter_professor_dici(obj_professor.get()))
        return jsonify(message="criado com sucesso")
    return jsonify(erro="id ja utilizada"), 400

@professores_bp.route("/professores/<int:id>", methods=['PUT'])
def update_professor(id):
    for professor in professores:
        if professor["id"] == id:
            atualizacao = request.json
            if not atualizacao.get("nome"):
                return jsonify(erro="professor sem nome"), 400
            professor["nome"] = atualizacao["nome"]
            if atualizacao.get("data_nascimento"):
                professor["data_nascimento"] = atualizacao['data_nascimento']
                professor["idade"] = atribuir_idade(professor['data_nascimento'])
            if atualizacao.get("salario"):
                professor["salario"] = atualizacao["salario"]
            if atualizacao.get("discipina"):
                professor["disciplina"] = atualizacao["disciplina"]
            return jsonify(message="atualizado com sucesso")
    return jsonify(erro="professor nao encontrado"), 400

@professores_bp.route("/professores/<int:id>", methods=['DELETE'])
def delete_professor(id):
    for professor in professores:
        if professor["id"] == id:
            professores.remove(professor)
            return jsonify(message="deletado com sucesso")
    return jsonify(erro="professor nao encontrado"), 400
