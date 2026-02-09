from promptlib.loader import load_yml

data = load_yml("prompts/driveflow_autorename.yml")

if data is not None:
        print("Successfully loaded the YAML file:")
        print(data)
else:
    print("Failed to load YAML file")
