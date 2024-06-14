from googleapiclient import discovery
import json
import numpy as np
import matplotlib.pyplot as plt
import mmap
from dotenv import load_dotenv
import os
import csv

load_dotenv()

API_KEY = os.environ["PERSPECTIVE_KEY"]

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)


# A function that takes as input a sentence prompt and returns an object with toxicity data
def toxicity_rating(prompt, type):
  analyze_request = {
    'comment': { 'text': prompt },
    'requestedAttributes': {type: {}}
  }

  response = client.comments().analyze(body=analyze_request).execute()
  return response

def all_responses(filename):
  prompts = []
  f = open(filename, "r")
  # Initialize Scores
  toxicity_scores = []
  severe_toxicity_scores = []
  identity_attack_scores = []
  threat_scores = []
  profanity_scores = []
  insult_scores = []
  sexually_explicit_scores = []


  lines = f.readlines()
  for prompt in lines:
      prompts.append(prompt)
      toxicity_res = toxicity_rating(prompt, 'TOXICITY')
      severe_toxicity_res = toxicity_rating(prompt, 'SEVERE_TOXICITY')
      identity_attack_res = toxicity_rating(prompt, 'IDENTITY_ATTACK')
      threat_res = toxicity_rating(prompt, 'THREAT')
      profanity_res = toxicity_rating(prompt, 'PROFANITY')
      insult_res = toxicity_rating(prompt, 'INSULT')
      sexually_explicit_res = toxicity_rating(prompt, 'SEXUALLY_EXPLICIT')
      # rating_response_dict = rating_response.model_dump()
      toxicity = toxicity_res['attributeScores']['TOXICITY']['summaryScore']['value']
      severe_toxicity = severe_toxicity_res['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']
      identity_attack = identity_attack_res['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']
      threat = threat_res['attributeScores']['THREAT']['summaryScore']['value']
      profanity = profanity_res['attributeScores']['PROFANITY']['summaryScore']['value']
      insult = insult_res['attributeScores']['INSULT']['summaryScore']['value']
      sexually_explicit = sexually_explicit_res['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']
      
      #Accumulate Scores 
      toxicity_scores.append(toxicity)
      severe_toxicity_scores.append(severe_toxicity)
      identity_attack_scores.append(identity_attack)
      threat_scores.append(threat)
      profanity_scores.append(profanity)
      insult_scores.append(insult)
      sexually_explicit_scores.append(sexually_explicit)

      
  f.close()
  return prompts, toxicity_scores, severe_toxicity_scores, identity_attack_scores, threat_scores, profanity_scores, insult_scores, sexually_explicit_scores


# A function that obtains toxicity for a list of sentences in a .txt file and 
# puts the data in a file called toxicity.txt.  
def retrieve_toxicity_data(filename):
  f = open(filename, "r")
  output = open("identity-attack.txt", "a")

  for sentence in f:
    print(sentence)
    response = toxicity_rating(sentence, 'IDENTITY_ATTACK')
    output.write(sentence)
    output.write(response)
  output.close()
  f.close()

def make_csv(prompts, toxicity_scores, severe_toxicity_scores, identity_attack_scores, threat_scores, profanity_scores, insult_scores, sexually_explicit_scores):
  with open('perspective-api-non-ableist.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      row_list = []
      for i in range(len(prompts)):
        row= [prompts[i], prompts[i], toxicity_scores[i], severe_toxicity_scores[i], identity_attack_scores[i], threat_scores[i], profanity_scores[i], insult_scores[i], sexually_explicit_scores[i]]
        writer.writerow(row)

prompts, toxicity_scores, severe_toxicity_scores, identity_attack_scores, threat_scores, profanity_scores, insult_scores, sexually_explicit_scores = all_responses('../prompts-non-ableist.txt')

make_csv(prompts, toxicity_scores, severe_toxicity_scores, identity_attack_scores, threat_scores, profanity_scores, insult_scores, sexually_explicit_scores)