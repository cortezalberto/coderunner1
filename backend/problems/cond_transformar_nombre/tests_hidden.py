import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_nombre_completo_mayusculas():
    """Verifica opción 1 con nombre completo"""
    assert student.transformar_nombre("Ana Maria Lopez", 1) == "ANA MARIA LOPEZ"

def test_nombre_completo_minusculas():
    """Verifica opción 2 con nombre completo"""
    assert student.transformar_nombre("CARLOS RODRIGUEZ", 2) == "carlos rodriguez"

def test_nombre_completo_title():
    """Verifica opción 3 con nombre completo"""
    assert student.transformar_nombre("jose garcia", 3) == "Jose Garcia"

def test_opcion_cero():
    """Verifica opción 0 (inválida)"""
    assert student.transformar_nombre("test", 0) == "Opción inválida"

def test_opcion_negativa():
    """Verifica opción negativa (inválida)"""
    assert student.transformar_nombre("test", -1) == "Opción inválida"
