from flask import Blueprint, jsonify, request
from apis.entidades import api_entidades
from apis.classes_entidades import *

alunos_bp = Blueprint("alunos", __name__)

alunos = api_entidades["alunos"]

@alunos_bp.route("/alunos", methods=['GET'])
def get_student():
    return jsonify(alunos)

@alunos_bp.route("/alunos/<int:id>", methods=['GET'])
def get_student_id(id):
    for aluno in alunos:
        if aluno["id"] == id:
            return jsonify(aluno)
    return jsonify(erro="aluno nao encontrado"), 400

@alunos_bp.route("/alunos", methods=['POST'])
def create_student():
    novo_aluno = request.json
    if not novo_aluno.get("id"):
        return jsonify(erro="aluno sem id"), 400
    if not novo_aluno.get("nome"):
        return jsonify(erro="aluno sem nome"), 400
    if not novo_aluno.get("nota_primeiro_semestre"):
        return jsonify(erro="aluno sem primeira nota"), 400
    if not novo_aluno.get("nota_segundo_semestre"):
        return jsonify(erro="aluno sem segunda nota"), 400
    if not novo_aluno.get("turma_id"):
        return jsonify(erro="aluno sem turma"), 400
    if novo_aluno.get("data_nascimento"):
        split = novo_aluno.get("data_nascimento").split('/')
        if not len(split[0]) == 4:
            return jsonify(erro="formato da data incorreto, passe no formato 'YYYY/MM/DD"), 400
    else:
         return jsonify(erro="aluno sem data de nascimento"),400
    if not any(aluno["id"] == novo_aluno["id"] for aluno in alunos):
        obj_aluno = Aluno(novo_aluno["id"], novo_aluno['nome'], novo_aluno['data_nascimento'], novo_aluno['nota_primeiro_semestre'], novo_aluno['nota_segundo_semestre'], novo_aluno['turma_id'])
        alunos.append(obj_aluno.converter_aluno_dici())
        return jsonify(message="criado com sucesso")
    return jsonify(erro="id ja utilizada"), 400

@alunos_bp.route("/alunos/<int:id>", methods=['PUT'])
def update_student(id):
    for aluno in alunos:
        if aluno["id"] == id:
            atualizacao = request.json
            if not atualizacao.get("nome"):
                return jsonify(erro="aluno sem nome"), 400
            aluno["nome"] = atualizacao["nome"]
            if atualizacao.get("data_nascimento"):
                aluno['data_nascimento'] = atualizacao['data_nascimento']
                aluno['idade'] = atribuir_idade(aluno['data_nascimento'])
            if atualizacao.get("nota_primeiro_semestre"):
                aluno['nota_primeiro_semestre'] = atualizacao['nota_primeiro_semestre']
            if atualizacao.get("nota_segundo_semestre"):
                aluno['nota_segundo_semestre'] = atualizacao['nota_segundo_semestre']
            aluno['media_final'] = media(aluno['nota_primeiro_semestre'], aluno['nota_segundo_semestre'] )
            return jsonify(message="atualizado com sucesso")
    return jsonify(erro="aluno nao encontrado"), 400

@alunos_bp.route("/alunos/<int:id>", methods=['DELETE'])
def delete_student(id):
    for aluno in alunos:
        if aluno["id"] == id:
            alunos.remove(aluno)
            return jsonify(message="deletado com sucesso")
    return jsonify(erro="aluno nao encontrado"), 400
