from flask import Flask, request, jsonify, render_template, session

import auxiliares.funciones
from datos.modelos import usuario, recetas, ingredientes
from auxiliares import funciones

app = Flask(__name__)
app.secret_key = ".dasfgjhaslfgñdojuuiriuerr"
valorExito = 200
valorYaExiste = 201
valorFaltanDatos = 202
valorNoEsJson = 203
valorNoEncontrado = 204
tamanoMinClave = 5
tamanoMinNombre = 5

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html", content = "login")
    if request.method == 'POST':
        _nombre = request.form.get('username')
        _clave = request.form.get('password')
        _datosUsuario = usuario.obtenerUsuario(_nombre)
        if funciones.verificarVacia(_datosUsuario):
            return render_template("index.html", content = "loginError", error = "Usuario no encontrado")
        elif _clave == _datosUsuario[0][2]:
            return render_template("index.html", content = "logged", user = _datosUsuario)
        else:
            return render_template("index.html", content="loginError", error=f"Contraseña incorrecta")

#TO do
@app.route("/login", methods=['POST'])
def login():
    data = request.form
    print(data['username'])
    print(data['password'])
    _usuario = usuario.obtenerUsuario(data)
    print(_usuario)
    return "ok", 200



#region endpoint usuario
@app.route('/usuarios', methods=['POST'])
def crearUsuario():
    nombreUsuario = request.form.get('newUsername')
    passUsuario = request.form.get('newPassword')
    if len(nombreUsuario) >= tamanoMinNombre and len(passUsuario) >= tamanoMinClave and not funciones.usuarioExiste(nombreUsuario):
        usuario.crearUsuario(nombreUsuario,passUsuario)
        return render_template("index.html", usuarios = usuario.obtenerUsuarios(), exito = True, mensaje = f"Se creó el usuario {nombreUsuario}")
    elif funciones.usuarioExiste(nombreUsuario):
        return render_template("index.html", usuarios = usuario.obtenerUsuarios(), content = "error", error = "Usuario ya existe")
    else:
        return render_template("index.html", usuarios = usuario.obtenerUsuarios(), content = "error", error = "No se ingresaron datos validos")

'''   
 if "nombre" in datosUsuario and "clave" in datosUsuario:
        if len(datosUsuario['nombre']) >= tamanoMinNombre and len(datosUsuario['clave']) >= tamanoMinClave and not funciones.usuarioExiste(datosUsuario['nombre']):
            usuario.crearUsuario(datosUsuario['nombre'], datosUsuario['clave'])
            return 'Creado', 200
        else:
            return 'Nombre o clave muy corta o usuario ya existe', 201  #chequear
    else:
        return 'No se proporcionaron datos validos', 400
'''


@app.route('/usuarios', methods=['GET'])
def obtenerUsuarios():
    datosUsuario = request.get_json()
    if datosUsuario is not dict:
        return render_template("index.html", usuarios = usuario.obtenerUsuarios())
    else:
        if 'nombre' in datosUsuario and funciones.usuarioExiste(datosUsuario['usuario']):
            return jsonify(usuario.obtenerUsuario(datosUsuario['nombre'])), 200
        else:
            return "No se encontró", 200



@app.route('/usuarios', methods=['DELETE'])
def borrarUsuario():
    datosUsuario = request.get_json()
    if "id" in datosUsuario and funciones.usuarioExisteID(datosUsuario["id"]):
        usuario.borrarUsuario(datosUsuario["id"])
        return "Borrado", 200
    else:
        return "No se proporcionó una id o no se encontro el usuario", 200


@app.route('/usuarios/<id>/borrar', methods=['DELETE', 'GET'])
def borrarUsuarioID(id):
    usuario.borrarUsuario(id)
    return render_template("index.html", usuarios=usuario.obtenerUsuarios(), exito = True, mensaje = f"Se borró el usuario {id}")


@app.route('/usuarios', methods=['UPDATE'])
def modificarUsuario():
    datosUsuario = request.get_json()
    if 'id' in datosUsuario and 'nombre' in datosUsuario and 'clave' in datosUsuario and len(datosUsuario["nombre"]) >= tamanoMinNombre and len(datosUsuario["clave"]) >= tamanoMinClave:
        usuario.modificarUsuario(datosUsuario["id"],datosUsuario["nombre"], datosUsuario["clave"])
        return "Modificado", 200


@app.route('/usuarios/<id>', methods=['GET'])
def verUsuario(id):
    _usuario = usuario.obtenerUsuarioId(id)
    return render_template("index.html", content="usuario", usuario=_usuario[0])


#endregion

#region endpoint recetas
@app.route('/recetas', methods=['POST'])
def crearReceta():
    datosReceta = request.get_json()
    if type(datosReceta) is dict:
        if "nombre" in datosReceta and "descripcion" in datosReceta and "puntuacion" in datosReceta:
            if funciones.verificarVacia(recetas.obtenerReceta(datosReceta["nombre"])):
                recetas.crearReceta(datosReceta['nombre'], datosReceta['descripcion'], datosReceta['puntuacion'])
                return "creada", valorExito
            return "nombre ya existe", valorYaExiste
        return "faltan datos", valorFaltanDatos
    else:
        return "No es JSON", valorNoEsJson


@app.route('/recetas', methods=['GET'])
def obtenerRecetas():
    datosReceta = request.get_json()
    if type(datosReceta) is dict:
        if "nombre" in datosReceta:
            return jsonify(recetas.obtenerReceta(datosReceta["nombre"])), valorExito
    return render_template("index.html", recetas = recetas.obtenerRecetas())


@app.route('/recetas', methods=['UPDATE'])
def modificarRecetas():
    datosReceta = request.get_json()
    if type(datosReceta) is dict:
        if "nombre" in datosReceta and "id" in datosReceta and "descripcion" in datosReceta and "puntuacion" in datosReceta:
            if not funciones.verificarVacia(recetas.obtenerRecetaID(datosReceta["id"])):
                recetas.modificiarReceta(datosReceta["id"], datosReceta["nombre"], datosReceta["puntuacion"], datosReceta["descripcion"])
                return "Modificado", 200
            else:
                return "Id no encontrado", valorNoEncontrado
        else:
            return "Faltan parametros", valorFaltanDatos
    else:
        return "No es un objeto JSON", valorNoEsJson


@app.route('/recetas', methods=['DELETE'])
def borrarReceta():
    datosReceta = request.get_json()
    if type(datosReceta) is dict:
        if "id" in datosReceta:
            recetas.borrarReceta(datosReceta["id"])
            return "Eliminado", 200
        return "No hay id", valorFaltanDatos
    return "No es un objeto JSON", valorNoEsJson

#endregion


#region endpoint ingredientes
@app.route("/ingredientes", methods=['GET'])
def obtenerIngredientes():
    return render_template("index.html", ingredientes= ingredientes.obtenerIngredientes())


#endregion

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5001)

