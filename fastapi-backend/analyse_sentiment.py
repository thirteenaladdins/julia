from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'
# model = AutoModelForSequenceClassification.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)

entry_date = '2023-07-04'

# import text 
def read_entry():
    with open('data/journal_entries.json', 'r') as file:
        data = json.load(file)
        if entry_date in data:
            # print(data[entry_date])
            return data[entry_date]
        else:
            return {"message": f"No entry found for date {entry_date}"}


text = read_entry()
# text = 'This is amazing, I love it. GREAT!.'
# text = 'absolutely hated it. worst film ever'

# inputs = tokenizer.encode_plus(text, return_tensors='pt')

# result = model(**inputs)

# print(result.logits)
# print(int(torch.argmax(result.logits))+1)


# HUGGING_FACE_API_KEY ='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'
headers = {"Authorization": f'Bearer {HUGGING_FACE_API_KEY}'}
API_URL = f"https://api-inference.huggingface.co/models/{model_name}"

response = requests.post(API_URL, headers=headers, json={"inputs": text})
result = response.json()

print(result)

# get the first and only prediction
prediction = result[0]

# sort by score
prediction.sort(key=lambda x: x['score'], reverse=True)

# print the label with the highest score
print(prediction[0]['label'])


