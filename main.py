from flask import Flask
from routes.alunos import alunos_bp
from routes.professores import professores_bp
from routes.turmas import turmas_bp

app = Flask(__name__)

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
