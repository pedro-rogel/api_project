from flask_restx import Resource, Namespace
from swagger.config import api
from apis.entidades import api_entidades
from controller.alunos_routes import *
ns_api = Namespace('API', description='API operations')

@ns_api.route('/datas')
class DataRoute(Resource):
    def get(self):
        return {
            "status_code": 200,
            "msg": "Sucesso",
            "data": api_entidades
        }