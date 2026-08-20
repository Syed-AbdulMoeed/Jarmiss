from e2b_code_interpreter import Sandbox
from llama_index.core.tools import FunctionTool
from dotenv import load_dotenv

load_dotenv()

# Define the tool
def execute_python(code: str):
    with Sandbox.create() as sandbox:
        execution = sandbox.run_code(code)
        return execution.text

def execute_python_tool():
    e2b_sandbox_tool = FunctionTool.from_defaults(
        name="execute_python",
        description="Execute python code in a Jupyter notebook cell and return result. To view a result, you must leave it as the last evaluated expression. Do not use print() statements.",
        fn=execute_python
    )
    return e2b_sandbox_tool

