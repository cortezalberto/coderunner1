#!/usr/bin/env python3
"""
Script para convertir problemas a estructura def main() con input/output
"""
import os
from pathlib import Path

# Problemas a convertir (excluir sumatoria, sec_saludo y cond_mayor_edad que ya están listos)
PROBLEMS = [
    "sec_area_rectangulo",
    "sec_promedio",
    "sec_conversion_temperatura",
    "sec_area_circulo",
    "sec_intercambio_variables",
    "sec_minutos_a_horas",
    "sec_precio_con_iva",
    "sec_velocidad_media",
    "sec_descuento",
    "cond_mayor_de_dos",
    "cond_aprobado",
    "cond_numero_par",
    "cond_validar_password",
    "cond_termina_vocal",
    "cond_transformar_nombre",
    "cond_terremoto",
    "cond_categorias_edad",
]

BASE_DIR = Path(__file__).parent / "backend" / "problems"

# Template para tests con StringIO
TEST_TEMPLATE_HEADER = """import importlib.util
import os
from io import StringIO
import sys

spec = importlib.util.spec_from_file_location('student_code', os.path.join(os.getcwd(), 'student_code.py'))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_existe_funcion():
    \"\"\"Verifica que existe la función main\"\"\"
    assert hasattr(student, 'main'), 'Debe existir la función main'
"""

def convert_problem(problem_id):
    problem_dir = BASE_DIR / problem_id
    if not problem_dir.exists():
        print(f"⚠️  {problem_id}: Directorio no existe")
        return False

    # Leer prompt actual para entender la lógica
    prompt_path = problem_dir / "prompt.md"
    if prompt_path.exists():
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_content = f.read()
        print(f"✓ {problem_id}: Prompt leído")

    # Leer tests_public actual para entender inputs/outputs
    tests_public_path = problem_dir / "tests_public.py"
    if tests_public_path.exists():
        with open(tests_public_path, "r", encoding="utf-8") as f:
            tests_content = f.read()

        # Si ya tiene StringIO, está convertido
        if "StringIO" in tests_content:
            print(f"✓ {problem_id}: Tests ya convertidos")
            return True
        else:
            print(f"⚠️  {problem_id}: Tests necesitan conversión manual")

    return True

if __name__ == "__main__":
    print("="* 60)
    print("ANÁLISIS DE PROBLEMAS A CONVERTIR")
    print("="* 60)

    for problem in PROBLEMS:
        convert_problem(problem)
        print()

    print("="* 60)
    print(f"Total problemas a revisar: {len(PROBLEMS)}")
    print("="* 60)
