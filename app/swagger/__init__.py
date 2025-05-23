from flask_restx import Api
from flask import Blueprint

swagger_bp = Blueprint("swagger_bp", __name__, url_prefix="/doc")

api = Api(
    swagger_bp,
    title="School System Swagger",
    description="Documentação da API",
    doc="/"
)

from ..swagger.alunos_doc import ns_api_alunos
from ..swagger.professores_doc import ns_api_professores
from ..swagger.turmas_doc import ns_api_turmas

api.add_namespace(ns_api_alunos)
api.add_namespace(ns_api_professores)
api.add_namespace(ns_api_turmas)
