from flask import Flask, jsonify
from routes.alunos import alunos_bp, alunos
from routes.professores import professores_bp, professores
from routes.turmas import turmas_bp, turmas

app = Flask(__name__)

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)

@app.route("/")
def homepage():
    return "Página principal"

@app.route("/reseta", methods=['POST'])
def reset_server():
    alunos.clear()
    professores.clear()
    turmas.clear()
    return jsonify(message="resetado com sucesso")

if __name__ == "__main__":
    app.run(debug=True, port=5002)
