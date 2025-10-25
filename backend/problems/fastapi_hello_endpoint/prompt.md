# Problema: Endpoint GET básico en FastAPI

Aprende a crear un endpoint GET simple usando FastAPI, el framework web moderno y de alto rendimiento para Python.

## Objetivo

Implementar la lógica que simula un endpoint FastAPI que responde a peticiones GET en `/` y retorna un diccionario JSON con un mensaje de bienvenida.

## Conceptos de FastAPI

En FastAPI, un endpoint básico se ve así:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
```

## Requisitos

Para este ejercicio conceptual:
1. Implementa una función `main()` que simule la respuesta del endpoint
2. La función debe imprimir un diccionario JSON con la clave `"message"` y valor `"Welcome to FastAPI!"`

## Entrada

No hay entrada. El endpoint no recibe parámetros.

## Salida

Imprime el diccionario Python:
```python
{"message": "Welcome to FastAPI!"}
```

## Conceptos a practicar

- **FastAPI**: Framework web moderno, rápido (alto rendimiento)
- **Decorador @app.get()**: Define un endpoint GET
- **Return automático a JSON**: FastAPI convierte automáticamente diccionarios Python a JSON
- **Type hints**: FastAPI usa anotaciones de tipo para validación automática

## Ejemplo

```
Entrada: (ninguna)
Salida: {"message": "Welcome to FastAPI!"}
```

## Restricciones

- La función debe llamarse `main()`
- Debe imprimir exactamente: `{"message": "Welcome to FastAPI!"}`
- Formato de diccionario Python (no string)
