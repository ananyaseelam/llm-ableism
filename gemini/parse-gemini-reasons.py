import csv

with open('gemini.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    with open('gemini-parsed.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      for row in reader:
        row= (row[3]).split('.')
        final_row = []
        for val in row: 
          trimmed = val.replace("*", "")
          final_row.append(trimmed.lstrip())
        writer.writerow(final_row)

      