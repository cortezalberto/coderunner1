# Problema: Función Pura en Haskell (Paradigma Funcional)

Aprende los conceptos fundamentales del **Paradigma Funcional** usando Haskell.

## Concepto: Paradigma Funcional

El paradigma funcional se basa en:
- **Funciones puras**: Sin efectos secundarios, siempre retornan el mismo resultado para los mismos argumentos
- **Inmutabilidad**: Los datos no se modifican después de crearse
- **Expresiones**: Todo es una expresión que evalúa a un valor
- **Composición de funciones**: Construcción de funciones complejas a partir de funciones simples

## Ejemplo en Haskell

```haskell
-- Función pura: duplica un número
duplicar :: Int -> Int
duplicar x = x * 2

-- Composición de funciones
cuadruplicar :: Int -> Int
cuadruplicar = duplicar . duplicar

-- Uso
resultado = cuadruplicar 5  -- 20
```

## Ejercicio

Para este ejercicio conceptual, simula una función pura de Haskell.

En Haskell, una función que duplica un número sería:
```haskell
duplicar :: Int -> Int
duplicar x = x * 2

-- Uso
duplicar 5  -- Resultado: 10
```

## Entrada

Un número entero.

## Salida

El número duplicado (multiplicado por 2).

**Ejemplo:**
```
Entrada: 5
Salida: 10
```

## Conceptos a practicar

- Funciones puras en Haskell
- Inmutabilidad
- Evaluación de expresiones
- Tipado estático fuerte
