# Problema: Validar contraseña

Implementa una función **`validar_password(password)`** que verifique si una contraseña tiene una longitud válida.

Una contraseña es válida si tiene **entre 8 y 14 caracteres** (incluyendo 8 y 14).

- Si la contraseña es válida, retornar: `"Ha ingresado una contraseña correcta"`
- Si la contraseña no es válida, retornar: `"Por favor, ingrese una contraseña de entre 8 y 14 caracteres"`

**Nota**: Usa la función `len()` para obtener la longitud de un string.

## Ejemplos
- `validar_password("abc12345")` → `"Ha ingresado una contraseña correcta"` (8 caracteres)
- `validar_password("password123456")` → `"Ha ingresado una contraseña correcta"` (14 caracteres)
- `validar_password("abc123")` → `"Por favor, ingrese una contraseña de entre 8 y 14 caracteres"` (6 caracteres)
- `validar_password("password12345678")` → `"Por favor, ingrese una contraseña de entre 8 y 14 caracteres"` (16 caracteres)

## Restricciones
- La función debe llamarse exactamente `validar_password`.
- Debe recibir un parámetro `password` (string).
- Debe retornar el mensaje correspondiente.
