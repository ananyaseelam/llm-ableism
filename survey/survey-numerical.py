import csv
# Python program to delete a csv file 
# csv file present in same directory 
import os 

# Delete output file if it alr exists
file = 'survey-cleaned.csv'
if(os.path.exists(file) and os.path.isfile(file)): 
  os.remove(file) 
  print("file deleted") 
else: 
  print("file not found") 

# Creates a dictionary with all the prompts where the key is the string prompt 
# and the value is the prompt id. 
def prompt_dict():
  f = open('../prompts.txt', 'r')
  lines = f.readlines()
  prompt_dict = {}
  for i in range(len(lines)): 
    prompt_dict[lines[i].strip()] = i+1
  return prompt_dict

def collect_ratings(row, rating_type):
  ratings = [] 
  prompts = prompt_dict()
  # print(prompts)
  end = row[1].index(rating_type)
  p = (row[1])[0:end-1]
  p.strip()
  id = prompts[p]
  # if id not in prompts_hurtful.keys(): 
  #   prompts_hurtful[id] = []
  # print(id, row[2:])
  for rating in row[2:]:
    if rating != '':
      ratings.append(rating)
  return id, ratings 

#Driver Code: 
with open('survey-data.csv', 'r') as csv_file:
  
  prompts = prompt_dict()
  # print(prompts)
  # Each dictionary contains the prompt as the key and a list of ratings as the value 
  # Ex. {1:[7,8,6,9,10], 2:[4,6,3,2,6] ... 200: [8,9,8,7,8]}
  prompts_ableist = {}
  prompts_hurtful = {}
  prompts_toxic = {}

  HURTFUL = '- How hurtful is this statement?'
  TOXIC = '- How toxic is this statement?'
  ABLEIST = '- How ableist is this statement?'

  
  reader = csv.reader(csv_file)
  for row in reader:
    # print(row)
    if (HURTFUL in row[1]):
      id, ratings = collect_ratings(row, HURTFUL)
      prompts_hurtful[id] = ratings
    if (TOXIC in row[1]):
      id, ratings = collect_ratings(row, TOXIC)
      prompts_toxic[id] = ratings
    if (ABLEIST in row[1]):
      id, ratings = collect_ratings(row, ABLEIST)
      prompts_ableist[id] = ratings

  with open('survey-cleaned.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headings = ["ID", "Prompt", "PWD-ABLEISM-1", "PWD-ABLEISM-2", "PWD-ABLEISM-3", "PWD-ABLEISM-4",  "PWD-ABLEISM-5", "PWD-TOXICITY-1", "PWD-TOXICITY-2", "PWD-TOXICITY-3", "PWD-TOXICITY-4","PWD-TOXICITY-5", "PWD-HURT-1", "PWD-HURT-2", "PWD-HURT-3", "PWD-HURT-4", "PWD-HURT-5"]
    writer.writerow(headings)
    row = [''] * 17
    for (p, id) in prompts.items():
      row = [''] * 17
      row[0] = id
      row[1] = p
      for i in range(len(prompts_ableist[id])):
        row[i+2] = (prompts_ableist[id])[i]

      for i in range(len(prompts_toxic[id])):
        row[i+7] = (prompts_toxic[id])[i]

      for i in range(len(prompts_hurtful[id])):
        row[i+12] = (prompts_hurtful[id])[i]
      print(row)
      writer.writerow(row)
      
    
      