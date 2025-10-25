import importlib.util
import os
from io import StringIO
import sys
import math

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función main"""
    assert hasattr(student, 'main'), 'Debe existir la función main'

def test_area_circulo_unitario():
    """Test con radio 1"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("1")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - math.pi) < 0.01, f"Se esperaba '{math.pi}', se obtuvo '{output}'"

def test_area_circulo_cinco():
    """Test con radio 5"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("5")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - 78.5398) < 0.01, f"Se esperaba '78.5398', se obtuvo '{output}'"

def test_area_circulo_cero():
    """Test con radio 0"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("0")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert result == 0, f"Se esperaba '0', se obtuvo '{output}'"
