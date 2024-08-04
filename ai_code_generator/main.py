from langchain_openai import ChatOpenAI

from src.apis import OPENAI_API_KEY

llm = ChatOpenAI(
    name = "Code Generator",
    api_key = OPENAI_API_KEY,
    model = "gpt-3.5-turbo-0125"
)
breakpoint()

result = llm.invoke(input="Write me a Poem")
breakpoint()

print(result)
