import requests
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = ".dasfgjhaslfgñdojuuiriuerr"


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return app.send_static_file("index.html")

@app.route("/login", methods=["POST"])
def login():
    _nombre = request.form.get('username')
    _clave = request.form.get('password')
    _radioLogin = request.form.get('radioLogin')
    #si radio es 1, la acción es login, si es 0 es registro
    parametros = {'nombre': _nombre ,'clave': _clave}
    if _radioLogin == "1":
        _response = requests.post('http://127.0.0.1:5001/api/login', json=parametros)
        if _response.status_code == 200 and _response.text == "Exito":
            session["nombre"] = _nombre
            return render_template("index.html", content = "logged", user = _nombre)
    else:
        requests.post('http://127.0.0.1:5001/api/registro', json=parametros)
    return app.send_static_file("index.html")

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5002)
