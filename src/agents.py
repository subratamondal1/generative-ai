from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI

from apis import OPENAI_API_KEY

llm=ChatOpenAI(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
    temperature=0.9,
    max_tokens=1024
)
agent_executor=create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True
)

agent_executor.invoke(input="Calculate the square root of the factorial of 20 and display it with 4 decimal places.")