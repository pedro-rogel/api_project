from flask import Flask, jsonify
from routes.professores import professores_bp, professores
from routes.turmas import turmas_bp, turmas
from routes.alunos import alunos_bp, alunos

app = Flask(__name__)

app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)
app.register_blueprint(alunos_bp)

@app.route("/")
def index():
    return "Página raiz"

@app.route("/resetar", methods=['POST'])
def reset_server():
    alunos.clear()
    turmas.clear()
    professores.clear()
    return jsonify(message="resetado com sucesso")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
