from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-pro")

print("Multi-line prompt input. Enter '.' on a line to send to LLM.  Type Ctrl-d to exit application.")
try:
    while True:
        contents = []
        print("llm>> ",end="")
        while True:
            line = input()
            if (len(line) == 1) and line.startswith('.'):
                break
            else:
                contents.append(line)
        if contents:
            print("Sending to LLM...")
            result = llm.invoke('\n'.join(contents))
            print(result)
except EOFError:
    print("Goodbye")
