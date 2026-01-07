import os
from langchain_classic.model_laboratory import ModelLaboratory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
import warnings
import readline
warnings.simplefilter("ignore")

llms = [
#    To instantiate an Ollama level
#    Ollama( model="llama2", base_url="http://35.236.12.22:11434"),
    ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL")),
    ChatOpenAI(model=os.getenv("OPENAI_MODEL")),
    ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))
]
model_lab = ModelLaboratory.from_llms(llms)
print("Welcome.  Type a prompt and I will query several LLMs to answer it. A blank line exits.")

while True:
    try:
        line = input("llm>> ")
        if line:
            model_lab.compare(line)
        else:
            break
    except:
        break
