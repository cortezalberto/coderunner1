#!/usr/bin/env python3
"""
Script para crear problemas de Programación 1 automáticamente
"""
import os
import json

# Definición de todos los problemas por unidad
PROBLEMS = {
    "estructuras-secuenciales": [
        # Ya creados: saludo, area_rectangulo, promedio, conversion_temperatura
        {
            "id": "sec_area_circulo",
            "title": "Área de un círculo",
            "difficulty": "easy",
            "tags": ["geometria", "pi", "formula"],
            "function": "area_circulo",
            "params": ["radio"],
            "formula": "π × radio²",
            "examples": [
                ("area_circulo(5)", "78.54 (aprox)"),
                ("area_circulo(10)", "314.16 (aprox)")
            ],
            "tests_public": [
                ("test_area_circulo_basico", "radio=1", "3.14159", 3),
                ("test_area_circulo_medio", "radio=5", "78.5398", 2),
                ("test_area_circulo_cero", "radio=0", "0", 2)
            ],
            "tests_hidden": [
                ("test_area_circulo_grande", "radio=100", "31415.93", 2),
                ("test_area_circulo_decimal", "radio=2.5", "19.6349", 1)
            ]
        },
        {
            "id": "sec_intercambio_variables",
            "title": "Intercambio de variables",
            "difficulty": "easy",
            "tags": ["variables", "tuplas", "asignacion"],
            "function": "intercambiar",
            "params": ["a", "b"],
            "formula": "Retornar (b, a)",
            "examples": [
                ("intercambiar(5, 10)", "(10, 5)"),
                ("intercambiar('hola', 'mundo')", "('mundo', 'hola')")
            ],
            "tests_public": [
                ("test_intercambio_numeros", "a=5, b=10", "(10, 5)", 3),
                ("test_intercambio_strings", "a='x', b='y'", "('y', 'x')", 2),
                ("test_intercambio_iguales", "a=7, b=7", "(7, 7)", 2)
            ],
            "tests_hidden": [
                ("test_intercambio_negativos", "a=-5, b=15", "(15, -5)", 2),
                ("test_intercambio_decimales", "a=1.5, b=2.5", "(2.5, 1.5)", 1)
            ]
        },
        {
            "id": "sec_minutos_a_horas",
            "title": "Conversión de minutos a horas",
            "difficulty": "easy",
            "tags": ["conversion", "division", "modulo"],
            "function": "minutos_a_horas",
            "params": ["minutos"],
            "formula": "horas = minutos // 60, mins = minutos % 60",
            "examples": [
                ("minutos_a_horas(90)", "(1, 30)"),
                ("minutos_a_horas(125)", "(2, 5)")
            ],
            "tests_public": [
                ("test_conversion_basica", "90 min", "(1, 30)", 3),
                ("test_conversion_exacta", "120 min", "(2, 0)", 2),
                ("test_conversion_menor_hora", "45 min", "(0, 45)", 2)
            ],
            "tests_hidden": [
                ("test_conversion_grande", "500 min", "(8, 20)", 2),
                ("test_conversion_dia", "1440 min", "(24, 0)", 1)
            ]
        },
        {
            "id": "sec_precio_con_iva",
            "title": "Precio con IVA",
            "difficulty": "easy",
            "tags": ["aritmetica", "porcentaje", "finanzas"],
            "function": "precio_con_iva",
            "params": ["precio", "iva"],
            "formula": "precio × (1 + iva/100)",
            "examples": [
                ("precio_con_iva(100, 21)", "121.0"),
                ("precio_con_iva(50, 10.5)", "55.25")
            ],
            "tests_public": [
                ("test_iva_21", "precio=100, iva=21", "121.0", 3),
                ("test_iva_10", "precio=50, iva=10", "55.0", 2),
                ("test_iva_cero", "precio=200, iva=0", "200.0", 2)
            ],
            "tests_hidden": [
                ("test_iva_decimal", "precio=75.50, iva=16", "87.58", 2),
                ("test_iva_alto", "precio=1000, iva=27", "1270.0", 1)
            ]
        },
        {
            "id": "sec_velocidad_media",
            "title": "Velocidad media",
            "difficulty": "easy",
            "tags": ["fisica", "division", "formula"],
            "function": "velocidad_media",
            "params": ["distancia", "tiempo"],
            "formula": "velocidad = distancia / tiempo",
            "examples": [
                ("velocidad_media(100, 2)", "50.0"),
                ("velocidad_media(150, 3)", "50.0")
            ],
            "tests_public": [
                ("test_velocidad_basica", "dist=100, tiempo=2", "50.0", 3),
                ("test_velocidad_decimal", "dist=150.5, tiempo=2.5", "60.2", 2),
                ("test_velocidad_unitaria", "dist=60, tiempo=1", "60.0", 2)
            ],
            "tests_hidden": [
                ("test_velocidad_grande", "dist=1000, tiempo=10", "100.0", 2),
                ("test_velocidad_precision", "dist=123.45, tiempo=6.78", "18.2", 1)
            ]
        },
        {
            "id": "sec_descuento",
            "title": "Aplicar descuento",
            "difficulty": "easy",
            "tags": ["porcentaje", "descuento", "finanzas"],
            "function": "aplicar_descuento",
            "params": ["precio", "descuento"],
            "formula": "precio × (1 - descuento/100)",
            "examples": [
                ("aplicar_descuento(100, 20)", "80.0"),
                ("aplicar_descuento(50, 10)", "45.0")
            ],
            "tests_public": [
                ("test_descuento_20", "precio=100, desc=20", "80.0", 3),
                ("test_descuento_50", "precio=200, desc=50", "100.0", 2),
                ("test_descuento_cero", "precio=150, desc=0", "150.0", 2)
            ],
            "tests_hidden": [
                ("test_descuento_decimal", "precio=99.99, desc=15", "84.99", 2),
                ("test_descuento_alto", "precio=500, desc=75", "125.0", 1)
            ]
        }
    ]
}

def create_problem_files(unit_id, problem):
    """Crea todos los archivos necesarios para un problema"""
    problem_id = problem["id"]
    problem_dir = f"backend/problems/{problem_id}"

    # Crear directorio
    os.makedirs(problem_dir, exist_ok=True)

    # metadata.json
    metadata = {
        "title": problem["title"],
        "subject_id": "programacion-1",
        "unit_id": unit_id,
        "difficulty": problem["difficulty"],
        "tags": problem["tags"],
        "timeout_sec": 3.0,
        "memory_mb": 128
    }
    with open(f"{problem_dir}/metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    # prompt.md
    examples_str = "\n".join([f"- `{ex[0]} -> {ex[1]}`" for ex in problem["examples"]])
    prompt = f"""# Problema: {problem["title"]}

Implementa una función **`{problem["function"]}({', '.join(problem["params"])})`**.

## Ejemplos
{examples_str}

**Fórmula**: {problem["formula"]}

**Restricciones**
- No uses input() ni prints dentro de la función.
- La función debe llamarse exactamente `{problem["function"]}`.
"""
    with open(f"{problem_dir}/prompt.md", "w", encoding="utf-8") as f:
        f.write(prompt)

    # starter.py
    params_str = ', '.join(problem["params"])
    starter = f"""def {problem["function"]}({params_str}):
    # TODO: Implementa la función
    pass
"""
    with open(f"{problem_dir}/starter.py", "w", encoding="utf-8") as f:
        f.write(starter)

    # tests_public.py
    tests_public = """import importlib.util
import os

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

"""
    for test_name, desc, expected, points in problem["tests_public"]:
        tests_public += f'''def {test_name}():
    """Test {desc}"""
    assert hasattr(student, "{problem["function"]}"), "Debe existir la función {problem["function"]}"
    # Implementar test según la lógica específica
    pass

'''

    with open(f"{problem_dir}/tests_public.py", "w", encoding="utf-8") as f:
        f.write(tests_public)

    # tests_hidden.py (similar)
    tests_hidden = """import importlib.util
import os

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

"""
    for test_name, desc, expected, points in problem["tests_hidden"]:
        tests_hidden += f'''def {test_name}():
    """Test oculto {desc}"""
    # Implementar test según la lógica específica
    pass

'''

    with open(f"{problem_dir}/tests_hidden.py", "w", encoding="utf-8") as f:
        f.write(tests_hidden)

    # rubric.json
    rubric_tests = []
    for test_name, _, _, points in problem["tests_public"]:
        rubric_tests.append({
            "name": test_name,
            "points": points,
            "visibility": "public"
        })
    for test_name, _, _, points in problem["tests_hidden"]:
        rubric_tests.append({
            "name": test_name,
            "points": points,
            "visibility": "hidden"
        })

    rubric = {
        "tests": rubric_tests,
        "max_points": sum(t[3] for t in problem["tests_public"] + problem["tests_hidden"])
    }

    with open(f"{problem_dir}/rubric.json", "w", encoding="utf-8") as f:
        json.dump(rubric, f, indent=2, ensure_ascii=False)

    print(f"✓ Creado: {problem_id}")

# Crear problemas restantes de Estructuras Secuenciales
for problem in PROBLEMS["estructuras-secuenciales"]:
    create_problem_files("estructuras-secuenciales", problem)

print("\n✅ Problemas creados exitosamente!")
