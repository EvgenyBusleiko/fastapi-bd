from pydantic import BaseModel, Field


class GoodsIn(BaseModel):
    name: str = Field(min_length=5)
    discription: str = Field(max_length=128)
    price: float = Field(gt=0)

class Goods(GoodsIn):
    id: int
