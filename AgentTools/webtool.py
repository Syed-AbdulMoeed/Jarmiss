import requests
from dotenv import load_dotenv
import os
from firecrawl import Firecrawl
load_dotenv()

def web_search(query: str):
    """
    A websearch tool that takes a string query as input and returns a dictionary containing 
    webpage urls as keys and their content in markdown as values.
    """
    try:
        app = Firecrawl()
        results = app.search(
            query, 
            limit=2,    
            scrape_options={ 
                "formats": ["markdown"] 
            }
        )

        web_results = results.web or []
        output = {}

        for r in web_results:
            # 1. Safely extract URL (try r.url, then r.metadata.url)
            url = getattr(r, "url", None)
            if not url and hasattr(r, "metadata"):
                url = getattr(r.metadata, "url", None) if not isinstance(r.metadata, dict) else r.metadata.get("url")

            # 2. Extract markdown
            markdown = getattr(r, "markdown", "") or ""

            # Truncate content
            if len(markdown) > 100:
                markdown = markdown[:100]

            if url:
                output[url] = markdown

        return output

    except Exception as e:
        return {"Exception": str(e)}
print(web_search("Who invented the aeroplane"))