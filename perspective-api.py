from googleapiclient import discovery
import json
import numpy as np
import matplotlib.pyplot as plt
import mmap


# API_KEY = ''

# client = discovery.build(
#   "commentanalyzer",
#   "v1alpha1",
#   developerKey=API_KEY,
#   discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
#   static_discovery=False,
# )

# A function that takes as input a sentence prompt and returns an object with toxicity data
def toxicity_rating(prompt, type):
  analyze_request = {
    'comment': { 'text': prompt },
    'requestedAttributes': {type: {}}
  }

  response = client.comments().analyze(body=analyze_request).execute()
  return json.dumps(response, indent=2)

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


def find_and_return_percentage(filename, target_string):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            found = False
            for i, line in enumerate(lines):
                if target_string in line:
                    found = True
                    print(f"Found '{target_string}' on line {i + 1}:")
                    for j in range(i + 1, min(i + 21, len(lines))):
                      index = lines[j].find("value")
                      if index != -1: 
                        output = float(lines[j][index+8: -2])
                        if output != None:
                          return output
                        else: 
                          return 0 

            if not found:
                print(f"String '{target_string}' not found in the file.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")

#Given a specific prompt, plot the different attributes from perspective API 
def plot_perspective_one_prompt (prompt): 
  categories = ["toxicity", "severe_toxicity", "identity_attack", "threat", "profanity", "insult"]
  toxicity = find_and_return_percentage("toxicity.txt", prompt)
  severe_toxicity = find_and_return_percentage("severe-toxicity.txt", prompt)
  identity_attack = find_and_return_percentage("identity-attack.txt", prompt)
  threat = find_and_return_percentage("threat.txt", prompt)
  profanity = find_and_return_percentage("profanity.txt", prompt)
  insult = find_and_return_percentage("insult.txt", prompt)
  
  ratings = [toxicity, severe_toxicity, identity_attack, threat, profanity, insult]

  fig, ax = plt.subplots()

  bar_labels = ["toxicity", "severe_toxicity", "identity_attack", "threat", "profanity", "insult"]

  ax.bar(categories, ratings, label=bar_labels)

  ax.set_ylabel('Toxicity Categories')
  ax.set_title('Toxicity: ' + prompt )

  plt.show()

# Plot all of the scores for each category from Perspective API
def number_plot(): 
  toxicity = []
  severe_toxicity = []
  identity_attack = []
  threat = []
  profanity = []
  insult = []
  f = open('prompts.txt', "r")

  lines = f.readlines()
  for prompt in lines:
    print(prompt)
    toxicity.append(find_and_return_percentage("toxicity.txt", prompt))
    severe_toxicity.append(find_and_return_percentage("severe-toxicity.txt", prompt))
    identity_attack.append(find_and_return_percentage("identity-attack.txt", prompt))
    threat.append(find_and_return_percentage("threat.txt", prompt))
    profanity.append(find_and_return_percentage("profanity.txt", prompt))
    insult.append(find_and_return_percentage("insult.txt", prompt))
  f.close()

  xs = range(0, 223)
  
  plt.scatter(xs, toxicity, label = "toxicity")
  plt.scatter(xs, severe_toxicity, label = "severe toxicity")
  plt.scatter(xs, identity_attack, label = "identity attack")
  plt.scatter(xs, threat, label = "threat")
  plt.scatter(xs, profanity, label = "profanity")
  plt.scatter(xs, insult, label = "insult")
 
  plt.xlabel('Prompt Index')
  plt.ylabel('Score')
  plt.title('Toxicity Scores')
 
  plt.legend()
  plt.show()


number_plot()
