from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field

# Define your desired data structure.
class GenreMovies(BaseModel):
    genre: str = Field(description="genre to lookup")
    movies: str = Field(description="list of movies in genre")

llm = GoogleGenerativeAI(model="gemini-pro")

# Set up a parser + inject instructions into the prompt template.
json_parser = JsonOutputParser(pydantic_object=GenreMovies)

json_prompt = PromptTemplate(
    template="Find the top 5 movies of the genre given by the user.\n{format_instructions}\n{genre}\n",
    input_variables=["genre"],
    partial_variables={"format_instructions": json_parser.get_format_instructions()},
)

print(json_parser.get_format_instructions())

chain = json_prompt | llm | json_parser
print(chain.invoke({"genre": "Science Fiction"}))
print(chain.invoke({"genre": "Drama"}))
print(chain.invoke({"genre": "Comic Book"}))
