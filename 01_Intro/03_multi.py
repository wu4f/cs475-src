from langchain.model_laboratory import ModelLaboratory
from langchain_community.llms import HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
import warnings
import readline
warnings.simplefilter("ignore")

llms = [
#    To instantiate an Ollama level
#    Ollama( model="llama2", base_url="http://35.236.12.22:11434"),
    HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", max_new_tokens=128),
    HuggingFaceHub(repo_id="google/flan-t5-small"),
    ChatOpenAI(model='gpt-4o'),
    ChatGoogleGenerativeAI(model="gemini-pro"),
    ChatGoogleGenerativeAI(model="gemini-1.5-pro"),
    ChatAnthropic(model="claude-3-sonnet-20240229"),
]
model_lab = ModelLaboratory.from_llms(llms)
print("Welcome.  Type a prompt and I will query several LLMs to answer it.")

while True:
    try:
        line = input("llm>> ")
        if line:
            model_lab.compare(line)
        else:
            break
    except:
        break
