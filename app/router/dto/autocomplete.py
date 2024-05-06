from pydantic import BaseModel


class AutocompleteResponse(BaseModel):
    suggestions: list[str]

    @classmethod
    def from_hits(cls, hits: dict):
        return cls(
            suggestions=[hit["_source"]["name"] for hit in hits],
        )
