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

def test_intercambio_numeros():
    """Test intercambio de números"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("5\n10")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "10\n5", f"Se esperaba '10\\n5', se obtuvo '{output}'"

def test_intercambio_strings():
    """Test intercambio de strings"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("x\ny")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "y\nx", f"Se esperaba 'y\\nx', se obtuvo '{output}'"

def test_intercambio_iguales():
    """Test con valores iguales"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("7\n7")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "7\n7", f"Se esperaba '7\\n7', se obtuvo '{output}'"
