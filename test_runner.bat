@echo off
cd /d "c:\2025Desarrollo\Los cortez\La Mendoza\python-playground-mvp"
docker run --rm -v "%cd%\backend\problems\sumatoria:/workspace:rw" -w //workspace py-playground-runner:latest sh -c "echo 'def suma(a,b): return a+b' > student_code.py && ls -la && pytest -v tests_public.py"
