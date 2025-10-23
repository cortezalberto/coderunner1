# Testing Guide

## Fase 3: Tests y Calidad de Código

Este documento describe la infraestructura de testing y linting creada para el proyecto.

## ✅ Completado

### 1. Estructura de Tests

**Backend Tests** (`backend/tests/`):
- `conftest.py` - Fixtures compartidas (test_db, sample data, mock_problem_dir)
- `test_problem_service.py` - 11 tests para ProblemService
- `test_submission_service.py` - 15 tests para SubmissionService
- `test_validators.py` - 24 tests para validadores

**Worker Tests** (`worker/tests/`):
- `conftest.py` - Fixtures compartidas (sample rubrics, docker results)
- `test_rubric_scorer.py` - 18 tests para RubricScorer
- `test_docker_runner.py` - 15 tests para DockerRunner (con mocks)

**Total**: 83 tests unitarios creados

### 2. Configuración de Linting

**Archivos Creados**:
- `pyproject.toml` - Configuración de Black, isort, pytest, mypy, coverage
- `.flake8` - Configuración de flake8 con reglas específicas
- `.pre-commit-config.yaml` - Hooks de pre-commit
- `backend/requirements-dev.txt` - Dependencias de desarrollo
- `worker/requirements-dev.txt` - Dependencias de desarrollo

**Herramientas Configuradas**:
- **Black**: Formateo de código (line-length=100)
- **isort**: Ordenamiento de imports (profile=black)
- **flake8**: Linting con reglas personalizadas
- **mypy**: Type checking (configurado pero opcional)
- **pytest**: Testing con coverage
- **pre-commit**: Hooks automáticos

## 📊 Estado Actual de Tests

### Resultado de Ejecución

```bash
docker compose exec backend pytest backend/tests/ -v
```

**Resumen**:
- ✅ **25 tests PASSED**
- ❌ **28 tests FAILED** (requieren ajustes menores)
- 📝 Total: 53 tests en backend

### Tests que Pasaron ✅

**ProblemService** (7/11):
- test_list_all_problems
- test_get_problem_dir_exists
- test_get_problem_dir_not_exists
- test_load_rubric_success
- test_load_rubric_invalid_json
- test_list_all_handles_missing_metadata
- test_singleton_instance

**SubmissionService** (11/15):
- test_create_submission
- test_create_submission_without_student_id
- test_update_job_id
- test_get_by_job_id_exists/not_exists
- test_get_by_id_exists/not_exists
- test_get_result_dict (con y sin test_results)
- test_get_statistics_empty_database
- test_singleton_instance

**Validators** (7/24):
- test_empty_code
- test_safe_code
- test_safe_imports
- test_valid_alphanumeric
- test_valid_with_hyphens_underscores

### Tests que Necesitan Ajustes ❌

**Problemas Identificados**:

1. **ProblemService.get_test_files()** - Retorna tupla de 3 elementos, tests esperan 2
   - Solución: Revisar [backend/services/problem_service.py](backend/services/problem_service.py:57-65)

2. **Validadores** - No lanzan excepciones como se esperaba
   - Algunos validadores retornan None en lugar de lanzar excepción
   - Solución: Actualizar tests o implementación de validadores

3. **SubmissionService tests con SQLAlchemy** - UNIQUE constraint en job_id
   - Tests crean múltiples submissions sin job_id único
   - Solución: Agregar job_id único en cada submission de test

## 🚀 Cómo Ejecutar Tests

### Backend Tests

```bash
# Dentro del contenedor backend
docker compose exec backend pytest backend/tests/ -v

# Con coverage
docker compose exec backend pytest backend/tests/ --cov=backend --cov-report=term-missing

# Un archivo específico
docker compose exec backend pytest backend/tests/test_problem_service.py -v

# Un test específico
docker compose exec backend pytest backend/tests/test_problem_service.py::TestProblemService::test_list_all_problems -v
```

### Worker Tests

```bash
# Instalar dependencias de testing primero
docker compose exec worker pip install pytest pytest-mock

# Ejecutar tests
docker compose exec worker pytest worker/tests/ -v

# Con coverage
docker compose exec worker pytest worker/tests/ --cov=worker --cov-report=term-missing
```

## 🔧 Configuración de Linting

### Instalar Dependencias de Desarrollo

```bash
# Backend
cd backend
pip install -r requirements-dev.txt

# Worker
cd worker
pip install -r requirements-dev.txt
```

### Ejecutar Linters

```bash
# Black - formateo automático
black backend/ worker/

# isort - ordenar imports
isort backend/ worker/

# flake8 - linting
flake8 backend/ worker/

# mypy - type checking
mypy backend/ worker/
```

### Pre-commit Hooks

```bash
# Instalar hooks
pre-commit install

# Ejecutar manualmente en todos los archivos
pre-commit run --all-files

# Los hooks se ejecutarán automáticamente en cada commit
git commit -m "mensaje"
```

## 📈 Coverage Report

Para generar reporte de cobertura de código:

```bash
# Generar coverage en HTML
docker compose exec backend pytest backend/tests/ --cov=backend --cov-report=html

# El reporte estará en backend/htmlcov/index.html
# Abrir en navegador para ver detalle por archivo
```

**Cobertura esperada**:
- **Meta**: >80% de cobertura en servicios principales
- **Actual**: Por determinar una vez que todos los tests pasen

## 🛠️ Tareas Pendientes

### Para Completar Fase 3:

1. **Arreglar tests fallidos** (prioridad alta):
   - [ ] Corregir `get_test_files()` return value
   - [ ] Ajustar expectativas de validadores
   - [ ] Agregar job_ids únicos en tests de SubmissionService

2. **Ejecutar tests de worker**:
   - [ ] Instalar pytest en contenedor worker
   - [ ] Ejecutar `test_rubric_scorer.py`
   - [ ] Ejecutar `test_docker_runner.py`

3. **Mejorar coverage**:
   - [ ] Ejecutar coverage report
   - [ ] Identificar código no cubierto
   - [ ] Agregar tests faltantes si coverage <80%

4. **Linting y formateo**:
   - [ ] Ejecutar Black en todo el código
   - [ ] Ejecutar isort en todo el código
   - [ ] Arreglar errores de flake8
   - [ ] Opcional: Ejecutar mypy y arreglar type hints

5. **Pre-commit hooks**:
   - [ ] Instalar pre-commit hooks
   - [ ] Probar que funcionen en un commit
   - [ ] Documentar workflow para desarrolladores

## 💡 Buenas Prácticas

### Escribir Nuevos Tests

```python
# backend/tests/test_my_service.py
import pytest
from backend.services.my_service import MyService

class TestMyService:
    """Test cases for MyService"""

    def test_something(self, test_db):
        """Test description"""
        service = MyService()
        result = service.do_something()

        assert result is not None
        assert result.property == expected_value
```

### Usar Fixtures

```python
@pytest.fixture
def sample_data():
    """Fixture description"""
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"
```

### Monkeypatch para Servicios

```python
def test_with_custom_dir(mock_problem_dir, monkeypatch):
    service = ProblemService()
    monkeypatch.setattr(service, 'problems_dir', mock_problem_dir)
    # Now service uses mock_problem_dir instead of real one
```

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Black Documentation](https://black.readthedocs.io/)
- [flake8 Documentation](https://flake8.pycqa.org/)
- [pre-commit Documentation](https://pre-commit.com/)

## 🎯 Próximos Pasos

Una vez que los tests pasen y el coverage sea >80%:

1. **Documentar** los resultados en REFACTORING_COMPLETE.md
2. **Actualizar** CLAUDE.md con estado de Fase 3
3. **Considerar** CI/CD pipeline (GitHub Actions) para ejecutar tests automáticamente
4. **Considerar** badges de coverage y build status en README

---

**Última actualización**: 23 Oct 2025
**Autor**: Claude Code
**Estado**: Fase 3 en progreso - 47% completado (tests creados, linting configurado, tests ejecutándose)
