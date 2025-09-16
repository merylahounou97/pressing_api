from enum import Enum


class ArticleSpecificityEnum(Enum):
    """Enum for the specificity of an article"""

    NONE = "NONE"
    BEBE = "BEBE"
    ENFANT = "ENFANT"
    REPASSAGE = "REPASSAGE"
    EXPRESS = "EXPRESS"
    # values = [NONE, BEBE, ENFANT, REPASSAGE, EXPRESS]


class ArticleCategoryEnum(Enum):
    """Enum for the category of an article"""

    NONE = "NONE"
    HOMME = "HOMME"
    FEMME = "FEMME"
    UNISEX = "UNISEX"
    MAISON = "MAISON"
    # values = [NONE, HOMME, FEMME, UNISEX, MAISON]


class ArticleStatusEnum(Enum):
    """Enum for the status of an article"""

    NONE = "NONE"
    INCHANGE = "INCHANGE"
    REVU = "REVU"
    NOUVEAU = "NOUVEAU"
    # values = [NONE, INCHANGE, REVU, NOUVEAU]


class ArticleFreqEnum(Enum):
    """Enum for the frequency of an article"""

    NONE = "NONE"
    RARE = "RARE"
    FREQUENT = "FREQUENT"
    # values = [NONE, RARE, FREQUENT]
