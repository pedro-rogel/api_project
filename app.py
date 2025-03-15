from flask import Flask, jsonify, make_response, request, url_for, redirect
from students import api_entidades

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

@app.route("/alunos", methods=['GET'])
def get_students():
    return make_response(jsonify(message='Lista de estudantes', data=api_entidades))

@app.route("/alunos", methods=['POST'])
def create_student():
    student = request.json
    api_entidades["students"].append(student)
    return make_response(jsonify(student))

@app.route(f"/alunos/<int:id>", methods=['GET'])
def get_id(id):
    for i in api_entidades['students']:
        if i['id'] == id:
            return jsonify(i)
    return jsonify({"error": "student not found"}), 404

@app.route("/alunos/<int:id>", methods=['DELETE'])
def delete_student(id):
    for students in api_entidades['students']:
        if students['id'] == id:
            return make_response(jsonify(messsage='Excluido', data=students))
        
    pass
if __name__ == "__main__":
    app.run(debug=True)
    