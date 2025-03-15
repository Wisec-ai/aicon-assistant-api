from typing import Optional, Dict
from commons.domain.utils.utils import get_current_str_datetime

class TransformerSystemInstruction:
    def __init__(
                    self, system_instruction: str,
                      document_exampels: str, additional_params: Optional[Dict[str,str]]=None):
        self.document_exampels = document_exampels
        self.additional_params = additional_params
        self.system_instruction = system_instruction
        self.default_params = {
            "few_examples": self.few_examples,
            "current_datetime":  get_current_str_datetime()
        }
        pass

    def generate_system_instruction(self):
        update_system_instruction = self.system_instruction
        
        params_to_update = {} if self.additional_params is None else self.additional_params
        params_to_update = {
            **params_to_update,
            **self.default_params
        }

        for param in params_to_update.keys():
            update_system_instruction = update_system_instruction.replace(f"{{{param}}}", params_to_update[param])
        
        return update_system_instruction