# 📖 Historias de Usuario - Python Playground MVP

**Fecha**: 25 de Octubre, 2025
**Proyecto**: Python Playground MVP
**Versión**: 1.0.0

---

## 📋 Índice

1. [Estudiantes](#-historias-de-estudiantes)
2. [Instructores/Docentes](#-historias-de-instructoresdocentes)
3. [Administradores del Sistema](#-historias-de-administradores-del-sistema)
4. [Casos de Uso Detallados](#-casos-de-uso-detallados)
5. [Flujos de Trabajo](#-flujos-de-trabajo)
6. [Criterios de Aceptación](#-criterios-de-aceptación)

---

## 👨‍🎓 Historias de Estudiantes

### HU-001: Explorar Ejercicios Disponibles

**Como** estudiante de programación
**Quiero** navegar por los ejercicios organizados por materia y unidad
**Para** encontrar problemas relevantes a lo que estoy aprendiendo

**Criterios de Aceptación:**
- ✅ Ver listado de 3 materias: Programación 1, Programación 2, Algoritmos
- ✅ Seleccionar una materia y ver sus 5 unidades temáticas
- ✅ Seleccionar una unidad y ver todos los problemas disponibles
- ✅ Ver título, dificultad y tags de cada problema
- ✅ Sistema de cascading dropdowns (selección jerárquica)

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-002: Resolver un Ejercicio

**Como** estudiante
**Quiero** escribir código Python en un editor profesional
**Para** resolver los ejercicios asignados cómodamente

**Criterios de Aceptación:**
- ✅ Ver enunciado del problema en formato legible
- ✅ Editor Monaco con syntax highlighting de Python
- ✅ Código inicial (starter code) precargado
- ✅ Autocompletado y numeración de líneas
- ✅ Poder escribir y editar código libremente
- ✅ No perder el código al cambiar de pestaña (localStorage)

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-003: Ejecutar Tests

**Como** estudiante
**Quiero** ejecutar mi código contra tests automáticos
**Para** saber si mi solución es correcta

**Criterios de Aceptación:**
- ✅ Botón "Ejecutar tests" claramente visible
- ✅ Indicador de "Ejecutando..." mientras procesa
- ✅ Resultados en menos de 5 segundos
- ✅ Ver cuántos tests pasaron/fallaron
- ✅ Ver puntaje obtenido vs puntaje máximo
- ✅ Poder re-ejecutar múltiples veces

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-004: Ver Resultados Detallados

**Como** estudiante
**Quiero** ver qué tests pasaron y cuáles fallaron
**Para** entender qué debo corregir en mi código

**Criterios de Aceptación:**
- ✅ Lista de tests con indicadores ✅/❌/⚠️
- ✅ Nombre descriptivo de cada test
- ✅ Mensaje de error cuando un test falla
- ✅ Puntos obtenidos por cada test
- ✅ Ver salida estándar (stdout) si hay prints
- ✅ Ver errores de ejecución (stderr) si los hay
- ✅ Distinción entre tests públicos y ocultos

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-005: Reiniciar Código

**Como** estudiante
**Quiero** volver al código inicial del ejercicio
**Para** empezar de nuevo si me equivoco mucho

**Criterios de Aceptación:**
- ✅ Botón "Reiniciar código" visible
- ✅ Confirmación antes de borrar mi código
- ✅ Código vuelve al estado inicial (starter.py)
- ✅ Se borra el código guardado en localStorage

**Prioridad:** Media
**Estimación:** Completado ✅

---

### HU-006: Persistencia de Código

**Como** estudiante
**Quiero** que mi código se guarde automáticamente
**Para** no perder mi trabajo si cierro el navegador

**Criterios de Aceptación:**
- ✅ Código se guarda automáticamente en cada cambio
- ✅ Al recargar la página, recupero mi código
- ✅ Guardado independiente por cada problema
- ✅ Sin límite de tiempo de persistencia

**Prioridad:** Media
**Estimación:** Completado ✅

---

## 👨‍🏫 Historias de Instructores/Docentes

### HU-101: Ver Estadísticas Globales

**Como** instructor
**Quiero** ver estadísticas generales de envíos
**Para** entender cómo están progresando mis estudiantes

**Criterios de Aceptación:**
- ✅ Total de envíos realizados
- ✅ Cantidad de envíos completados vs fallados
- ✅ Envíos pendientes/en cola
- ✅ Puntaje promedio global
- ✅ Actualización en tiempo real con botón "Refrescar"

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-102: Analizar Rendimiento por Problema

**Como** instructor
**Quiero** ver estadísticas específicas de cada problema
**Para** identificar qué ejercicios son más difíciles

**Criterios de Aceptación:**
- ✅ Lista de problemas con cantidad de envíos
- ✅ Puntaje promedio por problema
- ✅ Identificar problemas con bajo puntaje promedio
- ✅ Ordenamiento por diferentes métricas

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-103: Revisar Envíos Recientes

**Como** instructor
**Quiero** ver los últimos envíos de estudiantes
**Para** monitorear la actividad y detectar problemas

**Criterios de Aceptación:**
- ✅ Lista de últimos 20 envíos
- ✅ Ver ID de estudiante, problema, fecha/hora
- ✅ Ver estado: completado, fallado, en cola
- ✅ Ver puntaje obtenido
- ✅ Ver cantidad de tests (pasados/fallados/errores)
- ✅ Ver duración de ejecución

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-104: Crear Nuevos Ejercicios

**Como** instructor
**Quiero** agregar nuevos problemas al sistema
**Para** expandir el contenido disponible

**Criterios de Aceptación:**
- ✅ Estructura simple de 6 archivos
- ✅ Documentación clara del formato
- ✅ Sistema de rúbricas configurable
- ✅ Tests públicos y ocultos separados
- ✅ Configuración de timeout y recursos
- ✅ Validación automática al cargar

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-105: Configurar Jerarquía de Contenido

**Como** instructor
**Quiero** organizar problemas en materias y unidades
**Para** facilitar la navegación de estudiantes

**Criterios de Aceptación:**
- ✅ Archivo JSON de configuración (`subjects_config.json`)
- ✅ Definir materias con nombre y descripción
- ✅ Definir unidades dentro de cada materia
- ✅ Orden personalizable de unidades
- ✅ Cambios sin necesidad de modificar código

**Prioridad:** Media
**Estimación:** Completado ✅

---

## 👨‍💼 Historias de Administradores del Sistema

### HU-201: Monitorear Salud del Sistema

**Como** administrador
**Quiero** verificar el estado de todos los servicios
**Para** asegurar que el sistema funciona correctamente

**Criterios de Aceptación:**
- ✅ Endpoint `/api/health` con status de:
  - Base de datos (PostgreSQL)
  - Cache (Redis)
  - Cola de trabajos
  - Catálogo de problemas
- ✅ Timestamp de cada verificación
- ✅ Cantidad de trabajos en cola
- ✅ Cantidad de problemas cargados

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-202: Revisar Logs del Sistema

**Como** administrador
**Quiero** acceder a logs estructurados del sistema
**Para** diagnosticar problemas y auditar actividad

**Criterios de Aceptación:**
- ✅ Logs en formato JSON estructurado
- ✅ Niveles: INFO, WARNING, ERROR
- ✅ Timestamp, módulo, función, línea
- ✅ Contexto adicional (job_id, submission_id, etc.)
- ✅ Logs accesibles vía Docker: `docker compose logs`

**Prioridad:** Alta
**Estimación:** Completado ✅

---

### HU-203: Escalar el Sistema

**Como** administrador
**Quiero** poder escalar workers horizontalmente
**Para** manejar mayor carga de trabajo

**Criterios de Aceptación:**
- ✅ Arquitectura con cola Redis (desacoplada)
- ✅ Workers stateless (sin estado compartido)
- ✅ Posibilidad de levantar múltiples workers
- ✅ Balanceo automático de carga
- 📋 Documentación de escalamiento

**Prioridad:** Media
**Estimación:** Parcialmente completado (arquitectura lista, documentación pendiente)

---

### HU-204: Configurar Límites de Recursos

**Como** administrador
**Quiero** configurar límites de CPU, memoria y tiempo
**Para** prevenir abuso del sistema

**Criterios de Aceptación:**
- ✅ Límites globales configurables (worker/tasks.py)
- ✅ Límites por problema (metadata.json)
- ✅ Timeout de ejecución
- ✅ Límite de memoria (256MB default)
- ✅ Límite de CPU (1 core)
- ✅ Network deshabilitado

**Prioridad:** Alta
**Estimación:** Completado ✅

---

## 🔄 Casos de Uso Detallados

### CU-001: Estudiante Resuelve un Problema

**Actor Principal:** Estudiante

**Precondiciones:**
- Sistema desplegado y funcionando
- Al menos un problema disponible

**Flujo Principal:**
1. Estudiante accede a http://localhost:5173
2. Selecciona materia "Programación 1" del dropdown
3. Selecciona unidad "Estructuras Secuenciales"
4. Selecciona problema "Suma de dos números"
5. Lee el enunciado en el panel izquierdo
6. Escribe su solución en el editor Monaco:
   ```python
   def suma(a, b):
       return a + b
   ```
7. Hace clic en "▶️ Ejecutar tests"
8. Sistema muestra indicador "⏳ Ejecutando tests..."
9. Después de ~2 segundos, aparecen los resultados:
   - ✅ 4/4 tests pasados
   - Puntaje: 10/10 puntos
   - Duración: 2.1s
10. Ve lista detallada de tests con ✅ verdes

**Flujo Alternativo A: Tests Fallan**
- En paso 9, algunos tests fallan
- Sistema muestra ❌ rojos con mensajes de error
- Estudiante corrige código y vuelve a paso 7

**Flujo Alternativo B: Error de Sintaxis**
- En paso 9, código tiene error de sintaxis
- Sistema muestra ⚠️ con mensaje de error de Python
- Estudiante corrige y vuelve a paso 7

**Postcondiciones:**
- Código guardado en localStorage
- Envío registrado en base de datos
- Estadísticas actualizadas en panel admin

---

### CU-002: Instructor Crea Nuevo Problema

**Actor Principal:** Instructor

**Precondiciones:**
- Acceso al filesystem del servidor
- Conocimiento de estructura de problemas

**Flujo Principal:**
1. Instructor decide crear problema "Área de triángulo"
2. Crea directorio: `backend/problems/area_triangulo/`
3. Crea `prompt.md` con enunciado
4. Crea `starter.py` con código inicial:
   ```python
   def area_triangulo(base, altura):
       # TODO: Implementar
       pass
   ```
5. Crea `tests_public.py` con tests visibles
6. Crea `tests_hidden.py` con tests de evaluación
7. Crea `metadata.json`:
   ```json
   {
     "title": "Área de un triángulo",
     "subject_id": "programacion-1",
     "unit_id": "estructuras-secuenciales",
     "difficulty": "easy",
     "tags": ["geometria", "formula"],
     "timeout_sec": 3.0,
     "memory_mb": 128
   }
   ```
8. Crea `rubric.json`:
   ```json
   {
     "tests": [
       {"name": "test_triangulo_simple", "points": 3, "visibility": "public"},
       {"name": "test_triangulo_decimal", "points": 2, "visibility": "public"},
       {"name": "test_triangulo_grande", "points": 3, "visibility": "hidden"},
       {"name": "test_triangulo_cero", "points": 2, "visibility": "hidden"}
     ],
     "max_points": 10
   }
   ```
9. Prueba con curl:
   ```bash
   curl -X POST http://localhost:8000/api/submit \
     -H "Content-Type: application/json" \
     -d '{"problem_id": "area_triangulo", "code": "def area_triangulo(b,h):\n return b*h/2", "student_id": "test"}'
   ```
10. Verifica que aparezca en interfaz web

**Postcondiciones:**
- Nuevo problema disponible en el sistema
- Visible en dropdown de problemas
- Tests funcionando correctamente

---

### CU-003: Sistema Ejecuta Código en Sandbox

**Actor Principal:** Sistema (Worker)

**Precondiciones:**
- Submission en cola Redis
- Docker daemon disponible
- Imagen `py-playground-runner:latest` construida

**Flujo Principal:**
1. Worker detecta job en cola
2. Worker obtiene submission_id y problem_id
3. Carga código del estudiante
4. Carga tests_public.py y tests_hidden.py
5. Crea workspace temporal: `/workspaces/sandbox-{uuid}/`
6. Escribe archivos:
   - `student_code.py` (código del estudiante)
   - `tests_public.py`
   - `tests_hidden.py`
   - `conftest.py` (configuración pytest)
7. Traduce path para host: `$PWD/workspaces/sandbox-{uuid}`
8. Ejecuta Docker:
   ```bash
   docker run --rm \
     --network none \
     --read-only \
     --tmpfs /tmp:rw,noexec,nosuid,size=64m \
     --tmpfs /workspace:rw,noexec,nosuid,size=128m \
     --cpus=1.0 \
     --memory=256m \
     --memory-swap=256m \
     -v {host_path}:/workspace:rw \
     --user 1000:1000 \
     py-playground-runner:latest \
     timeout 5s pytest -q --tb=short --json-report .
   ```
9. Espera a que termine (con timeout)
10. Lee `report.json` del workspace
11. Parsea resultados de tests
12. Carga rubric.json del problema
13. Aplica puntuación según rúbrica
14. Guarda TestResult en base de datos
15. Actualiza Submission con score y status
16. Limpia workspace temporal
17. Marca job como completado

**Flujo Alternativo A: Timeout**
- En paso 9, ejecución excede timeout
- Docker container es matado
- Submission marcada como "timeout"

**Flujo Alternativo B: Error de Ejecución**
- En paso 9, Python lanza excepción
- pytest captura error
- Se guarda como test con outcome="error"

**Postcondiciones:**
- TestResult rows creados en DB
- Submission actualizado con score
- Frontend puede polling resultado

---

## 🔀 Flujos de Trabajo

### Flujo: Primera Vez Usando el Sistema

```
1. Usuario accede a http://localhost:5173
2. Ve interfaz con 3 dropdowns vacíos
3. Selecciona "Programación 1" en "Materia"
   → Dropdown "Unidad" se puebla automáticamente
4. Selecciona "Estructuras Secuenciales" en "Unidad"
   → Dropdown "Ejercicio" se puebla con 10 problemas
5. Selecciona "Saludo personalizado"
   → Panel izquierdo muestra enunciado
   → Editor carga código inicial
6. Lee enunciado
7. Escribe código
8. Click en "Ejecutar tests"
9. Ve resultados
10. Si está bien → Siguiente problema
11. Si está mal → Corrige y reintenta
```

### Flujo: Debugging de Error

```
1. Estudiante escribe código con bug
2. Ejecuta tests
3. Ve que test "test_saludo_con_acentos" falló
4. Lee mensaje: "AssertionError: Expected 'Héctor' but got 'Hctor'"
5. Revisa su código:
   def saludar(nombre):
       return f"Hola {nombre}"  # Falta el acento
6. Corrige:
   def saludar(nombre):
       return f"Hola {nombre}!"
7. Re-ejecuta
8. Tests pasan
```

### Flujo: Instructor Revisa Actividad

```
1. Instructor abre panel "Panel Docente"
2. Ve estadísticas:
   - 45 envíos totales
   - 32 completados
   - 13 fallados
   - Puntaje promedio: 7.8/10
3. Ve tabla "Por Problema":
   - "suma": 15 envíos, promedio 9.2 → Problema fácil ✅
   - "fibonacci": 8 envíos, promedio 4.1 → Problema difícil ⚠️
4. Revisa "Últimos Envíos":
   - estudiante123 | fibonacci | failed | 2/10 | hace 1 min
   - estudiante456 | suma | completed | 10/10 | hace 3 min
5. Decide revisar problema "fibonacci" para mejorarlo
```

---

## ✅ Criterios de Aceptación Globales

### Funcionalidad

- ✅ Todos los endpoints API responden correctamente
- ✅ Frontend carga sin errores en consola
- ✅ Código se ejecuta en menos de 5 segundos
- ✅ Tests públicos y ocultos funcionan
- ✅ Sistema de puntuación aplica rúbricas
- ✅ Múltiples envíos simultáneos son soportados

### Seguridad

- ✅ Código malicioso es bloqueado (imports peligrosos)
- ✅ Network deshabilitado en sandbox
- ✅ Límites de CPU/memoria aplicados
- ✅ Timeouts funcionan correctamente
- ✅ No hay SQL injection posible
- ✅ Filesystem es read-only en sandbox

### Performance

- ✅ Tiempo de respuesta < 5 segundos
- ✅ Frontend carga en < 2 segundos
- ✅ API responde en < 100ms (sin ejecución)
- ✅ Base de datos soporta 100+ envíos/hora
- ✅ Worker procesa 20+ jobs/minuto

### Usabilidad

- ✅ Interfaz intuitiva sin tutorial
- ✅ Mensajes de error claros
- ✅ Navegación fluida entre problemas
- ✅ Editor profesional con syntax highlighting
- ✅ Resultados fáciles de entender

### Mantenibilidad

- ✅ Código con service layer
- ✅ Logging estructurado
- ✅ Tests unitarios >80% cobertura
- ✅ Documentación completa (CLAUDE.md, README.md)
- ✅ TypeScript en frontend (type safety)

---

## 🎯 Roadmap de Historias Futuras

### Corto Plazo (Próximos 3 meses)

**HU-301: Autenticación de Usuarios**
- Registro e inicio de sesión
- Tracking individual de progreso
- Historial personal de envíos

**HU-302: Badges y Logros**
- Conseguir badges por completar problemas
- Leaderboard de puntuaciones
- Motivación gamificada

**HU-303: Hints/Pistas**
- Sistema de pistas progresivas
- Penalización opcional por usar pistas
- Pistas configurables por problema

### Mediano Plazo (6 meses)

**HU-304: Soporte Multi-lenguaje**
- JavaScript/Node.js
- Java
- C++
- Runners específicos por lenguaje

**HU-305: Code Review Automático**
- Análisis estático de código
- Sugerencias de buenas prácticas
- Detección de code smells

**HU-306: Explicaciones con IA**
- Explicación de errores con LLM
- Sugerencias de corrección
- Tutoriales personalizados

### Largo Plazo (12 meses)

**HU-307: Competencias en Tiempo Real**
- Salas de competencia
- Rankings en vivo
- Problemas con timer

**HU-308: Editor Colaborativo**
- Pair programming
- Code sharing
- Comentarios en línea

**HU-309: Métricas Avanzadas**
- Complejidad temporal/espacial
- Comparación con soluciones óptimas
- Gráficos de rendimiento

---

## 📊 Métricas de Éxito

### KPIs Actuales

| Métrica | Objetivo | Actual | Estado |
|---------|----------|--------|--------|
| Problemas disponibles | 20 | 20 | ✅ |
| Tiempo de ejecución | < 5s | ~2-3s | ✅ |
| Tests creados | 80+ | 86 | ✅ |
| Materias | 3 | 3 | ✅ |
| Unidades | 15 | 15 | ✅ |
| Uptime | >99% | N/A | 📊 |
| Envíos/día | N/A | N/A | 📊 |

### Objetivos de Adopción

- 🎯 10+ instructores usando el sistema
- 🎯 100+ estudiantes activos/mes
- 🎯 500+ envíos/mes
- 🎯 80%+ tasa de satisfacción
- 🎯 50+ problemas disponibles

---

**Última actualización:** 25 de Octubre, 2025
**Mantenido por:** Equipo Python Playground MVP
**Contacto:** Ver [README.md](README.md)
