# Problema: String termina en vocal

Implementa una función **`procesar_string(texto)`** que verifique si un string termina en vocal.

- Si el string termina con vocal (a, e, i, o, u), agregar un signo de exclamación `!` al final y retornar el resultado.
- Si el string NO termina con vocal, retornar el string tal cual (sin modificar).

**Nota**: Considera tanto vocales minúsculas como mayúsculas.

## Ejemplos
- `procesar_string("casa")` → `"casa!"`
- `procesar_string("papel")` → `"papel"`
- `procesar_string("Chile")` → `"Chile!"`
- `procesar_string("amor")` → `"amor"`

## Restricciones
- La función debe llamarse exactamente `procesar_string`.
- Debe recibir un parámetro `texto` (string).
- Debe retornar el string procesado.
- Considera vocales en mayúsculas y minúsculas.
