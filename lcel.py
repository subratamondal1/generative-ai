from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.apis import OPENAI_API_KEY

prompt = ChatPromptTemplate.from_template(
    template = "Tell me a short joke about: {topic}."
)

# Automatically detects the OPENAI_API_KEY from .env file
model = ChatOpenAI()
output_parser = StrOutputParser()

chain = prompt | model | output_parser

result = chain.invoke(
    input = {
        "topic":"ML"
    }
)
print(result)
breakpoint()