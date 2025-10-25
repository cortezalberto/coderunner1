# Problema: Clasificación de terremoto

Implementa una función **`clasificar_terremoto(magnitud)`** que clasifique un terremoto según la escala de Richter:

- **Menor que 3**: `"Muy leve"` (imperceptible)
- **Mayor o igual a 3 y menor que 4**: `"Leve"` (ligeramente perceptible)
- **Mayor o igual a 4 y menor que 5**: `"Moderado"` (sentido por personas, pero generalmente no causa daños)
- **Mayor o igual a 5 y menor que 6**: `"Fuerte"` (puede causar daños en estructuras débiles)
- **Mayor o igual a 6 y menor que 7**: `"Muy Fuerte"` (puede causar daños significativos)
- **Mayor o igual a 7**: `"Extremo"` (puede causar graves daños a gran escala)

## Ejemplos
- `clasificar_terremoto(2.5)` → `"Muy leve"`
- `clasificar_terremoto(3.7)` → `"Leve"`
- `clasificar_terremoto(4.8)` → `"Moderado"`
- `clasificar_terremoto(5.5)` → `"Fuerte"`
- `clasificar_terremoto(6.3)` → `"Muy Fuerte"`
- `clasificar_terremoto(8.0)` → `"Extremo"`

## Restricciones
- La función debe llamarse exactamente `clasificar_terremoto`.
- Debe recibir un parámetro `magnitud` (número decimal).
- Debe retornar el string correspondiente a la clasificación.
