from typing import Optional
from pydantic import BaseModel
from agent.domain.constants.domain_constants import DEFAULT_MAX_NUMBER_RETRIEVER_DOCUMENTS
from commons.domain.utils.utils import generate_uuid

class ChatDocumentoInfoRequest(BaseModel):
    question: str
    max_documents: Optional[int] = DEFAULT_MAX_NUMBER_RETRIEVER_DOCUMENTS
    conversation_id: Optional[str] = generate_uuid()
    session_id: str