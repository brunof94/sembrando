import requests
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = ".dasfgjhaslfgñdojuuiriuerr"
server = "http://127.0.0.1:5001/"


@app.route("/", methods=['GET'])
def index():
    if "nombre" in session:
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"]) # login y registro
def login():
    _nombre = request.form.get('username')
    _clave = request.form.get('password')
    _radioLogin = request.form.get('radioLogin')
    # si radio es 1, la acción es login, si es 0 es registro
    parametros = {'nombre': _nombre, 'clave': _clave}
    if _radioLogin == "1":
        _response = requests.post(server + 'api/login', json=parametros)
        if _response.status_code == 200 and _response.text == "Exito":
            session["nombre"] = _nombre
            return render_template("index.html", content="logged", user=_nombre)
        else:
            return render_template("login.html", content=_response.text, user=_nombre, _error=True)
    else:
        _response = requests.post(server + 'api/register', json=parametros)
        if _response.status_code == 200 and _response.text == "Exito":
            session["nombre"] = _nombre
            return render_template("index.html", content="registered", user=_nombre)
        else:
            return render_template("login.html", content=_response.text, user=_nombre, _error=True)
    return render_template("login.html")


@app.route("/usuario/modificar", methods = ["GET", "POST"])
def modificarUsuario():
    if request.method == "GET":
        parametros = {'nombre': session["nombre"]}
        _usuario = requests.post(server + 'api/usuario', json=parametros)
        return render_template("index.html", content = "modificarUsuario", usuario = _usuario.json()[0])
    elif request.method == "POST":
        _clave = request.form.get('txtClave')
        parametros = {'nombre': session["nombre"], 'clave' : _clave}
        _response = requests.post(server + 'api/usuario/modificar', json=parametros)
        return render_template("index.html", content="claveCambiada", mensaje = "Se cambio la contraseña del usuario")


@app.route("/usuario/eliminar", methods = ["POST"])
def eliminarUsuario():
    requests.post(server + 'api/usuario/eliminar', json={'nombre': session["nombre"]})
    session.clear()
    return render_template("login.html", content="eliminado", mensaje="Se borró el usuario")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("login.html")


@app.route("/recetas", methods=["GET"])
def recetas():
    if "nombre" in session:
        _response = requests.get(server + 'api/recetas')
        _response= _response.json()
        return render_template("recetas.html", content = "recetas", recetas = _response)
    else:
        return render_template("login.html")


@app.route("/recetas/<id>")
def verReceta(id):
    _response = requests.get(server + f"/api/receta/{id}")
    _response = _response.json()
    print(_response[1])
    return render_template("recetas.html", content = "receta", receta = _response[0][0], ingredientes = _response[1])


@app.route("/ingredientes", methods=["GET"])
def ingredientes():
    if "nombre" in session:
        _response = requests.get(server + 'api/recetas')
        _response= _response.json()
        return render_template("index.html", content = "ingredientes", ingredientes = _response)
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5002)
