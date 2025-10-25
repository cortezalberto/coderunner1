import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función procesar_string"""
    assert hasattr(student, 'procesar_string'), 'Debe existir la función procesar_string'

def test_termina_vocal_minuscula():
    """Verifica string que termina en vocal minúscula"""
    assert student.procesar_string("casa") == "casa!"

def test_no_termina_vocal():
    """Verifica string que NO termina en vocal"""
    assert student.procesar_string("papel") == "papel"

def test_termina_vocal_mayuscula():
    """Verifica string que termina en vocal mayúscula"""
    assert student.procesar_string("Chile") == "Chile!"
