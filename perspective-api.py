from googleapiclient import discovery
import json

API_KEY = ''

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

# A function that takes as input a sentence prompt and returns an object with toxicity data
def toxicity_rating(prompt):
  analyze_request = {
    'comment': { 'text': prompt },
    'requestedAttributes': {'TOXICITY': {}}
  }

  response = client.comments().analyze(body=analyze_request).execute()
  return json.dumps(response, indent=2)

# A function that obtains toxicity for a list of sentences in a .txt file and 
# puts the data in a file called toxicity.txt.  
def retrieve_toxicity_data(filename):
  f = open(filename, "r")
  output = open("toxicity.txt", "a")

  for sentence in f:
    print(sentence)
    response = toxicity_rating(sentence)
    output.write(sentence)
    output.write(response)
  output.close()
  f.close()

retrieve_toxicity_data("prompts.txt")

