from pydantic import BaseModel, Field


class ProsConsResponse(BaseModel):
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)