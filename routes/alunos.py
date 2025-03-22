from flask import Blueprint, jsonify, request
from apis.entidades import *

alunos_bp = Blueprint("alunos", __name__)

alunos = api_entidades["alunos"]
turmas = api_entidades['turmas']

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
    if not api_entidades['turmas']:
        return jsonify(erro="Não há turmas criadas"),400
    novo_aluno = request.json
    if not novo_aluno.get('id'):
        novo_aluno['id'] = alunos[-1]["id"] + 1 if alunos else 1   
    if not novo_aluno.get("nome"):
        return jsonify(erro="aluno sem nome"), 400
    if not novo_aluno.get("nota_primeiro_semestre"):
        return jsonify(erro="aluno sem primeira nota"), 400
    if novo_aluno['nota_primeiro_semestre'] > 10 or novo_aluno['nota_primeiro_semestre'] < 0:
        return jsonify(erro='Nota primeiro semestre inválida'), 400
    if not novo_aluno.get("nota_segundo_semestre"):
        return jsonify(erro="aluno sem segunda nota"), 400
    if novo_aluno['nota_segundo_semestre'] > 10 or novo_aluno['nota_segundo_semestre'] < 0:
        return jsonify(erro='Nota segundo semestre inválida'), 400
    if not novo_aluno.get("turma_id"):
        return jsonify(erro="aluno sem turma"), 400
    else:
        if not any(turma["id"] == novo_aluno["turma_id"] for turma in turmas):
            return jsonify(erro="Id da turma não encontrado"), 400
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
                if 0 <= atualizacao['nota_primeiro_semestre'] <= 10:
                    aluno['nota_primeiro_semestre'] = atualizacao['nota_primeiro_semestre']
                else:
                    return jsonify(erro='Nota primeiro semestre inválida'), 400
            if atualizacao.get("nota_segundo_semestre"):
                if 0 <= atualizacao['nota_segundo_semestre'] <= 10:
                    aluno['nota_segundo_semestre'] = atualizacao['nota_segundo_semestre']
                else:
                    return jsonify(erro='Nota segundo semestre inválida'), 400
                aluno['nota_segundo_semestre'] = atualizacao['nota_segundo_semestre']
            if atualizacao.get("turma_id"):
                if any(turma["id"] == atualizacao["turma_id"] for turma in turmas):
                    aluno["turma_id"] = atualizacao["turma_id"]
                else:
                    return jsonify(erro="Id da turma não encontrado"), 400           
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


