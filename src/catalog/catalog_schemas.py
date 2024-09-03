from pydantic import BaseModel, computed_field


class ArticleCreateInputSchema(BaseModel):
    code: str
    name: str
    description: str
    price: float
    express_price: float


class ArticleOutputSchema(ArticleCreateInputSchema):
    id: str
""" 
    @computed_field
    @property
    def price_discount_5(self):
        return self.price * 0.95
    
    @computed_field
    @property
    def price_discount_7(self):
        return self.price * 0.93
    
    @computed_field
    @property
    def price_discount_10(self):
        return self.price * 0.90
 """