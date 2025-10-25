import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función main"""
    assert hasattr(student, 'main'), 'Debe existir la función main'

def test_mensaje_correcto():
    """Verifica que imprime el mensaje correcto"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert output == "Hello, Spring Boot!", f"Se esperaba 'Hello, Spring Boot!', se obtuvo '{output}'"

def test_formato_exacto():
    """Verifica que el formato sea exacto (mayúsculas, puntuación)"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    # Verificar que contiene las palabras clave
    assert "Hello" in output, "El mensaje debe contener 'Hello'"
    assert "Spring Boot" in output, "El mensaje debe contener 'Spring Boot'"
    assert output.endswith("!"), "El mensaje debe terminar con '!'"
