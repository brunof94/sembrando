import random
from datos.modelos import recetas, usuario
from random_word import RandomWords

r = RandomWords()


def poblarUsuario():
    for i in range(40):
        poolPalabras = r.get_random_words(limit = 2)
        usuarioGenerado = poolPalabras[0]
        claveGenerada = poolPalabras[1]
        usuario.crearUsuario(usuarioGenerado, claveGenerada)
        print(f"Usuario {i + 1} creado")


def poblarRecetas():
    for i in range(20):
        poolPalabras = r.get_random_words(limit = 10)
        recetaGenerada = f"{poolPalabras[1]} {poolPalabras[2]}"
        puntuacionGenerada = int(random.randrange(1,5))
        descripcionGenerada = ""
        for j in poolPalabras:
            descripcionGenerada += " "+ j
        recetas.crearReceta(recetaGenerada, descripcionGenerada, puntuacionGenerada)
        print(f"Receta {i + 1} creada")


