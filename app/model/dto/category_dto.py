from pydantic import BaseModel

"""
DTO
"""


class Category(BaseModel):
    name: str
    types: str


"""
Response
"""


class CategoryListResponse(BaseModel):
    categories: list[Category]
