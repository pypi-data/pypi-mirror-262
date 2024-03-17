from uuid import UUID

from pydantic import BaseModel


class ResponseData(BaseModel):
    data: dict | None
    error: bool


class BaseRequestData(BaseModel):
    req_id: UUID
    data: dict
