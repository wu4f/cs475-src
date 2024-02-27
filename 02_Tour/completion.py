# Requires export GOOGLE_API_KEY=""
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-pro")

print("Multi-line prompt input. Type Ctrl-d on an empty line to submit it to the LLM.")
print("Ctrl-d on prompt exits application.")
while True:
    contents = []
    print("llm>> ",end="")
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    if contents:
        print("Sending to LLM...")
        content = '\n'.join(contents)
        result = llm.invoke(content)
        print(result)
    else:
        break
