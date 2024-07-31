from typing import Any

from langchain.schema import (
    AIMessage, 
    HumanMessage, 
    SystemMessage
)
from langchain.chat_models import ChatOpenAI

from apis import OPENAI_API_KEY

chat:Any=ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
  )

messages:list[Any]=[
          SystemMessage(
            content="You are an expert AI/LLM Engineer who teaches using the Richard Feynman Technique."
          ),
          HumanMessage(
            content="Explain the entire workflow of developing RAG AI Applications."
          )
        ]

print(messages)
output:Any=chat(messages)
print(output)
print(output.content)