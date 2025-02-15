import os
import github
import requests
import readline
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"),temperature=0)
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))

# Retrieve the GitHub token from the environment variable
github_token = os.getenv("GITHUB_TOKEN")
g = github.Github(github_token)

def process_pull_request(pr_number):
    """Given a pull request by its integer identifier, returns a summary of what it does and whether it is malicious"""
    pull = repo.get_pull(pr_number)
    pr_prompt = PromptTemplate(
        input_variables=["title", "body", "diff"],
         template="""You are a git pull request analyzer.  A pull request is given with its title, description, and its source-code diff.  Analyze the request to determine 3 things: 1. What the code in the pull request does.  2. Whether the code does what the title and description claims.  3. Whether the code is malicious. \n\n
      Title: {title}\n\n Description: {body}\n\n Diff: {diff}\n\n
      Answer: """
    )
    pr_data = {}
    pr_data['title'] = pull.title
    pr_data['body'] = pull.body or "No description provided."

    # Get the diff content
    diff_response = requests.get(pull.diff_url)
    pr_data['diff'] = diff_response.text

    chain = pr_prompt | llm
    summary = chain.invoke({
        'title': pr_data['title'],
        'body': pr_data['body'],
        'diff': pr_data['diff']
    })
    # Summarize the pull request
    return(summary)

#print(process_pull_request(22))

print("Welcome to my GitHub pull request tool.  Enter a GitHub repository.")
line = input("Gihub repository (wu4f/cs410g-src): ")

try:
    repo = g.get_repo(line)
    print(f"Using {repo}")
except:
    repo = g.get_repo("wu4f/cs410g-src")
    print("Using wu4f/cs410g-src")

print("Give me a git pull request number and I will analyze what's in it and whether it has malicious intent.  A blank line exits.")
while True:
    try:
        line = input("llm>> ")
        if line:
            result = process_pull_request(int(line))
            print(result)
        else:
            break
    except Exception as e:
        print(e)
        break

