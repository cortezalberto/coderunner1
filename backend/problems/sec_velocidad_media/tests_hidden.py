import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_velocidad_grande():
    """Test oculto con números grandes"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("1000\n10")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 100.0, f"Se esperaba '100.0', se obtuvo '{output}'"

def test_velocidad_precision():
    """Test oculto de precisión"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("123.45\n6.78")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - 18.21) < 0.1, f"Se esperaba cerca de '18.21', se obtuvo '{output}'"
