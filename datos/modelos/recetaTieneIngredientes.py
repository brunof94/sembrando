from datos.baseDeDatos import BaseDeDatos


def crearRecetaTieneIngrediente(idReceta, idIngrediente):
    crearRecetaTieneIngredienteSql = f"""
        INSERT INTO RecetaTieneIngredientes(receta, ingrediente)
        VALUES ('{idReceta}', '{idIngrediente}')
    """
    bd = BaseDeDatos()
    bd.ejecutar_sql(crearRecetaTieneIngredienteSql)
    return "creado", 200


def obtenerIngredientesDeReceta(idReceta):
    obtenerIngredientesDeRecetaSQL = f"""
        SELECT * 
        FROM RecetaTieneIngredientes
        WHERE receta = '{idReceta}'"""
    bd = BaseDeDatos()
    return bd.ejecutar_sql(obtenerIngredientesDeRecetaSQL)