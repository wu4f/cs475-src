import vertexai
import os
from vertexai.preview.generative_models import GenerativeModel

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = "us-west1"
vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-pro")

def get_response(model: GenerativeModel, prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

prompt = "What are the colors of the rainbow?"
print(get_response(model, prompt))
