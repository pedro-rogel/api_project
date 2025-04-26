from app import db
from ..utils import calcular_idade

class Professores(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    idade = db.Column(db.Integer)
    disciplina = db.Column(db.String(50), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(150), nullable=True)

    def __init__(self, nome, data_nascimento, disciplina, salario, descricao):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.idade = calcular_idade(data_nascimento)
        self.disciplina = disciplina
        self. salario = salario
        self.descricao = descricao

    def to_dict(self):
        return {
           "id": self.id,
           "nome": self.nome,
           "data_nascimento": self.data_nascimento,
           "idade": self.idade,
           "disciplina": self.disciplina,
           "salario": self.salario,
           "descricao": self.descricao
        }
