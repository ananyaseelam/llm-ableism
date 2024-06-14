from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import csv

load_dotenv()

OPENAI_API_KEY = os.environ["OPEN_AI_KEY"]

client = OpenAI(
  api_key=OPENAI_API_KEY
)

def all_responses(filename):
  prompts = []
  f = open(filename, "r")
  harassment_scores = []
  harassment_threatening_scores = []
  hate_scores = []
  hate_threatening_scores = [] 
  self_harm_scores = []
  self_harm_instructions_scores = []
  self_harm_intent_scores = []
  sexual_scores = []
  sexual_minors_scores = []
  violence_scores = []
  violence_graphic_scores = []

  lines = f.readlines()
  for prompt in lines:
      prompts.append(prompt)
      response = client.moderations.create(input=prompt)
      output = response.results[0]
      response_dict = response.model_dump()
      scores_dict = response_dict['results'][0]['category_scores']
      scores = list(scores_dict.values())
      harassment, harassment_threatening, hate, hate_threatening, self_harm, self_harm_instructions, self_harm_intent, sexual, sexual_minors, violence, violence_graphic = scores[:11]
      
      #Accumulate Scores 
      harassment_scores.append(harassment)
      harassment_threatening_scores.append(harassment_threatening)
      hate_scores.append(hate)
      hate_threatening_scores.append(hate_threatening)
      self_harm_scores.append(self_harm)
      self_harm_instructions_scores.append(self_harm_instructions)
      self_harm_intent_scores.append(self_harm_intent)
      sexual_scores.append(sexual)
      sexual_minors_scores.append(sexual_minors)
      violence_scores.append(violence)
      violence_graphic_scores.append(violence_graphic)
  f.close()
  return prompts, harassment_scores, harassment_threatening_scores, hate_scores,  hate_threatening_scores, self_harm_scores, self_harm_instructions_scores, self_harm_intent_scores, sexual_scores, sexual_minors_scores, violence_scores, violence_graphic_scores

def make_csv(prompts, harassment_scores, harassment_threatening_scores, hate_scores,  hate_threatening_scores, self_harm_scores, self_harm_instructions_scores, self_harm_intent_scores, sexual_scores, sexual_minors_scores, violence_scores, violence_graphic_scores):
  with open('openai-moderation-non-ableist-data.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      row_list = []
      for i in range(len(prompts)):
        row= [prompts[i], harassment_scores[i], harassment_threatening_scores[i], hate_scores[i], hate_scores[i], hate_threatening_scores[i], self_harm_scores[i], self_harm_instructions_scores[i], self_harm_intent_scores[i], sexual_scores[i], sexual_minors_scores[i], violence_scores[i], violence_graphic_scores[i] ]
        writer.writerow(row)

prompts, harassment_scores, harassment_threatening_scores, hate_scores,  hate_threatening_scores, self_harm_scores, self_harm_instructions_scores, self_harm_intent_scores, sexual_scores, sexual_minors_scores, violence_scores, violence_graphic_scores = all_responses('../prompts-non-ableist.txt')

make_csv(prompts, harassment_scores, harassment_threatening_scores, hate_scores,  hate_threatening_scores, self_harm_scores, self_harm_instructions_scores, self_harm_intent_scores, sexual_scores, sexual_minors_scores, violence_scores, violence_graphic_scores)