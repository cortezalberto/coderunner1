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

def test_iva_21():
    """Test con IVA del 21%"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("100\n21")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 121.0, f"Se esperaba '121.0', se obtuvo '{output}'"

def test_iva_10():
    """Test con IVA del 10%"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("50\n10")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 55.0, f"Se esperaba '55.0', se obtuvo '{output}'"

def test_iva_cero():
    """Test sin IVA"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("200\n0")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 200.0, f"Se esperaba '200.0', se obtuvo '{output}'"
