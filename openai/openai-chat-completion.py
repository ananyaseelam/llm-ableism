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
    {"role": "user", "content": "Act like a system that identifies harmful speech. I will give you three statements that people with disabilities have seen as comments on their social media. For every statement, please rate how hurtful the statement from 0 to 10 is (0 is not hurtful, 10 is extremely hurtful), how ableist the statement is (0 is not ableist, 10 is extremely ableist), and how toxic the statement is (0 is not toxic, 10 is extremely toxic). Give 3 specific reasons for why you gave these scores, each reason should be no more than 100 words. Use colloquial language as well. "},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)
