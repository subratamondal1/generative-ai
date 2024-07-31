from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from apis import OPENAI_API_KEY

# output parser
struct_parser=StrOutputParser()
print(struct_parser)

llm1=ChatOpenAI(
    name="gpt-3.5-turbo",
    api_key=OPENAI_API_KEY,
    temperature=0.9,
    max_tokens=1024
)

prompt1=PromptTemplate(
    input_variables=["input"],
    template="""Solve the math expression: {input}"""
)

chain1=prompt1|llm1|struct_parser
print(chain1)

llm2=ChatOpenAI(
    name="gpt-4o",
    api_key=OPENAI_API_KEY,
    temperature=0.2,
    max_tokens=1024
)

prompt2=PromptTemplate(
    input_variables=["input"],
    template="""Solve the math expression: {input}"""
)

chain2=prompt2|llm2|struct_parser
print(chain2)

sequential_chain=chain1|chain2

output=sequential_chain.invoke(input={
    "input": "5.1**7.3"
})

print(output)