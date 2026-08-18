from dotenv import load_dotenv
import sys
import asyncio
from google.genai import types
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.groq import Groq
from llama_index.core.agent.workflow import ReActAgent, AgentStream, ToolCallResult, FunctionAgent  

# Tools
from AgentTools.code_interpreter import execute_python_tool
from AgentTools.webtool import web_search_tool

# Load API Keys
load_dotenv()

class Jarmiss:
    """Implementation of Jarmiss, The Budget Jarmiss"""
    def __init__(self):
        try:

            # Get safe code interpreter tool
            execute_python = execute_python_tool()

            # Get web search tool
            web_search = web_search_tool()
            

            # Set LLM 
            '''llm = GoogleGenAI(
                model="gemini-3.5-flash",
                generation_config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_level="low"),
                ),)'''

            llm = Groq(
                model="openai/gpt-oss-120b",
                    additional_kwargs={
                        "tool_choice": "auto"
                    }   
                )  # or "openai/gpt-oss-120b", "moonshotai/kimi-k2-instruct"


            self.jarmiss = FunctionAgent(
                name="Jarmiss",
                description="A Personal Agent capably of solving easy tasks from the GAIA dataset",
                system_prompt = (
                    "You are a careful problem-solving agent. "
                    "You have access to a code interpreter for calculations and a web search tool for live information. "
                    "Use your tools efficiently as you have a limited action budget. "
                    "IMPORTANT: Once you have found the answer or computed the result, you MUST respond directly "
                    "to the user with the final answer and STOP calling tools." # Gives it an "exit condition"                ),
                ),
                tools=[execute_python, web_search],
                timeout=120,
                llm=llm
            )

            print(f"{self.jarmiss.name} initialized")
        except Exception as e:
            print("Error while initializing Jarmiss: ", e)   
            sys.exit()

    async def _solve(self, question: str):
        handler = self.jarmiss.run(user_msg=question)

        # Stream THOUGHTS, ACTIONS, OBSERVATION    
        async for ev in handler.stream_events():

            # ACTIONS AND THOUGHTS
            if isinstance(ev, AgentStream):
                print(f"{ev.delta}", end="", flush=True)

            # OBSERVATION
            elif isinstance(ev, ToolCallResult):
                print(f"\n\n[OBSERVATION]\nTool: {ev.tool_name}\nInput: {ev.tool_kwargs}\nResult: {ev.tool_output}")
                print("-" * 40)

        return await handler
            
        


    def __call__(self, question: str):
        """Solves a given question"""
        print("question: ", question)
        response = asyncio.run(self._solve(question))
        print("--------------------------")
        print(str(response))

agent = Jarmiss()
agent("How old was Imran Khan when he won the cricket world cup, use the web_search tool")
#agent("What is the area of a circle with radius 3, round to 3d.p")
    
