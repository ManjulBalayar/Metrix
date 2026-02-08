# Phase 1 Goals

## Tech stack

### Repo + packaging
- GitHub
- Python (FastAPI or plain library + CLI)
- Pydantic for schema validation
- YAML for prompt definitions
- pytest for schema/unit tests
- Docker (for Phase 3 deployment)

### GCP touchpoints (Phase 1-only, will be lightweight)
- Artifact Registry: store container images (even if we don't deploy yet)
- Cloud Storgae (option for now): later we can load prompts from GCS, but for Phase 1 will probably keep prompts in Git

Can just keep Phase 1 entirely local + GitHub.

## Phase 1 Features

### 1) Prompt-as-Code format (schema)
A prompt file must include these:
- `prompt_id` (stable identifier)
- `version` (semver like 1.2.0)
- `description`
- `model config` (provider, model name, temperature, max_tokens)
- templates (system + user template)
- input schema (what variables are required, types)
- output contract (format expectations; don't overdo yet)
- metadata (owner, tages, created_at)

### 2) Loader + renderer
- Load prompt YAML by `prompt_id` (+ optionally latest)
- Render templates with provided inputs
- Return a fully formed request payload (system , user, params_

### 3) Validation + guardrails (Phase 1 lvl)
- Validate YAML against schema (fail test)
- Validate required input keys exist
- Validate version string format
- Prevent duplicate (prompt_id, version) collisions

### 4) Local "registery" behavior (simple)
- A directory-based registry:
    - list prompts
    - get prompt versions
    - resolve "latest stable" (basic rule)

## Folder structure (DriveFlow example)
```
repo/
  prompts/
    driveflow_autorename/
      1.0.0.yaml
      1.1.0.yaml
    driveflow_customrename/
      1.0.0.yaml
  promptlib/
    schema.py
    loader.py
    renderer.py
    registry.py
  tests/
    test_schema.py
    test_loader.py
  app/                  # optional now; useful later
    main.py             # FastAPI
  Dockerfile
  pyproject.toml
```

## Concrete prompt storage example (DriveFlow example)
```
prompt_id: driveflow_autorename
version: 1.1.0
description: Rename file based on OCR content with strict filename rules.
owner: manjul
tags: [driveflow, renaming]

model:
  provider: openai
  name: gpt-4o-mini
  temperature: 0.2
  max_tokens: 120

inputs:
  ocr_text:
    type: string
    required: true
  original_filename:
    type: string
    required: true

output:
  format: filename
  rules:
    - "Return ONLY the filename, no quotes."
    - "Use Title Case."
    - "Max 80 characters."
    - "No special chars except dash and underscore."

system_prompt: |
  You are a precise file renaming assistant. Follow output rules strictly.

user_prompt_template: |
  OCR_TEXT:
  {{ocr_text}}

  ORIGINAL_FILENAME:
  {{original_filename}}

  Generate a concise filename following the rules.
```

## Phase 1 End Goal
You can run:
- `promptlint prompts/` -> validates all prompt files
- `promptctl render driveflow_autorename --version 1.1.0 --input ocr_text=...` -> outputs the rendered messages/params
- Unit tests pass
- Docker build works (even though no deployment yet)

## Possible nice to haves
- `status: draft|staging|prod` field
- `changelog:` field (human notes)
- basic CLI commands: `list`, `show`, `render`


