import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_sin_entrada():
    """Test oculto: verifica que no requiere entrada"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        student.main()
        output = sys.stdout.getvalue().strip()
        assert output == "Hello, Spring Boot!", f"Debe retornar el mensaje correcto sin entrada"
    finally:
        sys.stdout = old_stdout

def test_mensaje_completo():
    """Test oculto: verifica el mensaje completo"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert len(output) > 0, "El mensaje no puede estar vacío"
    assert "Hello, Spring Boot!" == output, "El mensaje debe ser exactamente 'Hello, Spring Boot!'"
