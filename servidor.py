from flask import Flask, request, jsonify, render_template, Markup, flash
from datos.modelos import usuario, recetas

app = Flask(__name__)
valorExito = 200
valorYaExiste = 201
valorFaltanDatos = 202
valorNoEsJson = 203
valorNoEncontrado = 204

@app.route("/")
def index():
    #return app.send_static_file("base.html")
    return render_template("index.html")



#region endpoint usuario
@app.route('/usuarios', methods=['POST'])
def crearUsuario():
    datosUsuario = request.get_json()
    if "nombre" in datosUsuario and "clave" in datosUsuario:
        if len(datosUsuario['nombre']) >= 5 and len(datosUsuario['clave']) >= 5 and len(usuario.obtenerUsuario(datosUsuario['nombre'])) == 0:
            usuario.crearUsuario(datosUsuario['nombre'], datosUsuario['clave'])
            print(usuario.obtenerUsuario(datosUsuario['nombre']))
            return 'OK', 200
        else:
            return 'Nombre o clave muy corta', 400 #chequear
    else:
        return 'No se proporcionaron datos validos', 400


@app.route('/usuarios', methods=['GET'])
def obtenerUsuarios():
    datosUsuario = request.get_json()
    if type(datosUsuario) != "dict":
        return render_template("index.html", usuarios = usuario.obtenerUsuarios())
    else:
        if 'nombre' in datosUsuario:
            return jsonify(usuario.obtenerUsuario(datosUsuario['nombre'])), 200
        else:
            return "No hay nombre", 200



@app.route('/usuarios', methods=['DELETE'])
def borrarUsuario():
    datosUsuario = request.get_json()
    if "id" in datosUsuario:
        usuario.borrarUsuario(datosUsuario["id"])
        return "Borrado", 200
    else:
        return "No se proporcionó una id", 200



@app.route('/usuarios', methods=['UPDATE'])
def modificarUsuario():
    datosUsuario = request.get_json()
    usuario.modificarUsuario(datosUsuario["id"],datosUsuario["nombre"], datosUsuario["clave"])
    return "Modificado", 200



#endregion

#region endpoint recetas
@app.route('/recetas', methods=['POST'])
def crearReceta():
    datosReceta = request.get_json()
    if type(datosReceta) is dict:
        if "nombre" in datosReceta and "descripcion" in datosReceta and "puntuacion" in datosReceta:
            if len(recetas.obtenerReceta(datosReceta["nombre"])) == 0:
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
        if len(datosReceta) > 0 and "nombre" in datosReceta:
            return jsonify(recetas.obtenerReceta(datosReceta["nombre"])), valorExito

    return render_template("index.html", recetas = recetas.obtenerRecetas())


@app.route('/recetas', methods=['UPDATE'])
def modificarRecetas():
    datosReceta = request.get_json()
    if type(datosReceta) is dict:
        if "nombre" in datosReceta and "id" in datosReceta and "descripcion" in datosReceta and "puntuacion" in datosReceta:
            if len(recetas.obtenerRecetaID(datosReceta["id"])) > 0:
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


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5001)

