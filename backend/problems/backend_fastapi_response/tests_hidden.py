import importlib.util
import os
from io import StringIO
import sys
import ast

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_claves_correctas():
    """Test oculto: verifica que contiene todas las claves correctas"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    result = ast.literal_eval(output)
    assert len(result) == 3, "Debe contener exactamente 3 claves"
    assert all(key in result for key in ["status", "message", "version"]), "Debe contener las claves correctas"
