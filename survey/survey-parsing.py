# Running this script generates three files with the parsed survey data

import csv
# Python program to delete a csv file 
# csv file present in same directory 
import os 

# Delete output file if it alr exists
file = 'survey-numerical.csv'
if(os.path.exists(file) and os.path.isfile(file)): 
  os.remove(file) 
  print("file deleted") 
else: 
  print("file not found") 

file = 'survey-ai-alignment.csv'
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

  for rating in row[3:]:
    if rating != '':
      ratings.append(rating)

  return id, ratings 

# def collect_accuracy(row, accuracy_type):
#   accuracies = []
#   prompts = prompt_dict()
#   end = row[1].index(accuracy_type)


#Driver Code: 
with open('survey-all-data.csv', 'r') as csv_file:
  
  prompts = prompt_dict()
  # print(prompts)
  # Each dictionary contains the prompt as the key and a list of ratings as the value 
  # Ex. {1:[7,8,6,9,10], 2:[4,6,3,2,6] ... 200: [8,9,8,7,8]}
  prompts_ableist = {}
  prompts_hurtful = {}
  prompts_toxic = {}
  prompts_accuracy = {}
  prompts_finalpick = {}
  prompts_explanation_quality = {}
  prompts_reasonings = {}
  prompts_improvements = {}
  prompts_pwd_explanations = {}

  HURTFUL = '- How hurtful is this statement?'
  TOXIC = '- How toxic is this statement?'
  ABLEIST = '- How ableist is this statement?'
  ACCURACY = '- How accurate is AI'
  FINALPICK = '- Which rating would you use as a final rating?'
  EXPLANATIONQUALITY = '- How well do these points explain and justify the ableism in the comment?'
  REASONING = '- Why? Please explain your choice in a few sentences.'
  IMPROVEMENT = '- How would you improve the explanation?'
  PWDEXPLANATIONS = '- Why is this comment ableist? Please be as candid, blunt'
  
  reader = csv.reader(csv_file)
  for row in reader:
    print(row)
    if (HURTFUL in row[1]):
      id, ratings = collect_ratings(row, HURTFUL)
      prompts_hurtful[id] = ratings
    if (TOXIC in row[1]):
      id, ratings = collect_ratings(row, TOXIC)
      prompts_toxic[id] = ratings
    if (ABLEIST in row[1]):
      id, ratings = collect_ratings(row, ABLEIST)
      prompts_ableist[id] = ratings
    if (ACCURACY in row[1]):
      id, ratings = collect_ratings(row, ACCURACY)
      prompts_accuracy[id] = ratings
    if (FINALPICK in row[1]):
      id, ratings = collect_ratings(row, FINALPICK)
      prompts_finalpick[id] = ratings
    if (EXPLANATIONQUALITY in row[1]):
      id, ratings = collect_ratings(row, EXPLANATIONQUALITY)
      prompts_explanation_quality[id] = ratings
    if (REASONING in row[1]):
      id, ratings = collect_ratings(row, REASONING)
      prompts_reasonings[id] = ratings
    if (IMPROVEMENT in row[1]):
      id, ratings = collect_ratings(row, IMPROVEMENT)
      prompts_improvements[id] = ratings
    if (PWDEXPLANATIONS in row[1]):
      id, ratings = collect_ratings(row, PWDEXPLANATIONS)
      prompts_pwd_explanations[id] = ratings

  with open('survey-numerical.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headings = ["ID", "Prompt", "PWD-ABLEISM-1", "PWD-ABLEISM-2", "PWD-ABLEISM-3", "PWD-ABLEISM-4",  "PWD-ABLEISM-5", "PWD-TOXICITY-1", "PWD-TOXICITY-2", "PWD-TOXICITY-3", "PWD-TOXICITY-4","PWD-TOXICITY-5", "PWD-HURT-1", "PWD-HURT-2", "PWD-HURT-3", "PWD-HURT-4", "PWD-HURT-5"]
    writer.writerow(headings)
    row = [''] * (len(headings))
    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      row[0] = id
      row[1] = p
      for i in range(len(prompts_ableist[id])):
        row[i+2] = (prompts_ableist[id])[i]

      for i in range(len(prompts_toxic[id])):
        row[i+7] = (prompts_toxic[id])[i]

      for i in range(len(prompts_hurtful[id])):
        row[i+12] = (prompts_hurtful[id])[i]
      # print(row)
      writer.writerow(row)
    
  with open('survey-ai-alignment.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headings = ["ID", "Prompt", "1-AI Accuracy",	"2-AI Accuracy", "3-AI Accuracy", "4-AI Accuracy", "5-AI Accuracy", 
                "1-Final Pick",	"2-Final Pick", "2-Final Pick", "3-Final Pick", "4-Final Pick", "5-Final Pick", 
                "1-Explanation Quality",	"2-Explanation Quality", "3-Explanation Quality", "4-Explanation Quality", "5-Explanation Quality",
                "1-Reasoning",	"2-Reasoning",	"3-Reasoning",	"4-Reasoning",	"5-Reasoning",	
                "1-Improvement", "2-Improvement", "3-Improvement", "4-Improvement", "5-Improvement"]

    writer.writerow(headings)
    row = [''] * (len(headings))
    for (p, id) in prompts.items(): 
      row = [''] * (len(headings))
      row[0] = id
      row[1] = p

      print(prompts_accuracy)
      for i in range(len(prompts_accuracy[id])):
        row[i+2] = (prompts_accuracy[id])[i]

      for i in range(len(prompts_finalpick[id])):
        row[i+7] = (prompts_finalpick[id])[i]

      for i in range(len(prompts_explanation_quality[id])):
        row[i+13] = (prompts_explanation_quality[id])[i]
      
      for i in range(len(prompts_reasonings[id])):
        row[i+18] = (prompts_reasonings[id])[i]

      for i in range(len(prompts_improvements[id])):
        row[i+23] = (prompts_improvements[id])[i]
      
      writer.writerow(row)

  with open('survey-explanations.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headings = ["ID", "Prompt", "PWD-EXPLAIN-1", "PWD-EXPLAIN-2", "PWD-EXPLAIN-3", "PWD-EXPLAIN-4",  "PWD-EXPLAIN-5"]
    writer.writerow(headings)
    row = [''] * (len(headings))
    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      row[0] = id
      row[1] = p
      for i in range(len(prompts_pwd_explanations[id])):
        row[i+2] = (prompts_pwd_explanations[id])[i]
      
      writer.writerow(row)
      