from unittest.mock import MagicMock
import pytest

@pytest.fixture
def mock_db_session():
    """Fixture pour simuler une session de base de données"""
    return MagicMock()