import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_limite_nino_adolescente():
    """Verifica límite entre Niño/a y Adolescente (12 años)"""
    assert student.categoria_edad(11) == "Niño/a"
    assert student.categoria_edad(12) == "Adolescente"

def test_limite_adolescente_adulto_joven():
    """Verifica límite entre Adolescente y Adulto/a joven (18 años)"""
    assert student.categoria_edad(17) == "Adolescente"
    assert student.categoria_edad(18) == "Adulto/a joven"

def test_limite_adulto_joven_adulto():
    """Verifica límite entre Adulto/a joven y Adulto/a (30 años)"""
    assert student.categoria_edad(29) == "Adulto/a joven"
    assert student.categoria_edad(30) == "Adulto/a"
