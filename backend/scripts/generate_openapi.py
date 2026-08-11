# scripts/generate_openapi.py
import json
from pathlib import Path
from app.main import create_app

app = create_app()

openapi_schema = app.openapi()

output_path = Path(__file__).resolve().parent.parent / "openapi.json"
output_path.write_text(json.dumps(openapi_schema, indent=2), encoding="utf-8")

print(f"OpenAPI schema written to: {output_path}")