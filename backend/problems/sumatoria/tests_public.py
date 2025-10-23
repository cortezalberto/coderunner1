import importlib.util
import sys
import os

# Cargamos el código del estudiante como "student_code"
spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_suma_basico():
    """Test básico de suma"""
    assert hasattr(student, "suma"), "Debe existir una función suma(a, b)"
    assert student.suma(2, 3) == 5

def test_suma_negativos():
    """Test con números negativos"""
    assert student.suma(-4, 10) == 6
