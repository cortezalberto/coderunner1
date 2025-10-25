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

def test_conversion_punto_congelacion():
    """Test en punto de congelación"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("0")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "32.0", f"Se esperaba '32.0', se obtuvo '{output}'"

def test_conversion_punto_ebullicion():
    """Test en punto de ebullición"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("100")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "212.0", f"Se esperaba '212.0', se obtuvo '{output}'"

def test_conversion_temperatura_ambiente():
    """Test con temperatura ambiente"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("25")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - 77.0) < 0.1, f"Se esperaba '77.0', se obtuvo '{output}'"
