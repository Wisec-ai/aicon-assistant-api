
from typing import List, Any, Optional
from agent.domain.constants.domain_constants import DEFAULT_MAX_NUMBER_RETRIEVER_DOCUMENTS
from commons.domain.constants.env_variables import PROJECT_ID, DATA_STORE_LOCATION, DATA_STORE_ID
from commons.domain.constants.exceptions import InternalServerException
from langchain_google_community import VertexAISearchRetriever

class AiRetriver:
    def __init__(self, max_documents: Optional[int]):
        self.retriever = self._define_retriver(max_documents)
        print(f"{self.retriever}")
        print(f"PROJECT_ID {PROJECT_ID}, DATA_STORE_LOCATION {DATA_STORE_LOCATION}, DATA_STORE_ID {DATA_STORE_ID} ")

    def _define_retriver(
                        self, 
                        max_documents: Optional[int] = DEFAULT_MAX_NUMBER_RETRIEVER_DOCUMENTS,
                        enable_extract_answers: bool = False) -> VertexAISearchRetriever:
        return VertexAISearchRetriever(
            project_id=PROJECT_ID,
            location_id=DATA_STORE_LOCATION,
            data_store_id=DATA_STORE_ID,
            get_extractive_answers=False,
            max_documents=max_documents,
        )

    def invoke(self, query: str) -> List[Any]:
        try:
            result_invoke = self.retriever.invoke(query)
            return result_invoke
        except Exception as error:
            print(f"Error ExceptionInvoke {error}")
            raise InternalServerException(f"{error}")
        
    def get_few_examples(self, query: str) -> str:
        documents = self.invoke(f"${query}")
        
        examples_list = [
            f"Documentos {index}:\n{document.page_content}"
            for index, document in enumerate(documents)
        ]

        return "\n\n".join(examples_list)