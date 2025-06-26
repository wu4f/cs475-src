import os
import github
import readline
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

# Retrieve the GitHub token from the environment variable
github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
g = github.Github(github_token)

def process_commit(commit_sha):
    """Given a git commit by its hexadecimal encoded 20-byte sha hash, returns a summary of what the commit implements and whether it is malicious"""
    commit = repo.get_commit(commit_sha)
    commit_prompt = PromptTemplate(
        input_variables=["author", "date", "message", "changes"],
        template="""You are a git commit analyzer.  A commit is given with the names of files and their changes.  Analyze the commit to determine 3 things: 1. What the code in the commit does.  2. Whether the code does what the commit message claims.  3. Whether the code in the commit is malicious.

      Commit author: {author} \n\n Commit date: {date} \n\n 
      Commit message: {message} \n\n File changes: {changes} \n\n

      Answer: """
    ) 
    commit_data = {}
    commit_data['sha'] = commit.sha
    commit_data['author'] = commit.commit.author.name
    commit_data['date'] = commit.commit.author.date
    commit_data['message'] = commit.commit.message
    commit_data['changes'] = "\n\n".join(f" - File: {file.filename}\n - Changes: {file.changes}\n - Additions: {file.additions}\n - Deletions: {file.deletions}\n - Diff: \n{file.patch}" for file in commit.files)
    chain = commit_prompt | llm
    summary = chain.invoke({
        'author': commit_data['author'],
        'date': commit_data['date'],
        'message': commit_data['message'],
        'changes': commit_data['changes']
    })
    return(summary.content)

print("Welcome to my GitHub commit tool.  Enter a GitHub repository.")
line = input("Gihub repository (wu4f/cs410g-src): ")

try:
    repo = g.get_repo(line)
    print(f"Using {repo}")
except:
    repo = g.get_repo("wu4f/cs410g-src")
    print("Using wu4f/cs410g-src")

print("Give me git commit hash (e.g. b9d9171679f13b588e2fd0a0200c1961fb74d438)  and I will analyze what's in it and whether it has malicious intent.  A blank line exits.")
while True:
    try:
        line = input("llm>> ")
        if line:
            result = process_commit(line)
            print(result)
        else:
            break
    except Exception as e:
        print(e)
        break

