from datos.baseDeDatos import BaseDeDatos


def obtenerUsuario(nombre):
    obtenerUsuarioSql = f"""
        SELECT id, nombre, clave 
        FROM usuarios 
        WHERE nombre = '{nombre}'"""

    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerUsuarioSql)

def obtenerUsuarioId(id):
    obtenerUsuarioSqlId = f"""
        SELECT id, nombre, clave 
        FROM usuarios 
        WHERE id = '{id}'"""

    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerUsuarioSqlId)

def crearUsuario(nombre, clave):

    crearUsuarioSql = f"""
        INSERT INTO usuarios(nombre, clave)
        VALUES ('{nombre}', '{clave}')
    """
    bd = BaseDeDatos()
    bd.ejecutar_sql(crearUsuarioSql)





def obtenerUsuarios():
    obtenerUsuarioSql = f"""
            SELECT * 
            FROM usuarios
    """
    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerUsuarioSql)



def modificarUsuario(id,nombre, clave):
    modificarUsuarioSql =  f"""
        UPDATE usuarios
        SET nombre='{nombre}', clave='{clave}'
        WHERE id = '{id}'"""
    bd = BaseDeDatos()
    bd.ejecutar_sql(modificarUsuarioSql)

#modificarUsuario(4,"Test", "Algo")

def borrarUsuario(id):
    borrarUsuarioSql = f"""
    DELETE
    FROM usuarios
    WHERE id ='{id}'"""
    bd = BaseDeDatos()
    bd.ejecutar_sql(borrarUsuarioSql)

#borrarUsuario(4)
