import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_descuento_decimal():
    """Test oculto con precio decimal"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("99.99\n15")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - 84.99) < 0.1, f"Se esperaba cerca de '84.99', se obtuvo '{output}'"

def test_descuento_alto():
    """Test oculto con descuento alto"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("500\n75")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 125.0, f"Se esperaba '125.0', se obtuvo '{output}'"
