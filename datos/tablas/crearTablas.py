import sqlite3

sql_tabla_usuarios = '''
CREATE TABLE usuarios(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT,
clave TEXT
)
'''

sql_tabla_recetas = '''
CREATE TABLE recetas(
id INTEGER PRIMARY KEY  AUTOINCREMENT,
nombre TEXT,
foto TEXT,
puntuacion TEXT,
descripcion TEXT
)
'''

sql_tabla_ingredientes = '''
CREATE TABLE ingredientes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre VARCHAR(20) UNIQUE,
foto BLOB,
descripcion VARCHAR(50)
)
'''

sql_tabla_creadoresRecetas = '''
CREATE TABLE creadoresRecetas(
receta INTEGER,
usuario INTEGER,
FOREIGN KEY (receta) REFERENCES recetas(id),
FOREIGN KEY (usuario) REFERENCES usuarios(id)
)
'''

sql_tabla_favoritos = '''
CREATE TABLE favoritos(
receta INTEGER,
usuario INTEGER,
FOREIGN KEY(receta) REFERENCES recetas(id),
FOREIGN KEY(usuario) REFERENCES usuarios(id)
)
'''

sql_tabla_tieneIngredientes = '''
CREATE TABLE tieneIngredientes(
ingrediente INTEGER, 
usuario  INTEGER, 
cantidad INTEGER,
FOREIGN KEY(ingrediente) REFERENCES ingredientes(id),
FOREIGN KEY(usuario) REFERENCES usuarios(id)
)
'''


if __name__ == '__main__':
    try:
        print('Creando Base de datos..')
        conexion = sqlite3.connect('../../queCenamosHoy.db')

        print('Creando Tablas..')
        conexion.execute(sql_tabla_usuarios)
        conexion.execute(sql_tabla_recetas)
        conexion.execute(sql_tabla_ingredientes)
        conexion.execute(sql_tabla_creadoresRecetas)
        conexion.execute(sql_tabla_favoritos)
        conexion.execute(sql_tabla_tieneIngredientes)

        conexion.close()
        print('Creacion Finalizada.')
    except Exception as e:
        print(f'Error creando base de datos: {e}', e)
