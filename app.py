from flask import Flask
from config import app
from swagger.config import api
from swagger.school_doc import ns_api
from controller.alunos_routes import alunos_bp  # ou o nome do seu arquivo real



app.register_blueprint(alunos_bp)
api.init_app(app)
api.add_namespace(ns_api)

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])