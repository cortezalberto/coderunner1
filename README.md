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

## 🎉 Mejoras Recientes (Oct 26, 2025)

**Performance optimizado para producción (300 usuarios concurrentes)**:
- ⚡ N+1 queries eliminados - **100x más rápido**
- 🚀 Redis caching (DB 1) - **99% reducción en lecturas de filesystem**
- 🎯 Problem list caching - **1000x más rápido** en requests subsiguientes
- 🔥 Validators con regex compilados - **2x más rápido**
- 📦 Docker images **30-40% más pequeñas** (.dockerignore)
- 🏆 Codebase health score: **8.2/10** (mejorado desde 7.5)

**Arquitectura refactorizada**:
- 🏗️ Frontend: Playground reducido de 783 → 189 líneas (-76% complejidad)
- 🪝 5 custom hooks extraídos (useHierarchyData, useProblems, useCodePersistence, useSubmission, useHints)
- 🧩 8 componentes especializados (20-110 líneas cada uno)
- 🛡️ ErrorBoundary para prevención de crashes
- 🗄️ Repository Pattern implementado en backend
- 🎯 Type hints en todos los 9 endpoints

**Producción lista**:
- 🚀 Uvicorn: 4 workers, 1000 concurrencia/worker
- 🐘 PostgreSQL: max_connections=200, tuning para SSD
- 🔴 Redis: Dual-DB (DB 0: queue, DB 1: cache)
- 🕐 Rate limiting: 5-60 req/min por endpoint
- 🧹 Workspace cleaner: Automated cada 30 minutos

Ver [REFACTORIZACIONES_APLICADAS.md](REFACTORIZACIONES_APLICADAS.md) y [CLAUDE_IMPROVEMENTS.md](CLAUDE_IMPROVEMENTS.md) para detalles completos.

---

## ✨ Características

### Para Estudiantes
- 🎯 **Editor Interactivo**: Monaco Editor con resaltado de sintaxis y autocompletado
- 📚 **31 Problemas**: Organizados jerárquicamente en 8 materias con 5 unidades cada una
- 📊 **Navegación Intuitiva**: Sistema de 3 niveles (Materia → Unidad → Problema)
- 💡 **Sistema de Hints Progresivo**: 4 niveles de ayuda (124 hints totales, 100% cobertura)
- ✅ **Calificación Automática**: Puntuación instantánea con tests públicos y ocultos
- 📈 **Resultados Detallados**: Visualización de tests, mensajes de error y tiempos de ejecución
- 🔒 **Ejecución Segura**: Código ejecutado en contenedores Docker aislados (no network, read-only)
- 💾 **Auto-guardado**: Código persistido en localStorage del navegador
- 🚫 **Anti-Cheating**: Sistema anti-paste y monitoreo de tabs para integridad académica
- 🎨 **Logos Dinámicos**: Logos de tecnologías que cambian según la materia seleccionada

### Para Instructores
- 📊 **Panel Administrativo**: Estadísticas y envíos de estudiantes
- 📋 **Historial Completo**: Seguimiento de todos los intentos con puntuaciones
- 🎓 **Problemas Personalizables**: Estructura simple para crear ejercicios
- 🔍 **Analíticas Detalladas**: Promedios de puntuación y tasas de completado
- 📝 **Sistema de Rúbricas**: Puntuación flexible por test
- 🛡️ **Integridad Académica**: Protección anti-paste para evaluaciones justas

### Características Técnicas
- ⚡ **Ejecución Rápida**: ~2-3 segundos por envío
- 🏗️ **Microservicios**: Backend (FastAPI), Worker (RQ), Frontend (React+TS), PostgreSQL, Redis (dual-DB)
- 🧪 **86 Tests Unitarios**: Cobertura del 85% en funcionalidad crítica
- 📚 **Type-Safe**: TypeScript strict mode en frontend, Pydantic v2 + type hints en backend
- 🔧 **Production-Ready**: Service layer, Repository pattern, logging estructurado JSON, validación multi-capa
- 🐳 **Completamente Dockerizado**: Desarrollo y producción en containers con health checks
- 🎨 **Interfaz Moderna**: React 18 + TypeScript + Vite 6 + Monaco Editor
- 🚀 **Escalable**: Configurado para 300 usuarios concurrentes (4 workers Uvicorn, 4 workers RQ)
- 🔴 **Redis Caching**: 99% reducción en lecturas de filesystem
- 📊 **Rate Limiting**: Protección contra abuso (5-60 req/min por endpoint)
- 🧹 **Auto-limpieza**: Workspace cleaner automatizado cada 30 minutos

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
Frontend (React+TypeScript+Monaco) → Backend (FastAPI) → Redis DB 0 (RQ Queue) → Worker → Docker Sandbox
                                            ↓                    ↓
                                      PostgreSQL          Redis DB 1 (Cache)

                                                          Cleaner (cada 30min)
                                                               ↓
                                                          Workspaces
```

### Stack Tecnológico

**Frontend:**
- React 18 con TypeScript (strict mode)
- Vite 6 para build y dev server
- Monaco Editor para edición de código
- Axios para peticiones HTTP
- CSS moderno con sistema de diseño coherente

**Backend:**
- FastAPI con service layer + repository pattern
- SQLAlchemy ORM + PostgreSQL 15 (200 max connections)
- Redis Queue (RQ) para jobs asíncronos (DB 0)
- Redis Cache para problemas y stats (DB 1, 99% reducción filesystem)
- Pydantic v2 para validación de schemas
- Logging estructurado en JSON con contexto
- Validación de seguridad multi-capa (validators, Docker sandbox)
- Rate limiting con slowapi (5-60 req/min por endpoint)
- Type hints en todos los endpoints y servicios

**Worker:**
- Python RQ worker (4 workers concurrentes)
- Docker SDK para ejecución sandboxed (--network none, --read-only)
- Sistema de rúbricas automático con scoring personalizado
- Manejo de timeouts (3-5s) y límites de recursos (256MB RAM, 1 CPU)
- Path translation para Docker-in-Docker
- Workspace cleaner service (cada 30min, limpia >1h)
- RQ Scheduler para tareas periódicas

**Infraestructura:**
- Docker + Docker Compose (6 servicios orquestados)
- PostgreSQL 15 (tuning para 300 usuarios: shared_buffers=512MB, max_connections=200)
- Redis 7 (dual-DB: 0=queue con 50 conn, 1=cache con 30 conn)
- Pytest para testing (86 tests, 85% coverage)
- Pre-commit hooks (black, isort, flake8, mypy)
- Health checks en todos los servicios
- Uvicorn multi-worker (4 workers, 1000 concurrencia/worker)

---

## 📚 Contenido Educativo

### Problemas Organizados Jerárquicamente

**8 Materias × 5 Unidades × Múltiples Problemas**

```
📚 Programación 1 (Python)
  ├── 📖 Estructuras Secuenciales (10 problemas)
  ├── 📖 Estructuras Condicionales (9 problemas)
  ├── 📖 Estructuras Repetitivas
  ├── 📖 Listas
  └── 📖 Funciones (1 problema)

📚 Programación 2 (Java)
  ├── 📖 POO Básico
  ├── 📖 Herencia y Polimorfismo
  ├── 📖 Manejo de Excepciones
  ├── 📖 Manejo de Archivos
  └── 📖 Estructuras de Datos

📚 Programación 3 (Spring Boot)
  ├── 📖 Fundamentos de Spring (1 problema)
  ├── 📖 Spring Boot Básico
  ├── 📖 Spring Web
  ├── 📖 Spring Data JPA
  └── 📖 Spring Security

📚 Programación 4 (FastAPI)
  ├── 📖 Fundamentos de FastAPI (1 problema)
  ├── 📖 Validación y Modelos
  ├── 📖 FastAPI con Bases de Datos
  ├── 📖 Seguridad en FastAPI
  └── 📖 FastAPI Avanzado

📚 Paradigmas de Programación (Java, Prolog, Haskell)
  ├── 📖 Paradigma Imperativo
  ├── 📖 Paradigma Orientado a Objetos (1 problema)
  ├── 📖 Paradigma Lógico (1 problema)
  ├── 📖 Paradigma Funcional (1 problema)
  └── 📖 Comparación de Paradigmas

📚 Algoritmos y Estructuras de Datos (PSeInt)
  ├── 📖 Estructuras de Datos Básicas
  ├── 📖 Algoritmos de Ordenamiento
  ├── 📖 Algoritmos de Búsqueda
  ├── 📖 Pilas y Colas
  └── 📖 Recursión

📚 Desarrollo Front End (HTML, CSS, JavaScript, TypeScript)
  ├── 📖 Fundamentos de HTML (1 problema)
  ├── 📖 CSS y Diseño (1 problema)
  ├── 📖 JavaScript Básico (1 problema)
  ├── 📖 JavaScript Avanzado
  └── 📖 TypeScript (1 problema)

📚 Desarrollo Backend (Python, FastAPI)
  ├── 📖 Fundamentos de Python (1 problema)
  ├── 📖 FastAPI Básico (1 problema)
  ├── 📖 Bases de Datos
  ├── 📖 Autenticación y Seguridad
  └── 📖 Deployment y Testing
```

**Total actual**: **31 problemas funcionales** con sistema de hints progresivo (4 niveles)

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
│   ├── services/              # Lógica de negocio (service layer)
│   │   ├── problem_service.py
│   │   ├── submission_service.py
│   │   └── subject_service.py
│   ├── repositories/          # Data access layer (NEW)
│   │   ├── submission_repository.py
│   │   └── test_result_repository.py
│   ├── sagas/                 # Distributed transactions (prepared)
│   ├── tests/                 # Tests unitarios (86 tests)
│   ├── problems/              # 31 ejercicios (8 materias)
│   ├── app.py                 # Endpoints HTTP (9 endpoints)
│   ├── models.py              # Modelos SQLAlchemy
│   ├── config.py              # Configuración centralizada
│   ├── validators.py          # Validación de entrada
│   ├── exceptions.py          # Excepciones custom
│   ├── logging_config.py      # Logging estructurado JSON
│   ├── cache.py               # Redis caching layer (NEW)
│   ├── database.py            # Database session management
│   └── subjects_config.json   # Jerarquía de contenido
│
├── worker/                    # RQ Worker
│   ├── services/             # Servicios del worker
│   │   ├── docker_runner.py  # Ejecución en Docker
│   │   ├── rubric_scorer.py  # Sistema de calificación
│   │   └── workspace_cleaner.py  # Limpieza automática (NEW)
│   ├── tests/                # Tests del worker
│   ├── tasks.py              # Definición de jobs
│   └── scheduler.py          # RQ Scheduler (NEW)
│
├── frontend/                  # React + TypeScript
│   ├── src/
│   │   ├── hooks/            # Custom hooks (NEW)
│   │   │   ├── useHierarchyData.ts
│   │   │   ├── useProblems.ts
│   │   │   ├── useCodePersistence.ts
│   │   │   ├── useSubmission.ts
│   │   │   ├── useHints.ts
│   │   │   └── index.ts
│   │   ├── types/            # Tipos TypeScript
│   │   │   └── api.ts        # Interfaces de API
│   │   ├── components/       # Componentes React
│   │   │   ├── playground/   # Playground components (NEW)
│   │   │   │   ├── AntiCheatingBanner.tsx
│   │   │   │   ├── ProblemSelector.tsx
│   │   │   │   ├── ProblemPrompt.tsx
│   │   │   │   ├── HintButton.tsx
│   │   │   │   ├── CodeEditor.tsx
│   │   │   │   ├── EditorActions.tsx
│   │   │   │   ├── ResultsPanel.tsx
│   │   │   │   └── TestResultsList.tsx
│   │   │   ├── PlaygroundRefactored.tsx  # Main (189 líneas)
│   │   │   ├── AdminPanel.tsx
│   │   │   ├── ErrorBoundary.tsx  # Crash prevention (NEW)
│   │   │   └── LanguageLogo.tsx   # Dynamic logos
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── package.json
│
├── runner/                    # Docker sandbox image
│   ├── Dockerfile            # Python 3.11 + pytest, non-root
│   └── README.md
│
├── workspaces/                # Sandboxes temporales (auto-cleanup)
├── docker-compose.yml        # Orquestación de 6 servicios
├── .dockerignore             # Optimización de imágenes (NEW)
├── start.bat / start.sh      # Scripts de inicio
├── CLAUDE.md                 # Guía completa del proyecto
├── TESTING.md                # Documentación de testing
├── HINT_SYSTEM.md            # Sistema de hints (NEW)
├── ANTI_PASTE_FEATURE.md     # Anti-cheating docs (NEW)
├── REFACTORIZACIONES_APLICADAS.md  # Refactoring Oct 26
├── CLAUDE_IMPROVEMENTS.md    # Production optimizations
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

### Documentación Principal
- **[CLAUDE.md](CLAUDE.md)** - Guía completa del proyecto (arquitectura, comandos, patrones)
- **[README.md](README.md)** - Este archivo (overview general)
- **[runner/README.md](runner/README.md)** - Docker runner image y seguridad

### Testing y Calidad
- **[TESTING.md](TESTING.md)** - Guía de testing (86 tests, 85% coverage)
- **[MEJORES_PRACTICAS_RECOMENDACIONES.md](MEJORES_PRACTICAS_RECOMENDACIONES.md)** - Best practices

### Características del Sistema
- **[HINT_SYSTEM.md](HINT_SYSTEM.md)** - Sistema de hints progresivo (4 niveles)
- **[ANTI_PASTE_FEATURE.md](ANTI_PASTE_FEATURE.md)** - Anti-cheating system

### Refactorizaciones
- **[REFACTORIZACIONES_APLICADAS.md](REFACTORIZACIONES_APLICADAS.md)** - Refactoring Oct 26, 2025
- **[CLAUDE_IMPROVEMENTS.md](CLAUDE_IMPROVEMENTS.md)** - Production optimizations
- **[REFACTORIZACION_TYPESCRIPT.md](REFACTORIZACION_TYPESCRIPT.md)** - Migración a TypeScript
- **[REFACTORING_SESSION_2025-10-25.md](REFACTORING_SESSION_2025-10-25.md)** - Initial refactoring

### User Stories
- **[HISTORIAS_USUARIO.md](HISTORIAS_USUARIO.md)** - 21 historias de usuario y casos de uso

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

## 📊 Estado del Proyecto

| Categoría | Estado | Métrica |
|-----------|--------|---------|
| **Problemas** | ✅ Producción | 31 problemas, 8 materias |
| **Tests** | ✅ 85% Coverage | 86 tests unitarios |
| **Frontend** | ✅ TypeScript | React 18 + Vite 6 |
| **Backend** | ✅ Production-ready | FastAPI + Service Layer |
| **Performance** | ✅ Optimizado | 100-1000x mejoras |
| **Security** | ✅ Multi-layer | Docker + Validators |
| **Scaling** | ✅ Configurado | 300 usuarios concurrentes |
| **Code Quality** | ✅ 8.2/10 | Mejorado desde 7.5 |
| **Docs** | ✅ Completa | 10+ archivos MD |

---

**Última actualización**: 26 de Octubre, 2025
