from commons.domain.repository.generative_model import LlmGenerativeModel

class ResponseQuestion:

    def __init__(self):
        self.flash_model = None
        self.robust_model = None

    def __set_flash_model(self, flash_model):
        self.flash_model = flash_model
    
    def __set_robust_model(self, robust_model):
        self.robust_model = robust_model
    
    def generate_async_response_by_question(
        self,
        system_instruction: str,
        question: str
    ):
        generative_model = LlmGenerativeModel(system_instruction=system_instruction)
        self.__set_robust_model(generative_model)

        iterator_response_llm_model = generative_model.generate_content(
            query = question,
            generation_config= generative_model._get_default_generation_config(),
            safety_settings= generative_model._get_default_satey_settings(),
        )

        return iterator_response_llm_model