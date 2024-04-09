from nltk.tokenize import WordPunctTokenizer, TreebankWordTokenizer, RegexpTokenizer
import tiktoken
from langchain_google_genai import ChatGoogleGenerativeAI

# See if we can use langchain llm to use  token count method
llm = ChatGoogleGenerativeAI(model="gemini-pro")


# Example string for tokenization
example_string = "What's the best way to tokenize a string in Python?"

# Tokenization Methods
# Method 1: White Space Tokenization
# This method splits the text based on white spaces
white_space_tokens = example_string.split()

# Method 2: WordPunct Tokenization
# This method splits the text into words and punctuation

wordpunct_tokenizer = WordPunctTokenizer()
wordpunct_tokens = wordpunct_tokenizer.tokenize(example_string)

# Method 3: Treebank Word Tokenization
# This method uses the standard word tokenization of the Penn Treebank

treebank_tokenizer = TreebankWordTokenizer()
treebank_tokens = treebank_tokenizer.tokenize(example_string)

# Method 4: Regexp Tokenization
# This method uses regular expressions to split the text
regexp_tokenizer = RegexpTokenizer(r'\s+', gaps=True)
regexp_tokens = regexp_tokenizer.tokenize(example_string)
white_space_tokens, wordpunct_tokens, treebank_tokens, regexp_tokens

# Testing tiktoken
# Let's say that we want to count tokens for a specific OpenAI model
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
# Count number of tokens
numerical_representation = encoding.encode(example_string)
tiktoken_bytes = [encoding.decode_single_token_bytes(token) for token in numerical_representation]
num_tokens = len(tiktoken_bytes)

gemini_token_count = llm.get_num_tokens(example_string)


# for i in llm_object:
#     if "token" in i:
#         print(i)  

# Get number of tokens sent to Gemini model

print(f"Token representations of Example String: {example_string}")
print("---------------------------------------------------")
print(f"White Space Tokenization: {white_space_tokens}")
print(f"WordPunct Tokenization: {wordpunct_tokens}")
print(f"Treebank Tokenization: {treebank_tokens}")
print(f"Regexp Tokenization: {regexp_tokens}")
print("---------------------------------------------------")
print(f"Using tiktoken (gpt-3.5-turbo) to count tokens")
print(f"tiktoken Tokenization: {tiktoken_bytes}")
print(f"tiktoken Numerical representation: {numerical_representation}")


print("---------------------------------------------------")
print(f"Number of tokens for Gemini model: {gemini_token_count} ")
print(f"Compared to number of tokens for tiktoken: {num_tokens}")

# Show break downs of the tokenizer output

# Google tokenizer proprietary
# So we need to instantiate the model first, then query it for token count
llm = ChatGoogleGenerativeAI(model="gemini-pro")
