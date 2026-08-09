import requests
from dotenv import load_dotenv
import os
# https://docs.ollama.com/capabilities/web-search
load_dotenv()
print(os.getenv("OLLAMA_API_KEY"))

res = requests.post(
    url="https://ollama.com/api/web_search",
    json = {
        "query": "Who is Imran Khan",
        "max_results": 3
    },
    headers= {
        "Authorization": f"Bearer {os.getenv("OLLAMA_API_KEY")}"
    }
)
res = res.json()
for result in res["results"]:
    print("----------------------------------")
    print(result["title"])
    print(result["url"])
    #print(result["content"])

# How to deal with the large amount of text from content????