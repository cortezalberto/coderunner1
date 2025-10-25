import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función categoria_edad"""
    assert hasattr(student, 'categoria_edad'), 'Debe existir la función categoria_edad'

def test_categoria_nino():
    """Verifica categoría Niño/a"""
    assert student.categoria_edad(8) == "Niño/a"

def test_categoria_adolescente():
    """Verifica categoría Adolescente"""
    assert student.categoria_edad(15) == "Adolescente"

def test_categoria_adulto_joven():
    """Verifica categoría Adulto/a joven"""
    assert student.categoria_edad(25) == "Adulto/a joven"

def test_categoria_adulto():
    """Verifica categoría Adulto/a"""
    assert student.categoria_edad(40) == "Adulto/a"
