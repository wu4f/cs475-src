from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from pydantic import BaseModel, Field
import readline

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

print(f"Format instructions given to the LLM from parser:\n {json_parser.get_format_instructions()}")

llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0)

chain = json_prompt | llm | json_parser

while True:
    line = input("llm>> ")
    if line:
        print(chain.invoke({"genre": line}))
    else:
        break
