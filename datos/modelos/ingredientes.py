from datos.baseDeDatos import BaseDeDatos

def obtenerIngrediente(nombre):
    obtenerIngredienteSql = f"""
        SELECT *
        FROM ingredientes
        WHERE nombre ='{nombre}'"""
    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerIngredienteSql)


def obtenerIngredienteID(id):
    obtenerIngredienteSql = f"""
        SELECT *
        FROM ingredientes
        WHERE id ='{id}'"""
    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerIngredienteSql)


def obtenerIngredientes():
    obtenerIngredienteSql = f"""
        SELECT *
        FROM ingredientes"""
    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerIngredienteSql)


def crearIngrediente(nombre, descripcion):
    crearIngredienteSql = f"""
        INSERT INTO ingredientes(nombre, foto, descripcion)
        VALUES ('{nombre}','foto', '{descripcion}')
    """
    bd = BaseDeDatos()
    bd.ejecutar_sql(crearIngredienteSql)
    return "creado", 200