from promptlib.loader import load_yml
from promptlib.schema import YAML, ModelConfig, InputField, Output
from pydantic import ValidationError
import json

def main_pipeline(file):
    
    # 1. load yml file
    data = load_yml(file)
    if data is not None:
            print("Successfully loaded the YAML file!")
    else:
        print("Failed to load YAML file")
    
    print("")

    # 2. Check schema format to see if it's valid
    try:
        prompt = YAML(**data)
        print("YAML format is valid!")
        return prompt
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

# Usage
if __name__ == "__main__":
    prompt = main_pipeline("prompts/driveflow_autorename.yml")
    if prompt:
        print(prompt)
        
        """
        Return clear format in JSON. Wanted keys are:
        - prompt_id
        - version
        - provider 
        - model 
        - params: contains temperature & max_tokens
        - messages: system and user prompt
        - output_contract: format of output, rules, etc.

        Only messages & params are sent to the model. Rest is just metadata.
        """
        user_inputs = {
            "ocr_text": "Invoice #12345 - Acme Corp - $500.00",
            "original_filename": "scan_001.pdf"
        }

        template = prompt.user_prompt_template.replace('{{', '{').replace('}}', '}')
        result = f"{prompt.system_prompt}{template.format(**user_inputs)}"
        print(result)

    prompt2 = main_pipeline("prompts/support_ticket_triage.yml")
    if prompt2:
        print(prompt2)

        user_inputs2 = {
            "user_message": "Computer webcam doesn't work properly.",
            "customer_plan": "Premium",
            "language": "English"
        }

        template2 = prompt2.user_prompt_template.replace('{{', '{').replace('}}', '}')
        result2 = f"{prompt2.system_prompt}{template2.format(**user_inputs2)}"
        print(result2)

        
