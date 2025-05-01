from app import db
from ..entities import Turmas, Professores, Alunos

class TurmaException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

def listar_turmas():
    turmas = Turmas.query.all()
    return [turma.to_dict() for turma in turmas]

def turma_por_id(id_turma):
    turma = Turmas.query.get(id_turma)
    if not turma:
        raise TurmaException("Turma nao encontrada")
    return turma.to_dict()
    
def adicionar_turma(turma_data):
    professores = Professores.query.all()
    if not professores:
        raise TurmaException("Nao ha professores para criar turmas")
    if not turma_data.get("nome"):
        raise TurmaException("Turma sem nome")
    if not turma_data.get("turno"):
        raise TurmaException("Turma sem turno")
    if not turma_data.get("descricao"):
        raise TurmaException("Turma sem descricao")
    if not turma_data.get("status"):
        raise TurmaException("Turma sem status")
    if not turma_data.get("professor_id"):
        raise TurmaException("Turma sem id de professor")
    try:
        id_professor = int(turma_data["professor_id"])
    except ValueError:
        raise TurmaException("Digite apenas numeros ao passar o Id do professor")
    professor = Professores.query.get(id_professor)
    if not professor:
        raise TurmaException("Id do professor nao encontrado")
    nova_turma = Turmas(
        nome=turma_data["nome"],
        turno=turma_data["turno"],
        descricao=turma_data["descricao"],
        status=turma_data["status"],
        professor_id=id_professor
    )
    db.session.add(nova_turma)
    db.session.commit()
    return "Turma criada com sucesso"

def atualizar_turma(id_turma, turma_data):
    turma = Turmas.query.get(id_turma)
    if not turma:
        raise TurmaException("Turma nao encontrada")
    if not turma_data.get("nome"):
        raise TurmaException("Turma sem nome")
    if turma_data.get("turno"):
        turma.turno = turma_data["turno"]
    turma.nome = turma_data["nome"]
    if turma_data.get("descricao"):
            turma.descricao = turma_data["descricao"]
    if turma_data.get("status"):
        turma.status = turma_data['status']
    if turma_data.get("professor_id"):
        try:
            id_professor = int(turma_data["professor_id"])
            professor = Professores.query.get(id_professor)
            if not professor:
                raise TurmaException("Id do professor nao encontrado")
            turma.professor_id = id_professor
        except ValueError:
            raise TurmaException("Digite apenas numeros ao passar o Id do professor")
    db.session.commit()
    return "Turma atualizada com sucesso"

def deletar_turma(id_turma):
    turma = Turmas.query.get(id_turma)
    if not turma:
        raise TurmaException("Turma nao encontrada")
    alunos = Alunos.query.filter_by(turma_id=id_turma).all()
    alunos_deletados = []
    for aluno in alunos:
        alunos_deletados.append(aluno.id)
        db.session.delete(aluno)
    db.session.delete(turma)
    db.session.commit()
    if alunos_deletados:
        ids_formatados = ', '.join([str(aluno_id) for aluno_id in alunos_deletados])
        return f"Turma deletada com sucesso. ID dos alunos removidos: [{ids_formatados}]"
    else:
        return "Turma deletada com sucesso. Nenhum aluno assoaciado"
