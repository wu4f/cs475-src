# Requires export GOOGLE_API_KEY=""
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

def query(llm, query, image_url):
  input(f"Q: {query} {image_url}")
  message = HumanMessage(
      content=[
          {
              "type": "text",
              "text": query,
          },
          {   "type": "image_url",
              "image_url": image_url
          }
      ]
  )
  response = llm.invoke([message])
  return response

image_url = "https://samsclass.info/126/proj/p12x-8.png"
print(query(llm, "Can you explain this image?", image_url))

# XSS in ChatGPT article
# https://securityboulevard.com/2024/02/xss-marks-the-spot-digging-up-vulnerabilities-in-chatgpt/
# image_url = 'https://www.imperva.com/blog/wp-content/uploads/sites/9/2024/02/Screenshot-2024-02-16-at-10.23.39-AM.png'
# image_url = 'https://www.imperva.com/blog/wp-content/uploads/sites/9/2024/02/Screenshot-2024-02-16-at-10.24.47-AM.png'

# XSS techniques article
# https://portswigger.net/research/exploiting-xss-in-hidden-inputs-and-meta-tags
# image_url = 'https://portswigger.net/cms/images/87/fa/ba3d-article-popover-xss-onbeforetoggle.png'
# image_url = 'https://portswigger.net/cms/images/91/43/e4e5-article-popovers-hidden-inputs.png'

# Malicious Python packages article
# https://thehackernews.com/2023/12/116-malware-packages-found-on-pypi.html
#image_url = 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgLEkzLRso43D7xzhA_mzmsAIXTXTtx0HcspQ1wiS4eWFArZpskXlFOLJuj7O2ZmJqpr0jdw2qd_IkRdM-mCmvvoo-os-wb8aWzGxvBaypDZvOo9Z1S0YLy7H_duLlz3J32hOOmRfPPQPXGMVlV78zJNQBi8W5_RgWxr_m4qqwXGcrJhCwQuhG8IemQPY7L/s728-rw-e365/malware.jpg'
#image_url = 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiWZWBKPTn6daxojtQ8nya0MKKw_HsJdEN5-en6DXkrkie0Mwe0-IVSg6-cQqKuirEduXLLTLsw9efgEMElVXjGmVbAvh4JYo0w0CxJ-JJyOJp4OoN22AYK1Stf2DEELft8xLwSsV-BOsWdM1oJ7u9jH3YFQNGW5NNO2SfvP0wFNLs0V5Q5j2_PwOF7242J/s728-rw-e365/python-2.jpg'
