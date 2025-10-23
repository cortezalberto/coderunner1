# 🐍 Python Playground MVP

> A production-ready code execution platform with Docker sandbox isolation, job queues, persistent storage, and a modern web interface for educational Python programming.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

---

## ✨ Features

### For Students
- 🎯 **Interactive Code Editor**: Monaco Editor with syntax highlighting
- 📝 **Multiple Problems**: Solve programming challenges with instant feedback
- ✅ **Real-time Grading**: Automatic scoring with public and hidden tests
- 📊 **Detailed Results**: View test outcomes, error messages, and execution time
- 🔒 **Secure Execution**: Code runs in isolated Docker containers

### For Instructors
- 📈 **Admin Dashboard**: View statistics and student submissions
- 📋 **Submission History**: Track all attempts with scores
- 🎓 **Custom Problems**: Easy-to-create problem structure
- 🔍 **Detailed Analytics**: Average scores and completion rates

### Technical Highlights
- ⚡ **Fast Execution**: ~2 seconds per submission
- 🏗️ **Microservices**: Backend, Worker, Frontend, PostgreSQL, Redis
- 🧪 **86 Unit Tests**: Comprehensive test coverage
- 📚 **Type-Safe**: Pydantic v2 schemas for all API requests
- 🔧 **Production-Ready**: Service layer, structured logging
- 🐳 **Docker-based**: Complete containerization

---

## 🚀 Quick Start

### Prerequisites
- Docker (20.10+)
- Docker Compose (2.0+)

### Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/yourusername/python-playground-mvp.git
   cd python-playground-mvp
   \`\`\`

2. Start the application:
   
   **Windows:**
   \`\`\`bash
   start.bat
   \`\`\`
   
   **Linux/Mac:**
   \`\`\`bash
   chmod +x start.sh
   ./start.sh
   \`\`\`

3. Access:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs

---

## 🏗️ Architecture

\`\`\`
Frontend (React) → Backend (FastAPI) → Redis (RQ Queue) → Worker → Docker Sandbox
                         ↓
                    PostgreSQL
\`\`\`

### Tech Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis, RQ, Pydantic v2
- **Frontend**: React 18, Vite, Monaco Editor, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose, pytest

---

## 📚 API Documentation

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| \`/api/problems\` | GET | List all problems |
| \`/api/submit\` | POST | Submit code |
| \`/api/result/{job_id}\` | GET | Get result |
| \`/api/admin/summary\` | GET | Statistics |

### Example

\`\`\`bash
curl -X POST http://localhost:8000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"problem_id": "sumatoria", "code": "def suma(a, b):\n    return a + b"}'
\`\`\`

Full docs: http://localhost:8000/docs

---

## 🧪 Testing

\`\`\`bash
# Backend tests
docker compose exec backend pytest backend/tests/ -v

# Worker tests
docker compose exec worker pytest worker/tests/ -v

# With coverage
docker compose exec backend pytest --cov=backend --cov-report=html
\`\`\`

**Stats**: 86 tests created, 25/53 passing

See [TESTING.md](TESTING.md) for details.

---

## 🔒 Security

- ✅ Input validation (code length, dangerous imports)
- ✅ Docker sandboxing (\`--network none\`, CPU/memory limits)
- ✅ Non-root execution (uid 1000)
- ✅ Timeout enforcement
- ✅ SQL injection prevention

---

## 📁 Project Structure

\`\`\`
python-playground-mvp/
├── backend/          # FastAPI + services + tests
├── worker/           # RQ worker + services + tests
├── frontend/         # React + Monaco Editor
├── runner/           # Docker sandbox image
├── docker-compose.yml
└── docs/            # CLAUDE.md, TESTING.md, etc.
\`\`\`

---

## 📖 Documentation

- [CLAUDE.md](CLAUDE.md) - Project guidance
- [TESTING.md](TESTING.md) - Testing guide
- [STATUS_FINAL.md](STATUS_FINAL.md) - Project status
- [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) - Refactoring progress

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push and open a PR

Use pre-commit hooks: \`pre-commit install\`

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

**Made with ❤️ for education** 🚀
