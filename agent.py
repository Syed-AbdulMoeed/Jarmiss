from dotenv import load_dotenv
import sys
import asyncio
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.agent.workflow import ReActAgent, AgentStream, ToolCallResult  
# Tools
from AgentTools.code_interpreter import execute_python_tool


# Load API Keys
load_dotenv()



class Jarmiss:
    """Implementation of Jarmiss, The Budget Jarmiss"""
    def __init__(self):
        try:

            # Get safe code interpreter tool
            execute_python = execute_python_tool()
            

            # Set LLM 
            llm = GoogleGenAI(model="gemini-3.6-flash")

            self.jarmiss = ReActAgent(
                name="Jarmiss",
                description="A Personal Agent capably of solving easy tasks from the GAIA dataset",
                system_prompt = (
                    "You are a helpful AI agent. "
                    "When calling tools, you MUST provide strictly valid JSON in Action Input. "
                    "Ensure all double quotes and newlines within Python code string arguments are properly escaped."
                ),
                tools=[execute_python],
                timeout=120,
                llm=llm
            )

            print(f"{self.jarmiss.name} initialized")
        except Exception as e:
            print("Error while initializing Jarmiss: ", e)   
            sys.exit()

    async def _solve(self, question: str):
        """Runs the agent inside a live event loop"""
        handler = self.jarmiss.run(user_msg=question)

        # Listen to the event stream
        async for ev in handler.stream_events():
            # THOUGHT and ACTION
            if isinstance(ev, AgentStream):
                print(f"{ev.delta}", end="", flush=True)

            # OBSERVATION
            elif isinstance(ev, ToolCallResult):
                print(f"\n\n [OBSERVATION]")
                print(f"Tool executed: {ev.tool_name}")
                print(f"Tool_input: {ev.tool_kwargs}")
                print(f"Result: {ev.tool_output}")
                print("-" * 40)

        response = await handler
        return response


    def __call__(self, question: str):
        """Solves a given question"""
        print("question: ", question)
        response = asyncio.run(self._solve(question))
        print("--------------------------")
        print(str(response))

agent = Jarmiss()
agent("What is 10/2, solve using python")

    
