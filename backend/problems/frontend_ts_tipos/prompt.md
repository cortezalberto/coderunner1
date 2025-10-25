# Problema: Tipos en TypeScript

Aprende sobre el sistema de tipos de TypeScript y cómo proporciona seguridad de tipos.

## Concepto: TypeScript

TypeScript es un superset de JavaScript que añade tipado estático opcional. Los tipos ayudan a detectar errores en tiempo de compilación y mejoran la experiencia de desarrollo.

## Ejemplo de función con tipos en TypeScript

```typescript
function multiplicar(a: number, b: number): number {
    return a * b;
}

console.log(multiplicar(4, 5)); // Output: 20
```

Los tipos `number` garantizan que solo se pueden pasar números a la función.

## Ejercicio

Para este ejercicio conceptual, simula el comportamiento de una función TypeScript tipada que multiplica dos números.

Dados dos números: 4 y 5, imprime el resultado de multiplicarlos.

## Salida esperada

```
20
```

## Conceptos a practicar

- Tipos en TypeScript
- Anotaciones de tipo
- Type safety
- Funciones tipadas
