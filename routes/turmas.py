from flask import Blueprint, jsonify, request
from apis.entities import api_entidades

turmas_bp = Blueprint("turmas", __name__)

turmas = api_entidades["turmas"]

@turmas_bp.route("/turmas", methods=['GET'])
def get_turmas():
    return jsonify(turmas)
