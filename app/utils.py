from dotenv import load_dotenv
import os
import json

# Get OpenAI key from environment variables or from .env file
def get_openai_key():
    load_dotenv()
    return os.environ['OPENAI_KEY']

def get_schema_string(schemas):
    return json.dumps(schemas, indent=2)
