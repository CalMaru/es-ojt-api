from pydantic import BaseModel

from app.model.dto.category_dto import NewsCategories
from app.model.dto.provider_dto import NewsProviders


class GetOptionsResponse(BaseModel):
    categories: NewsCategories
    providers: NewsProviders

    @classmethod
    def from_options(cls, categories: NewsCategories, providers: NewsProviders):
        return cls(
            categories=categories,
            providers=providers,
        )
