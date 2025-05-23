from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from .swagger import swagger_bp
    app.register_blueprint(swagger_bp)
    @app.route("/")
    def raiz():
        return redirect("/doc", code=302)
    

    from .controllers import alunos_bp, professores_bp, turmas_bp
    app.register_blueprint(alunos_bp)
    app.register_blueprint(professores_bp)
    app.register_blueprint(turmas_bp)

    return app


