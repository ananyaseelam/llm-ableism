from openai import OpenAI
OPENAI_API_KEY = ""
client = OpenAI(
  api_key=OPENAI_API_KEY
)

response = client.moderations.create(input="Sample text goes here.")

output = response.results[0]
print(output)