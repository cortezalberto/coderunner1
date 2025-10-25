import importlib.util
import os
from io import StringIO
import sys
import ast

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_formato_json_valido():
    """Test oculto: verifica formato JSON válido"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    # Debe poder evaluarse sin errores
    try:
        result = ast.literal_eval(output)
        assert isinstance(result, dict), "Debe ser un diccionario"
    except Exception as e:
        assert False, f"Error al evaluar la salida: {e}"

def test_sin_claves_adicionales():
    """Test oculto: verifica que no hay claves adicionales"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    result = ast.literal_eval(output)
    assert len(result) == 1, f"El diccionario debe tener exactamente 1 clave, tiene {len(result)}"
    assert list(result.keys()) == ["message"], f"La única clave debe ser 'message', se encontraron {list(result.keys())}"

def test_valor_exacto():
    """Test oculto: verifica el valor exacto con mayúsculas"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    result = ast.literal_eval(output)
    assert result["message"] == "Welcome to FastAPI!", f"El mensaje debe ser exactamente 'Welcome to FastAPI!', se obtuvo '{result['message']}'"
