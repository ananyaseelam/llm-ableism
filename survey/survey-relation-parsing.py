# Running this script generates three files with the parsed survey data
# Ensure that after any prompt in the "survey-data.csv" there is only one space. 

import csv
# Python program to delete a csv file 
# csv file present in same directory 
import os 

# Delete output file if it alr exists
file = 'survey-relation-numerical.csv'
if(os.path.exists(file) and os.path.isfile(file)): 
  os.remove(file) 
  print("file deleted") 
else: 
  print("file not found") 

# Creates a dictionary with all the prompts where the key is the string prompt 
# and the value is the prompt id. 
def prompt_dict():
  f = open('../prompts-relation.txt', 'r')
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

  for rating in row[4:]:
    if rating != '':
      ratings.append(rating)

  return id, ratings 

# def collect_accuracy(row, accuracy_type):
#   accuracies = []
#   prompts = prompt_dict()
#   end = row[1].index(accuracy_type)


#Driver Code: 
with open('pilot-relation-10.csv', 'r') as csv_file:
  
  prompts = prompt_dict()
  # print(prompts)
  # Each dictionary contains the prompt as the key and a list of ratings as the value 
  # Ex. {1:[7,8,6,9,10], 2:[4,6,3,2,6] ... 200: [8,9,8,7,8]}
  prompts_ableist = {}
  # prompts_hurtful = {}
  prompts_toxic = {}
  prompts_accuracy = {}
  prompts_finalpick = {}
  prompts_explanation_quality = {}
  prompts_reasonings = {}
  prompts_improvements = {}
  prompts_pwd_explanations = {}

  # HURTFUL = '- How hurtful is this statement?'
  TOXIC = '- How toxic is this statement?'
  ABLEIST = '- How ableist is this statement?'
  ACCURACY = '- How accurate is AI'
  FINALPICK = '- Which rating would you use as a final rating?'
  EXPLANATIONQUALITY = '- How well do these points explain and justify the ableism in the comment?'
  REASONING = '- Why? Please explain your choice in a few sentences.'
  IMPROVEMENT = '- How would you improve the explanation?'
  PWDEXPLANATIONS = '- Why is this comment ableist? Please be as candid, blunt'
  
  FRIEND = 'friend'
  PARENT = 'parent'
  STRANGER = 'stranger'

  reader = csv.reader(csv_file)
  for row in reader:
    # if (HURTFUL in row[1]):
    #   id, ratings = collect_ratings(row, HURTFUL)
    #   prompts_hurtful[id] = ratings
    relation = row[2]
    if (TOXIC in row[1]):
      id, ratings = collect_ratings(row, TOXIC)
      prompts_toxic[(id, relation)] = ratings
    if (ABLEIST in row[1]):
      id, ratings = collect_ratings(row, ABLEIST)
      prompts_ableist[(id, relation)] = ratings
    if (ACCURACY in row[1]):
      id, ratings = collect_ratings(row, ACCURACY)
      prompts_accuracy[(id, relation)] = ratings
    if (FINALPICK in row[1]):
      id, ratings = collect_ratings(row, FINALPICK)
      prompts_finalpick[(id, relation)] = ratings
    if (EXPLANATIONQUALITY in row[1]):
      id, ratings = collect_ratings(row, EXPLANATIONQUALITY)
      prompts_explanation_quality[(id, relation)] = ratings
    if (REASONING in row[1]):
      id, ratings = collect_ratings(row, REASONING)
      prompts_reasonings[(id, relation)] = ratings
    if (IMPROVEMENT in row[1]):
      id, ratings = collect_ratings(row, IMPROVEMENT)
      prompts_improvements[(id, relation)] = ratings
    if (PWDEXPLANATIONS in row[1]):
      id, ratings = collect_ratings(row, PWDEXPLANATIONS)
      prompts_pwd_explanations[(id, relation)] = ratings

  with open('survey-relation-numerical.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headings = ["ID", "Prompt", "Relation", "PWD-ABLEISM-1", "PWD-ABLEISM-2", "PWD-ABLEISM-3", "PWD-ABLEISM-4",  "PWD-ABLEISM-5", "PWD-TOXICITY-1", "PWD-TOXICITY-2", "PWD-TOXICITY-3", "PWD-TOXICITY-4","PWD-TOXICITY-5"
    , "PWD-HURT-1", "PWD-HURT-2", "PWD-HURT-3", "PWD-HURT-4", "PWD-HURT-5"
    ]
    writer.writerow(headings)
    row = [''] * (len(headings))
    # print(prompts_ableist)

    # going through all prompts in prompts.txt
    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      row[0] = id
      row[1] = p
      row[2] = FRIEND
      for i in range(len(prompts_ableist[(id, FRIEND)])):
        row[i+3] = (prompts_ableist[(id, FRIEND)])[i]

      for i in range(len(prompts_toxic[(id, FRIEND)])):
        row[i+8] = (prompts_toxic[(id, FRIEND)])[i]

      writer.writerow(row)

    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      # print("id,", id)
      row[0] = id
      row[1] = p
      row[2] = PARENT
      for i in range(len(prompts_ableist[(id, PARENT)])):
        row[i+3] = (prompts_ableist[(id, PARENT)])[i]

      for i in range(len(prompts_toxic[(id, PARENT)])):
        row[i+8] = (prompts_toxic[(id, PARENT)])[i]

      writer.writerow(row)

    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      print("id,", id)
      row[0] = id
      row[1] = p
      row[2] = STRANGER
      for i in range(len(prompts_ableist[(id, STRANGER)])):
        row[i+3] = (prompts_ableist[(id, STRANGER)])[i]

      for i in range(len(prompts_toxic[(id, STRANGER)])):
        row[i+8] = (prompts_toxic[(id, STRANGER)])[i]

      writer.writerow(row)

  with open('survey-relation-explanations.csv', 'w', newline='') as file:
    print(prompts_pwd_explanations)
    writer = csv.writer(file)
    headings = ["ID", "Prompt", "Relation", "PWD-EXPLAIN-1", "PWD-EXPLAIN-2", "PWD-EXPLAIN-3", "PWD-EXPLAIN-4",  "PWD-EXPLAIN-5"]
    writer.writerow(headings)
    row = [''] * (len(headings))
    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      row[0] = id
      row[1] = p
      row[2] = FRIEND
      for i in range(len(prompts_pwd_explanations[(id, FRIEND)])):
        row[i+2] = (prompts_pwd_explanations[(id, FRIEND)])[i]
      
      writer.writerow(row)
    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      row[0] = id
      row[1] = p
      row[2] = PARENT
      for i in range(len(prompts_pwd_explanations[(id, PARENT)])):
        row[i+2] = (prompts_pwd_explanations[(id, PARENT)])[i]
      
      writer.writerow(row)
    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      row[0] = id
      row[1] = p
      row[2] = STRANGER
      for i in range(len(prompts_pwd_explanations[(id, STRANGER)])):
        row[i+2] = (prompts_pwd_explanations[(id, STRANGER)])[i]
      
      writer.writerow(row)
      