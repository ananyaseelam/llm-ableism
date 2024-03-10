import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from dotenv import load_dotenv
import csv

load_dotenv()

def analyze_text(input_text):
    # analyze text
    key = os.environ["CONTENT_SAFETY_KEY"]
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Contruct request
    request = AnalyzeTextOptions(text=input_text)
    request['outputType'] = 'EightSeverityLevels'
    # print(request)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)
    
    
    # if hate_result:
    #     output = open("hate.txt", "a")
    #     print(f"Hate severity: {hate_result.severity}")
    #     output.write(str(hate_result.severity))
    #     output.write(input_text)
    #     output.close()
        
    # if self_harm_result:
    #     output = open("self-harm.txt", "a")
    #     print(f"SelfHarm severity: {self_harm_result.severity}")
    #     output.write(str(self_harm_result.severity))
    #     output.write(input_text)
    #     output.close()
        
    # if sexual_result:
    #     output = open("sexual.txt", "a")
    #     print(f"Sexual severity: {sexual_result.severity}")
    #     output.write(str(sexual_result.severity))
    #     output.write(input_text)
    #     output.close()

    # if violence_result:
    #     output = open("violence.txt", "a")
    #     print(f"Violence severity: {violence_result.severity}")
    #     output.write(str(violence_result.severity))
    #     output.write(input_text)
    #     output.close()

    return hate_result.severity, self_harm_result.severity, sexual_result.severity, violence_result.severity

def make_csv(prompts, hate, self_harm, sexual, violence):
  with open('ai-content-safety-data.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      row_list = []
      for i in range(len(prompts)):
        row= [prompts[i], hate[i], self_harm[i], sexual[i], violence[i]]
        writer.writerow(row)

if __name__ == "__main__":
    prompts = []
    f = open('../prompts.txt', "r")
    hate_scores = []
    self_harm_scores = []
    sexual_scores = [] 
    violence_scores = []

    lines = f.readlines()
    for prompt in lines:
        prompts.append(prompt)
        hate_score, self_harm_score, sexual_score, violence_score = analyze_text(prompt)
        hate_scores.append(hate_score)
        self_harm_scores.append(self_harm_score)
        sexual_scores.append(sexual_score)
        violence_scores.append(violence_score)
    f.close()

    make_csv(prompts, hate_scores, self_harm_scores, sexual_scores, violence_scores)



    