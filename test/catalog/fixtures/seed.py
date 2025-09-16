import pytest


articles = []


@pytest.fixture(scope="session")
def get_all_articles():
    """Fixture pour récupérer tous les articles"""
    return articles
