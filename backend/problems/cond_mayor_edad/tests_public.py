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

def test_mayor_edad_basico():
    """Verifica caso básico mayor de edad"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("20")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "Es mayor de edad", f"Se esperaba 'Es mayor de edad', se obtuvo '{output}'"

def test_menor_edad_basico():
    """Verifica caso básico menor de edad"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("15")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "Es menor de edad", f"Se esperaba 'Es menor de edad', se obtuvo '{output}'"

def test_edad_limite():
    """Verifica el caso límite de 18 años"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("18")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "Es menor de edad", f"Se esperaba 'Es menor de edad', se obtuvo '{output}'"
