import importlib.util
import os

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_limite_muy_leve_leve():
    """Verifica límite entre Muy leve y Leve (3.0)"""
    assert student.clasificar_terremoto(2.9) == "Muy leve"
    assert student.clasificar_terremoto(3.0) == "Leve"

def test_limite_leve_moderado():
    """Verifica límite entre Leve y Moderado (4.0)"""
    assert student.clasificar_terremoto(3.99) == "Leve"
    assert student.clasificar_terremoto(4.0) == "Moderado"

def test_limite_moderado_fuerte():
    """Verifica límite entre Moderado y Fuerte (5.0)"""
    assert student.clasificar_terremoto(4.99) == "Moderado"
    assert student.clasificar_terremoto(5.0) == "Fuerte"

def test_limite_fuerte_muy_fuerte():
    """Verifica límite entre Fuerte y Muy Fuerte (6.0)"""
    assert student.clasificar_terremoto(5.99) == "Fuerte"
    assert student.clasificar_terremoto(6.0) == "Muy Fuerte"

def test_limite_muy_fuerte_extremo():
    """Verifica límite entre Muy Fuerte y Extremo (7.0)"""
    assert student.clasificar_terremoto(6.99) == "Muy Fuerte"
    assert student.clasificar_terremoto(7.0) == "Extremo"
