# API de gestión de biblioteca

API REST en FastAPI para administrar libros y registrar préstamos. Permite crear, consultar, modificar y eliminar libros, marcar un préstamo y listar los que están disponibles.

Los datos se guardan en memoria (una lista de Python). Se pierden al reiniciar el servidor.

## Requisitos

- Python 3.10 o superior
- Windows (PowerShell o CMD)

## Instalación

En la carpeta del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Si PowerShell bloquea `Activate.ps1` (`UnauthorizedAccess`), usa una de estas opciones:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\venv\Scripts\activate
```

o, sin cambiar la política:

```powershell
.\venv\Scripts\activate.bat
```

Dependencias (`requirements.txt`): FastAPI, Uvicorn y Requests.

## Uso

Con el entorno virtual activado:

```powershell
uvicorn main:app --reload
```

La API queda en [http://127.0.0.1:8000](http://127.0.0.1:8000).

- Documentación interactiva (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Documentación alternativa (ReDoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

`--reload` reinicia el servidor cuando cambias `main.py`.

## Modelo de libro

| Campo        | Tipo    | Descripción              |
| ------------ | ------- | ------------------------ |
| `id`         | `int`   | Identificador del libro  |
| `title`      | `string`| Título                   |
| `desc`       | `string`| Descripción              |
| `n_paginas`  | `int`   | Número de páginas        |
| `autor`      | `string`| Nombre del autor         |
| `disponible` | `bool`  | `true` si se puede prestar |

Ejemplo de cuerpo JSON para crear o modificar:

```json
{
  "id": 1,
  "title": "Cien años de soledad",
  "desc": "Novela de realismo mágico",
  "n_paginas": 471,
  "autor": "Gabriel García Márquez",
  "disponible": true
}
```

## Rutas

| Método | Ruta                   | Función                                      |
| ------ | ---------------------- | -------------------------------------------- |
| GET    | `/`                    | Página principal de la API                   |
| POST   | `/libros`              | Crear un libro                               |
| GET    | `/libros`              | Mostrar todos los libros                     |
| GET    | `/libros/{libro_id}`   | Buscar un libro por ID                       |
| PUT    | `/libros/{libro_id}`   | Modificar un libro                           |
| DELETE | `/libros/{libro_id}`   | Eliminar un libro                            |
| POST   | `/prestamos`           | Registrar un préstamo (`libro_id` por query) |
| GET    | `/libros/disponibles`  | Consultar libros con `disponible: true`      |

El préstamo se registra así:

```
POST /prestamos?libro_id=1
```

Si el libro existe y `disponible` es `true`, pasa a `false`. No hay endpoint de devolución todavía.

## Ejemplos con curl

Crear un libro:

```powershell
curl -X POST http://127.0.0.1:8000/libros -H "Content-Type: application/json" -d "{\"id\": 1, \"title\": \"Cien años de soledad\", \"desc\": \"Novela\", \"n_paginas\": 471, \"autor\": \"Gabriel García Márquez\", \"disponible\": true}"
```

Listar libros:

```powershell
curl http://127.0.0.1:8000/libros
```

Buscar por ID:

```powershell
curl http://127.0.0.1:8000/libros/1
```

Registrar un préstamo:

```powershell
curl -X POST "http://127.0.0.1:8000/prestamos?libro_id=1"
```

## Estructura

```
API gestión de biblioteca/
├── main.py              # Aplicación FastAPI
├── requirements.txt     # Dependencias
└── README.md
```

## Nota

`GET /libros/disponibles` debe definirse **antes** que `GET /libros/{libro_id}` en `main.py`. Si no, FastAPI interpreta `"disponibles"` como un ID y la consulta falla.
