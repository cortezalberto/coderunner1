def main():
    """
    Simula una respuesta JSON de FastAPI.

    En FastAPI, cuando retornas un diccionario desde un endpoint,
    automáticamente se convierte a JSON.

    Ejemplo:
    @app.get("/status")
    def get_status():
        return {"status": "ok", "message": "API funcionando", "version": "1.0"}
    """

    # TODO: Implementa tu código aquí
    # Crea un diccionario con: status="ok", message="API funcionando", version="1.0"
    # Imprime el diccionario

    pass

if __name__ == "__main__":
    main()
