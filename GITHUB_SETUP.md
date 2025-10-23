# 🚀 Guía para Subir a GitHub

Este documento contiene las instrucciones para subir el proyecto Python Playground MVP a GitHub.

---

## ✅ Estado Actual

El repositorio Git local ya está configurado:
- ✅ Git inicializado
- ✅ .gitignore completo configurado
- ✅ README.md creado
- ✅ Commit inicial realizado (77 archivos, 7,832 líneas)
- ✅ Branch principal renombrado a `main`

**Commit inicial**: `ba6cc95`

---

## 📋 Pasos para Subir a GitHub

### Opción 1: Crear Repositorio Nuevo en GitHub

1. **Ir a GitHub** y crear un nuevo repositorio:
   - URL: https://github.com/new
   - Nombre sugerido: `python-playground-mvp`
   - Descripción: "A production-ready code execution platform for educational Python programming"
   - Visibilidad: Pública o Privada (según prefieras)
   - **NO** inicializar con README, .gitignore, o license (ya los tenemos)

2. **Conectar el repositorio local con GitHub:**

   ```bash
   # Reemplaza 'tu-usuario' con tu nombre de usuario de GitHub
   git remote add origin https://github.com/tu-usuario/python-playground-mvp.git

   # Verificar que el remote fue agregado
   git remote -v
   ```

3. **Subir el código:**

   ```bash
   # Push del branch main
   git push -u origin main
   ```

4. **Verificar** en GitHub que todos los archivos se subieron correctamente.

---

### Opción 2: Usar GitHub CLI (gh)

Si tienes GitHub CLI instalado:

```bash
# Crear repositorio y hacer push automáticamente
gh repo create python-playground-mvp --public --source=. --push

# O para repositorio privado:
gh repo create python-playground-mvp --private --source=. --push
```

---

## 🔑 Autenticación

### Con HTTPS (recomendado para empezar):

GitHub pedirá credenciales. Opciones:

1. **Personal Access Token** (recomendado):
   - Ir a: https://github.com/settings/tokens
   - Generate new token (classic)
   - Seleccionar scopes: `repo` (full control)
   - Copiar el token
   - Usar como contraseña al hacer push

2. **GitHub CLI**:
   ```bash
   gh auth login
   ```

### Con SSH (alternativa):

```bash
# 1. Generar clave SSH (si no tienes una)
ssh-keygen -t ed25519 -C "tu-email@example.com"

# 2. Agregar clave a GitHub
# Copiar la clave pública:
cat ~/.ssh/id_ed25519.pub
# Ir a: https://github.com/settings/keys
# Add SSH key y pegar la clave

# 3. Cambiar remote a SSH
git remote set-url origin git@github.com:tu-usuario/python-playground-mvp.git

# 4. Push
git push -u origin main
```

---

## 📝 Configurar el Repositorio en GitHub

Una vez subido el código:

### 1. Agregar Descripción y Topics

En la página principal del repositorio:
- **Description**: "Production-ready Python code execution platform with Docker sandboxing for education"
- **Topics**: `python`, `fastapi`, `docker`, `education`, `code-execution`, `react`, `postgresql`, `redis`, `pytest`, `playground`

### 2. Configurar About

- **Website**: (Si tienes demo en vivo)
- **Releases**: Crear release v1.0.0 del commit inicial

### 3. Proteger Branch Main (Opcional)

Settings → Branches → Add branch protection rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging (si configuras CI/CD)

### 4. Configurar Issues y Projects (Opcional)

- Habilitar Issues para tracking de bugs y features
- Crear GitHub Project para gestión de tareas

---

## 🎯 Próximos Pasos Sugeridos

### 1. Agregar Badges al README

Editar `README.md` y agregar:

```markdown
[![Build Status](https://github.com/tu-usuario/python-playground-mvp/workflows/Tests/badge.svg)](https://github.com/tu-usuario/python-playground-mvp/actions)
[![Coverage](https://codecov.io/gh/tu-usuario/python-playground-mvp/branch/main/graph/badge.svg)](https://codecov.io/gh/tu-usuario/python-playground-mvp)
```

### 2. Configurar GitHub Actions (CI/CD)

Crear `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: playground
          POSTGRES_PASSWORD: playground
          POSTGRES_DB: playground
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v --cov=backend

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### 3. Agregar LICENSE

Crear archivo `LICENSE` con licencia MIT:

```
MIT License

Copyright (c) 2025 Python Playground Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 4. Crear CONTRIBUTING.md

```markdown
# Contributing to Python Playground MVP

We love your input! We want to make contributing to this project as easy as possible.

## Development Process

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Coding Standards

- Follow PEP 8 for Python code
- Use Black for formatting (line-length=100)
- Write tests for new features
- Update documentation as needed

## Running Tests

\`\`\`bash
docker compose exec backend pytest backend/tests/ -v
docker compose exec worker pytest worker/tests/ -v
\`\`\`

## Pre-commit Hooks

\`\`\`bash
pre-commit install
pre-commit run --all-files
\`\`\`
```

---

## 🔄 Flujo de Trabajo para Commits Futuros

### Hacer Cambios

```bash
# 1. Verificar status
git status

# 2. Agregar archivos modificados
git add archivo1.py archivo2.py
# O agregar todos:
git add .

# 3. Commit con mensaje descriptivo
git commit -m "feat: descripción del cambio"

# 4. Push a GitHub
git push origin main
```

### Convención de Commits (Recomendado)

Usar prefijos para commits:
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bugs
- `docs:` - Cambios en documentación
- `test:` - Agregar o modificar tests
- `refactor:` - Refactorización de código
- `style:` - Cambios de formateo
- `chore:` - Tareas de mantenimiento

Ejemplos:
```bash
git commit -m "feat: add support for Java problems"
git commit -m "fix: resolve Docker timeout issue"
git commit -m "docs: update README with deployment guide"
git commit -m "test: add tests for RubricScorer"
```

---

## 📊 Estadísticas del Repositorio

Una vez subido, el repositorio contendrá:

- **77 archivos**
- **7,832 líneas de código**
- **5 servicios** (Backend, Worker, Frontend, PostgreSQL, Redis)
- **86 tests unitarios**
- **Documentación completa** (README, CLAUDE.md, TESTING.md, etc.)

### Lenguajes:
- Python (~60%)
- JavaScript/React (~25%)
- Markdown (~10%)
- Otros (~5%)

---

## 🎓 Recursos Adicionales

- [GitHub Docs](https://docs.github.com/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)

---

## ✅ Checklist Final

Antes de hacer el repositorio público:

- [ ] README.md completo y claro
- [ ] .gitignore configurado (no subir secrets)
- [ ] LICENSE agregado
- [ ] Documentación actualizada
- [ ] Tests pasando
- [ ] Variables de entorno documentadas en .env.example
- [ ] CONTRIBUTING.md (si aceptas contribuciones)
- [ ] Badges en README (opcional)
- [ ] GitHub Actions configurado (opcional)

---

**¡Tu proyecto está listo para GitHub!** 🚀

Último paso: ejecutar `git push -u origin main` después de configurar el remote.
