from datos.modelos import  usuario

def verificarVacia(lista):
    esVacia = False
    try:
        if len(lista) == 0:
            esVacia = True
    finally:
        return esVacia

def usuarioExiste(nombre):
    existe = False
    try:
        if len(usuario.obtenerUsuario(nombre)) != 0:
            existe = True
    finally:
        return existe

def usuarioExisteID(id):
    existe = False
    try:
        if len(usuario.obtenerUsuarioId(id)) != 0:
            existe = True
    finally:
        return existe