# 💡 Sistema de Pistas Progresivas - Progressive Hint System

## Descripción

Sistema de 4 niveles de pistas progresivas que ayuda a los estudiantes a resolver problemas sin darles la solución completa inmediatamente. Fomenta el aprendizaje activo mediante revelación progresiva de información.

## Características

### ✨ Funcionalidades

1. **4 Niveles de Pistas**: Progresión gradual desde orientación general hasta solución casi completa
2. **Contador Visual**: Muestra "Pista X de Y" en el botón y en los mensajes
3. **Cambio de Color**: El botón se vuelve gris cuando se agotan todas las pistas
4. **Reset Automático**: Las pistas se reinician al cambiar de problema
5. **Tooltip Informativo**: Indica qué pista se mostrará al hacer hover
6. **Fallback Genérico**: Mensaje de ayuda para problemas sin pistas configuradas

### 🎯 Niveles de Pistas (Estructura Recomendada)

#### Nivel 1: Orientación General
- Identifica qué datos necesitas leer
- Estructura general del problema
- Conceptos clave a recordar

**Ejemplo**: "Recuerda que debes crear una función main() que lea la entrada con input()."

#### Nivel 2: Guía de Funciones
- Qué funciones o métodos usar
- Formato de salida esperado
- Operaciones principales

**Ejemplo**: "Usa print() para mostrar el resultado. El formato debe ser exactamente 'Hola, {nombre}!'."

#### Nivel 3: Sintaxis y Código
- Ejemplos de sintaxis específica
- Fragmentos de código útiles
- Fórmulas o patrones

**Ejemplo**: "Puedes usar f-strings para formatear el texto: f'Hola, {nombre}!'"

#### Nivel 4: Solución Casi Completa
- Explicación paso a paso
- Todos los elementos necesarios mencionados
- No el código literal, pero muy cerca

**Ejemplo**: "Solución completa: Lee el nombre con input(), formatea con f-string y usa print() para mostrar el saludo."

## Implementación

### Frontend (Playground.tsx)

**Estado**:
```typescript
const [currentHintLevel, setCurrentHintLevel] = useState<number>(0)
```

**Función de Manejo**:
```typescript
const handleHint = () => {
  if (!selectedProblem || !selectedProblem.metadata.hints) {
    // Fallback message
    alert('💡 Pista: Lee cuidadosamente el enunciado...')
    return
  }

  const hints = selectedProblem.metadata.hints
  const maxLevel = hints.length

  if (currentHintLevel >= maxLevel) {
    alert(`🎓 Ya has visto todas las pistas (${maxLevel}/${maxLevel})`)
    return
  }

  const hintMessage = `💡 Pista ${currentHintLevel + 1} de ${maxLevel}:\n\n${hints[currentHintLevel]}`

  if (currentHintLevel === maxLevel - 1) {
    alert(`${hintMessage}\n\n⚠️ Esta es la última pista disponible.`)
  } else {
    alert(hintMessage)
  }

  setCurrentHintLevel(currentHintLevel + 1)
}
```

**Reset al Cambiar Problema**:
```typescript
useEffect(() => {
  setCurrentHintLevel(0)
}, [selectedProblemId])
```

**Botón con Estado Visual**:
```typescript
<button
  onClick={handleHint}
  style={{
    backgroundColor: currentHintLevel >= hintsLength ? '#9E9E9E' : '#4CAF50',
    // ... otros estilos
  }}
  disabled={!selectedProblem}
>
  💡 Dame una pista {currentHintLevel > 0 && `(${currentHintLevel}/${hintsLength})`}
</button>
```

### Backend (metadata.json)

**Estructura**:
```json
{
  "title": "Título del problema",
  "subject_id": "programacion-1",
  "unit_id": "estructuras-secuenciales",
  "difficulty": "easy",
  "tags": ["tag1", "tag2"],
  "timeout_sec": 3.0,
  "memory_mb": 128,
  "hints": [
    "Pista nivel 1: orientación general",
    "Pista nivel 2: funciones específicas",
    "Pista nivel 3: sintaxis y ejemplos",
    "Pista nivel 4: solución casi completa"
  ]
}
```

**Nota**: El campo `hints` es opcional. Si no existe, se muestra mensaje genérico.

### Tipos TypeScript (api.ts)

```typescript
export interface ProblemMetadata {
  title: string
  subject_id: string
  unit_id: string
  difficulty?: string
  tags?: string[]
  timeout_sec?: number
  memory_mb?: number
  hints?: string[]  // ← Nuevo campo
}
```

## Agregar Pistas a Problemas

### Método Manual

Edita `backend/problems/{problem_id}/metadata.json`:

```json
{
  ...existing fields...,
  "hints": [
    "Tu pista nivel 1",
    "Tu pista nivel 2",
    "Tu pista nivel 3",
    "Tu pista nivel 4"
  ]
}
```

### Método Automático (Script)

Usa `add_hints_to_problems.py` para agregar pistas genéricas a todos los problemas:

```bash
python add_hints_to_problems.py
```

**Qué hace**:
- Escanea todos los problemas en `backend/problems/`
- Agrega 4 pistas genéricas a los que no tienen
- Salta los que ya tienen pistas
- Reporta cuántos fueron actualizados

**Pistas genéricas por defecto**:
1. "Lee cuidadosamente el enunciado del problema y identifica qué datos necesitas leer con input()."
2. "Recuerda que debes crear una función main() que contenga toda tu lógica. Usa print() para mostrar el resultado."
3. "Revisa el código starter provisto. Completa la sección TODO con la lógica necesaria según el enunciado."
4. "Asegúrate de seguir el formato de salida exacto que pide el problema. Revisa los ejemplos de entrada/salida."

## Mejores Prácticas

### ✅ Hacer

1. **Progresión gradual**: Cada pista debe dar más información que la anterior
2. **Específico al problema**: Personaliza las pistas para cada ejercicio
3. **No dar código literal**: Explica QUÉ hacer, no des el código completo
4. **Usar ejemplos**: En nivel 3-4, muestra fragmentos de sintaxis útiles
5. **Mencionar errores comunes**: Advierte sobre pitfalls típicos

### ❌ Evitar

1. **No repetir el enunciado**: Las pistas deben AGREGAR información
2. **No dar la solución en nivel 1-2**: Respetar la progresión
3. **No ser demasiado vago**: "Piensa bien" no es una pista útil
4. **No asumir conocimiento previo**: Explicar conceptos necesarios
5. **No hacer las pistas muy largas**: Máximo 2-3 oraciones por pista

## Ejemplos de Buenos Conjuntos de Pistas

### Problema: Área del Círculo

```json
{
  "hints": [
    "La fórmula del área de un círculo es A = π × r²",
    "Python tiene una constante para π en el módulo math: import math y luego usa math.pi",
    "Lee el radio con float(input()) y eleva al cuadrado con r**2 o r*r",
    "Solución: import math, luego area = math.pi * radio * radio"
  ]
}
```

### Problema: Saludo Personalizado

```json
{
  "hints": [
    "Recuerda que debes crear una función main() que lea la entrada con input().",
    "Usa print() para mostrar el resultado. El formato debe ser exactamente 'Hola, {nombre}!'.",
    "Puedes usar f-strings para formatear el texto: f'Hola, {nombre}!'",
    "Solución completa: Lee el nombre con input(), formatea con f-string y usa print() para mostrar el saludo."
  ]
}
```

### Problema: Número Par/Impar

```json
{
  "hints": [
    "Un número es par si es divisible entre 2 (el residuo de la división es 0).",
    "El operador módulo (%) te da el residuo de una división: 5 % 2 = 1, 4 % 2 = 0",
    "Usa una condición if: if numero % 2 == 0: print('Par') else: print('Impar')",
    "Lee el número con int(input()), verifica con % 2, e imprime 'Par' o 'Impar' según corresponda."
  ]
}
```

## Estadísticas del Sistema

**Problemas con pistas**: 31/31 (100%)
- 2 problemas con pistas personalizadas
- 29 problemas con pistas genéricas

**Total de pistas en el sistema**: 124 pistas (31 problemas × 4 niveles)

## Beneficios Pedagógicos

### Para Estudiantes

- 📚 **Aprendizaje guiado**: No se sienten abandonados ante un problema difícil
- 💪 **Desarrollo de autonomía**: Pueden elegir cuánta ayuda necesitan
- 🎯 **Reducción de frustración**: Pistas evitan bloqueos totales
- 🧠 **Retención mejorada**: Llegar a la solución con ayuda progresiva refuerza el aprendizaje

### Para Instructores

- ⏱️ **Menos consultas repetitivas**: Pistas responden preguntas comunes
- 📊 **Datos de dificultad**: Ver cuántas pistas usan indica dificultad del problema
- 🎓 **Evaluación formativa**: Saber en qué nivel se atascan los estudiantes
- 🔄 **Escalable**: Sistema automático que funciona 24/7

## Métricas Futuras (Posibles Extensiones)

### Tracking de Uso
- Registrar cuántas pistas usa cada estudiante por problema
- Identificar problemas que requieren más ayuda
- Analytics de efectividad de las pistas

### Sistema de Créditos
- Limitar número de pistas por sesión
- Descontar puntos por usar pistas
- Gamificación: "Resuelto sin pistas" badges

### Pistas Adaptativas
- Analizar el código del estudiante
- Sugerir pistas específicas según errores detectados
- IA para generar pistas contextuales

## Referencias

- Implementación: `frontend/src/components/Playground.tsx`
- Tipos: `frontend/src/types/api.ts`
- Script: `add_hints_to_problems.py`
- Ejemplo: `backend/problems/sec_saludo/metadata.json`

---

**Implementado**: 25 de Octubre, 2025
**Versión**: 1.0
**Mantenedor**: Python Playground Development Team
