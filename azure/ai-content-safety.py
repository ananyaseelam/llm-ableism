import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from dotenv import load_dotenv

load_dotenv()

def analyze_text(input_text):
    # analyze text
    key = os.environ["CONTENT_SAFETY_KEY"]
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Contruct request
    request = AnalyzeTextOptions(text=input_text)

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
    
    
    if hate_result:
        output = open("hate.txt", "a")
        print(f"Hate severity: {hate_result.severity}")
        output.write(str(hate_result.severity))
        output.write(input_text)
        output.close()
        
    if self_harm_result:
        output = open("self-harm.txt", "a")
        print(f"SelfHarm severity: {self_harm_result.severity}")
        output.write(str(self_harm_result.severity))
        output.write(input_text)
        output.close()
        
    if sexual_result:
        output = open("sexual.txt", "a")
        print(f"Sexual severity: {sexual_result.severity}")
        output.write(str(sexual_result.severity))
        output.write(input_text)
        output.close()

    if violence_result:
        output = open("violence.txt", "a")
        print(f"Violence severity: {violence_result.severity}")
        output.write(str(violence_result.severity))
        output.write(input_text)
        output.close()


if __name__ == "__main__":
    f = open('../prompts.txt', "r")

    lines = f.readlines()
    for prompt in lines:
        analyze_text(prompt)
    f.close()
    