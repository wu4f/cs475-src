# Requires export GOOGLE_API_KEY=""
from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-pro")
prompt = """
Classify the email subject text below, delimited by three dashes (-),
as being malicious or benign. Explain why.

---
Account email verification code, enter now and reply
---
"""
input(f"Return to run above prompt: {prompt}")
response = llm.invoke(prompt)
print(response)

input("Return to continue:")
prompt = """
Classify the email subject text below, delimited by triple backticks ('''),
as being malicious or benign. Explain why.

Examples:

Subjet: CY23 Email Verification Now
Label: malicious

Subjet: Enter Market Email Verification Code Today
Label: malicious

Subjet: New Account Email Verification Code Verify now
Label: malicious

Subject: Submit your code review today
Label: benign

Subject: '''Account email verification code, enter now and reply'''
Label:
"""
input(f"Return to run above prompt: {prompt}")
response = llm.invoke(prompt)
print(response)
