"""
Here, we check the YAML structure, validate required fields, and reject any malformed prompts and files.
"""

def validate_yml(data):
    """
    Receive data from loader in a dictionary format.
    Check for required fields and the format of the YAML.
    
    Things that stay consisten across all yml files are:
    - prompt_id, version, status, timestamps (created & updated)
    - owner
    - model
    - inputs
    - system_prompt
    - user_prompt_template
    - output
    """
    
    keys = data.keys()
    keys_set = set(data.keys())

    # First layer, check for presence of needed keys
    required = {
        'prompt_id', 'version', 'status', 'created_at',
        'updated_at', 'owner', 'model', 'inputs',
        'system_prompt', 'user_prompt_template', 'output',
    }
    
    missing = required - keys_set

    if missing:
        raise ValueError(f"Missing required keys: {missing}")
    
    # Second layer, check type + shape
    # model must be a dict, model.temperature & model.max_tokens must be numbers
    # inputs and outputs must be a dict. inputs has `type` and `required` boolean needed.
    # outputs demands correct filename match, and a list of rules.
    # tags are supposed to be a list


    return missing

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

keys = validate_yml(data)
print(keys)
print(type(keys))
