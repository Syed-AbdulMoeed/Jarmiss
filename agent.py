from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.agent import ReActAgent

# Load API Keys
load_dotenv()


class Jarmiss:
    """Implementation of Jarmiss, The Budget Jarmiss"""
    def __init__(self):
        llm = GoogleGenAI(model="gemini-3.5-flash")

        self.jarmiss = ReActAgent(
            name="Jarmiss",
            description="A Personal Agent capably of solving easy tasks from the GAIA dataset",
            system_prompt="TO-DO",
            tools=[],
            verbose=True, # To see thoughts and observations
            max_iterations=10,
            llm=llm
        )

    def __call__(self, question: str):
        """Solves A given question"""
        pass

Jarmiss()
    
