from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Libro(BaseModel):
    id: int
    title: str
    desc: str
    n_paginas: int
    autor: str
    disponible: bool  # Cambiado a tipo booleano

# lista para almacenar libros
libros = []

# Página principal de la API
@app.get("/")
def inicio():
    return {"mensaje": "API de biblioteca"}

# Creación de un nuevo libro
@app.post("/libros")
def crear_libro(libro: Libro):
    libros.append(libro)
    return libro

# Mostrar todos los libros
@app.get("/libros")
def mostrar_libros():
    if not libros:
        return {"mensaje": "No se han encontrado libros"}
    return libros

# Buscar un libro
@app.get("/libros/{libro_id}")
def buscar_libro(libro_id: int):
    for libro in libros:
        if libro.id == libro_id:
            return libro
    return {"mensaje": "Libro no encontrado"}

# Modificar un libro
@app.put("/libros/{libro_id}")
def modificar_libro(libro_id: int, datos: Libro):
    for libro in libros:
        if libro.id == libro_id:
            libro.title = datos.title
            libro.desc = datos.desc
            libro.n_paginas = datos.n_paginas
            libro.autor = datos.autor
            libro.disponible = datos.disponible
            return libro
    return {"mensaje": "Libro no encontrado"}

# Eliminar un libro
@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int):
    for libro in libros:
        if libro.id == libro_id:
            libros.remove(libro)
            return {"mensaje": "Libro eliminado"}
    return {"mensaje": "Libro no encontrado"}

# Registrar un préstamo
@app.post("/prestamos")
def hacer_prestamo(libro_id: int):
    for libro in libros:
        if libro.id == libro_id:
            if libro.disponible:
                libro.disponible = False
                return {"mensaje": "Préstamo registrado con éxito", "libro": libro}
            else:
                return {"mensaje": "El libro no está disponible para préstamo"}
    return {"mensaje": "Libro no encontrado"}

@app.get("/libros/disponibles")
def libros_disponibles():
    disponibles = [libro for libro in libros if libro.disponible]
    if not disponibles:
        return {"mensaje": "No hay libros disponibles"}
    return disponibles
