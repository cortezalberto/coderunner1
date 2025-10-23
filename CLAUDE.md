# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ✅ Current Status (Updated: 23 Oct 2025)

**System Status**: Fully Functional ✅

The project is **production-ready** with all core features working:
- ✅ Code execution in isolated Docker containers
- ✅ Test validation with public/hidden tests
- ✅ Automatic scoring with rubrics
- ✅ Service layer architecture (Phase 1: 100%, Phase 2: 100%)
- ✅ Pydantic v2 schema validation on all endpoints
- ✅ Security: input validation, network isolation, resource limits
- ✅ Structured JSON logging

**Critical Fix Applied**: Docker-in-Docker volume mounting issue resolved (see "Critical: Docker-in-Docker Configuration" section below). Tests now execute correctly.

**Phase 2 Completed** (23 Oct 2025):
- ✅ Worker services created: DockerRunner, RubricScorer
- ✅ Pydantic v2 schemas for all API requests/responses
- ✅ All endpoints tested and working with new architecture
- ⏳ Frontend refactoring (optional optimization) pending

**Phase 3: 85% Complete** (23 Oct 2025):
- ✅ Test infrastructure created (83 unit tests)
- ✅ Linting configuration (Black, flake8, isort, mypy)
- ✅ Pre-commit hooks configured
- ✅ TESTING.md documentation created
- ⏳ Some tests need minor adjustments (25/53 passing in backend)
- ⏳ Worker tests created but not yet executed

**Important Files**:
- [ANALISIS_Y_CORRECCIONES.md](ANALISIS_Y_CORRECCIONES.md) - Complete analysis and fixes applied
- [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) - Refactoring progress (Phases 1 & 2 complete, Phase 3 85%)
- [TESTING.md](TESTING.md) - Testing guide with instructions for running tests and linters

## Project Overview

**Python Playground Suite** - A production-ready code execution platform with Docker sandbox isolation, job queues, persistent storage, and a modern web interface. Students submit Python code that is executed in isolated Docker containers with strict security constraints.

## Architecture

This is a microservices architecture with the following components:

```
Frontend (React+Monaco) → Backend (FastAPI) → Redis (RQ Queue) → Worker → Docker Sandbox
                              ↓
                         PostgreSQL
```

### Core Services

1. **backend/** - FastAPI REST API with service layer architecture
   - **app.py** - FastAPI application, routes/endpoints
   - **services/** - Business logic layer (ProblemService, SubmissionService)
   - **models.py** - SQLAlchemy ORM models (Submission, TestResult)
   - **database.py** - Database session management
   - **config.py** - Centralized configuration with environment variables
   - **validators.py** - Input validation and security checks
   - **exceptions.py** - Custom exception hierarchy
   - **logging_config.py** - Structured JSON logging
   - Receives code submissions via `/api/submit`
   - Enqueues jobs in Redis using RQ
   - Stores results in PostgreSQL
   - Provides admin endpoints for metrics

2. **worker/** - RQ worker process with service layer architecture
   - **tasks.py** - Main job orchestration (coordina servicios)
   - **services/docker_runner.py** - Docker execution service with path translation
   - **services/rubric_scorer.py** - Automatic grading service with scoring logic
   - Consumes jobs from Redis queue
   - Executes code in isolated Docker containers via DockerRunner
   - Applies rubrics to calculate scores via RubricScorer
   - Saves detailed results to database

3. **runner/** - Minimal Docker image for sandboxed execution
   - Python 3.11 + pytest only
   - Non-root user (sandbox uid 1000)
   - Used by worker for each submission

4. **frontend/** - React + Vite + Monaco Editor
   - Problem selector and code editor
   - Real-time result polling
   - Admin panel for instructors

5. **PostgreSQL** - Persistent storage
   - Submissions table with job metadata
   - TestResults table for individual test outcomes

6. **Redis** - Job queue and caching

### Execution Flow

```
1. Student submits code via frontend
2. Backend creates Submission record in DB (status: "pending")
3. Backend enqueues job in Redis (RQ) with job_id
4. Backend updates Submission status to "queued"
5. Worker picks up job from queue
6. Worker creates temp directory with:
   - student_code.py (submitted code)
   - tests_public.py + tests_hidden.py (from backend/problems/)
   - conftest.py (pytest plugin for JSON report generation)
7. Worker runs: docker run --network none --read-only --cpus 1 --memory 256m ...
8. Container executes pytest and generates report.json
9. Worker parses report.json, applies rubric scoring
10. Worker saves to DB: TestResult rows + updates Submission (status: "completed")
11. Frontend polls /api/result/{job_id} every 1s and displays results
```

### Database Models

**Submission** (backend/models.py):
- job_id, student_id, problem_id, code
- status (pending/queued/running/completed/failed/timeout)
- score_total, score_max, passed, failed, errors
- stdout, stderr, duration_sec
- Relationship: one-to-many with TestResult

**TestResult** (backend/models.py):
- test_name, outcome, duration, message
- points, max_points, visibility (public/hidden)

## Development Commands

### Quick Start (Recommended)

```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

This automatically builds the runner image and starts all services.

### Full Stack (Docker Compose)

```bash
# Build runner image first (one-time)
docker build -t py-playground-runner:latest ./runner

# Start all services
docker compose up --build

# Stop and remove volumes (reset database)
docker compose down -v
```

Services will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Verify all services are running:**
```bash
docker compose ps
# All services should show "Up" or "Up (healthy)" status
# If any service is "Exit 1" or keeps restarting, check logs:
docker compose logs <service_name>
```

**Quick health check:**
```bash
# Test backend API
curl http://localhost:8000/api/problems
# Or with PowerShell on Windows:
Invoke-RestMethod -Uri http://localhost:8000/api/problems -Method Get
```

### Local Development (Individual Services)

**Backend:**
```bash
# Linux/Mac
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://playground:playground@localhost:5432/playground
export REDIS_URL=redis://localhost:6379/0
uvicorn backend.app:app --reload

# Windows
cd backend
pip install -r requirements.txt
set DATABASE_URL=postgresql://playground:playground@localhost:5432/playground
set REDIS_URL=redis://localhost:6379/0
python -m uvicorn backend.app:app --reload
```

**Worker:**
```bash
# Linux/Mac
cd worker
pip install -r requirements.txt
export DATABASE_URL=postgresql://playground:playground@localhost:5432/playground
rq worker --url redis://localhost:6379 submissions

# Windows
cd worker
pip install -r requirements.txt
set DATABASE_URL=postgresql://playground:playground@localhost:5432/playground
rq worker --url redis://localhost:6379 submissions
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f worker
docker compose logs -f frontend

# Database logs
docker compose logs -f postgres
```

### Database Access

```bash
# PostgreSQL shell
docker compose exec postgres psql -U playground

# Common queries
SELECT * FROM submissions ORDER BY created_at DESC LIMIT 10;
SELECT * FROM test_results WHERE submission_id = 1;
```

## Problem Structure

Problems live in `backend/problems/<problem_id>/` with:

- `prompt.md` - Problem statement (supports Markdown)
- `starter.py` - Initial code template
- `tests_public.py` - Tests visible to students
- `tests_hidden.py` - Hidden tests (for grading)
- `metadata.json` - Title, difficulty, tags, timeout_sec, memory_mb
- `rubric.json` - Points per test and visibility

### Rubric System

Example `rubric.json`:
```json
{
  "tests": [
    {"name": "test_suma_basico", "points": 3, "visibility": "public"},
    {"name": "test_suma_negativos", "points": 2, "visibility": "public"},
    {"name": "test_suma_negativos_avanzado", "points": 3, "visibility": "hidden"},
    {"name": "test_suma_grande", "points": 2, "visibility": "hidden"}
  ],
  "max_points": 10
}
```

**Important:** Test names in rubric.json must match the actual pytest function names.

- **public** tests: Full details (outcome, message, duration) shown to students
- **hidden** tests: Only shown as "passed/failed", no details or error messages
- Scores calculated: points awarded only if test passes

### Test File Pattern

Both `tests_public.py` and `tests_hidden.py` must:

1. Import student code dynamically using importlib:
```python
import importlib.util
import os

spec = importlib.util.spec_from_file_location(
    "student_code",
    os.path.join(os.getcwd(), "student_code.py")
)
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)
```

2. Define pytest test functions that use `student.function_name()`
3. Use descriptive test names matching rubric entries exactly

**Example:**
```python
def test_suma_basico():
    """Test básico de suma"""
    assert hasattr(student, "suma"), "Debe existir una función suma(a, b)"
    assert student.suma(2, 3) == 5
```

### Legacy Support

If `tests_public.py` and `tests_hidden.py` don't exist, worker falls back to `tests.py` (from old MVP structure).

## Security Implementation

### Multi-Layer Security

**1. Input Validation Layer** ([backend/validators.py](backend/validators.py))

Before code reaches the worker, it's validated for:
- **Dangerous imports**: Blocks `import os`, `import subprocess`, `import sys`, `__import__`, `eval()`, `exec()`, `compile()`
- **Code length**: Maximum 50KB by default
- **Problem existence**: Verifies problem_id exists in filesystem
- **Problem ID format**: Validates alphanumeric + underscores only

All submissions pass through `validate_submission_request()` before being enqueued.

**2. Docker Sandbox Isolation**

The worker executes every submission in a Docker container with:

```bash
docker run --rm \
  --network none \              # No network access
  --read-only \                 # Filesystem is read-only
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --tmpfs /workspace:rw,noexec,nosuid,size=128m \
  --cpus=1.0 \                  # CPU limit
  --memory=256m \               # Memory limit
  --memory-swap=256m \          # No swap
  -v $workspace:/workspace:rw \ # Mount student code
  -w /workspace \
  py-playground-runner:latest \
  pytest -q --tb=short .
```

**Additional safeguards:**
- Timeout enforcement (default 5s, configurable per problem)
- Non-root user in container (sandbox uid 1000)
- No capabilities, no privileged mode
- Worker runs on separate process from API
- Workspace cleanup after execution

**Limitations:**
- This prevents most attack vectors but is not foolproof
- For high-stakes environments, consider additional layers:
  - gVisor runtime
  - Separate VM/host for worker
  - Module import whitelist
  - Static analysis before execution

## API Endpoints

### Student Endpoints

- `GET /api/problems` - List all problems with prompts and starters
- `POST /api/submit` - Submit code (returns job_id)
  - Body: `{"problem_id": "string", "code": "string", "student_id": "string"?}`
- `GET /api/result/{job_id}` - Poll for results

### Admin Endpoints

- `GET /api/admin/summary` - Aggregate statistics
  - Returns: total submissions, completed, failed, pending, avg_score, by_problem stats
- `GET /api/admin/submissions?limit=50&problem_id=...&student_id=...` - Recent submissions
  - Query params: limit (default 50), offset, problem_id, student_id

### Response Format

**Queued submission:**
```json
{
  "job_id": "abc123",
  "status": "queued",
  "message": "Submission enqueued successfully"
}
```

**Completed submission:**
```json
{
  "job_id": "abc123",
  "status": "completed",
  "ok": true,
  "score_total": 8.0,
  "score_max": 10.0,
  "passed": 3,
  "failed": 1,
  "errors": 0,
  "duration_sec": 0.234,
  "test_results": [
    {
      "test_name": "test_suma_basico",
      "outcome": "passed",
      "duration": 0.001,
      "points": 3,
      "max_points": 3,
      "visibility": "public",
      "message": ""
    }
  ],
  "stdout": "...",
  "stderr": "",
  "created_at": "2025-10-22T19:00:00",
  "completed_at": "2025-10-22T19:00:05"
}
```

## Adding New Features

### Following the Service Layer Pattern

When adding new features to the backend, follow this pattern:

1. **Create a service class** in `backend/services/` if it involves business logic:
```python
# backend/services/my_service.py
from ..logging_config import get_logger
from ..exceptions import ValidationError

logger = get_logger(__name__)

class MyService:
    def do_something(self, param):
        logger.info(f"Doing something with {param}")
        # Business logic here
        return result

# Singleton instance
my_service = MyService()
```

2. **Use the service in routes** ([backend/app.py](backend/app.py)):
```python
from .services.my_service import my_service

@app.get("/api/my-endpoint")
def my_endpoint(db: Session = Depends(get_db)):
    return my_service.do_something("value")
```

3. **Add validation** if accepting user input ([backend/validators.py](backend/validators.py)):
```python
def validate_my_input(value: str):
    if not value:
        raise ValidationError("Value cannot be empty")
```

4. **Add custom exceptions** if needed ([backend/exceptions.py](backend/exceptions.py)):
```python
class MyCustomError(Exception):
    pass
```

5. **Add configuration** if using environment variables ([backend/config.py](backend/config.py)):
```python
class Settings:
    MY_NEW_SETTING: str = os.getenv("MY_NEW_SETTING", "default_value")
```

6. **Use structured logging** throughout:
```python
logger.info("Action completed", extra={"key": "value"})
logger.error("Error occurred", exc_info=True)
```

## Adding New Problems

1. Create directory:
```bash
# Linux/Mac
mkdir -p backend/problems/new_problem

# Windows
mkdir backend\problems\new_problem
```

2. Create all required files:
```bash
# Linux/Mac
cd backend/problems/new_problem
touch prompt.md starter.py tests_public.py tests_hidden.py metadata.json rubric.json

# Windows
cd backend\problems\new_problem
type nul > prompt.md
type nul > starter.py
type nul > tests_public.py
type nul > tests_hidden.py
type nul > metadata.json
type nul > rubric.json
```

3. Fill in each file (see `backend/problems/sumatoria/` as reference)

4. Test locally:
```bash
# Linux/Mac
curl -X POST http://localhost:8000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"problem_id": "new_problem", "code": "def my_func():\n    pass", "student_id": "test"}'

# Windows (CMD)
curl -X POST http://localhost:8000/api/submit ^
  -H "Content-Type: application/json" ^
  -d "{\"problem_id\":\"new_problem\",\"code\":\"def my_func():\n    pass\",\"student_id\":\"test\"}"
```

5. Poll for results:
```bash
curl http://localhost:8000/api/result/JOB_ID
```

## Frontend Architecture

- **App.jsx** - Main component with tab navigation (Ejercicios, Panel Docente)
- **Playground.jsx** - Student interface (problem selector, Monaco editor, results display)
- **AdminPanel.jsx** - Instructor dashboard (stats, recent submissions table)
- Uses Monaco Editor for syntax highlighting and autocomplete
- Polls `/api/result/{job_id}` every 1s until status is completed/failed/timeout
- Displays public test results in detail, hidden tests as locked items

## Code Architecture Details

### Backend Service Layer Pattern

The backend follows a **service layer architecture** to separate business logic from HTTP routes:

**Service Classes:**
- **ProblemService** ([backend/services/problem_service.py](backend/services/problem_service.py))
  - `list_all()` - Returns all problems with metadata, prompts, and starters
  - `get_problem_dir(problem_id)` - Gets filesystem path for a problem
  - `get_test_files(problem_id)` - Locates tests_public.py and tests_hidden.py
  - `load_rubric(problem_id)` - Loads and parses rubric.json
  - Used by `/api/problems` endpoint

- **SubmissionService** ([backend/services/submission_service.py](backend/services/submission_service.py))
  - `create_submission()` - Creates new submission record
  - `update_job_id()` - Updates submission with RQ job_id
  - `get_by_job_id()` - Retrieves submission by job_id
  - `get_result_dict()` - Formats submission as API response with test results
  - `get_statistics()` - Aggregates metrics for admin dashboard
  - `list_submissions()` - Paginated list with filters
  - Used by `/api/submit`, `/api/result/{job_id}`, `/api/admin/*` endpoints

**Configuration & Validation:**
- **Settings class** ([backend/config.py](backend/config.py))
  - Centralized configuration loaded from environment variables
  - Database URLs, Redis connection, CORS origins, Docker settings, resource limits
  - Singleton instance: `settings`

- **Input Validators** ([backend/validators.py](backend/validators.py))
  - `validate_code_safety()` - Detects dangerous imports (os, subprocess, eval, exec, etc.)
  - `validate_code_length()` - Enforces max code size
  - `validate_problem_exists()` - Checks problem directory exists
  - `validate_submission_request()` - Main validation for /api/submit

- **Custom Exceptions** ([backend/exceptions.py](backend/exceptions.py))
  - `ProblemNotFoundError`, `TestExecutionError`, `DockerExecutionError`
  - `RubricError`, `ValidationError`

**Logging:**
- **Structured JSON logging** ([backend/logging_config.py](backend/logging_config.py))
  - All logs output as JSON with timestamp, level, logger, message, module, function, line
  - Supports extra context fields: job_id, submission_id, problem_id
  - Use `get_logger(__name__)` in all modules

### Key Configuration Files

- `docker-compose.yml` - Orchestrates all services, defines health checks
- `.env.example` - Environment variable template (copy to .env for local dev)
- `backend/config.py` - Centralized settings with environment variable support
- `backend/database.py` - SQLAlchemy setup with session management
- `backend/models.py` - Database schema definitions (Submission, TestResult)
- `worker/tasks.py` - Main job processing logic with Docker execution

## Important: Dockerfile Context Configuration

All Dockerfiles use the **root directory (`.`)** as build context in docker-compose.yml. This is critical for proper builds:

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
# Context is root (.), so paths must be relative to root
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend ./backend
```

**Worker Dockerfile** (`worker/Dockerfile`):
```dockerfile
# Context is root (.), so paths must be relative to root
COPY worker/requirements.txt ./worker/
RUN pip install --no-cache-dir -r worker/requirements.txt
COPY backend ./backend  # Worker needs backend code for models
COPY worker ./worker
```

**Why this matters:** If you change the context or COPY paths incorrectly, pip won't find requirements.txt and services will fail with "ModuleNotFoundError". Always use paths relative to the root directory.

## Port Configuration

**Important for Windows users:** The default PostgreSQL (5432) and Redis (6379) ports may have permission issues on Windows. The project is configured with alternative ports:

- **PostgreSQL**: External port `15432` → Internal port `5432`
- **Redis**: External port `16379` → Internal port `6379`
- **Backend**: Port `8000` (no change)
- **Frontend**: Port `5173` (no change)

To change ports, edit `docker-compose.yml`:
```yaml
postgres:
  ports:
    - "15432:5432"  # external:internal
```

**Note:** Internal container-to-container communication always uses the internal port (e.g., `postgres:5432` in DATABASE_URL).

## Common Tasks

**Build runner image manually:**
```bash
docker build -t py-playground-runner:latest ./runner
```

**Change resource limits globally:**
Edit environment variables in `docker-compose.yml` or modify `DEFAULT_TIMEOUT`, `DEFAULT_MEMORY_MB`, `DEFAULT_CPUS` in `worker/tasks.py`

**Change resource limits per problem:**
Edit `metadata.json`:
```json
{
  "timeout_sec": 3.0,
  "memory_mb": 128
}
```

**Reset database completely:**
```bash
docker compose down -v
docker compose up --build
```

**Restart a single service after code changes:**
```bash
# Restart backend after modifying backend code
docker compose restart backend

# Or rebuild if you changed dependencies
docker compose up -d --build backend

# View logs to verify changes
docker compose logs -f backend
```

**Test API endpoints manually:**
```bash
# Test problem listing
curl http://localhost:8000/api/problems

# Test submission
curl -X POST http://localhost:8000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"problem_id":"sumatoria","code":"def suma(a,b): return a+b","student_id":"test"}'

# Test admin statistics
curl http://localhost:8000/api/admin/summary

# View backend logs for structured JSON output
docker compose logs backend | grep -E '^\{' | python -m json.tool
```

**Test a problem manually (inside runner container):**
```bash
# Linux/Mac
docker run -it --rm -v $(pwd)/backend/problems/sumatoria:/workspace -w /workspace py-playground-runner:latest bash
# Inside container:
echo "def suma(a,b): return a+b" > student_code.py
pytest -v tests_public.py

# Windows (PowerShell)
docker run -it --rm -v ${PWD}/backend/problems/sumatoria:/workspace -w /workspace py-playground-runner:latest bash
# Inside container:
echo "def suma(a,b): return a+b" > student_code.py
pytest -v tests_public.py

# Windows (CMD) - use absolute path
docker run -it --rm -v C:\path\to\python-playground-mvp\backend\problems\sumatoria:/workspace -w /workspace py-playground-runner:latest bash
```

## Critical: Docker-in-Docker Configuration

The worker runs Docker commands to execute student code in isolated containers. This creates a **Docker-in-Docker** scenario that requires special configuration:

### The Problem

The worker container uses the host's Docker daemon (via mounted `/var/run/docker.sock`) to spawn runner containers. When the worker creates temporary workspaces in `/tmp/sandbox-xxx`, these paths exist **inside the worker container**, not on the host. When Docker tries to mount these paths into the runner container, it fails because Docker daemon looks for paths on the **host filesystem**.

### The Solution

1. **Shared Workspace Directory** ([docker-compose.yml](docker-compose.yml)):
   - Worker mounts `./workspaces:/workspaces` as a bind mount
   - This directory exists on both the host and inside the worker
   - Environment variable `HOST_WORKSPACE_DIR=${PWD}/workspaces` tells worker the host path

2. **Path Translation** ([worker/tasks.py](worker/tasks.py:140-141)):
   ```python
   # Convert /workspaces/sandbox-xxx (worker) to HOST_WORKSPACE_DIR/sandbox-xxx (host)
   workspace_rel = workspace.replace(WORKSPACE_DIR, "").lstrip("/")
   host_workspace = f"{HOST_WORKSPACE_DIR}/{workspace_rel}"
   ```

3. **File Permissions** ([worker/tasks.py](worker/tasks.py:80,85,96,100-105,138)):
   - Worker creates files as root, but runner uses uid 1000 (sandbox user)
   - All workspace files get `chmod 666` and directory gets `chmod 777`
   - Required for runner to read tests and write report.json

### Why This Matters

Without this setup, you'll see errors like:
- `ERROR: file or directory not found: tests_public.py`
- `docker: Error response from daemon: Duplicate mount point`
- `PermissionError: [Errno 13] Permission denied`

The `workspaces/` directory must exist at the project root. It's created automatically but can be manually created: `mkdir workspaces`

## Troubleshooting

**First-time startup is slow:**
- First run takes 5-10 minutes to download and build all images (postgres, redis, runner, backend, worker, frontend)
- Monitor progress with: `docker compose logs -f`
- Be patient, subsequent startups are much faster

**Port 5173 or 8000 already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

**Worker can't access Docker daemon:**
- Ensure `/var/run/docker.sock` is mounted in worker service (check docker-compose.yml)
- Check Docker daemon is running: `docker ps`
- Verify worker has permission to access socket
- **Windows:** Ensure Docker Desktop is using WSL 2 and user has permissions in Docker Desktop settings
- **Linux:** Add user to docker group: `sudo usermod -aG docker $USER && newgrp docker`

**Runner image not found:**
```bash
docker build -t py-playground-runner:latest ./runner
# Or use docker compose profile:
docker compose --profile build up --build
```

**Frontend can't reach backend:**
- Check CORS settings in `backend/app.py` (allow_origins)
- Check proxy configuration in `frontend/vite.config.js`
- Verify backend service is running: `docker compose ps`
- Ensure backend is healthy: `curl http://localhost:8000/health` (if health endpoint exists)

**Tests timing out:**
- Increase timeout in problem's `metadata.json` (timeout_sec)
- Or modify `DEFAULT_TIMEOUT` in `worker/tasks.py`
- Check container logs: `docker compose logs -f worker`

**Database connection errors:**
- Wait for postgres healthcheck: `docker compose ps`
- Check DATABASE_URL in environment
- Access DB directly: `docker compose exec postgres psql -U playground`
- If corruption suspected: `docker compose down -v && docker compose up postgres -d`

**RQ worker not processing jobs:**
- Check Redis connection: `docker compose exec redis redis-cli ping`
- View worker logs: `docker compose logs -f worker`
- Check queue status using RQ dashboard or redis-cli
- Verify job was enqueued: `docker compose exec redis redis-cli LLEN rq:queue:submissions`

**Docker Desktop not starting (Windows/Mac):**
- Restart Docker Desktop application
- Check system requirements (WSL 2 for Windows, sufficient RAM)
- Verify virtualization is enabled in BIOS

**ModuleNotFoundError (sqlalchemy, rq, etc.):**
This indicates Dockerfile COPY paths are incorrect. The build context is the root directory (`.`), not the service directory:
```dockerfile
# ❌ WRONG (if context is root)
COPY requirements.txt ./
RUN pip install -r requirements.txt

# ✅ CORRECT (if context is root)
COPY backend/requirements.txt ./backend/
RUN pip install -r backend/requirements.txt
```
Solution: Rebuild with `docker compose build --no-cache backend` (or worker)

**Worker command "rq: not found":**
The `rq` CLI command may not be in PATH after pip install. Use the Python module syntax:
```yaml
# In docker-compose.yml
command: python -m rq.cli worker --url redis://redis:6379/0 submissions
```

## Current Refactoring Status

The codebase is currently undergoing a phased refactoring to improve maintainability and code quality. See [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) for detailed progress.

**Completed:**
- ✅ Phase 1 (100%): Core infrastructure
  - Centralized configuration ([backend/config.py](backend/config.py))
  - Structured JSON logging ([backend/logging_config.py](backend/logging_config.py))
  - Input validation with security checks ([backend/validators.py](backend/validators.py))
  - Custom exception hierarchy ([backend/exceptions.py](backend/exceptions.py))

- ✅ Phase 2 (35%): Service layer architecture
  - ProblemService for problem management
  - SubmissionService for submission CRUD and statistics
  - Both services fully integrated and tested

**In Progress:**
- ⏳ Phase 2 remaining tasks:
  - DockerRunner service (worker)
  - RubricScorer service (worker)
  - Frontend React hooks refactoring
  - Pydantic schemas for request/response validation

**When continuing refactoring:**
1. Always read [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) first for current status
2. Follow the established service layer pattern (see "Adding New Features" section)
3. Use structured logging with `get_logger(__name__)`
4. Add validation for all user inputs
5. Test endpoints after making changes

## Extension Points

The architecture supports:
- Multiple workers for horizontal scaling (add more worker services in docker-compose.yml)
- Different runner images per language (modify RUNNER_IMAGE env var)
- Custom test frameworks beyond pytest (update conftest.py pattern)
- Authentication middleware in FastAPI (add to backend/app.py)
- Webhook notifications on completion (add to worker/tasks.py after DB commit)
- Rate limiting per student (add Redis-based counter in backend)
- Submission history and analytics (query PostgreSQL)
