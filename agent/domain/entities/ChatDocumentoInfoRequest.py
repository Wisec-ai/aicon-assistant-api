from typing import Optional
from pydantic import BaseModel
from agent.domain.constants.domain_constants import DEFAULT_MAX_NUMBER_RETRIEVER_DOCUMENTS

class ChatDocumentoInfoRequest(BaseModel):
    question: str
    max_documents: Optional[int] = DEFAULT_MAX_NUMBER_RETRIEVER_DOCUMENTS