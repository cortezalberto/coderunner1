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

def test_descuento_20():
    """Test con 20% de descuento"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("100\n20")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 80.0, f"Se esperaba '80.0', se obtuvo '{output}'"

def test_descuento_50():
    """Test con 50% de descuento"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("200\n50")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 100.0, f"Se esperaba '100.0', se obtuvo '{output}'"

def test_descuento_cero():
    """Test sin descuento"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("150\n0")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert float(output) == 150.0, f"Se esperaba '150.0', se obtuvo '{output}'"
