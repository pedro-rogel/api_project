from flask_restx import Resource, Namespace, fields
from ..swagger import api
from ..models.professores_models import ProfessorException, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, deletar_professor

ns_api_professores = Namespace('professores', description='Operações rest relacionadas aos Professores')

model_professores = ns_api_professores.model("Professores", {
    "nome": fields.String(required=True, description="Nome do Professor"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento no formato 'YYYY/MM/DD'"),
    "disciplina": fields.String(required=True, description="Nome da Disciplina"),
    "salario": fields.Float(required=True, description="Salario do Professor"),
    "descricao": fields.String(required=True, description="Descricao do Professor"),
})

model_professores_output = ns_api_professores.model("ProfessoresOutPut", {
    "id": fields.Integer(description="Id do Professor"),
    "nome": fields.String(description="Nome do Professor"),
    "data_nascimento": fields.String(description="Data de nascimento no formato 'YYYY/MM/DD'"),
    "idade": fields.Integer(description="Idade do Professor"),
    "disciplina": fields.String(description="Nome da Disciplina"),
    "salario": fields.Float(description="Salario do Professor"),
    "descricao": fields.String(description="Descrição do Professor"),
})

@ns_api_professores.route('/')
class ProfessoresGetPost(Resource):
    @ns_api_professores.response(200,"Código", model_professores)
    def get(self):
        try:
            return {listar_professores()}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400
    
    @ns_api_professores.expect(model_professores)
    @ns_api_professores.doc(description="Cria um novo professor")  
    def post(self):
        data = api.payload
        try:
            msg = adicionar_professor(data)
            return {"data": data, "mensagem": msg}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400
        
@ns_api_professores.expect(model_professores_output)
@ns_api_professores.route('/<int:id>')
@ns_api_professores.param('id', 'Id do Professor')
class ProfessorPorId(Resource):
    @ns_api_professores.response(200, "Professores CRUD", model_professores)
    @ns_api_professores.doc(description="Retorna o professor pelo id")
    def get(self, id):
        try:
            return {"data": professor_por_id(id)}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400  
    
    @ns_api_professores.expect(model_professores)
    @ns_api_professores.doc(description="Atualiza os dados do professor pelo id")
    def put(self, id):
        data = api.payload
        try: 
            msg = atualizar_professor(id, data)
            return {"data": professor_por_id(id), "mensagem": msg}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400
    
    @ns_api_professores.doc(description="Deleta o professor pelo id")    
    def delete(self, id):
        try:
            msg = deletar_professor(id)
            return {"data": msg}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400
