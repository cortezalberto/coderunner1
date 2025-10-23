@echo off
echo 🐍 Python Playground Suite - Starting...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Build runner image
echo 📦 Building sandbox runner image...
docker build -t py-playground-runner:latest ./runner
if errorlevel 1 (
    echo ❌ Failed to build runner image
    pause
    exit /b 1
)
echo ✅ Runner image built
echo.

REM Start services
echo 🚀 Starting all services with Docker Compose...
docker compose up --build

pause
