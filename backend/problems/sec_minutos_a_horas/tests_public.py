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

def test_conversion_hora_y_media():
    """Test con 90 minutos"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("90")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip().split('\n')
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert len(output) == 2, "Debe imprimir dos líneas (horas y minutos)"
    assert output[0] == "1", f"Horas: se esperaba '1', se obtuvo '{output[0]}'"
    assert output[1] == "30", f"Minutos: se esperaba '30', se obtuvo '{output[1]}'"

def test_conversion_exacta():
    """Test con múltiplo exacto de 60"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("120")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip().split('\n')
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output[0] == "2"
    assert output[1] == "0"

def test_conversion_menor_hora():
    """Test con menos de una hora"""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO("45")
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip().split('\n')
    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert output[0] == "0"
    assert output[1] == "45"
