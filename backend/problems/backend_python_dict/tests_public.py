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

def test_diccionario_correcto():
    """Verifica que imprime el diccionario correcto"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    # Evaluar el diccionario
    result = ast.literal_eval(output)
    assert isinstance(result, dict), "Debe ser un diccionario"
    assert result.get("id") == 1, "El id debe ser 1"
    assert result.get("name") == "Ana", "El name debe ser 'Ana'"
    assert result.get("active") is True, "El active debe ser True"
