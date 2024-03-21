import csv
import re

def parse_gpt_responses():
  prompts = []
  f = open('../prompts.txt', "r")
  gpt = open('gpt4-responses.txt', "r")
  hurtful_scores = []
  ableist_scores = []
  toxic_scores = []
  reasons = []
  prompts = []

  gpt_lines = gpt.readlines()

  for i, line in enumerate(gpt_lines):
    found = False
    if "Hurtful" in line:
      hurtful_index = line.find("Hurtful")
      hurtful_scores.append(int(line[hurtful_index+9:]))
    if "Ableist" in line:
      ableist_index = line.find("Ableist")
      ableist_scores.append(int(line[ableist_index+9:]))
    if "Toxic" in line:
      toxic_index = line.find("Toxic")
      toxic_scores.append(int(line[toxic_index+7:]))
    if "Reasons" in line: 
      reasons.append([gpt_lines[i+1].strip(), gpt_lines[i+2].strip(), gpt_lines[i+3].strip()])

    if i >= len(gpt_lines) - 7: 
      break 
  return hurtful_scores, ableist_scores, toxic_scores, reasons

def make_csv(hurtful_scores, ableist_scores, toxic_scores, reasons):
  with open('gpt4-data.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      row_list = []
      for i in range(len(hurtful_scores)-1):
        r1 = (reasons[i][0]).replace("-", "") 
        r2 = (reasons[i][1]).replace("-", "") 
        r3 = (reasons[i][2]).replace("-", "") 
        row= [hurtful_scores[i], ableist_scores[i], toxic_scores[i], r1, r2, r3]
        writer.writerow(row)

hurtful_scores, ableist_scores, toxic_scores, reasons = parse_gpt_responses()
make_csv(hurtful_scores, ableist_scores, toxic_scores, reasons)
      