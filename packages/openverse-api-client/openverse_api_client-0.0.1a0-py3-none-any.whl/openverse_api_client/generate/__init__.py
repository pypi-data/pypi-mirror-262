from pathlib import Path

from openverse_api_client.generate.python import generate_python
from openverse_api_client.generate.typescript import generate_typescript

def generate():
    python_files = generate_python()
    typescript_files = generate_typescript()

    python_out = Path(__file__).parents[1]
    typescript_out = Path(__file__).parents[3] / "packages" / "openverse-api-client" / "src"

    for file, source in python_files.items():
        path = python_out / file
        path.unlink(missing_ok=True)
        path.write_text(source)
    
    for file, source in typescript_files.items():
        path = typescript_out / file
        path.unlink(missing_ok=True)
        path.write_text(source)
