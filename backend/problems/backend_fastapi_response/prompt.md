# Problema: Response JSON con FastAPI

Aprende cómo FastAPI retorna respuestas JSON automáticamente.

## Concepto: Responses en FastAPI

FastAPI convierte automáticamente diccionarios de Python a JSON. Esto hace que crear APIs REST sea muy simple y eficiente.

## Ejemplo en FastAPI

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "Usuario",
        "status": "active"
    }
```

Cuando accedes a `/user/123`, FastAPI retorna:
```json
{
    "id": 123,
    "name": "Usuario",
    "status": "active"
}
```

## Ejercicio

Para este ejercicio conceptual, simula una respuesta de API.

Crea un diccionario que represente el status de la API con:
- `"status"`: "ok"
- `"message"`: "API funcionando"
- `"version"`: "1.0"

## Salida esperada

```
{'status': 'ok', 'message': 'API funcionando', 'version': '1.0'}
```

## Conceptos a practicar

- Responses JSON en FastAPI
- Conversión automática dict → JSON
- Estructura de respuestas API
