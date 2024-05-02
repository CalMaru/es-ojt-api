from pydantic import BaseModel

"""
DTO
"""


class Category(BaseModel):
    major: str
    minor: str


"""
Response
"""


class CategoryListResponse(BaseModel):
    categories: list[Category]
