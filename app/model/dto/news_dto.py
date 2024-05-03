from pydantic import BaseModel


class News(BaseModel):
    news_id: str
    provider: str
    date: str
    title: str
    content: str

    @classmethod
    def from_hit(cls, hit: dict):
        source = hit["_source"]
        highlight = hit["highlight"]

        title = highlight.get("title", source["title"])
        content = highlight.get("content", source["content"])

        return cls(
            news_id=hit["_id"],
            provider=source["provider"],
            date=source["date"],
            title=title,
            content=content,
        )
