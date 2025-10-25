# Problema: Categorías de edad

Implementa el código en la función que se llame **`main`** que clasifique a una persona según su edad en una de las siguientes categorías:
Entrada:
El programa leerá exactamente un valor desde la entrada estándar (stdin).
Ese valor será un número entero; puedes convertirlo con int().
Salida:
Imprimir exactamente una línea seguida de un salto de línea final.
La única salida posible debe ser una de las dos cadenas precisas:
"Es mayor de edad" (cuando edad > 18)
"No es mayor de edad" (en cualquier otro caso)
No imprimir adicionales (mensajes, prompts, etiquetas, ni espacios innecesarios).
Formato y comparación:
La comparación en el autograder será exacta (incluye mayúsculas, minúsculas y espacios).
El autograder puede aplicar strip() antes de comparar si se desea tolerancia a espacios en los extremos.
Comportamiento esperado en bordes:
Para edad = 18 debe imprimirse "No es mayor de edad".
Para valores mayores a 18 imprimir "Es mayor de edad".
Para valores menores o iguales a 18 imprimir "No es mayor de edad".
Robustez:
Se asume entrada válida; no es necesario manejar excepciones por entradas no numéricas.
Ejemplos (entrada completa -> salida exacta):
Entrada: "20\n" -> Salida: "Es mayor de edad\n"
Entrada: "18\n" -> Salida: "No es mayor de edad\n"
Entrada: "0\n" -> Salida: "No es mayor de edad\n"
- El programa  debe llamarse exactamente `main`.

