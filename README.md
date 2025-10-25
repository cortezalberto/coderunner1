# 🐍 Python Playground MVP

> Plataforma educativa de ejecución de código Python con aislamiento Docker, colas de trabajo, almacenamiento persistente e interfaz web moderna.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-8.2%2F10-brightgreen.svg)](REFACTORING_SESSION_2025-10-25.md)

---

## 🎉 Mejoras Recientes (Oct 2025)

**Performance optimizado para producción**:
- ⚡ N+1 queries eliminados - **100x más rápido**
- 🚀 Caching de problemas - **1000x más rápido** en requests subsiguientes
- 🔥 Validators optimizados - **2x más rápido**
- 📦 Docker images **30-40% más pequeñas**
- 🎯 Type hints en todos los endpoints
- 🏆 Codebase health score: **8.2/10**

Ver [REFACTORING_SESSION_2025-10-25.md](REFACTORING_SESSION_2025-10-25.md) para detalles completos.

---

## ✨ Características

### Para Estudiantes
- 🎯 **Editor Interactivo**: Monaco Editor con resaltado de sintaxis
- 📚 **Múltiples Problemas**: 31 ejercicios organizados jerárquicamente (8 materias)
- 📊 **Navegación Intuitiva**: Sistema de 3 niveles (Materia → Unidad → Problema)
- ✅ **Calificación en Tiempo Real**: Puntuación automática con tests públicos y ocultos
- 📈 **Resultados Detallados**: Visualización de tests, mensajes de error y tiempos de ejecución
- 🔒 **Ejecución Segura**: Código ejecutado en contenedores Docker aislados
- 💾 **Auto-guardado**: Código persistido en localStorage del navegador

### Para Instructores
- 📊 **Panel Administrativo**: Estadísticas y envíos de estudiantes
- 📋 **Historial Completo**: Seguimiento de todos los intentos con puntuaciones
- 🎓 **Problemas Personalizables**: Estructura simple para crear ejercicios
- 🔍 **Analíticas Detalladas**: Promedios de puntuación y tasas de completado
- 📝 **Sistema de Rúbricas**: Puntuación flexible por test

### Características Técnicas
- ⚡ **Ejecución Rápida**: ~2-3 segundos por envío
- 🏗️ **Microservicios**: Backend, Worker, Frontend, PostgreSQL, Redis
- 🧪 **86 Tests Unitarios**: Cobertura comprensiva del código
- 📚 **Type-Safe**: TypeScript en frontend, Pydantic v2 en backend
- 🔧 **Production-Ready**: Service layer, logging estructurado, validación de entrada
- 🐳 **Completamente Dockerizado**: Desarrollo y producción en containers
- 🎨 **Interfaz Moderna**: React 18 + TypeScript + Vite + Monaco Editor

---

## 🚀 Inicio Rápido

### Prerequisitos
- Docker (20.10+)
- Docker Compose (2.0+)

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/yourusername/python-playground-mvp.git
   cd python-playground-mvp
   ```

2. **Iniciar la aplicación:**

   **Windows:**
   ```bash
   start.bat
   ```

   **Linux/Mac:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

3. **Acceder a la aplicación:**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/api/health

---

## 🏗️ Arquitectura

```
Frontend (React+TypeScript+Monaco) → Backend (FastAPI) → Redis (RQ Queue) → Worker → Docker Sandbox
                                            ↓
                                      PostgreSQL
```

### Stack Tecnológico

**Frontend:**
- React 18 con TypeScript (strict mode)
- Vite 6 para build y dev server
- Monaco Editor para edición de código
- Axios para peticiones HTTP
- CSS moderno con sistema de diseño coherente

**Backend:**
- FastAPI con service layer architecture
- SQLAlchemy ORM + PostgreSQL
- Redis Queue (RQ) para jobs asíncronos
- Pydantic v2 para validación de schemas
- Logging estructurado en JSON
- Validación de seguridad multi-capa

**Worker:**
- Python RQ worker
- Docker SDK para ejecución sandboxed
- Sistema de rúbricas automático
- Manejo de timeouts y límites de recursos

**Infraestructura:**
- Docker + Docker Compose
- PostgreSQL 15
- Redis 7
- Pytest para testing
- Pre-commit hooks

---

## 📚 Contenido Educativo

### Problemas Organizados Jerárquicamente

**3 Materias × 5 Unidades × Múltiples Problemas**

```
📚 Programación 1
  ├── 📖 Estructuras Secuenciales (10 problemas)
  ├── 📖 Estructuras Condicionales (9 problemas)
  ├── 📖 Estructuras Repetitivas
  ├── 📖 Listas
  └── 📖 Funciones (1 problema)

📚 Programación 2
  ├── 📖 POO Básico
  ├── 📖 Herencia
  ├── 📖 Excepciones
  ├── 📖 Archivos
  └── 📖 Estructuras de Datos

📚 Algoritmos y Complejidad
  ├── 📖 Ordenamiento
  ├── 📖 Búsqueda
  ├── 📖 Recursión
  ├── 📖 Complejidad
  └── 📖 Programación Dinámica
```

**Total actual**: 20 problemas funcionales

---

## 📊 API Documentation

### Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/subjects` | GET | Listar todas las materias |
| `/api/subjects/{id}/units` | GET | Obtener unidades de una materia |
| `/api/subjects/{id}/units/{id}/problems` | GET | Obtener problemas de una unidad |
| `/api/problems` | GET | Listar todos los problemas |
| `/api/problems/hierarchy` | GET | Jerarquía completa con conteos |
| `/api/submit` | POST | Enviar código para evaluación |
| `/api/result/{job_id}` | GET | Obtener resultado de ejecución |
| `/api/admin/summary` | GET | Estadísticas administrativas |
| `/api/admin/submissions` | GET | Historial de envíos |
| `/api/health` | GET | Estado del sistema |

### Ejemplo de Uso

**Enviar código:**
```bash
curl -X POST http://localhost:8000/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "problem_id": "sumatoria",
    "code": "def suma(a, b):\n    return a + b",
    "student_id": "estudiante123"
  }'
```

**Respuesta:**
```json
{
  "job_id": "63126950-729a-4902-8b00-a11d103c7aaa",
  "status": "queued",
  "message": "Submission enqueued successfully"
}
```

**Obtener resultado:**
```bash
curl http://localhost:8000/api/result/63126950-729a-4902-8b00-a11d103c7aaa
```

**Documentación completa**: http://localhost:8000/docs

---

## 🧪 Testing

```bash
# Tests del backend
docker compose exec backend pytest backend/tests/ -v

# Tests del worker
docker compose exec worker pytest worker/tests/ -v

# Con cobertura
docker compose exec backend pytest backend/tests/ --cov=backend --cov-report=html

# Test específico
docker compose exec backend pytest backend/tests/test_problem_service.py::TestProblemService::test_list_all_problems -v

# Type checking del frontend
cd frontend && npx tsc --noEmit
```

**Estadísticas de Testing:**
- 86 tests unitarios creados
- Cobertura de servicios críticos
- Tests de integración end-to-end

Ver [TESTING.md](TESTING.md) para documentación detallada.

---

## 🔒 Seguridad

### Capas de Seguridad Implementadas

**1. Validación de Entrada** (`backend/validators.py`):
- Bloqueo de imports peligrosos: `os`, `subprocess`, `sys`, `eval()`, `exec()`, `compile()`
- Límite de tamaño de código (50KB por defecto)
- Validación de formato de `problem_id`
- Verificación de existencia de problemas

**2. Aislamiento Docker**:
```bash
docker run --rm \
  --network none              # Sin acceso a red
  --read-only                 # Sistema de archivos solo lectura
  --tmpfs /tmp:rw,noexec,nosuid,size=64m
  --tmpfs /workspace:rw,noexec,nosuid,size=128m
  --cpus=1.0                  # Límite de CPU
  --memory=256m               # Límite de memoria
  --memory-swap=256m          # Sin swap
  py-playground-runner:latest
```

**3. Control de Recursos**:
- Timeout por ejecución (3-5 segundos configurables)
- Límites de CPU y memoria
- Usuario no-root (uid 1000)
- Limpieza automática de workspaces

**4. Prevención de SQL Injection**:
- SQLAlchemy ORM con prepared statements
- Validación de todos los inputs con Pydantic

---

## 📁 Estructura del Proyecto

```
python-playground-mvp/
├── backend/                    # API FastAPI
│   ├── services/              # Lógica de negocio
│   │   ├── problem_service.py
│   │   ├── submission_service.py
│   │   └── subject_service.py
│   ├── tests/                 # Tests unitarios
│   ├── problems/              # 20 ejercicios
│   ├── app.py                 # Endpoints HTTP
│   ├── models.py              # Modelos SQLAlchemy
│   ├── config.py              # Configuración
│   ├── validators.py          # Validación de entrada
│   ├── exceptions.py          # Excepciones custom
│   ├── logging_config.py      # Logging estructurado
│   └── subjects_config.json   # Jerarquía de contenido
│
├── worker/                    # RQ Worker
│   ├── services/             # Servicios del worker
│   │   ├── docker_runner.py  # Ejecución en Docker
│   │   └── rubric_scorer.py  # Sistema de calificación
│   ├── tests/                # Tests del worker
│   └── tasks.py              # Definición de jobs
│
├── frontend/                  # React + TypeScript
│   ├── src/
│   │   ├── types/            # Tipos TypeScript
│   │   │   └── api.ts        # Interfaces de API
│   │   ├── components/       # Componentes React
│   │   │   ├── Playground.tsx
│   │   │   └── AdminPanel.tsx
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── package.json
│
├── runner/                    # Docker sandbox image
│   ├── Dockerfile            # Python 3.11 + pytest
│   └── README.md
│
├── docker-compose.yml        # Orquestación de servicios
├── start.bat / start.sh      # Scripts de inicio
├── CLAUDE.md                 # Guía para Claude Code
├── TESTING.md                # Documentación de testing
├── REFACTORIZACION_TYPESCRIPT.md  # Migración a TypeScript
└── README.md                 # Este archivo
```

---

## 🛠️ Desarrollo

### Comandos Comunes

```bash
# Iniciar todos los servicios
docker compose up -d

# Ver estado
docker compose ps

# Ver logs
docker compose logs -f backend
docker compose logs -f worker
docker compose logs -f frontend

# Reiniciar un servicio
docker compose restart backend

# Reconstruir tras cambios
docker compose up -d --build backend

# Detener todo
docker compose down

# Reset completo (incluye base de datos)
docker compose down -v && docker compose up --build
```

### Desarrollo Local (sin Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://playground:playground@localhost:5432/playground
uvicorn backend.app:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev

# Type checking
npx tsc --noEmit
```

**Worker:**
```bash
cd worker
pip install -r requirements.txt
export DATABASE_URL=postgresql://playground:playground@localhost:5432/playground
rq worker --url redis://localhost:6379 submissions
```

---

## 🎯 Agregar Nuevos Problemas

1. **Seleccionar materia/unidad** de `backend/subjects_config.json`

2. **Crear directorio:**
   ```bash
   mkdir backend/problems/mi_problema
   ```

3. **Crear 6 archivos requeridos:**
   - `prompt.md` - Enunciado del problema
   - `starter.py` - Código inicial
   - `tests_public.py` - Tests visibles para estudiantes
   - `tests_hidden.py` - Tests ocultos para evaluación
   - `metadata.json` - Configuración (materia, unidad, dificultad, tags)
   - `rubric.json` - Puntos por test

4. **Probar:**
   ```bash
   curl -X POST http://localhost:8000/api/submit \
     -H "Content-Type: application/json" \
     -d '{"problem_id": "mi_problema", "code": "...", "student_id": "test"}'
   ```

Ver ejemplo completo en: `backend/problems/sumatoria/`

---

## 📖 Documentación

- **[CLAUDE.md](CLAUDE.md)** - Guía completa del proyecto para Claude Code
- **[TESTING.md](TESTING.md)** - Guía de testing
- **[REFACTORIZACION_TYPESCRIPT.md](REFACTORIZACION_TYPESCRIPT.md)** - Migración a TypeScript
- **[HISTORIAS_USUARIO.md](HISTORIAS_USUARIO.md)** - Historias de usuario y casos de uso

---

## 🐛 Troubleshooting

**Servicios no inician:**
```bash
# Verificar Docker está corriendo
docker ps

# Ver logs de errores
docker compose logs
```

**Puerto ocupado:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

**Worker no procesa jobs:**
```bash
# Verificar Redis
docker compose exec redis redis-cli ping

# Ver logs del worker
docker compose logs worker -f
```

**Tests fallan:**
```bash
# Reconstruir runner image
docker build -t py-playground-runner:latest ./runner

# Verificar permisos (Linux/Mac)
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crear branch de feature (`git checkout -b feature/mi-feature`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push al branch (`git push origin feature/mi-feature`)
5. Crear Pull Request

**Hooks de pre-commit:**
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

---

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE)

---

## 👥 Autores

Proyecto creado como MVP educativo para enseñanza de programación Python.

---

## 🙏 Agradecimientos

- FastAPI por el excelente framework web
- Monaco Editor por el editor de código
- Docker por el sistema de aislamiento
- La comunidad de Python y React

---

**Hecho con ❤️ para la educación** 🚀

**Última actualización**: 25 de Octubre, 2025
