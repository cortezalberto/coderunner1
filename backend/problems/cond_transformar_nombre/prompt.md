# Problema: Transformar nombre

Implementa una función **`transformar_nombre(nombre, opcion)`** que transforme un nombre según la opción seleccionada:

- **Opción 1**: Convertir a MAYÚSCULAS (usar método `upper()`)
- **Opción 2**: Convertir a minúsculas (usar método `lower()`)
- **Opción 3**: Primera letra en mayúscula (usar método `title()`)

Si se ingresa una opción inválida (diferente de 1, 2 o 3), retornar el mensaje: `"Opción inválida"`

## Ejemplos
- `transformar_nombre("pedro", 1)` → `"PEDRO"`
- `transformar_nombre("MARIA", 2)` → `"maria"`
- `transformar_nombre("juan", 3)` → `"Juan"`
- `transformar_nombre("ana", 5)` → `"Opción inválida"`

## Restricciones
- La función debe llamarse exactamente `transformar_nombre`.
- Debe recibir dos parámetros: `nombre` (string) y `opcion` (número entero).
- Debe retornar el nombre transformado o el mensaje de error.
