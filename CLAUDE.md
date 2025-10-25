# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current Status

**System**: Production-ready ✅ (Last updated: 25 Oct 2025)
**Problem Count**: 20 problems across 3 subjects (10 Secuenciales, 9 Condicionales, 1 Funciones)
**Test Coverage**: 86 tests created, Phase 3: 85% complete (tests infrastructure complete)
**Frontend**: TypeScript migration completed ✅
**Documentation**: Comprehensive with user stories and use cases

**Recent Improvements**:
- Frontend: **Migrated to TypeScript** with full type safety, race condition fixes, localStorage persistence, AbortController cleanup
- Backend: Metadata validation, health check with dependencies, None-safety
- Architecture: Service layer (100%), Pydantic v2 schemas, structured logging
- Documentation: Created HISTORIAS_USUARIO.md with 21 user stories and detailed use cases

See [REFACTORIZACION_APLICADA.md](REFACTORIZACION_APLICADA.md), [REFACTORIZACION_TYPESCRIPT.md](REFACTORIZACION_TYPESCRIPT.md), and [HISTORIAS_USUARIO.md](HISTORIAS_USUARIO.md) for detailed changes and use cases.

## Quick Reference

**Most Common Commands:**
```bash
# Start everything (first time)
docker build -t py-playground-runner:latest ./runner && docker compose up --build

# Start everything (subsequent runs)
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f backend
docker compose logs -f worker

# Stop everything
docker compose down

# Reset database
docker compose down -v && docker compose up --build

# Verify system health
curl http://localhost:8000/api/health | python -m json.tool
```

**Access Points:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## Project Overview

**Python Playground Suite** - A production-ready code execution platform with Docker sandbox isolation, job queues, persistent storage, and a modern web interface. Students submit Python code that is executed in isolated Docker containers with strict security constraints.

## Architecture

This is a microservices architecture with the following components:

```
Frontend (React+TypeScript+Monaco) → Backend (FastAPI) → Redis (RQ Queue) → Worker → Docker Sandbox
                                            ↓
                                      PostgreSQL
```

### Core Services

1. **backend/** - FastAPI REST API with service layer architecture
   - **app.py** - Routes/endpoints
   - **services/** - Business logic (ProblemService, SubmissionService, SubjectService)
   - **models.py** - SQLAlchemy ORM (Submission, TestResult)
   - **config.py** - Centralized configuration
   - **validators.py** - Input validation and security checks
   - **exceptions.py** - Custom exception hierarchy
   - **logging_config.py** - Structured JSON logging

2. **worker/** - RQ worker with service layer architecture
   - **tasks.py** - Job orchestration
   - **services/docker_runner.py** - Docker execution with path translation
   - **services/rubric_scorer.py** - Automatic grading

3. **runner/** - Minimal Docker image for sandboxed execution
   - Python 3.11 + pytest, non-root user (uid 1000)

4. **frontend/** - React + TypeScript + Vite + Monaco Editor
   - Hierarchical problem selector (Subject → Unit → Problem)
   - Real-time result polling with AbortController
   - Full type safety with TypeScript interfaces for all API responses

5. **PostgreSQL** - Submissions and TestResults tables

6. **Redis** - Job queue (RQ)

### Execution Flow

```
1. Student submits code → Backend creates Submission (status: "pending")
2. Backend enqueues job in Redis → status: "queued"
3. Worker picks up job from queue
4. Worker creates temp workspace with student_code.py, tests_public.py, tests_hidden.py, conftest.py
5. Worker runs: docker run --network none --read-only --cpus 1 --memory 256m ...
6. Container executes pytest → generates report.json
7. Worker parses report, applies rubric scoring
8. Worker saves TestResult rows + updates Submission (status: "completed")
9. Frontend polls /api/result/{job_id} every 1s and displays results
```

### Database Models

**Submission** (backend/models.py):
- job_id, student_id, problem_id, code, status
- score_total, score_max, passed, failed, errors
- Relationship: one-to-many with TestResult

**TestResult** (backend/models.py):
- test_name, outcome, duration, message
- points, max_points, visibility (public/hidden)

## Critical Architecture Decisions

### Docker-in-Docker Path Translation

The worker spawns Docker containers using the host's Docker daemon. This creates a path mismatch:
- Worker creates files in `/workspaces/sandbox-xxx` (inside worker container)
- Docker daemon looks for paths on **host filesystem**, not worker filesystem

**Solution**:
1. `./workspaces` bind-mounted to both host and worker (see docker-compose.yml)
2. Worker translates paths: `/workspaces/sandbox-xxx` → `${PWD}/workspaces/sandbox-xxx`
3. Files get chmod 666, directories get chmod 777 (runner uses uid 1000, worker creates as root)

Without this: "file not found" errors. See worker/tasks.py:140-141.

### Dockerfile Build Context

All Dockerfiles use root (`.`) as context in docker-compose.yml. COPY paths must be `backend/file`, not `./file`.

```dockerfile
# ✅ CORRECT (context is root)
COPY backend/requirements.txt ./backend/
RUN pip install -r backend/requirements.txt

# ❌ WRONG (context is root)
COPY requirements.txt ./
RUN pip install -r requirements.txt
```

Wrong context → ModuleNotFoundError. See docker-compose.yml build contexts.

## Development Commands

### Quick Start

```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### Docker Compose

```bash
# Build runner image (one-time)
docker build -t py-playground-runner:latest ./runner

# Start all services
docker compose up --build

# Verify services
docker compose ps  # All should show "Up" or "Up (healthy)"

# Health check
curl http://localhost:8000/api/health
```

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://playground:playground@localhost:5432/playground  # Linux/Mac
set DATABASE_URL=postgresql://playground:playground@localhost:5432/playground    # Windows
uvicorn backend.app:app --reload
```

**Worker:**
```bash
cd worker
pip install -r requirements.txt
export DATABASE_URL=postgresql://playground:playground@localhost:5432/playground  # Linux/Mac
rq worker --url redis://localhost:6379 submissions
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev

# TypeScript type checking (optional)
npx tsc --noEmit
```

### Testing and Code Quality

**Run Tests:**
```bash
# Backend tests
docker compose exec backend pytest backend/tests/ -v

# With coverage
docker compose exec backend pytest backend/tests/ --cov=backend --cov-report=term-missing

# Specific test
docker compose exec backend pytest backend/tests/test_problem_service.py::TestProblemService::test_list_all_problems -v

# Worker tests
docker compose exec worker pip install pytest pytest-mock
docker compose exec worker pytest worker/tests/ -v
```

**Run Linters:**
```bash
# Install dev dependencies
pip install -r backend/requirements-dev.txt

# Format and lint
black backend/ worker/
isort backend/ worker/
flake8 backend/ worker/
mypy backend/ worker/

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

See [TESTING.md](TESTING.md) for detailed documentation.

### Database Access

```bash
# PostgreSQL shell
docker compose exec postgres psql -U playground

# Common queries
SELECT * FROM submissions ORDER BY created_at DESC LIMIT 10;
SELECT * FROM test_results WHERE submission_id = 1;
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f worker

# Structured JSON logs
docker compose logs backend | grep -E '^\{' | python -m json.tool
```

## Hierarchical Subject/Unit System

The platform organizes problems using a **three-level hierarchy**: Subject → Unit → Problem.

### Configuration

Subjects and units are defined in [backend/subjects_config.json](backend/subjects_config.json). Edit this file to add new subjects/units - no code changes needed.

**Current subjects:**
- **Programación 1**: Estructuras Secuenciales, Condicionales, Repetitivas, Listas, Funciones
- **Programación 2**: POO Básico, Herencia, Excepciones, Archivos, Estructuras de Datos
- **Algoritmos y Complejidad**: Ordenamiento, Búsqueda, Recursión, Complejidad, Programación Dinámica

### API Endpoints

**Student**:
- GET /api/problems - List all problems
- POST /api/submit - Submit code (returns job_id)
- GET /api/result/{job_id} - Poll for results

**Hierarchy Navigation**:
- GET /api/subjects - List all subjects
- GET /api/subjects/{subject_id}/units - Get units for a subject
- GET /api/subjects/{subject_id}/units/{unit_id}/problems - Get problems for a unit
- GET /api/problems/hierarchy - Complete hierarchy with problem counts

**Admin**:
- GET /api/admin/summary - Aggregate statistics
- GET /api/admin/submissions - Recent submissions with filters

Full schemas: http://localhost:8000/docs

### Frontend Navigation

Three cascading dropdowns:
1. **📚 Materia** (Subject) - User selects a subject
2. **📖 Unidad Temática** (Unit) - Auto-populates from selected subject
3. **🎯 Ejercicio** (Problem) - Shows problems for selected unit

See [frontend/src/components/Playground.tsx](frontend/src/components/Playground.tsx)

## Problem Structure

Problems live in `backend/problems/<problem_id>/` with 6 required files:

- `prompt.md` - Problem statement (Markdown)
- `starter.py` - Initial code template
- `tests_public.py` - Tests visible to students
- `tests_hidden.py` - Hidden tests for grading
- `metadata.json` - Title, subject_id, unit_id, difficulty, tags, timeout_sec, memory_mb
- `rubric.json` - Points per test and visibility

### Rubric System

**Critical**: Test names in rubric.json must match pytest function names exactly.

```json
{
  "tests": [
    {"name": "test_suma_basico", "points": 3, "visibility": "public"},
    {"name": "test_suma_hidden", "points": 2, "visibility": "hidden"}
  ],
  "max_points": 5
}
```

- **public** tests: Full details shown (outcome, message, duration)
- **hidden** tests: Only pass/fail, no error messages
- Points awarded only if test passes

### Test File Pattern

Both test files must use importlib to dynamically import student code:

```python
import importlib.util
import os

spec = importlib.util.spec_from_file_location(
    "student_code",
    os.path.join(os.getcwd(), "student_code.py")
)
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)

def test_suma_basico():
    assert hasattr(student, "suma"), "Debe existir una función suma(a, b)"
    assert student.suma(2, 3) == 5
```

See `backend/problems/sumatoria/` for complete examples.

## Security Implementation

### Multi-Layer Security

**1. Input Validation** ([backend/validators.py](backend/validators.py))

Before code reaches worker:
- Blocks dangerous imports: `os`, `subprocess`, `sys`, `__import__`, `eval()`, `exec()`, `compile()`
- Enforces max code length (50KB default)
- Validates problem_id format and existence

**2. Docker Sandbox Isolation**

```bash
docker run --rm \
  --network none \              # No network
  --read-only \                 # Read-only filesystem
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --tmpfs /workspace:rw,noexec,nosuid,size=128m \
  --cpus=1.0 --memory=256m --memory-swap=256m \
  -v $workspace:/workspace:rw \
  py-playground-runner:latest pytest -q --tb=short .
```

Additional safeguards:
- Timeout enforcement (default 5s, configurable per problem)
- Non-root user (uid 1000)
- Workspace cleanup after execution

**Limitations**: For high-stakes environments, consider gVisor runtime, separate VM/host for worker, or static analysis.

## Service Layer Architecture

The backend follows a **service layer pattern** to separate business logic from HTTP routes.

### Service Classes

**ProblemService** ([backend/services/problem_service.py](backend/services/problem_service.py)):
- `list_all()`, `get_problem_dir()`, `get_test_files()`, `load_rubric()`
- `list_by_subject_and_unit()`, `group_by_subject_and_unit()`

**SubjectService** ([backend/services/subject_service.py](backend/services/subject_service.py)):
- `list_all_subjects()`, `get_subject()`, `list_units_by_subject()`
- `get_hierarchy()`, `validate_subject_unit()`
- Reads from subjects_config.json

**SubmissionService** ([backend/services/submission_service.py](backend/services/submission_service.py)):
- `create_submission()`, `update_job_id()`, `get_by_job_id()`
- `get_result_dict()`, `get_statistics()`, `list_submissions()`

**DockerRunner** (worker/services/docker_runner.py):
- Handles Docker execution with path translation

**RubricScorer** (worker/services/rubric_scorer.py):
- Applies scoring logic to test results

### Adding New Features

Follow this pattern:

1. **Create service class** in `backend/services/`:
```python
from ..logging_config import get_logger
logger = get_logger(__name__)

class MyService:
    def do_something(self, param):
        logger.info(f"Doing something with {param}")
        return result

my_service = MyService()  # Singleton
```

2. **Use in routes** (backend/app.py):
```python
from .services.my_service import my_service

@app.get("/api/my-endpoint")
def my_endpoint(db: Session = Depends(get_db)):
    return my_service.do_something("value")
```

3. **Add validation** (backend/validators.py)
4. **Add exceptions** (backend/exceptions.py)
5. **Add configuration** (backend/config.py)
6. **Use structured logging**: `logger.info("Message", extra={"key": "value"})`

## Adding New Problems

1. Choose subject/unit from [backend/subjects_config.json](backend/subjects_config.json)
2. Create directory: `mkdir backend/problems/new_problem`
3. Create 6 files: `prompt.md`, `starter.py`, `tests_public.py`, `tests_hidden.py`, `metadata.json`, `rubric.json`
4. Fill metadata.json with subject_id and unit_id
5. Test locally:

```bash
# Submit test
curl -X POST http://localhost:8000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"problem_id": "new_problem", "code": "def my_func():\n    pass", "student_id": "test"}'

# Check results
curl http://localhost:8000/api/result/JOB_ID

# Verify hierarchy
curl http://localhost:8000/api/problems/hierarchy | python -m json.tool
```

## Common Tasks

**Restart service after code changes:**
```bash
docker compose restart backend
# Or rebuild if dependencies changed:
docker compose up -d --build backend
```

**Reset database:**
```bash
docker compose down -v && docker compose up --build
```

**Change resource limits globally:**
Edit `DEFAULT_TIMEOUT`, `DEFAULT_MEMORY_MB`, `DEFAULT_CPUS` in worker/tasks.py

**Change resource limits per problem:**
Edit problem's metadata.json (timeout_sec, memory_mb)

**Test problem manually:**
```bash
docker run -it --rm -v $(pwd)/backend/problems/sumatoria:/workspace -w /workspace py-playground-runner:latest bash
# Inside container:
echo "def suma(a,b): return a+b" > student_code.py
pytest -v tests_public.py
```

## Port Configuration

**Windows users**: Default ports may have permission issues. Configured with alternatives:
- PostgreSQL: External `15432` → Internal `5432`
- Redis: External `16379` → Internal `6379`
- Backend: `8000`
- Frontend: `5173`

Container-to-container communication uses internal ports (e.g., `postgres:5432` in DATABASE_URL).

## Troubleshooting

**First-time startup is slow**: 5-10 minutes to download/build images. Monitor: `docker compose logs -f`

**Port already in use**:
```bash
# Windows: netstat -ano | findstr :8000 && taskkill /PID <PID> /F
# Linux: lsof -i :8000 && kill -9 <PID>
```

**Worker can't access Docker daemon**:
- Check `/var/run/docker.sock` mounted in docker-compose.yml
- Windows: Verify Docker Desktop uses WSL 2
- Linux: Add user to docker group: `sudo usermod -aG docker $USER && newgrp docker`

**Runner image not found**: `docker build -t py-playground-runner:latest ./runner`

**ModuleNotFoundError**: Dockerfile COPY paths incorrect. Use `backend/requirements.txt` not `requirements.txt`. Rebuild: `docker compose build --no-cache backend`

**Tests timing out**: Increase timeout_sec in metadata.json or DEFAULT_TIMEOUT in worker/tasks.py

**Database connection errors**: Wait for healthcheck: `docker compose ps`

**RQ worker not processing**: Check Redis: `docker compose exec redis redis-cli ping`

## Refactoring Status

See [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) for detailed progress.

**Completed**:
- ✅ Phase 1 (100%): Core infrastructure (config, logging, validation, exceptions)
- ✅ Phase 2 (100%): Service layer architecture, Pydantic v2 schemas

**In Progress**:
- ⏳ Phase 3 (85%): Testing (83 tests, 25/53 passing), linting, pre-commit hooks

**When continuing refactoring**:
1. Read REFACTORING_COMPLETE.md first
2. Follow service layer pattern
3. Use structured logging: `get_logger(__name__)`
4. Add validation for inputs
5. Test after changes

## Frontend Architecture

**TypeScript Migration** ✅ (Completed: 25 Oct 2025)
- Migrated from JavaScript to TypeScript for improved type safety
- Centralized API types in `src/types/api.ts`
- All components fully typed with interfaces

**Components**:
- **App.tsx** - Tab navigation (Ejercicios, Panel Docente)
- **Playground.tsx** - Student interface with cascading dropdowns, Monaco editor, result polling with AbortController
- **AdminPanel.tsx** - Instructor dashboard
- **types/api.ts** - TypeScript interfaces for all API requests/responses

**Features**:
- Monaco Editor for Python syntax highlighting
- Code persisted to localStorage
- Full TypeScript type checking with strict mode
- Type-safe API calls with Axios

**Tech Stack**:
- React 18 with TypeScript
- Vite 6 for build tooling
- Monaco Editor for code editing
- Axios for HTTP requests
- TypeScript strict mode enabled

**Development Workflow**:
```bash
# Run dev server (hot reload enabled)
npm run dev

# Type check without compiling
npx tsc --noEmit

# Build for production
npm run build

# Preview production build
npm run preview
```

**Adding New Components**:
1. Create `.tsx` files (not `.jsx`)
2. Import types from `src/types/api.ts`
3. Define component props interface:
   ```typescript
   interface MyComponentProps {
     title: string
     onSubmit: (data: FormData) => void
   }

   function MyComponent({ title, onSubmit }: MyComponentProps) {
     const [value, setValue] = useState<string>('')
     // ...
   }
   ```

**Adding New API Types**:
Edit `frontend/src/types/api.ts` and add/export new interfaces. Types are automatically available throughout the app.

## Extension Points

- Multiple workers for scaling (add worker services in docker-compose.yml)
- Different languages (change RUNNER_IMAGE env var)
- Custom test frameworks (update conftest.py)
- Authentication (add middleware to backend/app.py)
- Webhooks (add to worker/tasks.py after commit)
- Rate limiting (Redis counter in backend)
