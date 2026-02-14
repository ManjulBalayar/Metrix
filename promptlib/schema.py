from pydantic import BaseModel, ValidationError, Field, field_validator, model_validator
from typing import List, Dict, Any, Optional, Literal, Union
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
    required: bool = True
    default: Optional[Any] = None
    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_required_and_default(self):
        """
        If required is False, default should be provided.
        """
        if not self.required and self.default is None:
            raise ValueError("Non-required fields should have a default value")
        return self

class Output(BaseModel):
    """
    Output configuration that supports multiple formats.
    """
    format: str # like "filename", "json", "text", "markdown"

    # Optional fields for different output types
    rules: Optional[List[str]] = None 
    json_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None # alternate to json_schema
    constraints: Optional[Dict[str, Any]] = None
    example: Optional[str] = None

    @model_validator(mode="after")
    def validate_output_spec(self):
        """
        Ensure at least some output specification exists
        """
        has_spec = any([
            self.rules,
            self.json_schema,
            self.schema,
            self.constraints,
            self.example
        ])
        if not has_spec:
            raise ValueError(
                'Output must have at least one specification: '
                'rules, json_schema, output_schema, constraints, or example'
            )
        return self

class YAML(BaseModel):
    # required metadata
    prompt_id: str = Field(min_length=1)
    version: str
    status: Literal["draft", "staging", "prod", "deprecated"] # only stages
    owner: str = Field(min_length=1) # Non-empty
    
    # optional metadata
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # model configuration
    model: ModelConfig

    # Inputs & outputs
    inputs: Dict[str, InputField] = Field(min_length=1) # At least 1 input
    output: Output

    # Prompts
    system_prompt: str = Field(min_length=1) # non-empty
    user_prompt_template: str = Field(min_length=1) # non-empty

    # optional advanced features
    functions: Optional[List[Dict[str, Any]]] = None # for function calling
    examples: Optional[List[Dict[str, Any]]] = None  # few-shot examples
    metadata: Optional[Dict[str, Any]] = None        # any additional metadata
   
    @field_validator('version')
    @classmethod
    def validate_semver(cls, v: str) -> str:
        """Validate semantic versioning format (x.y.z)"""
        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError('version must be in semver format (e.g., 1.0.0)')
        return v
    
    @field_validator('system_prompt', 'user_prompt_template')
    @classmethod
    def validate_non_empty_string(cls, v: str) -> str:
        """Ensure strings are not just whitespace"""
        if not v.strip():
            raise ValueError('must not be empty or whitespace only')
        return v
    
    @field_validator('created_at', 'updated_at')
    @classmethod
    def validate_datetime_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate ISO 8601 datetime format"""
        if v is None:
            return v
        if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?$', v):
            raise ValueError('datetime must be in ISO 8601 format (e.g., 2026-02-01T14:32:00Z)')
        return v
