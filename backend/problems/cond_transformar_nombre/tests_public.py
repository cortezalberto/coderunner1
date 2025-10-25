import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función transformar_nombre"""
    assert hasattr(student, 'transformar_nombre'), 'Debe existir la función transformar_nombre'

def test_opcion_mayusculas():
    """Verifica opción 1 (mayúsculas)"""
    assert student.transformar_nombre("pedro", 1) == "PEDRO"

def test_opcion_minusculas():
    """Verifica opción 2 (minúsculas)"""
    assert student.transformar_nombre("MARIA", 2) == "maria"

def test_opcion_title():
    """Verifica opción 3 (primera letra mayúscula)"""
    assert student.transformar_nombre("juan", 3) == "Juan"

def test_opcion_invalida():
    """Verifica opción inválida"""
    assert student.transformar_nombre("ana", 5) == "Opción inválida"
