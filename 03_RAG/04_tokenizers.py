from nltk.tokenize import WordPunctTokenizer, RegexpTokenizer
import tiktoken
from langchain_google_genai import GoogleGenerativeAI
import readline

regexp = RegexpTokenizer(r'\s+', gaps=True)
wordpunct = WordPunctTokenizer()

def tokenize_compare(sentence):
    print("Whitespace tokenizer")
    print_tokens(regexp.tokenize(sentence))
    print("Wordpunct tokenizer")
    print_tokens(wordpunct.tokenize(sentence))
    print("gpt-3.5-turbo (cl100k_base) tokenizer")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    numerical_representation = encoding.encode(sentence)
    tiktokens = [encoding.decode_single_token_bytes(token).decode('utf8') for token in numerical_representation]
    print_tokens(tiktokens)
    print(f"tiktoken Numerical representation: {numerical_representation}")
  
def print_tokens(tokens):
  for count, token in enumerate(tokens):
     print(f"[{count}]{token} ",end="")
  print()

while True:
    line = input(">> ")
    if line:
        tokenize_compare(line)
    else:
        break
print(f"\n----------Enter a query to estimate the cost of querying gemini-1.5-pro----------")

completion_llm=GoogleGenerativeAI(model="gemini-1.5-pro")

def calculate_completion_cost(query, input_cost, output_cost):
    prompt_tokens = completion_llm.get_num_tokens(query)
    response = completion_llm.invoke(query)
    output_tokens = completion_llm.get_num_tokens(response)
    total_cost= prompt_tokens * input_cost + output_tokens * output_cost
    print(f"-----This is the ouput-----\n {response}")
    print(f"-----Token estimation and cost calculation-----")
    print(f"The number of input tokens: {prompt_tokens} and the number of output tokens: {output_tokens}")
    print(f"The rate for input tokens: {input_cost}/token and the rate for output tokens: {output_cost}/token")
    print(f"Total cost is: {total_cost}")

#Cost per million tokens
GEMINI_15_INPUT = 3.5

GEMINI_15_OUTPUT = 10.5

#cost per token
per_token_input=GEMINI_15_INPUT/1000000
per_token_output=GEMINI_15_OUTPUT/1000000

while True:
    line = input(">> ")
    if line:
        calculate_completion_cost(line, per_token_input, per_token_output)
    else:
        break

