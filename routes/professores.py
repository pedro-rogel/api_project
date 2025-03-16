from flask import Blueprint, jsonify, request
from apis.entities import api_entidades

professores_bp = Blueprint("professores", __name__)

professores = api_entidades["professores"]

@professores_bp.route("/professores", methods=['GET'])
def get_professores():
    return jsonify(professores)
