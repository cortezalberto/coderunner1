# Problema: Consulta Simple en Prolog (Paradigma Lógico)

Aprende los conceptos fundamentales del **Paradigma Lógico** usando Prolog.

## Concepto: Paradigma Lógico

El paradigma lógico se basa en:
- **Hechos**: Afirmaciones verdaderas
- **Reglas**: Relaciones lógicas
- **Consultas**: Preguntas al sistema
- **Unificación**: Búsqueda de soluciones

## Ejemplo en Prolog

```prolog
% Hechos
padre(juan, maria).
padre(juan, pedro).

% Regla
hijo(X, Y) :- padre(Y, X).

% Consulta
?- padre(juan, maria).
% Respuesta: true
```

## Ejercicio

Para este ejercicio conceptual, simula una consulta Prolog.

Dados los hechos:
- `padre(juan, maria)` es verdadero
- Consulta: `?- padre(juan, maria)`

## Salida

Imprime la respuesta de Prolog:
```
true
```

## Conceptos a practicar

- Hechos en Prolog
- Consultas
- Sistema de inferencia lógica
