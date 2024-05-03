from typing import Optional

from pydantic import BaseModel


class AutocompleteParams(BaseModel):
    sources: Optional[list[str]]
    key: str
    value: str
    sort: Optional[list[dict]]
