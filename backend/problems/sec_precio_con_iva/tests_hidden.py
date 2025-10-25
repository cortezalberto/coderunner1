import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_iva_decimal():
    """Test oculto con IVA decimal"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("75.50\n16")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    result = float(output)
    assert abs(result - 87.58) < 0.01, f"Se esperaba cerca de '87.58', se obtuvo '{output}'"

def test_iva_alto():
    """Test oculto con IVA alto"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("1000\n27")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 1270.0, f"Se esperaba '1270.0', se obtuvo '{output}'"
