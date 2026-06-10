import ast
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path.cwd()
SOURCE_SUFFIXES = {".py", ".ipynb"}
IGNORE_PARTS = {".git", ".venv", "venv", "env", "__pycache__"}


def iter_source_files():
    for path in ROOT.rglob("*"):
        if any(part in IGNORE_PARTS for part in path.parts):
            continue
        if path.suffix in SOURCE_SUFFIXES:
            yield path


def notebook_code(path):
    nb = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in nb.get("cells", [])
        if cell.get("cell_type") == "code"
    )


def read_code(path):
    if path.suffix == ".ipynb":
        return notebook_code(path)
    return path.read_text(encoding="utf-8", errors="ignore")


imports = defaultdict(set)
parse_errors = {}

for path in iter_source_files():
    rel = str(path.relative_to(ROOT))
    code = read_code(path)
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        parse_errors[rel] = str(exc)
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name.split(".")[0]].add(rel)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports[node.module.split(".")[0]].add(rel)

requirements = []
req_path = ROOT / "requirements.txt"
if req_path.exists():
    for line in req_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0]
        requirements.append(name)

package_to_import = {
    "opencv_python": "cv2",
    "Pillow": "PIL",
    "scikit_learn": "sklearn",
    "Unidecode": "unidecode",
}

print("IMPORTS")
for module in sorted(imports):
    print(f"{module}: {', '.join(sorted(imports[module]))}")

print("\nREQUIREMENTS_USAGE")
for package in requirements:
    module = package_to_import.get(package, package.replace("-", "_"))
    files = sorted(imports.get(module, []))
    status = "USED" if files else "NOT_FOUND"
    print(f"{package} -> {module}: {status}" + (f" | {', '.join(files)}" if files else ""))

print("\nPARSE_ERRORS")
for rel, err in parse_errors.items():
    print(f"{rel}: {err}")
