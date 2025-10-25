# Ejercicio conceptual de FastAPI
# En un proyecto real, usarías:
#
# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to FastAPI!"}

def main():
    """
    Simula un endpoint GET de FastAPI.

    En FastAPI real, el decorador @app.get("/") indica que esta función
    maneja peticiones GET a la ruta raíz "/".

    El diccionario que retornes se convierte automáticamente a JSON.

    Para este ejercicio:
    - Imprime un diccionario con la clave "message"
    - El valor debe ser "Welcome to FastAPI!"
    """

    # TODO: Implementa tu código aquí
    # Debes imprimir: {"message": "Welcome to FastAPI!"}

    pass

if __name__ == "__main__":
    main()
