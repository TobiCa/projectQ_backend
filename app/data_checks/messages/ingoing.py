from pydantic import BaseModel, Field

class IngoingMessage(BaseModel):
    """
    Represents a message for ingoing data checks.
    """
    user_id: str
    content: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": "user123",  # Fixed field name
                "content": "This is an example ingoing message."
            }
        }
