"""
Vercel Serverless Function Entry Point for PlacementPilot FastAPI backend.
Vercel inspects the root api/ directory and routes requests to the exposed ASGI `app`.
"""
import os
import sys

# Ensure backend root is discoverable in Python's import search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app
from mangum import Mangum

# Handler for AWS Lambda / Vercel Serverless
handler = Mangum(app, lifespan="off")

