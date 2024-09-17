from unittest.mock import MagicMock

import pytest

@pytest.fixture(scope="session")
def mock_db_session():
    """Fixture pour simuler une session de base de données"""
    return MagicMock()