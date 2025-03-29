from flask import Blueprint, jsonify, request
from models.turmas_models import TurmaNaoEncontrada, listar_turmas, get_turmas_id, create_turma, update_turma_put, deletar_turma

turmas_bp = Blueprint("turmas", __name__)

@turmas_bp.route("/turmas", methods=['GET'])
def get_turmas():
    return jsonify(listar_turmas()), 200

@turmas_bp.route("/turmas/<int:id>", methods=['GET'])
def listar_turmas_id(id):
   try:
       return jsonify(get_turmas_id(id)), 200
   except TurmaNaoEncontrada as erro:
       return jsonify(erro=erro.msg), 400

@turmas_bp.route("/turmas", methods=['POST'])
def create_turma_post():
    nova_turma = request.json
    try:
        create_turma(nova_turma)
        return jsonify(nova_turma), 200
    except TurmaNaoEncontrada as erro:
        return jsonify(error=erro.msg), 400

@turmas_bp.route("/turmas/<int:id>", methods=['PUT'])
def update_turma(id):
    atualizacao = request.json
    try:
        update_turma_put(id, atualizacao)
        return jsonify(get_turmas_id(id)), 200
    except TurmaNaoEncontrada as erro:
        return jsonify(erro=erro.msg), 400

@turmas_bp.route("/turmas/<int:id>", methods=['DELETE'])
def delete_turma(id):
    try:
        deletar_turma(id)
        return jsonify(message="Deletado com sucesso"), 200
    except TurmaNaoEncontrada as erro:
        return jsonify(erro=erro.msg)
