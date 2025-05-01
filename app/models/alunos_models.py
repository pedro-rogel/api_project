from app import db
from ..entities import Alunos, Turmas
from ..utils import DataException, calcular_idade, verificar_data

class AlunoException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

def listar_alunos():
    alunos = Alunos.query.all()
    return [aluno.to_dict() for aluno in alunos]

def aluno_por_id(id_aluno):
    aluno = Alunos.query.get(id_aluno)
    if not aluno:
        raise AlunoException("Aluno nao encontrado")
    return aluno.to_dict()

def adicionar_aluno(aluno_data):
    turmas = Turmas.query.all()
    if not turmas:
        raise AlunoException("Nao ha turmas para criar alunos") 
    if not aluno_data.get("nome"):
         raise AlunoException("Aluno sem nome")
    if not aluno_data.get("data_nascimento"):
        raise AlunoException("Aluno sem data de nascimento")
    else:
        try:
            data_nasc = verificar_data(aluno_data["data_nascimento"])
            if data_nasc is True:
                data_nasc = aluno_data["data_nascimento"]
        except DataException as e:
            raise AlunoException(str(e))
    try:
        if not aluno_data.get("nota_primeiro_semestre"):
            raise AlunoException("Aluno sem primeira nota")
        if not 0 <= aluno_data["nota_primeiro_semestre"] <= 10:
            raise AlunoException("Primeira nota inválida, passe um valor entre 0 e 10")
        if not aluno_data.get("nota_segundo_semestre"):
            raise AlunoException("Aluno sem segunda nota")
        if not 0 <= aluno_data["nota_segundo_semestre"] <= 10:
            raise AlunoException("Segunda nota inválida, passe um valor entre 0 e 10")
    except TypeError:
        raise AlunoException("Digite apenas valores numericos nas notas")
    if not aluno_data.get("turma_id"):
        raise AlunoException("Aluno sem id de turma")
    try:
        id_turma = int(aluno_data["turma_id"])
    except ValueError:
        raise AlunoException("Digite apenas numeros ao passar o Id da turma")
    turma = Turmas.query.get(id_turma)
    if not turma:
        raise AlunoException("Id da turma nao encontrada")
    novo_aluno = Alunos(
        nome=aluno_data["nome"],
        data_nascimento=data_nasc,
        nota_primeiro_semestre=aluno_data["nota_primeiro_semestre"],
        nota_segundo_semestre=aluno_data["nota_segundo_semestre"],
        turma_id=id_turma
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return "Aluno criado com sucesso"

def atualizar_aluno(id_aluno, aluno_data):
    aluno = Alunos.query.get(id_aluno)
    if not aluno:
        raise AlunoException("Aluno nao encontrado")
    if not aluno_data.get("nome"):
       raise AlunoException("Aluno sem nome")
    aluno.nome = aluno_data["nome"]
    if aluno_data.get("data_nascimento"):
        try:
            data_nascimento = verificar_data(aluno_data["data_nascimento"])
            if data_nascimento is True:
                aluno.data_nascimento = aluno_data["data_nascimento"]
                aluno.idade = calcular_idade(aluno_data["data_nascimento"])
        except DataException as e:
            raise AlunoException(str(e))
    try:
        if aluno_data.get("nota_primeiro_semestre"):
            if 0 <= aluno_data["nota_primeiro_semestre"] <= 10:
                aluno.nota_primeiro_semestre = aluno_data["nota_primeiro_semestre"]
                aluno.media_final = aluno.calcular_media
            else:
                raise AlunoException("Primeira nota inválida, passe um valor entre 0 e 10")
        if aluno_data.get("nota_segundo_semestre"):
            if 0 <= aluno_data["nota_segundo_semestre"] <= 10:
                aluno.nota_segundo_semestre = aluno_data["nota_segundo_semestre"]
                aluno.media_final = aluno.calcular_media
            else:
                raise AlunoException("Segunda nota inválida, passe um valor entre 0 e 10")
    except TypeError:
        raise AlunoException("Digite apenas valores numericos nas notas")
    if aluno_data.get("turma_id"):
        try:
            id_turma = int(aluno_data["turma_id"])
            turma = Turmas.query.get(id_turma)
            if not turma:
                raise AlunoException("Id da turma nao encontrado")
            aluno.turma_id = id_turma
        except ValueError:
            raise AlunoException("Digite apenas numeros ao passar o Id da turma")
    db.session.commit()
    return "Aluno atualizado com sucesso"

def deletar_aluno(id_aluno):
    aluno = Alunos.query.get(id_aluno)
    if not aluno:
        raise AlunoException("Aluno nao encontrado")
    db.session.delete(aluno)
    db.session.commit()
    return "Aluno deletado com sucesso"
