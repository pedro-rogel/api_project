from config import app
from routes.alunos_routes import alunos_bp
from routes.professores_routes import professores_bp
from routes.turmas_routes import turmas_bp

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
