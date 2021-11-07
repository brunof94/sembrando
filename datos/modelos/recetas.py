from datos.baseDeDatos import BaseDeDatos

def obtenerReceta(nombre):
    obtenerRecetaSql = f"""
        SELECT *
        FROM recetas
        WHERE nombre ='{nombre}'"""
    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerRecetaSql)


def crearReceta(nombre, descripcion, puntuacion):
    crearRecetaSql = f"""
        INSERT INTO recetas(nombre, foto, puntuacion, descripcion)
        VALUES ('{nombre}','foto', '{puntuacion}', '{descripcion}')
    """
    bd = BaseDeDatos()
    bd.ejecutar_sql(crearRecetaSql)
    return "creado", 200

def obtenerRecetas():
    obtenerRecetasSql = f"""
            SELECT *
            FROM recetas"""
    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerRecetasSql)


def modificiarReceta(id, nombre, puntuacion, descripcion):
    modificarRecetaSql = f"""
    UPDATE recetas
    SET nombre = '{nombre}', puntuacion = '{puntuacion}', descripcion = '{descripcion}'
    WHERE id = '{id}'"""
    bd = BaseDeDatos()
    bd.ejecutar_sql(modificarRecetaSql)
    return "Modificado"

def obtenerRecetaID(id):
    obtenerRecetaSql = f"""
        SELECT *
        FROM recetas
        WHERE id ='{id}'"""
    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerRecetaSql)

def borrarReceta(id):
    borrarRecetaSql = f"""
    DELETE
    FROM recetas
    WHERE id = '{id}'"""
    bd = BaseDeDatos()
    bd.ejecutar_sql(borrarRecetaSql)
    return "Borrada"