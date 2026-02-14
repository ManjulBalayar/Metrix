from typing import Dict, Any
from promptlib.loader import load_yml
from promptlib.schema import YAML, ModelConfig, InputField, Output
from promptlib.renderer import PromptRenderer
from pydantic import ValidationError
import json

def main_pipeline(yaml_path: str, user_inputs: Dict[str, Any]):
    
    # 1. load yml file
    data = load_yml(yaml_path)
    if data is not None:
            print("Successfully loaded the YAML file!")
    else:
        print("Failed to load YAML file")
    
    print("")

    # 2. Check schema format to see if it's valid
    try:
        prompt = YAML(**data)
        print("YAML format is valid!")
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

    # 3. Render with renderer.py and make LLM prompt
    renderer = PromptRenderer(prompt)
    try:
        # get formatted prompts
        full_prompt = renderer.render_full_prompt(user_inputs)
        print(f"Full Prompt: {full_prompt}\n")

        return renderer, prompt
    except ValueError as e:
        print(f"Rendering error: {e}")
        return None

# Usage
if __name__ == "__main__":
    # Prompt 1: File renaming
    main_pipeline(
        "prompts/driveflow_autorename.yml",
        {
            "ocr_text": "Invoice #12345 - Acme Corp - $500.00",
            "original_filename": "scan_001.pdf"
        }
    )

    print("-"*100)

    # Prompt 2: Support triage with defaults
    main_pipeline(
        "prompts/support_ticket_triage.yml",
        {
            "user_message": "Computer webcam doesn't work properly."
            # customer_plan and language will use defaults from YAML
        }
    )

    print("-"*100)

    # Prompt 3: Email subject line generator
    main_pipeline(
        "prompts/email_subject_generator.yml",
        {
            "email_body": "Hi James, I'm reaching for the internship! Where can I apply?",
            # rest will be default
        }
    )

