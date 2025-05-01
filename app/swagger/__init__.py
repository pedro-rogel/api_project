from flask_restx import Api

api = Api(
    title="School System Swagger",
    description="Documentação da API",
    doc="/doc"
)

from ..swagger.alunos_doc import ns_api_alunos
from ..swagger.professores_doc import ns_api_professores
from ..swagger.turmas_doc import ns_api_turmas

api.add_namespace(ns_api_alunos)
api.add_namespace(ns_api_professores)
api.add_namespace(ns_api_turmas)
