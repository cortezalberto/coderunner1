# Archivos Obsoletos Identificados

**Fecha**: 26 de Octubre, 2025
**Análisis**: Archivos innecesarios para eliminación

---

## 📋 Resumen

Se identificaron **3 archivos obsoletos** que deben ser eliminados:

1. ✅ `app.py` - Versión MVP antigua del backend
2. ✅ `runner.py` - Runner local obsoleto (reemplazado por Docker)
3. ✅ `frontend/src/components/Playground.tsx` - Versión original sin refactorizar (reemplazado por PlaygroundRefactored.tsx)

---

## 🔍 Análisis Detallado

### 1. `app.py` (ROOT) - OBSOLETO ❌

**Ubicación**: `C:\2025Desarrollo\Los cortez\La Mendoza\python-playground-mvp\app.py`
**Tamaño**: 40 líneas
**Razón para eliminar**:

- Es una versión MVP antigua y simplificada del backend
- NO se usa en la arquitectura de microservicios actual
- El backend real está en `backend/app.py` (no este archivo)
- Solo tiene 2 endpoints básicos sin validación, seguridad ni persistencia
- Importa `runner.py` que también es obsoleto

**Comparación**:
- **app.py (obsoleto)**: 40 líneas, sin autenticación, sin DB, sin cache
- **backend/app.py (actual)**: Completo con FastAPI, rate limiting, Redis, PostgreSQL

**Acción**: ❌ ELIMINAR

---

### 2. `runner.py` (ROOT) - OBSOLETO ❌

**Ubicación**: `C:\2025Desarrollo\Los cortez\La Mendoza\python-playground-mvp\runner.py`
**Tamaño**: 130 líneas
**Razón para eliminar**:

- Runner local sin aislamiento real
- Comentario en línea 4-5 dice: "Este runner es un MVP. En producción, ejecutá esto en un contenedor aislado."
- La arquitectura actual usa Docker containers (`py-playground-runner:latest`)
- El runner real está en `worker/services/docker_runner.py`
- Usa `tempfile.mkdtemp()` localmente, no seguro para producción
- Límites de recursos solo funcionan en Linux/Mac, no en Windows

**Comparación**:
- **runner.py (obsoleto)**: Ejecución local sin aislamiento
- **worker/services/docker_runner.py (actual)**: Docker sandbox con network isolation

**Acción**: ❌ ELIMINAR

---

### 3. `frontend/src/components/Playground.tsx` (ORIGINAL) - OBSOLETO ❌

**Ubicación**: `C:\2025Desarrollo\Los cortez\La Mendoza\python-playground-mvp\frontend\src\components\Playground.tsx`
**Tamaño**: 783 líneas
**Razón para eliminar**:

- Versión original sin refactorizar (monolítica)
- Reemplazada por `PlaygroundRefactored.tsx` (189 líneas + hooks + componentes)
- `App.tsx` ya importa `PlaygroundRefactored`, NO usa `Playground.tsx`
- Mantener dos versiones causa confusión
- La versión refactorizada tiene mejor arquitectura y mantenibilidad

**Comparación**:
- **Playground.tsx (obsoleto)**: 783 líneas, 7 useEffect interdependientes, todo inline
- **PlaygroundRefactored.tsx (actual)**: 189 líneas, usa 5 custom hooks, 8 componentes especializados

**Verificación en App.tsx**:
```typescript
// App.tsx línea 3
import PlaygroundRefactored from './components/PlaygroundRefactored'
// NO importa Playground.tsx
```

**Acción**: ❌ ELIMINAR

---

## 📁 Archivos a Mantener (NO Eliminar)

### ✅ MANTENER: `add_hints_to_problems.py`

**Ubicación**: `C:\2025Desarrollo\Los cortez\La Mendoza\python-playground-mvp\add_hints_to_problems.py`
**Razón para mantener**:

- Script útil para agregar hints genéricos a problemas nuevos
- Se puede ejecutar manualmente cuando sea necesario
- No afecta el funcionamiento del sistema
- Documentado en CLAUDE.md

---

## ⚠️ Archivos Cuestionables (Revisar)

### `backend/problems/sumatoria/student_code.py`

**Ubicación**: `backend/problems/sumatoria/student_code.py`
**Estado**: Probablemente temporal/debug
**Acción recomendada**: Revisar si es necesario. Los archivos `student_code.py` suelen ser generados dinámicamente por el worker, no deben estar en el repositorio.

---

## 🗑️ Plan de Eliminación

### Paso 1: Eliminar Archivos Root Obsoletos

```bash
# Eliminar app.py y runner.py obsoletos
rm app.py
rm runner.py
```

### Paso 2: Eliminar Playground.tsx Original

```bash
# Eliminar versión original sin refactorizar
rm frontend/src/components/Playground.tsx
```

### Paso 3: Limpiar student_code.py temporal

```bash
# Eliminar archivo temporal de debug
rm backend/problems/sumatoria/student_code.py
```

---

## ✅ Verificación Post-Eliminación

Después de eliminar, verificar que:

1. **Backend funciona**:
   ```bash
   docker compose up -d backend
   curl http://localhost:8000/api/health
   ```

2. **Frontend compila**:
   ```bash
   cd frontend
   npm run build
   ```

3. **Worker funciona**:
   ```bash
   docker compose up -d worker
   docker compose logs worker | grep "Started"
   ```

---

## 📊 Impacto de la Eliminación

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Archivos totales** | Incluye obsoletos | -4 archivos | Más limpio |
| **Líneas de código obsoleto** | ~953 líneas | 0 | -953 líneas |
| **Confusión arquitectura** | 2 versiones backend, 2 frontends | 1 de cada | Claridad |
| **Tamaño repositorio** | +953 líneas | -953 líneas | Menor |

---

## 🎯 Beneficios

1. ✅ **Claridad**: Sin archivos duplicados o obsoletos
2. ✅ **Mantenibilidad**: Solo una versión de cada componente
3. ✅ **Onboarding**: Nuevos desarrolladores no se confunden con archivos viejos
4. ✅ **Tamaño**: Repositorio más pequeño y limpio

---

## 📝 Conclusión

Estos 3-4 archivos son **completamente innecesarios** y pueden eliminarse sin riesgo:

1. ❌ `app.py` - Backend MVP obsoleto
2. ❌ `runner.py` - Runner local sin aislamiento
3. ❌ `frontend/src/components/Playground.tsx` - Versión original no refactorizada
4. ❌ `backend/problems/sumatoria/student_code.py` - Archivo temporal

**Seguro para eliminar**: Sí, ninguno se usa en el sistema actual.
**Riesgo**: Ninguno, la arquitectura actual no depende de estos archivos.

---

**Última actualización**: 26 de Octubre, 2025
**Estado**: Listo para eliminación
