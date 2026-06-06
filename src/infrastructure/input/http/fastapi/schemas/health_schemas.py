from pydantic import BaseModel


class HealthResponseSchema(BaseModel):
    status: str
    version: str
    timestamp: str
