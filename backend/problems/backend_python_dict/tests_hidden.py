import importlib.util
import os
from io import StringIO
import sys
import ast

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_contiene_claves():
    """Test oculto: verifica que contiene todas las claves"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    result = ast.literal_eval(output)
    assert "id" in result, "Debe contener la clave 'id'"
    assert "name" in result, "Debe contener la clave 'name'"
    assert "active" in result, "Debe contener la clave 'active'"
