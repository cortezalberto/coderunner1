import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    """Verifica que existe la función clasificar_terremoto"""
    assert hasattr(student, 'clasificar_terremoto'), 'Debe existir la función clasificar_terremoto'

def test_muy_leve():
    """Verifica clasificación Muy leve"""
    assert student.clasificar_terremoto(2.5) == "Muy leve"

def test_leve():
    """Verifica clasificación Leve"""
    assert student.clasificar_terremoto(3.7) == "Leve"

def test_moderado():
    """Verifica clasificación Moderado"""
    assert student.clasificar_terremoto(4.8) == "Moderado"

def test_fuerte():
    """Verifica clasificación Fuerte"""
    assert student.clasificar_terremoto(5.5) == "Fuerte"

def test_muy_fuerte():
    """Verifica clasificación Muy Fuerte"""
    assert student.clasificar_terremoto(6.3) == "Muy Fuerte"

def test_extremo():
    """Verifica clasificación Extremo"""
    assert student.clasificar_terremoto(8.0) == "Extremo"
