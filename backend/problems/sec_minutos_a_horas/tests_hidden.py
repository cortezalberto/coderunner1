import importlib.util
import os

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_conversion_grande():
    """Test oculto con número grande"""
    assert student.minutos_a_horas(500) == (8, 20)

def test_conversion_dia():
    """Test oculto con un día completo"""
    assert student.minutos_a_horas(1440) == (24, 0)
