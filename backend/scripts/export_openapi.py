"""Write the OpenAPI spec of the app to a file, without starting a server.

Usage (in backend/): uv run python -m scripts.export_openapi <output-path>
"""

import json
import sys
from pathlib import Path

from app.main import app

Path(sys.argv[1]).write_text(json.dumps(app.openapi(), indent=2) + "\n", encoding="utf-8")
