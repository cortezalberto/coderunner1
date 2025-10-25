# Problema: Clase Simple en Java (Paradigma Orientado a Objetos)

Aprende los conceptos fundamentales del **Paradigma Orientado a Objetos** usando Java.

## Concepto: Paradigma OO

El paradigma orientado a objetos se basa en:
- **Clases**: Plantillas para crear objetos
- **Objetos**: Instancias de clases con estado y comportamiento
- **Encapsulamiento**: Datos y métodos juntos
- **Abstracción**: Ocultar complejidad

## Ejemplo en Java

```java
public class Persona {
    private String nombre;
    private int edad;

    public Persona(String nombre, int edad) {
        this.nombre = nombre;
        this.edad = edad;
    }

    public String saludar() {
        return "Hola, soy " + nombre;
    }
}
```

## Ejercicio

Para este ejercicio conceptual, simula el comportamiento de una clase Java.
Imprime el mensaje que retornaría el método `saludar()` de un objeto Persona.

## Entrada

- Nombre: "Juan"
- Edad: 25

## Salida

```
Hola, soy Juan
```

## Conceptos a practicar

- Clases y objetos
- Métodos
- Estado del objeto
