from enum import Enum
class ArticleSpecificityEnum(Enum):
    """Enum for the specificity of an article"""

    NONE = "none"
    BEBE = "bebe"
    ENFANT = "enfant"
    REPASSAGE = "repassage"
    EXPRESS = "express"
    # values = [NONE, BEBE, ENFANT, REPASSAGE, EXPRESS]

class ArticleCategoryEnum(Enum):
    """Enum for the category of an article"""

    NONE = ""
    HOMME = "homme"
    FEMME = "femme"
    UNISEX = "unisex"
    MAISON = "maison"
    # values = [NONE, HOMME, FEMME, UNISEX, MAISON]

class ArticleStatusEnum(Enum):
    """Enum for the status of an article"""
    NONE = ""
    INCHANGE = "inchange"
    REVU = "revu"
    NOUVEAU = "nouveau"
    # values = [NONE, INCHANGE, REVU, NOUVEAU]

class ArticleFreqEnum(Enum):
    """Enum for the frequency of an article"""
    NONE = ""
    RARE = "rare"
    FREQUENT = "frequent"
    # values = [NONE, RARE, FREQUENT]

