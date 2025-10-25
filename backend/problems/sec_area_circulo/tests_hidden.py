import importlib.util
import os
from io import StringIO
import sys
import math

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_area_circulo_grande():
    """Test oculto con radio grande"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("100")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - 31415.93) < 1, f"Se esperaba '31415.93', se obtuvo '{output}'"

def test_area_circulo_decimal():
    """Test oculto con radio decimal"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("2.5")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - 19.6349) < 0.01, f"Se esperaba '19.6349', se obtuvo '{output}'"
