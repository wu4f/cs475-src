from langchain_community.llms import Ollama
import sys
import readline
ollama_address = sys.argv[1]
model_name = sys.argv[2]
llm = Ollama( model=model_name, base_url=f"http://{ollama_address}:11434" )
while True:
    line = input("llm>> ")
    if line:
        for chunks in llm.stream(line):
            print(chunks,end="")
        print("")
    else:
        break
