import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_contiene_elementos():
    """Test oculto: verifica que contiene los elementos correctos"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    student.main()

    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert "h1" in output, "Debe contener el selector h1"
    assert "color" in output, "Debe contener la propiedad color"
    assert "blue" in output, "Debe contener el valor blue"
