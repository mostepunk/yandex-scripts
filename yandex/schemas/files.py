from pydantic import BaseModel


class File(BaseModel):
    content_type: str
    created: str
    etag: str
    isdir: bool
    modified: str
    name: str
    path: str
    size: int
