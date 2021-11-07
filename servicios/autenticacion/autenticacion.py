from datos.modelos import usuario as modeloUsuario


def crearUsuario(nombre, clave):
    modeloUsuario.crearUsuario(nombre, clave)

def obtenerUsuario(nombre):
    modeloUsuario.obtenerUsuario(nombre)

def obtenerUsuarios():
    modeloUsuario.obtenerUsuarios()

def modificarUsuario(id, nombre, clave):
    modeloUsuario.modificarUsuario(id, nombre, clave)

def borrarUsuario(id):
    modeloUsuario.borrarUsuario(id)