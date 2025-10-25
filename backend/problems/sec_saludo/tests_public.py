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

def test_saludo_basico():
    """Test básico de saludo"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("Juan")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "Hola, Juan!", f"Se esperaba 'Hola, Juan!', se obtuvo '{output}'"

def test_saludo_otro_nombre():
    """Test con otro nombre"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("María")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "Hola, María!", f"Se esperaba 'Hola, María!', se obtuvo '{output}'"

def test_saludo_nombre_corto():
    """Test con nombre corto"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("Ana")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output == "Hola, Ana!", f"Se esperaba 'Hola, Ana!', se obtuvo '{output}'"
