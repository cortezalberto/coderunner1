import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_todas_vocales_minusculas():
    """Verifica todas las vocales minúsculas"""
    assert student.procesar_string("perro") == "perro!"
    assert student.procesar_string("cafe") == "cafe!"
    assert student.procesar_string("kiwi") == "kiwi!"
    assert student.procesar_string("bu") == "bu!"

def test_todas_vocales_mayusculas():
    """Verifica todas las vocales mayúsculas"""
    assert student.procesar_string("CASA") == "CASA!"
    assert student.procesar_string("CHILE") == "CHILE!"

def test_consonantes_finales():
    """Verifica strings que terminan en consonantes"""
    assert student.procesar_string("amor") == "amor"
    assert student.procesar_string("sol") == "sol"
