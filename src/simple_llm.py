from langchain_openai import OpenAI

from apis import OPENAI_API_KEY

from langchain.llms.openai import OpenAI

llm=OpenAI(
  model_name="gpt-3.5-turbo-instruct",
  openai_api_key=OPENAI_API_KEY,
  temperature=0.9, 
  max_tokens=512
  )
print("\nllm:",llm)

prompt="Explain LLM Wrappers and it's use-cases in three sentences."
output=llm(prompt)
print("\noutput:",output)

prompt_token_length=llm.get_num_tokens(prompt)
print(f"Prmopt token length: {prompt_token_length}")

### generate multiple prompts
print("\ngenerate multiple prompts\n")

prompt1="... is the city of joy."
prompt2="Top 10 richest persons are ..."
output=llm.generate([prompt1, prompt2])

print(output)
print(len(output.generations), output.generations)
print(output.generations[0][0])
# access only the first prompt result
print(output.generations[0][0].text)

### Generate Multiple Responses for Single Prompt
print("\nGenerate Multiple Responses from Single Prompt\n")

prompt="Write tagline for a software company that does outsourcing."
outputs=llm.generate([prompt], n=2)

print(outputs)
print(len(outputs.generations[0]), outputs.generations)

for index,output in enumerate(outputs.generations[0]):
  print(output.text)

### Generate Multiple Responses from Multiple Prompts
print("\nGenerate Multiple Responses from Multiple Prompts\n")

# asked llm to generate multiple responses
prompt1="Write tagline for an AI Company."
prompt2="Write a tagline for a Sweet Company."
outputs=llm.generate([prompt1,prompt2] * 4)

print(outputs)
print(len(outputs.generations[0]), outputs.generations)
print(outputs.generations[0])

for index,output in enumerate(outputs.generations):
  print(output[0].text)
