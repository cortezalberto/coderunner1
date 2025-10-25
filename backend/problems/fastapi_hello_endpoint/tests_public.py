import importlib.util
import os
from io import StringIO
import sys
import ast

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función main"""
    assert hasattr(student, 'main'), 'Debe existir la función main'

def test_imprime_diccionario():
    """Verifica que imprime un diccionario"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    # Debe poder evaluarse como un diccionario Python
    try:
        result = ast.literal_eval(output)
        assert isinstance(result, dict), f"La salida debe ser un diccionario, se obtuvo {type(result)}"
    except (ValueError, SyntaxError) as e:
        assert False, f"La salida no es un diccionario Python válido: {e}"

def test_contiene_clave_message():
    """Verifica que el diccionario contiene la clave 'message'"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    result = ast.literal_eval(output)
    assert "message" in result, "El diccionario debe contener la clave 'message'"

def test_mensaje_correcto():
    """Verifica que el mensaje es correcto"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    result = ast.literal_eval(output)
    expected = {"message": "Welcome to FastAPI!"}
    assert result == expected, f"Se esperaba {expected}, se obtuvo {result}"
