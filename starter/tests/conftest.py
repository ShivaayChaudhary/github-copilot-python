import os
import sys
import random
import pytest

# Ensure project root is importable so tests can `import app`
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app as flask_app

# Seed RNG early so tests that rely on puzzle generation are deterministic
random.seed(0)


@pytest.fixture
def app():
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
