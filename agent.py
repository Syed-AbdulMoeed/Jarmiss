from dotenv import load_dotenv
import sys
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.agent import ReActAgent
# Tools
from AgentTools.code_interpreter import execute_python_tool


# Load API Keys
load_dotenv()



class Jarmiss:
    """Implementation of Jarmiss, The Budget Jarmiss"""
    def __init__(self):
        try:

            # Get safe code interpreter tool
            code_interpreter = execute_python_tool()
            tools = code_interpreter.to_tool_list()

            # Set LLM 
            llm = GoogleGenAI(model="gemini-3.5-flash")

            self.jarmiss = ReActAgent(
                name="Jarmiss",
                description="A Personal Agent capably of solving easy tasks from the GAIA dataset",
                system_prompt="TO-DO",
                tools=[execute_python_tool],
                verbose=True, # To see thoughts and observations
                max_iterations=10,
                llm=llm
            )

            print(f"{self.jarmiss.name} initialized")
        except Exception as e:
            print("Error while initializing Jarmiss: ", e)   
            sys.exit()

    def __call__(self, question: str):
        """Solves A given question"""
        self.agent()

agent = Jarmiss()
agent

    
