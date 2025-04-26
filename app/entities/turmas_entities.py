from app import db

class Turmas(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    turno = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.String(150), nullable=True)
    status = db.Column(db.Boolean, nullable=False)

    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    professor = db.relationship('Professores', backref='turmas')

    def __init__(self, nome, turno, descricao, status, professor_id):
        self.nome = nome
        self.turno = turno
        self.descricao = descricao
        self.status = status
        self.professor_id = professor_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "turno": self.turno,
            "descricao": self.descricao,
            "status": self.status,
            "professor_id": self.professor_id
        }
