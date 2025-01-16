"""Tests for the pipeline API."""
import sys
from unittest.mock import MagicMock

import pytest


class Project:
    """Mock Mocha Pro project."""
    notes: str = ""


def get_current_project() -> Project:
    """Mock the get_current_project function."""
    return Project()

@pytest.fixture
def mock_mocha_project_api(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock the Mocha Pro API."""
    """Mock the Mocha Pro API."""
    sys.modules["mocha.projects"] = MagicMock()
    monkeypatch.setattr(sys.modules,
        "mocha.project.get_current_project", get_current_project)
    monkeypatch.setattr(sys.modules,
        "mocha.project.Project", Project)

def test_get_ayon_data(mock_mocha_project_api: None) -> None: # noqa: ARG001
    """Test getting AYON data."""
    sys.modules["ayon_core.tools.utils"] = MagicMock()
    from ayon_mocha.api import MochaProHost
    host = MochaProHost()
    assert host.get_ayon_data() == 1
