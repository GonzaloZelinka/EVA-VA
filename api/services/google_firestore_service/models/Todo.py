from datetime import datetime, timezone
from pydantic import BaseModel, Field

from api.config import Config


class Todo(BaseModel):
    task: str = Field(..., title="The title of the todo")
    completed: bool = Field(False, title="The status of the todo")
    date: datetime = Field(..., title="The date and time of the todo")
    createdAt: datetime = Field(
        datetime.now(timezone.utc), title="The date and time the todo was created"
    )
    updatedAt: datetime = Field(
        datetime.now(timezone.utc), title="The date and time the todo was last updated"
    )
    createdBy: str = Field(Config.USER_ID, title="The user id of the todo")
