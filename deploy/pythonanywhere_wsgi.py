"""
Template WSGI per PythonAnywhere.

Copia questo contenuto nel file WSGI della tua web app PythonAnywhere
e sostituisci USERNAME, CHANGE_ME_SECRET e CHANGE_ME_PASSWORD.
"""

import os
import sys

USERNAME = "Veyoy"
PROJECT_DIR = f"/home/{USERNAME}/appstudio"

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault("SECRET_KEY", "CHANGE_ME_SECRET")
os.environ.setdefault("APP_PASSWORD", "CHANGE_ME_PASSWORD")
os.environ.setdefault(
    "PROGRESS_DB_PATH",
    os.path.join(PROJECT_DIR, "instance", "user_progress.db"),
)
os.environ.setdefault(
    "SOURCE_DB_PATH",
    os.path.join(PROJECT_DIR, "data", "study_sources.db"),
)
os.environ.setdefault(
    "TUTORIAL_PATH",
    os.path.join(PROJECT_DIR, "data", "python_tutorial.json"),
)

from app import app as application  # noqa: E402
