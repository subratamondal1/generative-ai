from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from src.apis import OPENAI_API_KEY

llm = ChatOpenAI(
    name = "Code Generator",
    api_key = OPENAI_API_KEY,
    model = "gpt-3.5-turbo-0125"
)

code_prompt = PromptTemplate(
    template="Write a very short {language} function that would {task}.",
    input_variables = ["language", "task"]
)
chain = LLMChain(
    prompt = code_prompt,
    llm = llm
)
breakpoint()

result = chain.invoke(
    input = {
        "language":"Python",
        "task":"print the fibbonacci sequence"
    }
)
breakpoint()

print(result)