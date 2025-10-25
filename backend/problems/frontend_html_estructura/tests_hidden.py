import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_formato_correcto():
    """Test oculto: verifica formato exacto"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert "<h1>" in output and "</h1>" in output, "Debe contener las etiquetas de apertura y cierre de h1"
    assert "Hola Mundo" in output, "Debe contener el texto 'Hola Mundo'"
