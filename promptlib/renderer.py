from typing import Dict, Any
from promptlib.schema import YAML

"""
This file is responsible for taking the schema prompt and actually
putting it in a proper template for the LLM. In the future, need to
consider adding smart handling for LLM API choice. But for now we 
will mainly deal with one API model which is Llama 3.1b for now. Later,
I need to be able to support multiple LLMs as each of them have different
docs and adapters.
"""

class PromptRenderer:
    def __init__(self, prompt: YAML):
        self.prompt = prompt

    def validate_inputs(self, user_inputs: Dict) -> Dict:
        # Check required, add defaults
        complete_inputs = {}
        
        # Check required inputs
        for key, field in self.prompt.inputs.items():
            if field.required and key not in user_inputs:
                raise ValueError(f"Required input '{key}' not provided")
        
        # Add provided inputs and defaults
        for key, field in self.prompt.inputs.items():
            if key in user_inputs:
                complete_inputs[key] = user_inputs[key]
            elif not field.required and field.default is not None:
                complete_inputs[key] = field.default
        
        return complete_inputs

    def render_user_prompt(self, user_inputs: Dict[str, Any]) -> str:
        """
        Render the user prompt template with provided inputs.
        """
        complete_inputs = self.validate_inputs(user_inputs)
        
        # Convert {{variable}} to {variable} and format
        template = self.prompt.user_prompt_template.replace('{{', '{').replace('}}', '}')

        try:
            return template.format(**complete_inputs)
        except KeyError as e:
            raise ValueError(f"Template variable {e} not found in inputs")

    def render_full_prompt(self, user_inputs: Dict[str, Any]) -> str:
        """
        Render the complete prompt (system + user).
        """
        user_prompt = self.render_user_prompt(user_inputs)
        return f"{self.prompt.system_prompt}{user_prompt}"

    def to_groq_format(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get it into groq, or Llama 3.1 8b format cuz it's free ¯\_(ツ)_/¯
        """

        pass

    def to_openai_format(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def to_api_request(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Choosing the right API format based on the provider chosen by
        the user.

        User needs to specify the following in their yml file:
        - provider (e.g., openai, anthropic)
        - model (e.g., gpt-4o-mini)
        - temperature & max_tokens
        """
        provider = self.prompt.model.provider.lower()

        if provider == "openai":
            return self.to_openai_format(user_inputs)
        elif provider == "groq":
            return self.to_groq_format(user_inputs)

    def get_metadata(self) -> Dict[str, Any]:
        """
        Getting the metadata for logging and tracking purposes.
        """
        return {
            "prompt_id": self.prompt.prompt_id,
            "version": self.prompt.version,
            "status": self.prompt.status,
            "owner": self.prompt.owner,
            "tags": self.prompt.owner,
            "provider": self.prompt.model.provider,
            "model": self.prompt.model.name
        }
