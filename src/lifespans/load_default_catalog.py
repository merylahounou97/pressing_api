import csv

from src.catalog.catalog_enums import ArticleCategoryEnum, ArticleFreqEnum, ArticleStatusEnum
from src.catalog.catalog_model import ArticleModel


def load_default_catalog_fun(db):
    """Load the default catalog from csv file"""
    totalArticles = db.query(ArticleModel).count()
    if totalArticles == 0:
        colunms = ["id",
                "code",
                "name",
                "details",
                "category",
                "price","status","freq","description","express_price",
                ]   
        with open("src/catalog/seed/catalog.csv",encoding="utf-8-sig") as articles_file:
            articles = csv.DictReader(articles_file,delimiter=";",dialect="excel", strict=True)
            articles.fieldnames = colunms   
            for article in articles:
                if articles.line_num > 1:
                    article["id"] = str(article["id"])
                    article["price"] = int(article["price"].replace(' ',''))
                    article["express_price"] = int(article["express_price"].replace(' ',''))
                    for key in ["category","status","freq"]:
                        if article[key] == "":
                            article[key] = "NONE"
                    article["category"] = ArticleCategoryEnum(article["category"].replace(' ','').upper())
                    article["status"] = ArticleStatusEnum(article["status"].replace('é','e').upper())
                    article["freq"] = ArticleFreqEnum(article["freq"].replace('é','e').upper())
                    article_mod = ArticleModel(**article)
                    db.add(article_mod)
            db.commit()