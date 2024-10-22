from pydantic import BaseModel, Field, computed_field


class ArticleCreateInputSchema(BaseModel):
    code: str
    name: str
    description: str
    price: float
    express_price: float


class ArticleEditInputSchema(BaseModel):
    code: str = Field(default=None)
    name: str = Field(default=None)
    description: str = Field(default=None)
    price: float = Field(default=None)
    express_price: float = Field(default=None)


class ArticleOutputSchema(ArticleCreateInputSchema):
    id: int
    
    @computed_field
    @property
    def price_discount_5(self)->int:
        return  int(self.price * 0.95)
    
    @computed_field
    @property
    def price_discount_7(self)->int:
        return int(self.price * 0.93)
    
    @computed_field
    @property
    def price_discount_10(self)->int:
        return int(self.price * 0.90)

