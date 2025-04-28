from flask_restx import Resource, Namespace, fields
from ..swagger import api
from ..models.alunos_models import AlunoException, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, deletar_aluno

ns_api_alunos = Namespace("alunos", description="Operações rest relacionadas aos Alunos")

modelo_aluno = ns_api_alunos.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento no formato 'YYYY/MM/DD'"),
    "nota_primeiro_semestre": fields.Float(required=True, description="Nota do 1º semestre"),
    "nota_segundo_semestre": fields.Float(required=True, description="Nota do 2º semestre"),
    "turma_id": fields.Integer(required=True, description="ID da turma")
})

modelo_aluno_output = ns_api_alunos.model("AlunoOutPut", {
    "id": fields.Integer(description="Id do Aluno"),
    "nome": fields.String(description="Nome do aluno"),
    "data_nascimento": fields.String(description="Data de nascimento no formato 'YYYY/MM/DD'"),
    "idade": fields.String(description='Idade'),
    "nota_primeiro_semestre": fields.Float(description="Nota do 1º semestre"),
    "nota_segundo_semestre": fields.Float(description="Nota do 2º semestre"),
    "media_final": fields.Float(description="Média final do aluno"),
    "turma_id": fields.Integer(description="ID da turma")
})

@ns_api_alunos.route('/')
class AlunosGetPost(Resource):
    @ns_api_alunos.response(200, "Alunos", modelo_aluno_output)
    def get(self):
        """Retorna todos os alunos cadastrados"""
        return {"data": listar_alunos()}, 200
    
    @ns_api_alunos.expect(modelo_aluno)
    def post(self):
        """Cria um aluno"""
        data = api.payload
        try:
            msg = adicionar_aluno(data)
            return {"data": data, "mensagem": msg}, 200
        except AlunoException as erro:
            return {"erro": erro.msg}, 400
    

@ns_api_alunos.route("/<int:id>")
@ns_api_alunos.param("id", "Id do aluno")
class AlunosPorId(Resource):
    @ns_api_alunos.marshal_list_with(modelo_aluno_output)
    def get(self, id):
        """Retorna o aluno pelo id passado"""
        try:
            return {"data": aluno_por_id(id)}, 200           
        except AlunoException as erro:
            return {"erro": erro.msg}, 400
    
    @ns_api_alunos.expect(modelo_aluno)
    def put(self, id):
        """ATualiza o aluno pelo id passado"""
        data = api.payload
        try:
            msg = atualizar_aluno(id,data)
            return {"data": aluno_por_id(id), "mensagem": msg}, 200
        except AlunoException as erro:
            return {"erro": erro.msg}, 400
        
    def delete(self, id):
        """Deleta um aluno pelo id passado"""
        try:
            msg = deletar_aluno(id)
            return {"data": msg}, 200
        except AlunoException as erro:
            return {"erro": erro.msg}, 400
        
    