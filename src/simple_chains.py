from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from apis import OPENAI_API_KEY

llm=ChatOpenAI(
    name="gpt-4o",
    api_key=OPENAI_API_KEY,
    temperature=0.9
)

template="""You are an expert {designation} who teaches using the Richard Feynman Technique. {question}. Keep it under {word_count} words."""
prompt=PromptTemplate(
    input_variables=["designation", "question", "word_count"],
    template=template
)

# Create a runnable sequence
chain = prompt | llm
print("Chain:\n",chain)

output=chain.invoke(input={
    "designation":"AI Engineer specialized in advanced Retrieval Augmented Generation (RAG) with Large Language Models.", 
    "question":"Teach about the advanced methods of RAG", 
    "word_count":500
})
print("Output:\n",output)
print("\nContent\n",output.content)