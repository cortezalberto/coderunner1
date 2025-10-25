import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función validar_password"""
    assert hasattr(student, 'validar_password'), 'Debe existir la función validar_password'

def test_password_valida_8():
    """Verifica contraseña válida de 8 caracteres"""
    assert student.validar_password("abc12345") == "Ha ingresado una contraseña correcta"

def test_password_valida_14():
    """Verifica contraseña válida de 14 caracteres"""
    assert student.validar_password("password123456") == "Ha ingresado una contraseña correcta"

def test_password_muy_corta():
    """Verifica contraseña muy corta"""
    assert student.validar_password("abc123") == "Por favor, ingrese una contraseña de entre 8 y 14 caracteres"

def test_password_muy_larga():
    """Verifica contraseña muy larga"""
    assert student.validar_password("password12345678") == "Por favor, ingrese una contraseña de entre 8 y 14 caracteres"
