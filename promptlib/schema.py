from pydantic import BaseModel, ValidationError, Field, field_validator
from typing import List, Dict, Any, Optional, Literal
import re

"""
Here, we check the YAML structure, validate required fields, and reject any malformed prompts and files.
"""

class ModelConfig(BaseModel):
    provider: str
    name: str
    temperature: float = Field(ge=0.0, le=2.0) # Between 0 and 2
    max_tokens: int = Field(gt=0) # Must be a pos

class InputField(BaseModel):
    type: Literal["string", "int", "float", "bool"] # The only allowed types
    required: bool

class Output(BaseModel):
    format: str
    rules: List[str] = Field(min_length=1) # At least 1 rule from user

class YAML(BaseModel):
    prompt_id: str = Field(min_length=1)
    version: str
    status: Literal["draft", "staging", "prod"] # only stages
    description: Optional[str] = None
    owner: str = Field(min_length=1) # Non-empty
    tags: Optional[List[str]] = None
    created_at: str
    updated_at: str
    model: ModelConfig
    inputs: Dict[str, InputField] = Field(min_length=1) # At least 1 input
    output: Output
    system_prompt: str = Field(min_length=1) # non-empty
    user_prompt_template: str = Field(min_length=1) # non-empty

    @field_validator('version')
    @classmethod
    def validate_semver(cls, v: str) -> str:
        """
        Validate semantic versionaing format (x. y. z)
        """
        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError('version must be in semver format (e.g., 1.0.0)')
        return v

    @field_validator('system_prompt', 'user_prompt_template')
    @classmethod
    def validate_non_empty_string(cls, v: str) -> str:
        """
        Make sure strings are not just whitespaces
        """
        if not v.strip():
            raise ValueError('must not be empty or whitespace only')
        return v

    

data = {
  "prompt_id": "driveflow_autorename",
  "version": "1.1.0",
  "status": "prod",
  "description": "Rename file based on OCR content with strict filename rules.",
  "owner": "manjul",
  "tags": [
    "driveflow",
    "renaming"
  ],
  "created_at": "2026-02-01T14:32:00Z",
  "updated_at": "2026-02-08T19:10:00Z",
  "model": {
    "provider": "openai",
    "name": "gpt-4o-mini",
    "temperature": 0.2,
    "max_tokens": 120
  },
  "inputs": {
    "ocr_text": {
      "type": "string",
      "required": True
    },
    "original_filename": {
      "type": "string",
      "required": True
    }
  },
  "output": {
    "format": "filename",
    "rules": [
      "Return ONLY the filename, no quotes.",
      "Use Title Case.",
      "Max 80 characters.",
      "No special chars except dash and underscore."
    ]
  },
  "system_prompt": "You are a precise file renaming assistant. Follow output rules strictly.\n",
  "user_prompt_template": "OCR_TEXT:\n{{ocr_text}}\n\nORIGINAL_FILENAME:\n{{original_filename}}\n\nGenerate a concise filename following the rules.\n"
}

try:
    p = YAML(**data)
    print("Validation successful!")
    print(f"\nPrompt ID: {p.prompt_id}")
    print(f"Version: {p.version}")
    print(f"Status: {p.status}")
    print(f"Model: {p.model.provider} - {p.model.name}")
except ValidationError as e:
    print("Validation failed:")
    print(e)
