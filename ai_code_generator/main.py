import argparse

from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.apis import OPENAI_API_KEY

parser = argparse.ArgumentParser()
parser.add_argument("--task", default="Return a List of numbers")
parser.add_argument("--language", default="Python")
args = parser.parse_args()

llm = ChatOpenAI(
    name = "Code Generator",
    api_key = OPENAI_API_KEY,
    model = "gpt-3.5-turbo-0125"
)

code_prompt = PromptTemplate(
    template="Write a very short {language} function that would {task}.",
    input_variables = ["language", "task"]
)

test_code_prompt = PromptTemplate(
    template = "Can you help me write a test for the {language} code:\n{code}.",
    input_variables = ["language", "code"]
)

# Legacy Chaining
legacy_chain = LLMChain(
    prompt = code_prompt,
    llm = llm,
    output_key = "code" # will go as input to the next chain
)

legacy_test_chain = LLMChain(
    prompt = test_code_prompt,
    llm = llm,
    output_key = "test"
)

# legacy sequential chaining
legacy_sequential_chain = SequentialChain(
    chains = [legacy_chain, legacy_test_chain],
    input_variables = ["language", "task"],
    output_variables = ["code", "test"]
)

legacy_sequential_result = legacy_sequential_chain.invoke(
    input = {
        "language":"Python",
        "task":"print the fibbonacci sequence"
    }
)
print(legacy_sequential_result, "\n", "="*100)

# Latest Chaining with LCEL 
lcel_code_chain = code_prompt | llm | StrOutputParser()
lcel_test_code_chain = test_code_prompt | llm | StrOutputParser()

breakpoint()

lcel_sequential_chain = (
    {
        "code": lcel_code_chain,
        "language": RunnablePassthrough()
    }
    | lcel_test_code_chain
)

# Invoke the LCEL chain
lcel_result = lcel_sequential_chain.invoke(
    input = {
        "language": args.language,
        "task": args.task
    }
)
breakpoint()

print(lcel_result)