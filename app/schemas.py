from typing import Any

from pydantic import BaseModel, field_validator


class PostCreate(BaseModel):
    title: str
    content: str
    author: str


class PostReplace(BaseModel):
    title: str
    content: str
    author: str


class PostPatch(BaseModel):
    title: str | None = None
    content: str | None = None
    author: str | None = None

    @field_validator("title", "content", "author")
    @classmethod
    def reject_null(cls, value: Any) -> Any:
        if value is None:
            raise ValueError("must not be null; omit the field to leave it unchanged")
        return value


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author: str
