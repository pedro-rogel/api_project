from flask import Flask, jsonify
app = Flask(__name__)
app.route('https://viacep.com.br/ws/01001000/json/', methods=['GET'])
def ex():
    dados = {'message': 'Welcome'}
    return jsonify(dados)


if __name__ == "__main__":
    app.run(debug=True)