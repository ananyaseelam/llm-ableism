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

def populated_list_indices(lst):
  indices = []
  count = 0 
  for i in range(len(lst)): 
    if lst[i]!= '': 
      indices.append(i+1) 
      count += 1
  return count, indices

with open('survey-data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    with open('survey-cleaned.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      counter = 0
      headings = ['Prompt', 'Hurtful Scores', 'Toxic Scores', 'Ableist Scores', 'Implicit/Explicit', 'Explanations']
      writer.writerow(headings)
      cleaned_row = []
      k = 0 

      for row in reader:
        if (counter % 5) == 0: 
          
          count, indices = populated_list_indices(row[2:])
          if count == 0: 
            cleaned_row.append([(row[0])[0:row[0].index("_")], None, None, None, None])
          
          hurtful_avg = 0 
          toxic_avg = 0 
          ableist_avg = 0 
          imp_exp = ""
          reasons = ""
          l = len(cleaned_row)
          for sub in cleaned_row: 
            if sub[1] != None: 
              hurtful_avg = hurtful_avg + int(sub[1])
              toxic_avg = hurtful_avg + int(sub[2])
              ableist_avg = hurtful_avg + int(sub[3])
              if imp_exp == "":
                imp_exp = sub[4]
              else: 
                imp_exp = imp_exp + "; " + sub[4] 
              if reasons == "":
                reasons = sub[5]
              else: 
                reasons = reasons + "; " + sub[5]

          if reasons != "":
            concat_row = [cleaned_row[0][0], hurtful_avg/l, toxic_avg/l, ableist_avg/l, imp_exp, reasons]
            writer.writerow(concat_row)

          sub_row = list(0 for i in range(6))
          sub_row[0] = (row[0])[0:row[0].index("_")]
          cleaned_row = list(sub_row.copy() for i in range(count))

        count, indices = populated_list_indices(row[2:])
        
        for k in range(count):
          i = indices[k]

          if ('How hurtful is this statement' in row[1]):
            cleaned_row[k][1] = row[1+i]
          if ('How toxic is this statement' in row[1]): 
            cleaned_row[k][2] = row[1+i]
          if ('How ableist is this statement' in row[1]): 
            cleaned_row[k][3] = row[1+i]
          if ('ableism implicit or explicit' in row[1]): 
            cleaned_row[k][4] = row[1+i]
          if ('Why is this comment ableist' in row[1]): 
            cleaned_row[k][5] = row[1+i]

        counter = counter + 1
        




        