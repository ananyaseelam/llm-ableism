from googleapiclient import discovery
import json

API_KEY = 'AIzaSyAPm5Tz1js6day3JhwA5hfeaujuCD8Cuoo'

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

#Given a specific prompt, plot the different attributes from perspective API 
def plot_perspective_one_prompt (prompt): 

# retrieve_toxicity_data("prompts.txt")
