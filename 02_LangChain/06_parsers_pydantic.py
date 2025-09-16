import os
import readline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

# Define your desired data structure.
class GenreMovies(BaseModel):
    genre: str = Field(description="genre to lookup")
    movies: list[str] = Field(description="list of movies in genre")

# Set up a parser based on structure
json_parser = JsonOutputParser(pydantic_object=GenreMovies)

# Set up prompt to include formatting specified by parser.
json_prompt = PromptTemplate(
    template="Find the top 5 movies of the genre given by the user.\n{format_instructions}\n{genre}\n",
    input_variables=["genre"],
    partial_variables={"format_instructions": json_parser.get_format_instructions()},
)

print(f"This program lists the top 5 movies of a particular genre in a JSON format.  The format instructions given to the LLM from the parser are:\n {json_parser.get_format_instructions()}")

chain = json_prompt | llm | json_parser

while True:
    line = input("llm>> ")
    if line:
        print(chain.invoke({"genre": line}))
    else:
        break
