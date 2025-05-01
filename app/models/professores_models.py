from app import db
from ..entities import Professores, Turmas
from ..utils import DataException, calcular_idade, verificar_data

class ProfessorException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

def listar_professores():
    professores = Professores.query.all()
    return [professor.to_dict() for professor in professores]

def professor_por_id(id_professor):
    professor = Professores.query.get(id_professor)
    if not professor:
        raise ProfessorException("Professor nao encontrado")
    return professor.to_dict()
    
def adicionar_professor(professor_data):
    if not professor_data.get("nome"):
        raise ProfessorException("Professor sem nome") 
    if not professor_data.get("data_nascimento"):
        raise ProfessorException("Professor sem data de nascimento")
    else:
        try:
            data_nasc = verificar_data(professor_data["data_nascimento"])
            if data_nasc is True:
                data_nasc = professor_data["data_nascimento"]
        except DataException as e:
            raise ProfessorException(str(e))
    if not professor_data.get("disciplina"):
        raise ProfessorException("Professor sem disciplina")
    if not professor_data.get("salario"):
        raise ProfessorException("Professor sem salario")
    else:
        salario = professor_data["salario"]
        try:
            salario = float(salario)
        except ValueError:
            raise ProfessorException("Digite apenas valores numericos no salario")
    if not professor_data.get("descricao"):
        raise ProfessorException("Professor sem descricao")
    novo_professor = Professores(
        nome=professor_data["nome"],
        data_nascimento=data_nasc,
        disciplina=professor_data["disciplina"],
        salario=salario,
        descricao=professor_data["descricao"])
    db.session.add(novo_professor)
    db.session.commit()
    return "Professor criado com sucesso"

def atualizar_professor(id_professor, professor_data):
    professor = Professores.query.get(id_professor)
    if not professor:
        raise ProfessorException("Professor nao encontrado")
    if not professor_data.get("nome"):
        raise ProfessorException("Professor sem nome")
    professor.nome = professor_data["nome"]
    if professor_data.get("data_nascimento"):
        try:
            data_nascimento = verificar_data(professor_data["data_nascimento"])
            if data_nascimento is True:
                professor.data_nascimento = professor_data["data_nascimento"]
                professor.idade = calcular_idade(professor_data["data_nascimento"])
        except DataException as e:
            raise ProfessorException(str(e))
    if professor_data.get("salario"):
        salario = professor_data["salario"]
        try:
            novo_salario = float(salario)
            professor.salario = novo_salario
        except ValueError:
            raise ProfessorException("Digite apenas valores numericos no salario")
    if professor_data.get("discipina"):
        professor.disciplina = professor_data["disciplina"]
    if professor_data.get("descricao"):
        professor.descricao = professor_data["descricao"]
    db.session.commit()
    return "Professor atualizado com sucesso"
    
def deletar_professor(id_professor):
    professor = Professores.query.get(id_professor)
    if not professor:
        raise ProfessorException("Professor nao encontrado")
    turmas = Turmas.query.filter_by(professor_id=id_professor).all()
    turmas_deletadas = []
    for turma in turmas:
        turmas_deletadas.append(turma.id)
        db.session.delete(turma)
    db.session.delete(professor)
    db.session.commit()
    if turmas_deletadas:
        ids_formatados = ', '.join([str(turma_id) for turma_id in turmas_deletadas])
        return f"Professor deletado com sucesso. ID das turmas removidas: [{ids_formatados}]"
    else:
        return "Professor deletado com sucesso. Nenhuma turma assoaciada"
