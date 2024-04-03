from datetime import datetime, timezone
from pydantic import BaseModel, Field
from api.config import Config


class Error(BaseModel):
    message: str = Field(..., title="The error message")
    code: int = Field(..., title="The error code")
    details: str = Field(..., title="The error details")
    initialRequestText: str = Field(None, title="The initial request")
    initialRequestType: str = Field(None, title="The initial request type")
    createdBy: str = Field(Config.USER_ID, title="The user who created the error")
    createdAt: datetime = Field(
        datetime.now(timezone.utc), title="The date and time the error was created"
    )
    updatedAt: datetime = Field(
        datetime.now(timezone.utc), title="The date and time the error was last updated"
    )
