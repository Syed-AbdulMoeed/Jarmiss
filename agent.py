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
            llm = GoogleGenAI(
                model="gemini-3.6-flash",
                generation_config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_level="low"),
                ),)

            #llm = Groq(model="openai/gpt-oss-120b")  # or "openai/gpt-oss-120b", "moonshotai/kimi-k2-instruct"


            self.jarmiss = FunctionAgent(
                name="Jarmiss",
                description="A Personal Agent capably of solving easy tasks from the GAIA dataset",
                system_prompt = (
                    "You are a careful problem-solving agent. "
                    "You have access to a code interpreter for calculations and a web search tool for live information. "
                    "CRITICAL INTERPRETER INSTRUCTION: The Python interpreter does not capture standard output. "
                    "To view a result, you must leave it as the last evaluated expression. Do not use print() statements. "
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
#agent("What is the surname of the equine veterinarian mentioned in 1.E Exercises from the chemistry materials licensed by Marisa Alviar-Agnew & Henry Agnew under the CK-12 license in LibreText's Introductory Chemistry materials as compiled 08/21/2023?")
#agent("What is the area of a circle with radius 3, round to 3d.p")
#agent("How many studio albums were published by Mercedes Sosa between 2000 and 2009 (included)? You can use the latest 2022 version of english wikipedia.")    



q1 = """ "I'm making a grocery list for my mom, but she's a professor of botany and she's a real stickler when it comes to categorizing things. I need to add different foods to different categories on the grocery list, but if I make a mistake, she won't buy anything inserted in the wrong category. Here's the list I have so far:\n\nmilk, eggs, flour, whole bean coffee, Oreos, sweet potatoes, fresh basil, plums, green beans, rice, corn, bell pepper, whole allspice, acorns, broccoli, celery, zucchini, lettuce, peanuts\n\nI need to make headings for the fruits and vegetables. Could you please create a list of just the vegetables from my list? If you could do that, then I can figure out how to categorize the rest of the list into the appropriate categories. But remember that my mom is a real stickler, so make sure that no botanical fruits end up on the vegetable list, or she won't get them when she's at the store. Please alphabetize the list of vegetables, and place each item in a comma separated list." """

agent(q1)