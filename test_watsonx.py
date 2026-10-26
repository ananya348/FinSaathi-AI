
import os
from pathlib import Path
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference

# Find and load .env beside this script
env_path = Path(__file__).resolve().parent / ".env"
print("Looking for .env at:", env_path)
print("File exists:", env_path.is_file())

load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("WATSONX_API_KEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
url = os.getenv("WATSONX_URL")

print("API key loaded:", bool(api_key))
print("Project ID loaded:", bool(project_id))
print("URL loaded:", repr(url))

if not all([api_key, project_id, url]):
    raise ValueError(
        "Missing credentials. Check the .env file path "
        "and make sure the variable names match exactly."
    )
