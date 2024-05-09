from pydantic import BaseModel


class AutocompleteResponse(BaseModel):
    suggestions: list[str]

    @classmethod
    def from_hits(cls, hits: dict, item: str):
        return cls(
            suggestions=[hit["_source"][item] for hit in hits],
        )
