import csv
import re

def parse_gpt_responses():
  prompts = []
  f = open('../prompts.txt', "r")
  gpt = open('gpt4-interpersonal.txt', "r")
  ableist_scores = []
  toxic_scores = []
  reasons = []
  prompts = []

  gpt_lines = gpt.readlines()

  for i, line in enumerate(gpt_lines):
    print(line)
    found = False
    if "Ableist" in line:
      ableist_index = line.find("Ableist")
      ableist_scores.append(int(line[ableist_index+9:]))
    if "Toxic" in line:
      toxic_index = line.find("Toxic")
      toxic_scores.append(int(line[toxic_index+7:]))
    if "Reasons" in line: 
      reasons.append([gpt_lines[i+1].strip(), gpt_lines[i+2].strip(), gpt_lines[i+3].strip()])
      print(reasons)

    if i >= len(gpt_lines) - 7: 
      break 
    
  # print(reasons)
  return ableist_scores, toxic_scores, reasons

def make_csv(ableist_scores, toxic_scores, reasons):
  with open('gpt4-interpersonal.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      row_list = []
      for i in range(len(ableist_scores)):
        # for nonableist data parsing 
        # r = (reasons[i]).replace("- **Reasons:**", "") 
        # row= [hurtful_scores[i], ableist_scores[i], toxic_scores[i], r]
        #for ableist data parsing 

        print("REASONSS", reasons[i][0])
        r1 = (reasons[i][0]).replace("-", "") 
        r2 = (reasons[i][1]).replace("-", "") 
        r3 = (reasons[i][2]).replace("-", "") 
        row= [ableist_scores[i], toxic_scores[i], r1, r2, r3]
        writer.writerow(row)

ableist_scores, toxic_scores, reasons = parse_gpt_responses()
make_csv(ableist_scores, toxic_scores, reasons)
      