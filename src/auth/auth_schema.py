from pydantic import BaseModel


class LoginForm(BaseModel):
    """Modèle de données pour la connexion
    Attributes:
        identifier (str): Identifiant de connexion
        password (str): Mot de passe
    """

    identifier: str
    password: str


class Token(BaseModel):
    """Modèle de token
    Attributes:
        access_token (str): Token d'accès
        token_type (str): Type de token
    """

    access_token: str
    token_type: str
