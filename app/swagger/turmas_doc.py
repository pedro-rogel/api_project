from flask_restx import Resource, Namespace, fields
from ..swagger import api
from ..models.turmas_models import TurmaException, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, deletar_turma

ns_api_turmas = Namespace('turmas', description='Operações rest relacionadas a Turmas')

modelo_turmas = ns_api_turmas.model('Turmas', {
    'nome': fields.String(required=True, description='Nome da Turma'),
    'turno': fields.String(required=True, description='Turno'),
    'descricao': fields.String(required=True, description='Descrição'),
    'status': fields.Boolean(required=True, description='Status da turma'),
    'professor_id': fields.Integer(required=True, description='Id do professor')
})

modelo_turmas_output = ns_api_turmas.model('TurmasOutPut', {
    'id': fields.Integer(description="Id da turma"),
    'nome': fields.String(description='Nome da Turma'),
    'turno': fields.String(description='Turno da turma'),
    'descricao': fields.String(description='Descrição da turma'),
    'status': fields.Boolean(description='Status da turma'),
    'professor_id': fields.Integer(description='Id do professor')
})

@ns_api_turmas.route('/turmasswagger')
class TurmasGetPost(Resource):
    @ns_api_turmas.response(200,'Turmas', modelo_turmas_output)
    def get(self):
        """Retorna todas as turmas cadastradas"""
        try:
            return {"data":listar_turmas()}, 200
        except TurmaException as erro:
            return {"error": erro.msg}
        
    @ns_api_turmas.expect(modelo_turmas)    
    def post(self):
        """Cria um nova turma"""
        data = api.payload
        try:
            msg = adicionar_turma(data)
            return {"data": data, "mensagem": msg}, 200
        except TurmaException as erro:
            return {"erro": erro.msg}, 400
    

@ns_api_turmas.route ('/turmasswagger/<int:id>')  
@ns_api_turmas.param('id', 'Id da turma')
class TurmasPorId(Resource):
    @ns_api_turmas.marshal_list_with(modelo_turmas_output)
    def get(self, id):
        """Retorna a turma pelo id passado"""
        try:
            return {"data": turma_por_id(id)}, 200
        except TurmaException as erro:
            return {"erro": erro.msg}, 400
        
    @ns_api_turmas.expect(modelo_turmas)
    def put(self, id):
        """Atualiza a turma pelo id passado"""
        data = api.payload
        try:
           msg = atualizar_turma(id, data)    
           return {"data": turma_por_id(id), "mensagem": msg}, 200
        except TurmaException as erro:
            return {"erro": erro.msg}, 400
        
    def delete(self, id):
        """Deleta a turma pelo id passado"""
        try:
            msg = deletar_turma(id)
            return {"mensagem": msg}, 200
        except TurmaException as erro:
            return {"erro": erro.msg}, 400
