from flask import jsonify, make_response, request
from main import app
from apis.entities import api_entidades

app.config['JSON_SORT_KEYS'] = False

@app.route("/alunos", methods=['GET'])
def get_student():
    if not api_entidades["students"]:
        return make_response(jsonify(message="No registered students"))
    return make_response(jsonify(data=api_entidades["students"], message="List of students"))

@app.route(f"/alunos/<int:id>", methods=['GET'])
def get_student_id(id):
    for student in api_entidades["students"]:
        if student["id"] == id:
            return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route("/alunos", methods=['POST'])
def create_student():
    student = request.json
    api_entidades["students"].append(student)
    return make_response(jsonify(data=student, message="Successful creation"))

@app.route("/alunos/<int:id>", methods=['PUT'])
def update_student(id):
    for student in api_entidades["students"]:
        if student["id"] == id:
            r = request.json
            student["name"] = r["name"]
            return make_response(jsonify(message="Successful update"))
    return jsonify({"error": "Student not found"}), 404

@app.route("/alunos/<int:id>", methods=['DELETE'])
def delete_student(id):
    for student in api_entidades["students"]:
        if student["id"] == id:
            api_entidades["students"].remove(student)
            return make_response(jsonify(message="Successful deletion"))
    return jsonify({"error": "Student not found"}), 404