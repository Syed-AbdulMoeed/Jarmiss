from llama_index.core.tools import FunctionTool
from firecrawl import Firecrawl
from dotenv import load_dotenv


load_dotenv()

def web_search(query: str) -> dict:
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

        # Get webresults
        web_results = results.web or []
        output = {}

        # Depending on its internal execution .serach returns either a Document or WebSearchResult object which are handled differently
        for r in web_results:
            # Safely extract URL (try r.url, then r.metadata.url)
            url = getattr(r, "url", None)
            if not url and hasattr(r, "metadata"):
                url = getattr(r.metadata, "url", None) if not isinstance(r.metadata, dict) else r.metadata.get("url")

            # Extract markdown
            markdown = getattr(r, "markdown", "Cannot scrape this webpage") 

            # Truncate content TO-DO: This is a potential Bottleneck
            if len(markdown) > 10000:
                markdown = markdown[:10000]

            # Add to output
            if url:
                output[url] = markdown

        return output

    except Exception as e:
        return {"Exception": str(e)}

def web_search_tool():
    web_search_tool = FunctionTool.from_defaults(
        name="web_search_tool",
        description="A websearch tool that takes a string query as input and returns a dictionary containing webpage urls as keys and their content in markdown as values.",
        fn=web_search
    )
    return web_search_tool