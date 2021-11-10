import random
from datos.modelos import recetas, usuario, ingredientes
from random_word import RandomWords
from datos.baseDeDatos import BaseDeDatos

r = RandomWords()


def poblarUsuario(numero):
    for i in range(numero):
        try:
            poolPalabras = r.get_random_words(limit = 2)
            usuarioGenerado = poolPalabras[0]
            claveGenerada = poolPalabras[1]
            usuario.crearUsuario(usuarioGenerado, claveGenerada)
            print(f"Usuario {i + 1}: {usuarioGenerado}")
        except:
            print(Exception)


def poblarRecetas(numero):
    for i in range(numero):
        try:
            poolPalabras = r.get_random_words(limit = 10)
            recetaGenerada = f"{poolPalabras[1]} {poolPalabras[2]}"
            puntuacionGenerada = int(random.randrange(1,5))
            descripcionGenerada = ""
            for j in poolPalabras:
                descripcionGenerada += " "+ j
            recetas.crearReceta(recetaGenerada, descripcionGenerada, puntuacionGenerada)
            print(f"Receta {i + 1}: {recetaGenerada}")
        except:
            print(Exception)


def poblarIngredientes(numero):
    for i in range(numero):
        try:
            poolPalabras = r.get_random_words(limit=10)
            ingredienteGenerado = f"{poolPalabras[1]}"
            descripcionGenerada = ""
            for j in poolPalabras:
                descripcionGenerada += " " + j
            ingredientes.crearIngrediente(ingredienteGenerado, descripcionGenerada)
            print(f"Ingrediente {i + 1}: {ingredienteGenerado}")
        except:
            print(Exception)


poblarUsuario(20)
poblarRecetas(17)
poblarIngredientes(10)

def poblarCreadoresRecetas():

    bd = BaseDeDatos()
    numeroRecetas = bd.ejecutar_sql(f"SELECT COUNT(1) FROM recetas")[0][0]
    numeroUsuarios = bd.ejecutar_sql(f"SELECT COUNT(1) FROM usuarios")[0][0]
    for i in range(numeroRecetas):

        bd.ejecutar_sql(f"INSERT INTO creadoresRecetas (receta, usuario)"
                        f"")
    print(numeroRecetas, numeroUsuarios)

#poblarCreadoresRecetas()