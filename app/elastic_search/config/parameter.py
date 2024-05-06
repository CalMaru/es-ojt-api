from typing import Optional

from pydantic import BaseModel


class AutocompleteParams(BaseModel):
    sources: list[str]
    should: list[dict]
    sort: Optional[list[dict]]

    @classmethod
    def from_reporter(cls, query: str, query_jamo: str):
        should = [
            {"prefix": {"item": query}},
            {"term": {"nameJamoNGram": query_jamo}},
            {"term": {"nameJamoNGramEdge": query_jamo}},
            {"term": {"nameJamoNGramEdgeBack": query_jamo}},
        ]
        return cls(sources=["name"], should=should, sort=None)
