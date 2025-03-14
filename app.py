from flask import Flask, jsonify, make_response, request
from students import api_entidades

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/alunos/", methods=['GET'])
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
    

if __name__ == "__main__":
    app.run(debug=True)
    
    

# for i in api_entidades['students']:
#     if i['id'] == 1:
#         print(i)

