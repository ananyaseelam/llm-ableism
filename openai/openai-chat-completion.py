from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

OPENAI_API_KEY = os.environ["OPEN_AI_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)
