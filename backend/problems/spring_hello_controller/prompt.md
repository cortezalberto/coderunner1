# Problema: Hello World REST Controller

Crea un controlador REST básico en Spring Boot que responda con un mensaje de bienvenida.

## Objetivo

Implementar un **REST Controller** que exponga un endpoint GET en `/api/hello` y retorne el mensaje `"Hello, Spring Boot!"`.

## Requisitos

1. **Crear una clase Controller** con la anotación `@RestController`
2. **Mapear el endpoint** usando `@GetMapping("/api/hello")`
3. **Retornar el mensaje** `"Hello, Spring Boot!"`

## Ejemplo de uso

```
GET /api/hello

Respuesta: "Hello, Spring Boot!"
```

## Conceptos a practicar

- `@RestController`: Marca la clase como un controlador REST
- `@GetMapping`: Mapea peticiones HTTP GET a un método
- Retorno de String: Spring Boot lo convierte automáticamente a JSON/texto

## Entrada

No hay entrada. El endpoint no recibe parámetros.

## Salida

La cadena de texto: `"Hello, Spring Boot!"`

## Restricciones

- El método debe llamarse `hello()`
- La clase debe llamarse `HelloController`
- El endpoint debe ser exactamente `/api/hello`
