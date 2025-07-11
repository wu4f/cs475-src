import readline
import tiktoken
from nltk.tokenize import WordPunctTokenizer, RegexpTokenizer

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

print("Enter a text query to see how it is tokenized")
while True:
    line = input(">> ")
    if line:
        tokenize_compare(line)
    else:
        break
