

class OrderModel(BaseModel):
    id: str
    date: datetime
    num_command: str
    type_command: TypeCommandEnum
    customer_id: str
    collect: bool
    delivery: bool
    code_article: str
    details_article: str
    specificity: str
    coef_1: int
    coef_2: int
    cat_remise: int
    quantity: int
    number_of_pieces: int
    cintre: int
    delivery_unit: int
    delivery_amount: int
    touch_ups: int
    discount: float


class OrderCreateOutputSchema(OrderCreateInputSchema):
    delivery_date: datetime
    payment_due: float
    customer_name: str
    client_status: str
    subscription: str
    distance: float
    Price: float
    Price_discount: float
    delivery_price: float
    total_before_discount: float
    total_after_discount: float
    total_net: float

