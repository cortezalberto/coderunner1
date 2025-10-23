from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
from runner import run_submission
import pathlib, json

app = FastAPI(title="Python Playground MVP")

class Submission(BaseModel):
    problem_id: str
    code: str
    # overrides opcionales
    timeout_sec: Optional[float] = None
    memory_mb: Optional[int] = None

@app.get("/api/problems")
def list_problems() -> Dict[str, Any]:
    problems = {}
    pdir = pathlib.Path("problems")
    for pr in pdir.iterdir():
        if pr.is_dir():
            meta_path = pr / "metadata.json"
            prompt_path = pr / "prompt.md"
            meta = {}
            if meta_path.exists():
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
            problems[pr.name] = {"metadata": meta, "prompt": prompt}
    return problems

@app.post("/api/submit")
def submit(sub: Submission):
    result = run_submission(
        problem_id=sub.problem_id,
        code=sub.code,
        timeout_sec=sub.timeout_sec,
        memory_mb=sub.memory_mb
    )
    return result
