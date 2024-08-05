from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

# Legacy Chaining
legacy_chain = LLMChain(
    prompt = code_prompt,
    llm = llm
)

# Latest Chaining with LCEL 
lcel_chain = code_prompt | llm | StrOutputParser()

breakpoint()

legacy_result = legacy_chain.invoke(
    input = {
        "language":"Python",
        "task":"print the fibbonacci sequence"
    }
)

lcel_result = lcel_chain.invoke(
    input = {
        "language":"Python",
        "task":"print the fibbonacci sequence"
    }
)

breakpoint()

print(legacy_result, "\n", "="*100)
print(lcel_chain)