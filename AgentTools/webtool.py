import requests
from dotenv import load_dotenv
import os
from firecrawl import Firecrawl
load_dotenv()

def web_search(query: str):
    """A websearch tool that takes a string query as input and returns a dictionary containing the url and the content in markdown from the internet"""
    try:
        # Getting initial results
        app = Firecrawl()
        results = app.search(
            query, 
            limit=2,    
            scrape_options={ 
            "formats": ["markdown"] # return result in readable markdown 
        })

        # Dealing with long outputs by truncating
        for result in results:
            if len(result.markdown) > 2000:
                result.markdown = result.markdown[:2000]

        return {r.url: r.markdown for r in results}
    except Exception:
        return "There was an error with scraping, try another query"
