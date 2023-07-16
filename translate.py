import openai
import csv
import time
import pandas as pd
import json

# Set up the OpenAI API client
openai.api_key = "" # Replace with your API key
model_engine = "gpt-3.5-turbo" # Replace with the engine ID of your choice

# Function to translate a text using the OpenAI API
def translate(text):
    response = openai.Completion.create(
        engine=model_engine,
        prompt="Translate the following text from English to Arabic: \n" + text + "\n\nTranslation:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def ChatTranslation(text):

    prompt = f"Translate the values in this JSON text from English to Arabic, while keeping the keys as they are and preserving any code blocks:{text}"
    response = None

    response = openai.ChatCompletion.create(
    model=model_engine,
    messages=[{"role":"user", "content":prompt}],
    max_tokens=1024,
    temperature=0.7,
)
    return response.choices[0].message.content


# Open the CSV file for reading
with open('/media/khalid/HDD2/instructionsDS/alpaca.csv', 'r', encoding='utf-8') as input_file:
    reader = csv.reader(input_file)
    headers = next(reader) # Save the headers
    rows = list(reader) # Read the remaining rows


# Translate the text in each row
response_list = []
for row in rows:
    response = ChatTranslation({"instruction": row[1], "input": row[2], "output": row[3] }) # Assumes the text is in the first column of each ro
    s = response.replace("\'", "\"")
    dictData= json.loads(s)
    response_list.append(dictData)


df = pd.DataFrame(response_list, columns=['instruction','input','output'])
df.to_json(f'/media/khalid/HDD2/instructionsDS/alpaca_translation2.json',
            force_ascii=False,
            orient='records',
            lines=True)
