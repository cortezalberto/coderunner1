"""
Script to add generic 4-level hints to all problems that don't have them.
"""
import json
import pathlib

PROBLEMS_DIR = pathlib.Path("backend/problems")

# Generic hints that work for most problems
GENERIC_HINTS = [
    "Lee cuidadosamente el enunciado del problema y identifica qué datos necesitas leer con input().",
    "Recuerda que debes crear una función main() que contenga toda tu lógica. Usa print() para mostrar el resultado.",
    "Revisa el código starter provisto. Completa la sección TODO con la lógica necesaria según el enunciado.",
    "Asegúrate de seguir el formato de salida exacto que pide el problema. Revisa los ejemplos de entrada/salida."
]

def add_hints_to_problem(problem_dir: pathlib.Path):
    """Add hints to a problem's metadata.json if it doesn't have them"""
    metadata_path = problem_dir / "metadata.json"

    if not metadata_path.exists():
        print(f"[SKIP] {problem_dir.name}: no metadata.json found")
        return False

    # Load existing metadata
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    # Check if hints already exist
    if 'hints' in metadata and metadata['hints']:
        print(f"[SKIP] {problem_dir.name}: already has hints ({len(metadata['hints'])} hints)")
        return False

    # Add generic hints
    metadata['hints'] = GENERIC_HINTS

    # Write back with pretty formatting
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"[ADDED] {problem_dir.name}: added 4 generic hints")
    return True

def main():
    """Process all problems"""
    if not PROBLEMS_DIR.exists():
        print(f"[ERROR] Problems directory not found: {PROBLEMS_DIR}")
        return

    print(f"Scanning problems in {PROBLEMS_DIR}...\n")

    updated_count = 0
    skipped_count = 0

    # Get all problem directories
    problem_dirs = sorted([d for d in PROBLEMS_DIR.iterdir() if d.is_dir()])

    for problem_dir in problem_dirs:
        if add_hints_to_problem(problem_dir):
            updated_count += 1
        else:
            skipped_count += 1

    print(f"\n{'='*60}")
    print(f"Updated: {updated_count} problems")
    print(f"Skipped: {skipped_count} problems (already have hints or no metadata)")
    print(f"Total: {len(problem_dirs)} problems")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
