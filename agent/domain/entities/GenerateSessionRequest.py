from pydantic import BaseModel

class GenerateSessionRequest(BaseModel):
    email: str