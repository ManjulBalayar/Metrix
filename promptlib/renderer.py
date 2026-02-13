
"""
This file is responsible for taking the schema prompt and actually
putting it in a proper template for the LLM. In the future, need to
consider adding smart handling for LLM API choice. But for now we 
will mainly deal with one API model which is Llama 3.1b for now. Later,
I need to be able to support multiple LLMs as each of them have different
docs and adapters.
"""

class PrompRenderer:
    def __init__(self, prompt: YAML):
        self.prompt = prompt

    def validate_inputs(self, user_inputs: Dict) -> Dict:
        # Check required, add defaults
        pass

    def format_prompt(self, user_inputs: Dict) -> str:
        # Replace {{}} with {}, format template
        pass
    
    def to_api_request(self, user_inputs: Dict) -> Dict:
        # Build API paylod
        pass
