import vertexai
from enum import Enum
from typing import List, Optional, Any, Dict
from vertexai.generative_models import GenerativeModel, SafetySetting
from commons.domain.constants.env_variables import PROJECT_ID, REGION
from commons.domain.constants.domain_constants import LLM_DEFAULT_CONFIG

class LlEnumModel(Enum):
    BASIC_001 = "gemini-1.5-flash-002"
    PRO_001 = "gemini-1.5-pro-002"

class LlmGenerativeModel:
    def __init__(   self, 
                    system_instruction: Optional[str] = None, 
                    type_model: Optional[str] = LlEnumModel.PRO_001.value
                ):
        self.model = self._define_model(system_instruction, type_model)
        pass
    
    def _define_model(
                        self,
                        system_instruction: Optional[str] = None,
                        type_model: Optional[str] = LlEnumModel.PRO_001.value
                    ):

        vertexai.init(project=PROJECT_ID, location=REGION)
        if(system_instruction is not None):

            return GenerativeModel(
                type_model,
                system_instruction=[system_instruction]
            )
        return GenerativeModel(
                type_model
        )

    def set_model(self, model: GenerativeModel) -> None:
        self.model = model

    def _get_default_generation_config(self) -> Dict[str, Any]:
        return LLM_DEFAULT_CONFIG
    
    def generate_content(self, query: str = '',
                                generation_config: Optional[Dict[str, Any]] = None,
                                safety_settings: Optional[List[Any]] = None,
                                enable_stream: bool = True ) -> Any:
        generated_content = self.model.generate_content(
                        [query],
                        generation_config=generation_config,
                        safety_settings=safety_settings,
                        stream=enable_stream
                        )
        return generated_content

    def get_text_from_iterator(self, iterator_response) -> str:
        llm_text_response = ""
        for response in iterator_response:
            text_response = response.text
            llm_text_response = llm_text_response +  f"{text_response}"  
        return llm_text_response

    def get_text_from_content(self, content_response) -> str:
        return content_response.candidates[0].content.parts[0].text

    def _get_default_satey_settings(self) -> List[Any]:
        return [
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
        ] 
