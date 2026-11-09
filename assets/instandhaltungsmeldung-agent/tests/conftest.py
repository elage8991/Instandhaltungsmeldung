"""Local conftest for tests/ — ensures app/ is on sys.path for all agent tests."""
import pytest


@pytest.fixture(autouse=True)
def _add_app_to_path(add_agent_to_path):
    """Auto-use the root add_agent_to_path fixture for every test in tests/."""
    yield
