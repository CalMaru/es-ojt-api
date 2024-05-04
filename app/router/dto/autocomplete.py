from pydantic import BaseModel


class AutocompleteResponse(BaseModel):
    suggestions: list[str]
