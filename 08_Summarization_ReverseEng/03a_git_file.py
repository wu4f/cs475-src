import os
from github import Github, Auth
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
g = Github(auth=Auth.Token(github_token))

def summarize_file(file_path):
    """Given a file path in the repository, returns a summary of what the file does and a description of the last commit."""
    try:
        file_content = repo.get_contents(file_path).decoded_content.decode("utf-8")
        commits = repo.get_commits(path=file_path)
        commit = commits[0]
        commit_data = f"- Commit SHA: {commit.sha}\n  Author: {commit.commit.author.name}\n  Date: {commit.commit.author.date}\n  Message: {commit.commit.message}\n"
        full_commit = repo.get_commit(commit.sha)
        for file in full_commit.files:
           if file.filename == file_path:
               full_commit_data = f" - File: {file.filename}\n - Changes: {file.changes}\n - Additions: {file.additions}\n - Deletions: {file.deletions}\n - Diff: \n{file.patch}"
    except Exception as e:
        return("Problem accessing file")

    prompt = PromptTemplate(
        input_variables=["file_path", "file_content", "commit_data", "full_commit_data"],
        template="""You are a git file analyzer.  The code to the file and information on its last commit is given.  1. Explain what the file does.  2. Summarize what happened in the last commit for the file.
      File name: {file_path}\n\n
      File contents: {file_content}\n\n
      Last commit: {commit_data} \n\n
      Last commit modifications: {full_commit_data}\n\n

      Answer: """
    )
    chain = prompt | llm
    summary = chain.invoke({
        'file_path': file_path,
        'file_content': file_content,
        'commit_data': commit_data,
        'full_commit_data': full_commit_data
    })
    return(summary.content)

print("Welcome to my GitHub file tool.  Enter a GitHub repository.")
line = input("Gihub repository (wu4f/cs475-src): ")
try:
    repo = g.get_repo(line)
    print(f"Using {repo}")
except:
    repo = g.get_repo("wu4f/cs475-src")
    print("Using wu4f/cs475-src")

print("Give me a path to a file in the repository and I will summarize its code and last commit.  A blank line exits.")
while True:
    try:
        line = input("llm>> ")
        if line:
            result = summarize_file(line)
            print(result)
        else:
            break
    except Exception as e:
        print(e)
        break

