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

@ns_api_professores.route('/professoresswagger')
class ProfessoresGetPost(Resource):
    @ns_api_professores.response(200,"Código", model_professores_output)
    def get(self):
        """Retorna todos os professores cadastrados"""
        try:
            return {"data" : listar_professores()}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400
    
    @ns_api_professores.expect(model_professores)
    def post(self):
        """Cria um novo professor"""
        data = api.payload
        try:
            msg = adicionar_professor(data)
            return {"data": data, "mensagem": msg}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400
        
@ns_api_professores.route('/professoresswagger/<int:id>')
@ns_api_professores.param('id', 'Id do Professor')
class ProfessorPorId(Resource):
    @ns_api_professores.marshal_list_with(model_professores_output)
    def get(self, id):
        """Retorna um professor pelo id passado"""
        try:
            return {"data": professor_por_id(id)}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400  
    
    @ns_api_professores.expect(model_professores)
    def put(self, id):
        """Atualiza o professor pelo id passado"""
        data = api.payload
        try: 
            msg = atualizar_professor(id, data)
            return {"data": professor_por_id(id), "mensagem": msg}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400
    

    def delete(self, id):
        """Deleta o professor pelo id passado"""
        try:
            msg = deletar_professor(id)
            return {"data": msg}, 200
        except ProfessorException as erro:
            return {"erro": erro.msg}, 400
