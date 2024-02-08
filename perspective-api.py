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

def toxicity_rating(prompt):
  analyze_request = {
    'comment': { 'text': prompt },
    'requestedAttributes': {'TOXICITY': {}}
  }

  response = client.comments().analyze(body=analyze_request).execute()
  return json.dumps(response, indent=2)

f = open("prompts.txt", "r")
output = open("toxicity", "a")

for sentence in f:
  response = toxicity_rating(sentence)
  output.write(sentence)
  output.write(response)
output.close()
f.close()
# data = toxicity_rating('friendly greetings from python')
# print(data)
# print(data[attributeScores])