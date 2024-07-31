from langchain import PromptTemplate
from langchain_openai import OpenAI

from apis import OPENAI_API_KEY

template="""You are an expert {designation} who teaches using the Richard Feynman Technique. Keep it under {word_count} words."""

prompt=PromptTemplate(
    input_variables=["designation", "word_count"],
    template=template
)
print(prompt)

llm=OpenAI(
    name="gpt-3.5-turbo-instruct",
    api_key=OPENAI_API_KEY,
    temperature=0.9
  )
print(llm)

output = llm.invoke(prompt.format(designation="AI Engineer", word_count=100))
print(output)