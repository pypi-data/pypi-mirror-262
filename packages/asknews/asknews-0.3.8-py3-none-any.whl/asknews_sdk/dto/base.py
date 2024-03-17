from typing import ClassVar
from pydantic import BaseModel


class BaseSchema(BaseModel):
    __content_type__: ClassVar[str] = "application/json"
