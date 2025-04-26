from pydantic import BaseModel


class MessageResponse(BaseModel):
    """
    Scheme for simple message response
    """

    message: str
