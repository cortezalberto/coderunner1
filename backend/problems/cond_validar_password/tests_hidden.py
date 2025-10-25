import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_password_valida_10():
    """Verifica contraseña válida de 10 caracteres"""
    assert student.validar_password("mypass1234") == "Ha ingresado una contraseña correcta"

def test_password_vacia():
    """Verifica contraseña vacía"""
    assert student.validar_password("") == "Por favor, ingrese una contraseña de entre 8 y 14 caracteres"

def test_password_limite_inferior():
    """Verifica límite inferior (7 caracteres)"""
    assert student.validar_password("pass123") == "Por favor, ingrese una contraseña de entre 8 y 14 caracteres"
