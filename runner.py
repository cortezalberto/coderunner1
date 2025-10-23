import subprocess, tempfile, os, shutil, json, sys, textwrap, signal, pathlib, time
import platform

# NOTA: Este runner es un MVP. En producción, ejecutá esto en un contenedor aislado.
# Establecemos límites aproximados de tiempo/memoria usando "resource" (Linux/Mac).
# En Windows, los límites de recursos no están disponibles.

DEFAULT_TIMEOUT = 2.5  # segundos
DEFAULT_MEM_MB = 128   # MB

# Importar resource solo si está disponible (Linux/Mac)
try:
    import resource
    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False

def _limit_resources(memory_mb: int):
    """Limita recursos del proceso (solo funciona en Linux/Mac)"""
    if not HAS_RESOURCE:
        # Windows no soporta resource, los límites se manejan vía timeout
        return

    # Memoria
    mem_bytes = memory_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
    resource.setrlimit(resource.RLIMIT_DATA, (mem_bytes, mem_bytes))
    # CPU time (suave, por seguridad el timeout de subprocess también corta)
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))

def run_submission(problem_id: str, code: str, timeout_sec=None, memory_mb=None):
    timeout_sec = float(timeout_sec) if timeout_sec else DEFAULT_TIMEOUT
    memory_mb = int(memory_mb) if memory_mb else DEFAULT_MEM_MB

    base = pathlib.Path("problems") / problem_id
    tests_path = base / "tests.py"
    meta_path = base / "metadata.json"

    if not tests_path.exists():
        return {"ok": False, "error": f"tests.py no encontrado para {problem_id}"}

    # Permitir override desde metadata.json
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            timeout_sec = float(meta.get("timeout_sec", timeout_sec))
            memory_mb = int(meta.get("memory_mb", memory_mb))
        except Exception:
            pass

    workdir = tempfile.mkdtemp(prefix=f"play-{problem_id}-")
    try:
        student_file = os.path.join(workdir, "student_code.py")
        with open(student_file, "w", encoding="utf-8") as f:
            f.write(code)

        # Copiar tests.py al workdir
        shutil.copy2(tests_path, os.path.join(workdir, "tests.py"))

        cmd = [sys.executable, "-I", "-B", "-S", "-m", "pytest", "-q", "tests.py"]
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONSAFEPATH"] = "1"

        def preexec():
            # Drop recursos en el proceso hijo
            _limit_resources(memory_mb)

        start = time.time()
        proc = subprocess.Popen(
            cmd,
            cwd=workdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            preexec_fn=preexec if HAS_RESOURCE else None,
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            proc.kill()
            return {
                "ok": False,
                "error": "timeout",
                "timeout_sec": timeout_sec,
                "stdout": "",
                "stderr": "",
            }

        duration = time.time() - start
        # Parse muy simple del output de pytest
        passed = failed = errors = 0
        summary_line = ""
        for line in (stdout.splitlines() + stderr.splitlines()):
            if "failed" in line or "passed" in line or "error" in line:
                summary_line = line.strip()

        # Ejemplos de summary:
        # "3 passed in 0.02s"
        # "1 failed, 2 passed in 0.01s"
        # "2 failed, 1 passed, 1 error in 0.02s"
        tokens = summary_line.replace(",", "").split()
        for i, tok in enumerate(tokens):
            if tok.isdigit():
                n = int(tok)
                if i+1 < len(tokens):
                    kind = tokens[i+1]
                    if kind.startswith("passed"):
                        passed = n
                    elif kind.startswith("failed"):
                        failed = n
                    elif kind.startswith("error"):
                        errors = n

        ok = (proc.returncode == 0)
        return {
            "ok": ok,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "duration_sec": round(duration, 4),
            "stdout": stdout,
            "stderr": stderr,
            "returncode": proc.returncode,
        }
    finally:
        # Mantén los temporales para auditar si querés:
        shutil.rmtree(workdir, ignore_errors=True)
