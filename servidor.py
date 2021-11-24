from flask import Flask, request, jsonify, render_template, session

import auxiliares.funciones
from datos.modelos import usuario, recetas, ingredientes, recetaTieneIngredientes
from auxiliares import funciones

app = Flask(__name__)
app.secret_key = ".dasfgjhaslfgñdojuuiriuerr"
valorExito = 200
valorYaExiste = 201
valorFaltanDatos = 202
valorNoEsJson = 203
valorNoEncontrado = 204
valorClaveIncorrecta = 205
tamanoMinClave = 5
tamanoMinNombre = 5


# la vista de admin solo se ingresa con el usuario admin
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html", content="login")
    if request.method == 'POST':
        _nombre = request.form.get('username')
        _clave = request.form.get('password')
        if _nombre == "admin" and _clave == "admin":
            return render_template("index.html", content="logged", user="Admin")
        # _datosUsuario = usuario.obtenerUsuario(_nombre)
        # if funciones.verificarVacia(_datosUsuario):
        #     return render_template("index.html", content = "loginError", error = "Usuario no encontrado")
        # elif _clave == _datosUsuario[0][2]:
        #     return render_template("index.html", content = "logged", user = _datosUsuario)
        else:
            return render_template("index.html", content="loginError", error=f"Contraseña incorrecta")


@app.route("/api/login", methods=['POST'])
def apiLogin():
    try:
        _nombre = request.json['nombre']
        _clave = request.json['clave']
        _datosUsuario = usuario.obtenerUsuario(_nombre)
        if funciones.verificarVacia(_datosUsuario):  # Si no encuentra al usuario
            return "No encontrado", 200
        elif _clave == _datosUsuario[0][2]:  # login
            return "Exito", 200
        else:
            return "Contraseña incorrecta", 200  # contraseña incorrecta
    except:
        return "Bad Request", 400


@app.route("/api/register", methods=['POST'])
def apiRegister():
    try:
        _nombre = request.json['nombre']
        _clave = request.json['clave']
        _datosUsuario = usuario.obtenerUsuario(_nombre)

        if len(_nombre) >= tamanoMinNombre and len(_clave) >= tamanoMinClave:
            if funciones.verificarVacia(_datosUsuario):
                usuario.crearUsuario(_nombre, _clave)
                return "Exito", 200
            else:
                return "Ya existe", 200
        else:
            return "Contraseña o nombre de usuario corto", 200

    except:
        return "Bad Request", 400


# TO do
@app.route("/login", methods=['POST'])
def login():
    data = request.form
    print(data['username'])
    print(data['password'])
    _usuario = usuario.obtenerUsuario(data)
    print(_usuario)
    return "ok", 200


# region endpoint usuario
@app.route('/usuarios', methods=['POST'])
def crearUsuario():
    nombreUsuario = request.form.get('newUsername')
    passUsuario = request.form.get('newPassword')
    if len(nombreUsuario) >= tamanoMinNombre and len(passUsuario) >= tamanoMinClave and not funciones.usuarioExiste(
            nombreUsuario):
        usuario.crearUsuario(nombreUsuario, passUsuario)
        return render_template("index.html", usuarios=usuario.obtenerUsuarios(), exito=True,
                               mensaje=f"Se creó el usuario {nombreUsuario}")
    elif funciones.usuarioExiste(nombreUsuario):
        return render_template("index.html", usuarios=usuario.obtenerUsuarios(), content="error",
                               error="Usuario ya existe")
    else:
        return render_template("index.html", usuarios=usuario.obtenerUsuarios(), content="error",
                               error="No se ingresaron datos validos")


@app.route('/usuarios', methods=['GET'])
def obtenerUsuarios():
    datosUsuario = request.get_json()
    if datosUsuario is not dict:
        return render_template("index.html", usuarios=usuario.obtenerUsuarios())
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
    return render_template("index.html", usuarios=usuario.obtenerUsuarios(), exito=True,
                           mensaje=f"Se borró el usuario {id}")


@app.route('/api/usuario', methods=["POST"])
def obtenerUsuarioNombreAPI():
    try:
        nombre = request.get_json()["nombre"]
        if funciones.usuarioExiste(nombre):
            return jsonify(usuario.obtenerUsuario(nombre)), 200
        else:
            return "no existe", 200
    except:
        return "bad request", 400


@app.route('/api/usuario/modificar', methods=['POST'])
def modificarUsuario():
    datosUsuario = request.get_json()
    try:
        _usuario = usuario.obtenerUsuario(datosUsuario['nombre'])[0]
        if len(datosUsuario["clave"]) > 3:
            usuario.modificarUsuario(_usuario[0], _usuario[1], datosUsuario["clave"])
            return "Modificado", 200
    except Exception:
        print(Exception)
        return "Bad request", 400


@app.route('/api/usuario/eliminar', methods=["POST"])
def eliminarUsuarioAPI():
    datosUsuario = request.get_json()
    _usuario = usuario.obtenerUsuario(datosUsuario["nombre"])[0]
    usuario.borrarUsuario(_usuario[0])
    return "Eliminado", 200


@app.route('/usuarios/<id>', methods=['GET'])
def verUsuario(id):
    _usuario = usuario.obtenerUsuarioId(id)
    return render_template("index.html", content="usuario", usuario=_usuario[0])


@app.route('/usuarios/<id>/modificar', methods=['GET'])
def modificarUsuarioVista(id):
    _usuario = usuario.obtenerUsuarioId(id)
    return render_template("index.html", content="modificarUsuario", usuario=_usuario)


@app.route('/usuarios/<id>/modificado', methods=['POST'])
def modificarUsuarioID(id):
    nombreUsuario = request.form.get('updatedUsername')
    passUsuario = request.form.get('updatedPassword')
    if funciones.usuario.obtenerUsuario(nombreUsuario):  # comprobar si ya existe
        return render_template("index.html", usuarios=usuario.obtenerUsuarios(), content="error",
                               error="No se pueden repetir nombres de usuarios")
    usuario.modificarUsuario(id, nombreUsuario, passUsuario)
    return render_template("index.html", usuarios=usuario.obtenerUsuarios(), exito=True,
                           mensaje=f"Se modificó el usuario {id}")


# endregion

# region endpoint recetas
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
    return render_template("index.html", recetas=recetas.obtenerRecetas())


@app.route("/api/recetas", methods=['GET'])
def obtenerRecetasAPI():
    _recetas = recetas.obtenerRecetas()
    _recetas = jsonify(_recetas)
    return _recetas, 200


@app.route("/api/receta/<id>")
def obtenerRecetaAPI(id):
    _receta = recetas.obtenerRecetaID(id)
    _ingredientesID = recetaTieneIngredientes.obtenerIngredientesDeReceta(id)
    _ingredientes = []
    for ingrediente in _ingredientesID:
        i = ingredientes.obtenerIngredienteID(ingrediente[1])
        _ingredientes.append(i)
    return jsonify([_receta, _ingredientes]), 200


@app.route('/recetas', methods=['UPDATE'])
def modificarRecetas():
    datosReceta = request.get_json()
    if type(datosReceta) is dict:
        if "nombre" in datosReceta and "id" in datosReceta and "descripcion" in datosReceta and "puntuacion" in datosReceta:
            if not funciones.verificarVacia(recetas.obtenerRecetaID(datosReceta["id"])):
                recetas.modificiarReceta(datosReceta["id"], datosReceta["nombre"], datosReceta["puntuacion"],
                                         datosReceta["descripcion"])
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


# endregion


# region endpoint ingredientes
@app.route("/ingredientes", methods=['GET'])
def obtenerIngredientes():
    return render_template("index.html", ingredientes=ingredientes.obtenerIngredientes())


@app.route("/api/ingredientes", methods=['GET'])
def obtenerIngredientesAPI():
    _ingredientes = ingredientes.obtenerIngredientes()
    _ingredientes = jsonify(_ingredientes)
    return _ingredientes, 200


@app.route("/api/ingredientes", methods=["POST"])
def crearIngrediente():
    try:
        _nombre = request.json['nombre']
        _descripcion = request.json['clave']
        _datosIngrediente = ingredientes.obtenerIngrediente(_nombre)

        if len(_nombre) >= 2 and len(_datosIngrediente) >= 10:
            if funciones.verificarVacia(_datosIngrediente):
                ingredientes.crearIngrediente(_nombre, _descripcion)
                return "Exito", 200
            else:
                return "Ya existe", 200
        else:
            return "Contraseña o nombre de usuario corto", 200

    except:
        return "Bad Request", 400


# endregion


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5001)
