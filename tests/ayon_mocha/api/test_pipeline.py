"""Tests for the pipeline API."""
import sys
from unittest.mock import MagicMock

import pytest


class Project:
    notes: str = ""


def get_current_project():
    return Project()

@pytest.fixture
def mock_mocha_project_api(monkeypatch):
    """Mock the Mocha Pro API."""
    sys.modules["mocha.projects"] = MagicMock()
    monkeypatch.setattr(sys.modules,
        "mocha.project.get_current_project", get_current_project)
    monkeypatch.setattr(sys.modules,
        "mocha.project.Project", Project)

def test_get_ayon_data(mock_mocha_project_api):
    """Test getting AYON data."""
    sys.modules["ayon_core.tools.utils"] = MagicMock()
    from ayon_mocha.api import MochaProHost
    host = MochaProHost()
    assert host.get_ayon_data() == 1
