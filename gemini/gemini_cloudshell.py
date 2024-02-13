import vertexai
import os
from vertexai.preview.generative_models import GenerativeModel

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = "us-west1"
vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-pro")
prompt = "Give me some sage advice."
model_response = model.generate_content(prompt)
print(model_response.text)
