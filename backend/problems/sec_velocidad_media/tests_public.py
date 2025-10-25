import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función main"""
    assert hasattr(student, "main"), "Debe existir la función main"

def test_velocidad_basica():
    """Test básico de velocidad"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("100\n2")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 50.0, f"Se esperaba '50.0', se obtuvo '{output}'"

def test_velocidad_decimal():
    """Test con decimales"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("150.5\n2.5")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - 60.2) < 0.1, f"Se esperaba cerca de '60.2', se obtuvo '{output}'"

def test_velocidad_unitaria():
    """Test con tiempo unitario"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("60\n1")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 60.0, f"Se esperaba '60.0', se obtuvo '{output}'"
