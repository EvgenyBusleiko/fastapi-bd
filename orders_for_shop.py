from pydantic import BaseModel, Field
from  datetime import date

class OrderIn(BaseModel):
    user_id: int = Field()
    good_id: int = Field()
    order_date: date = Field()
    order_status: str = Field(min_length=5)


class Order(OrderIn):
    id: int