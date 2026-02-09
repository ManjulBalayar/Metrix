import yaml
from pathlib import Path

"""
Loads YAML files from `prompts` folder. We parse the YAML file here and
give a plain data struture to then give it to the `schema.py` for validation.

We need to find the right file (by `prompt_id` + version). Read it from disk,
parse the YAML file into a Python dictionary and handle helpful errors like
missing files or YAML syntax error. 
"""

def load_yml(file):
    """
    Load and parse a YAML file with error handling.
    """

    try:
        script_dir = Path(__file__).parent
        file_path = script_dir.parent / file

        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")

        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data is None:
            raise ValueError(f"YAML file is empty: {file_path}")

        return data

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{file}':")
        print(f"  {e}")
        return None

    except PermissionError as e:
        print(f"Error: Permission denied reading '{file}'")
        return None

    except Exception as e:
        print(f"Unexpected error laoding '{file}': {type(e).__name__}: {e}")
        return None

#Usage
if __name__ == "__main__":
    data = load_yml("prompts/driveflow_autorename.yml")

    if data is not None:
        print("Successfully loaded the YAML file:")
        print(data)
    else:
        print("Failed to load YAML file")
