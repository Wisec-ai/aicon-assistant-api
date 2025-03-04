from pydantic import BaseModel

class DocumentInfo(BaseModel):
    company_id: str
    file_name: str