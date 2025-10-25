#!/usr/bin/env python3
"""
Generador automático de problemas para Programación 1
Genera las 4 unidades restantes: Condicionales, Repetitivas, Listas, Funciones
"""
import os
import json

BASE_PATH = "backend/problems"

# Definiciones compactas de problemas por unidad
PROBLEMS_DATA = {
    "estructuras-condicionales": [
        {
            "id": "cond_mayor_de_dos",
            "title": "Mayor de dos números",
            "function": "mayor",
            "params": ["a", "b"],
            "desc": "Retorna el mayor de dos números",
            "examples": ["mayor(5, 10) -> 10", "mayor(20, 15) -> 20"],
            "tests_pub": [("test_mayor_primero", "a > b", 3), ("test_mayor_segundo", "b > a", 2), ("test_iguales", "a == b", 2)],
            "tests_hid": [("test_negativos", "negativos", 2), ("test_decimales", "decimales", 1)]
        },
        {
            "id": "cond_par_impar",
            "title": "Par o impar",
            "function": "es_par",
            "params": ["n"],
            "desc": "Retorna True si n es par, False si es impar",
            "examples": ["es_par(4) -> True", "es_par(7) -> False"],
            "tests_pub": [("test_par", "número par", 3), ("test_impar", "número impar", 2), ("test_cero", "cero", 2)],
            "tests_hid": [("test_negativo_par", "negativo par", 2), ("test_negativo_impar", "negativo impar", 1)]
        },
        {
            "id": "cond_positivo_negativo",
            "title": "Clasificar número",
            "function": "clasificar_numero",
            "params": ["n"],
            "desc": "Retorna 'positivo', 'negativo' o 'cero' según el número",
            "examples": ["clasificar_numero(5) -> 'positivo'", "clasificar_numero(-3) -> 'negativo'"],
            "tests_pub": [("test_positivo", "positivo", 3), ("test_negativo", "negativo", 2), ("test_cero", "cero", 2)],
            "tests_hid": [("test_decimal_positivo", "decimal positivo", 2), ("test_decimal_negativo", "decimal negativo", 1)]
        },
        {
            "id": "cond_calificacion",
            "title": "Letra de calificación",
            "function": "letra_calificacion",
            "params": ["nota"],
            "desc": "Retorna 'A' si nota >= 90, 'B' si >= 80, 'C' si >= 70, 'D' si >= 60, 'F' si < 60",
            "examples": ["letra_calificacion(95) -> 'A'", "letra_calificacion(75) -> 'C'"],
            "tests_pub": [("test_A", "nota A", 2), ("test_C", "nota C", 2), ("test_F", "nota F", 2)],
            "tests_hid": [("test_B", "nota B", 2), ("test_D", "nota D", 1), ("test_limite", "límite", 1)]
        },
        {
            "id": "cond_edad_categoria",
            "title": "Categoría por edad",
            "function": "categoria_edad",
            "params": ["edad"],
            "desc": "Retorna 'niño' si < 12, 'adolescente' si < 18, 'adulto' si < 65, 'adulto mayor' si >= 65",
            "examples": ["categoria_edad(10) -> 'niño'", "categoria_edad(25) -> 'adulto'"],
            "tests_pub": [("test_nino", "niño", 2), ("test_adulto", "adulto", 2), ("test_adulto_mayor", "adulto mayor", 2)],
            "tests_hid": [("test_adolescente", "adolescente", 2), ("test_limites", "casos límite", 2)]
        },
        {
            "id": "cond_bisiesto",
            "title": "Año bisiesto",
            "function": "es_bisiesto",
            "params": ["anio"],
            "desc": "Retorna True si el año es bisiesto",
            "examples": ["es_bisiesto(2020) -> True", "es_bisiesto(2021) -> False"],
            "tests_pub": [("test_multiplo_4", "múltiplo de 4", 2), ("test_no_bisiesto", "no bisiesto", 2), ("test_siglo", "año siglo", 3)],
            "tests_hid": [("test_2000", "año 2000", 2), ("test_1900", "año 1900", 1)]
        },
        {
            "id": "cond_triangulo_valido",
            "title": "Triángulo válido",
            "function": "es_triangulo_valido",
            "params": ["a", "b", "c"],
            "desc": "Retorna True si los tres lados pueden formar un triángulo",
            "examples": ["es_triangulo_valido(3, 4, 5) -> True", "es_triangulo_valido(1, 2, 10) -> False"],
            "tests_pub": [("test_triangulo_valido", "triángulo válido", 3), ("test_triangulo_invalido", "inválido", 3)],
            "tests_hid": [("test_equilatero", "equilátero", 2), ("test_escaleno", "escaleno", 2)]
        },
        {
            "id": "cond_descuento_tienda",
            "title": "Descuento por compra",
            "function": "calcular_descuento",
            "params": ["total"],
            "desc": "Retorna 20% desc si total >= 1000, 10% si >= 500, 5% si >= 100, 0% si < 100",
            "examples": ["calcular_descuento(1200) -> 240.0", "calcular_descuento(400) -> 0.0"],
            "tests_pub": [("test_desc_20", "descuento 20%", 3), ("test_desc_10", "descuento 10%", 2), ("test_sin_desc", "sin descuento", 2)],
            "tests_hid": [("test_desc_5", "descuento 5%", 2), ("test_limite", "caso límite", 1)]
        },
        {
            "id": "cond_signo_zodiacal",
            "title": "Signo zodiacal simplificado",
            "function": "signo_zodiacal",
            "params": ["mes", "dia"],
            "desc": "Retorna signo zodiacal (simplificado para mes completo)",
            "examples": ["signo_zodiacal(3, 25) -> 'Aries'", "signo_zodiacal(7, 10) -> 'Cáncer'"],
            "tests_pub": [("test_aries", "Aries", 2), ("test_cancer", "Cáncer", 2), ("test_capricornio", "Capricornio", 2)],
            "tests_hid": [("test_geminis", "Géminis", 2), ("test_escorpio", "Escorpio", 2)]
        },
        {
            "id": "cond_imc_categoria",
            "title": "Categoría IMC",
            "function": "categoria_imc",
            "params": ["peso", "altura"],
            "desc": "Calcula IMC y retorna categoría: 'bajo peso' <18.5, 'normal' <25, 'sobrepeso' <30, 'obesidad' >=30",
            "examples": ["categoria_imc(70, 1.75) -> 'normal'"],
            "tests_pub": [("test_normal", "peso normal", 3), ("test_sobrepeso", "sobrepeso", 2), ("test_obesidad", "obesidad", 2)],
            "tests_hid": [("test_bajo_peso", "bajo peso", 2), ("test_limite", "caso límite", 1)]
        }
    ],
    "estructuras-repetitivas": [
        {
            "id": "rep_suma_n",
            "title": "Suma de 1 a N",
            "function": "suma_hasta_n",
            "params": ["n"],
            "desc": "Retorna la suma de 1 + 2 + ... + n",
            "examples": ["suma_hasta_n(5) -> 15", "suma_hasta_n(10) -> 55"],
            "tests_pub": [("test_suma_5", "suma hasta 5", 3), ("test_suma_10", "suma hasta 10", 2), ("test_suma_1", "n=1", 2)],
            "tests_hid": [("test_suma_100", "suma hasta 100", 2), ("test_suma_0", "n=0", 1)]
        },
        {
            "id": "rep_factorial",
            "title": "Factorial",
            "function": "factorial",
            "params": ["n"],
            "desc": "Retorna n! = n × (n-1) × ... × 1",
            "examples": ["factorial(5) -> 120", "factorial(0) -> 1"],
            "tests_pub": [("test_factorial_5", "5!", 3), ("test_factorial_0", "0!", 2), ("test_factorial_1", "1!", 2)],
            "tests_hid": [("test_factorial_10", "10!", 2), ("test_factorial_grande", "número grande", 1)]
        },
        {
            "id": "rep_contar_digitos",
            "title": "Contar dígitos",
            "function": "contar_digitos",
            "params": ["n"],
            "desc": "Retorna la cantidad de dígitos de n",
            "examples": ["contar_digitos(12345) -> 5", "contar_digitos(7) -> 1"],
            "tests_pub": [("test_un_digito", "un dígito", 2), ("test_cinco_digitos", "cinco dígitos", 3), ("test_cero", "cero", 2)],
            "tests_hid": [("test_negativo", "número negativo", 2), ("test_grande", "número grande", 1)]
        },
        {
            "id": "rep_invertir_numero",
            "title": "Invertir número",
            "function": "invertir_numero",
            "params": ["n"],
            "desc": "Retorna el número con dígitos invertidos",
            "examples": ["invertir_numero(12345) -> 54321", "invertir_numero(100) -> 1"],
            "tests_pub": [("test_123", "invertir 123", 3), ("test_100", "invertir 100", 2), ("test_un_digito", "un dígito", 2)],
            "tests_hid": [("test_palindromo", "palíndromo", 2), ("test_negativo", "negativo", 1)]
        },
        {
            "id": "rep_fibonacci",
            "title": "N-ésimo Fibonacci",
            "function": "fibonacci",
            "params": ["n"],
            "desc": "Retorna el n-ésimo número de Fibonacci",
            "examples": ["fibonacci(6) -> 8", "fibonacci(10) -> 55"],
            "tests_pub": [("test_fib_6", "fib(6)", 3), ("test_fib_0", "fib(0)", 2), ("test_fib_1", "fib(1)", 2)],
            "tests_hid": [("test_fib_15", "fib(15)", 2), ("test_fib_20", "fib(20)", 1)]
        },
        {
            "id": "rep_es_primo",
            "title": "Número primo",
            "function": "es_primo",
            "params": ["n"],
            "desc": "Retorna True si n es primo",
            "examples": ["es_primo(7) -> True", "es_primo(10) -> False"],
            "tests_pub": [("test_primo_7", "7 es primo", 3), ("test_no_primo_10", "10 no es primo", 2), ("test_2", "2 es primo", 2)],
            "tests_hid": [("test_primo_grande", "primo grande", 2), ("test_1", "1 no es primo", 1)]
        },
        {
            "id": "rep_tabla_multiplicar",
            "title": "Tabla de multiplicar",
            "function": "tabla_multiplicar",
            "params": ["n"],
            "desc": "Retorna lista con tabla del n del 1 al 10",
            "examples": ["tabla_multiplicar(3) -> [3, 6, 9, ..., 30]"],
            "tests_pub": [("test_tabla_3", "tabla del 3", 3), ("test_tabla_1", "tabla del 1", 2), ("test_tabla_10", "tabla del 10", 2)],
            "tests_hid": [("test_tabla_7", "tabla del 7", 2), ("test_suma_tabla", "suma correcta", 1)]
        },
        {
            "id": "rep_mcd",
            "title": "Máximo común divisor",
            "function": "mcd",
            "params": ["a", "b"],
            "desc": "Retorna el MCD usando algoritmo de Euclides",
            "examples": ["mcd(48, 18) -> 6", "mcd(100, 50) -> 50"],
            "tests_pub": [("test_mcd_48_18", "mcd(48,18)", 3), ("test_mcd_100_50", "mcd(100,50)", 2), ("test_mcd_primos", "números primos", 2)],
            "tests_hid": [("test_mcd_iguales", "números iguales", 2), ("test_mcd_grande", "números grandes", 1)]
        },
        {
            "id": "rep_potencia",
            "title": "Potencia iterativa",
            "function": "potencia",
            "params": ["base", "exponente"],
            "desc": "Calcula base^exponente usando un bucle",
            "examples": ["potencia(2, 3) -> 8", "potencia(5, 0) -> 1"],
            "tests_pub": [("test_2_3", "2^3", 3), ("test_5_0", "5^0", 2), ("test_10_2", "10^2", 2)],
            "tests_hid": [("test_negativo", "exponente negativo", 2), ("test_grande", "potencia grande", 1)]
        },
        {
            "id": "rep_suma_pares",
            "title": "Suma de pares hasta N",
            "function": "suma_pares",
            "params": ["n"],
            "desc": "Retorna la suma de números pares desde 2 hasta n",
            "examples": ["suma_pares(10) -> 30", "suma_pares(5) -> 6"],
            "tests_pub": [("test_suma_pares_10", "hasta 10", 3), ("test_suma_pares_5", "hasta 5", 2), ("test_suma_pares_1", "hasta 1", 2)],
            "tests_hid": [("test_suma_pares_100", "hasta 100", 2), ("test_suma_pares_par", "n par", 1)]
        }
    ],
    "listas": [
        {
            "id": "lista_suma",
            "title": "Suma de lista",
            "function": "suma_lista",
            "params": ["lista"],
            "desc": "Retorna la suma de todos los elementos",
            "examples": ["suma_lista([1, 2, 3]) -> 6", "suma_lista([]) -> 0"],
            "tests_pub": [("test_suma_simple", "lista simple", 3), ("test_lista_vacia", "lista vacía", 2), ("test_negativos", "con negativos", 2)],
            "tests_hid": [("test_decimales", "decimales", 2), ("test_grande", "lista grande", 1)]
        },
        {
            "id": "lista_maximo",
            "title": "Máximo de lista",
            "function": "maximo_lista",
            "params": ["lista"],
            "desc": "Retorna el elemento máximo",
            "examples": ["maximo_lista([3, 1, 5, 2]) -> 5"],
            "tests_pub": [("test_max_simple", "lista simple", 3), ("test_un_elemento", "un elemento", 2), ("test_negativos", "negativos", 2)],
            "tests_hid": [("test_duplicados", "con duplicados", 2), ("test_ordenada", "lista ordenada", 1)]
        },
        {
            "id": "lista_promedio",
            "title": "Promedio de lista",
            "function": "promedio_lista",
            "params": ["lista"],
            "desc": "Retorna el promedio de los elementos",
            "examples": ["promedio_lista([10, 20, 30]) -> 20.0"],
            "tests_pub": [("test_prom_simple", "lista simple", 3), ("test_prom_iguales", "elementos iguales", 2), ("test_prom_decimales", "decimales", 2)],
            "tests_hid": [("test_prom_negativos", "con negativos", 2), ("test_prom_precision", "precisión", 1)]
        },
        {
            "id": "lista_invertir",
            "title": "Invertir lista",
            "function": "invertir_lista",
            "params": ["lista"],
            "desc": "Retorna una nueva lista con elementos en orden inverso",
            "examples": ["invertir_lista([1, 2, 3]) -> [3, 2, 1]"],
            "tests_pub": [("test_inv_simple", "lista simple", 3), ("test_inv_vacia", "lista vacía", 2), ("test_inv_un_elem", "un elemento", 2)],
            "tests_hid": [("test_inv_palindromo", "palíndromo", 2), ("test_inv_strings", "strings", 1)]
        },
        {
            "id": "lista_contar",
            "title": "Contar elemento",
            "function": "contar_elemento",
            "params": ["lista", "elemento"],
            "desc": "Retorna cuántas veces aparece elemento en lista",
            "examples": ["contar_elemento([1, 2, 1, 3], 1) -> 2"],
            "tests_pub": [("test_cont_varias", "varias veces", 3), ("test_cont_una", "una vez", 2), ("test_cont_cero", "cero veces", 2)],
            "tests_hid": [("test_cont_todos", "todos iguales", 2), ("test_cont_strings", "strings", 1)]
        },
        {
            "id": "lista_eliminar_duplicados",
            "title": "Eliminar duplicados",
            "function": "eliminar_duplicados",
            "params": ["lista"],
            "desc": "Retorna lista sin elementos duplicados (mantiene orden)",
            "examples": ["eliminar_duplicados([1, 2, 1, 3]) -> [1, 2, 3]"],
            "tests_pub": [("test_elim_dup", "con duplicados", 3), ("test_sin_dup", "sin duplicados", 2), ("test_vacia", "lista vacía", 2)],
            "tests_hid": [("test_todos_dup", "todos duplicados", 2), ("test_strings", "strings", 1)]
        },
        {
            "id": "lista_buscar",
            "title": "Buscar elemento",
            "function": "buscar_elemento",
            "params": ["lista", "elemento"],
            "desc": "Retorna el índice de elemento, o -1 si no existe",
            "examples": ["buscar_elemento([10, 20, 30], 20) -> 1"],
            "tests_pub": [("test_busc_existe", "elemento existe", 3), ("test_busc_no_existe", "no existe", 2), ("test_busc_inicio", "al inicio", 2)],
            "tests_hid": [("test_busc_duplicado", "elemento duplicado", 2), ("test_busc_strings", "strings", 1)]
        },
        {
            "id": "lista_filtrar_pares",
            "title": "Filtrar pares",
            "function": "filtrar_pares",
            "params": ["lista"],
            "desc": "Retorna nueva lista solo con números pares",
            "examples": ["filtrar_pares([1, 2, 3, 4]) -> [2, 4]"],
            "tests_pub": [("test_filt_mixtos", "pares e impares", 3), ("test_filt_solo_pares", "solo pares", 2), ("test_filt_solo_impares", "solo impares", 2)],
            "tests_hid": [("test_filt_vacia", "lista vacía", 2), ("test_filt_negativos", "negativos", 1)]
        },
        {
            "id": "lista_concatenar",
            "title": "Concatenar listas",
            "function": "concatenar_listas",
            "params": ["lista1", "lista2"],
            "desc": "Retorna una lista con elementos de ambas listas",
            "examples": ["concatenar_listas([1, 2], [3, 4]) -> [1, 2, 3, 4]"],
            "tests_pub": [("test_concat_normales", "dos listas", 3), ("test_concat_vacia1", "primera vacía", 2), ("test_concat_vacia2", "segunda vacía", 2)],
            "tests_hid": [("test_concat_ambas_vacias", "ambas vacías", 2), ("test_concat_strings", "strings", 1)]
        },
        {
            "id": "lista_ordenar",
            "title": "Ordenar lista",
            "function": "ordenar_lista",
            "params": ["lista"],
            "desc": "Retorna nueva lista ordenada ascendentemente",
            "examples": ["ordenar_lista([3, 1, 2]) -> [1, 2, 3]"],
            "tests_pub": [("test_ord_desordenada", "desordenada", 3), ("test_ord_ordenada", "ya ordenada", 2), ("test_ord_vacia", "vacía", 2)],
            "tests_hid": [("test_ord_inversa", "inversa", 2), ("test_ord_duplicados", "duplicados", 1)]
        }
    ],
    "funciones": [
        {
            "id": "func_cuadrado",
            "title": "Función cuadrado",
            "function": "cuadrado",
            "params": ["x"],
            "desc": "Retorna x al cuadrado",
            "examples": ["cuadrado(5) -> 25", "cuadrado(-3) -> 9"],
            "tests_pub": [("test_cuad_positivo", "positivo", 3), ("test_cuad_negativo", "negativo", 2), ("test_cuad_cero", "cero", 2)],
            "tests_hid": [("test_cuad_decimal", "decimal", 2), ("test_cuad_grande", "grande", 1)]
        },
        {
            "id": "func_es_vocal",
            "title": "Es vocal",
            "function": "es_vocal",
            "params": ["letra"],
            "desc": "Retorna True si letra es vocal (a,e,i,o,u mayúscula o minúscula)",
            "examples": ["es_vocal('a') -> True", "es_vocal('b') -> False"],
            "tests_pub": [("test_vocal_min", "vocal minúscula", 2), ("test_vocal_may", "vocal mayúscula", 2), ("test_consonante", "consonante", 2)],
            "tests_hid": [("test_vocal_acentuada", "acentuada", 2), ("test_numero", "número", 2)]
        },
        {
            "id": "func_contar_vocales",
            "title": "Contar vocales",
            "function": "contar_vocales",
            "params": ["texto"],
            "desc": "Retorna cantidad de vocales en texto",
            "examples": ["contar_vocales('Hola') -> 2"],
            "tests_pub": [("test_cont_voc_simple", "texto simple", 3), ("test_cont_voc_sin", "sin vocales", 2), ("test_cont_voc_vacio", "vacío", 2)],
            "tests_hid": [("test_cont_voc_mix", "mayúsculas y minúsculas", 2), ("test_cont_voc_numeros", "con números", 1)]
        },
        {
            "id": "func_celsius_fahrenheit",
            "title": "Convertir temperatura",
            "function": "celsius_a_fahrenheit",
            "params": ["celsius"],
            "desc": "Convierte Celsius a Fahrenheit",
            "examples": ["celsius_a_fahrenheit(0) -> 32.0"],
            "tests_pub": [("test_temp_congelacion", "congelación", 3), ("test_temp_ebullicion", "ebullición", 2), ("test_temp_ambiente", "ambiente", 2)],
            "tests_hid": [("test_temp_negativa", "negativa", 2), ("test_temp_decimal", "decimal", 1)]
        },
        {
            "id": "func_calcular_area_circulo",
            "title": "Área de círculo",
            "function": "area_circulo",
            "params": ["radio"],
            "desc": "Calcula área del círculo",
            "examples": ["area_circulo(5) -> 78.54 (aprox)"],
            "tests_pub": [("test_area_radio_1", "radio 1", 3), ("test_area_radio_5", "radio 5", 2), ("test_area_radio_0", "radio 0", 2)],
            "tests_hid": [("test_area_decimal", "radio decimal", 2), ("test_area_grande", "radio grande", 1)]
        },
        {
            "id": "func_es_palindromo",
            "title": "Es palíndromo",
            "function": "es_palindromo",
            "params": ["texto"],
            "desc": "Retorna True si texto es palíndromo (ignora espacios y mayúsculas)",
            "examples": ["es_palindromo('anilina') -> True"],
            "tests_pub": [("test_pal_simple", "palíndromo simple", 3), ("test_pal_no", "no palíndromo", 2), ("test_pal_espacios", "con espacios", 2)],
            "tests_hid": [("test_pal_mayusculas", "mayúsculas", 2), ("test_pal_frase", "frase", 1)]
        },
        {
            "id": "func_contar_palabras",
            "title": "Contar palabras",
            "function": "contar_palabras",
            "params": ["texto"],
            "desc": "Retorna cantidad de palabras en texto",
            "examples": ["contar_palabras('Hola mundo') -> 2"],
            "tests_pub": [("test_cont_pal_dos", "dos palabras", 3), ("test_cont_pal_una", "una palabra", 2), ("test_cont_pal_vacio", "vacío", 2)],
            "tests_hid": [("test_cont_pal_muchos_espacios", "múltiples espacios", 2), ("test_cont_pal_puntuacion", "puntuación", 1)]
        },
        {
            "id": "func_sumar_lista",
            "title": "Sumar lista (función)",
            "function": "sumar_lista",
            "params": ["numeros"],
            "desc": "Retorna suma de lista usando función",
            "examples": ["sumar_lista([1, 2, 3]) -> 6"],
            "tests_pub": [("test_sum_lista_simple", "lista simple", 3), ("test_sum_lista_vacia", "lista vacía", 2), ("test_sum_lista_negativos", "negativos", 2)],
            "tests_hid": [("test_sum_lista_decimales", "decimales", 2), ("test_sum_lista_grande", "lista grande", 1)]
        },
        {
            "id": "func_producto_lista",
            "title": "Producto de lista",
            "function": "producto_lista",
            "params": ["numeros"],
            "desc": "Retorna producto de todos los elementos",
            "examples": ["producto_lista([2, 3, 4]) -> 24"],
            "tests_pub": [("test_prod_simple", "simple", 3), ("test_prod_con_cero", "con cero", 2), ("test_prod_uno", "un elemento", 2)],
            "tests_hid": [("test_prod_negativos", "negativos", 2), ("test_prod_decimales", "decimales", 1)]
        },
        {
            "id": "func_maximo_tres",
            "title": "Máximo de tres",
            "function": "maximo_de_tres",
            "params": ["a", "b", "c"],
            "desc": "Retorna el mayor de tres números",
            "examples": ["maximo_de_tres(1, 5, 3) -> 5"],
            "tests_pub": [("test_max3_primero", "primero mayor", 2), ("test_max3_segundo", "segundo mayor", 2), ("test_max3_tercero", "tercero mayor", 2)],
            "tests_hid": [("test_max3_iguales", "todos iguales", 2), ("test_max3_negativos", "negativos", 2)]
        }
    ]
}

def create_problem_files(unit_id, problem):
    """Crea todos los archivos para un problema"""
    problem_id = problem["id"]
    problem_dir = os.path.join(BASE_PATH, problem_id)

    os.makedirs(problem_dir, exist_ok=True)

    # metadata.json
    metadata = {
        "title": problem["title"],
        "subject_id": "programacion-1",
        "unit_id": unit_id,
        "difficulty": "easy",
        "tags": ["basico", "practica"],
        "timeout_sec": 3.0,
        "memory_mb": 128
    }
    with open(os.path.join(problem_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    # prompt.md
    examples_str = "\n".join([f"- `{ex}`" for ex in problem["examples"]])
    prompt = f"""# Problema: {problem["title"]}

Implementa una función **`{problem["function"]}({", ".join(problem["params"])})`**.

{problem["desc"]}

## Ejemplos
{examples_str}

**Restricciones**
- La función debe llamarse exactamente `{problem["function"]}`.
"""
    with open(os.path.join(problem_dir, "prompt.md"), "w", encoding="utf-8") as f:
        f.write(prompt)

    # starter.py
    params_str = ", ".join(problem["params"])
    starter = f"""def {problem["function"]}({params_str}):
    # TODO: Implementa la función
    pass
"""
    with open(os.path.join(problem_dir, "starter.py"), "w", encoding="utf-8") as f:
        f.write(starter)

    # tests_public.py
    tests_public = f"""import importlib.util
import os

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

"""
    for test_name, desc, points in problem["tests_pub"]:
        tests_public += f'''def {test_name}():
    """Test {desc}"""
    assert hasattr(student, "{problem["function"]}"), "Debe existir la función {problem["function"]}"
    # TODO: Implementar test real
    pass

'''
    with open(os.path.join(problem_dir, "tests_public.py"), "w", encoding="utf-8") as f:
        f.write(tests_public)

    # tests_hidden.py
    tests_hidden = f"""import importlib.util
import os

spec = importlib.util.spec_from_file_location("student_code", os.path.join(os.getcwd(), "student_code.py"))
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

"""
    for test_name, desc, points in problem["tests_hid"]:
        tests_hidden += f'''def {test_name}():
    """Test oculto {desc}"""
    # TODO: Implementar test real
    pass

'''
    with open(os.path.join(problem_dir, "tests_hidden.py"), "w", encoding="utf-8") as f:
        f.write(tests_hidden)

    # rubric.json
    rubric_tests = []
    for test_name, _, points in problem["tests_pub"]:
        rubric_tests.append({"name": test_name, "points": points, "visibility": "public"})
    for test_name, _, points in problem["tests_hid"]:
        rubric_tests.append({"name": test_name, "points": points, "visibility": "hidden"})

    total_points = sum(t[2] for t in problem["tests_pub"] + problem["tests_hid"])
    rubric = {"tests": rubric_tests, "max_points": total_points}

    with open(os.path.join(problem_dir, "rubric.json"), "w", encoding="utf-8") as f:
        json.dump(rubric, f, indent=2, ensure_ascii=False)

    print(f"✓ Creado: {problem_id}")

def main():
    print("Generando problemas para las 4 unidades restantes...\n")

    for unit_id, problems in PROBLEMS_DATA.items():
        print(f"\n📚 Unidad: {unit_id}")
        print("=" * 60)
        for problem in problems:
            create_problem_files(unit_id, problem)

    print(f"\n\n✅ ¡Completado! Se crearon {sum(len(p) for p in PROBLEMS_DATA.values())} problemas.")

if __name__ == "__main__":
    main()
