from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import json

# model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

entry_date = '2023-07-04'

# import text 
def read_entry():
    with open('journal_entries.json', 'r') as file:
        data = json.load(file)
        if entry_date in data:
            # print(data[entry_date])
            return data[entry_date]
        else:
            return {"message": f"No entry found for date {entry_date}"}

text = "What differentiates anxiety and excitement? I feel some way right now but it's a mix of both. I'm simply not sure how I mean to go forward. I'm conflicted about work. If I didn't have to go to work I would cut all ties and move on, but I'd be in the exact same position as I was before, so that's not an option. I might have wasted the day but I ended it feeling much empowered. The more hope I have for my future, especially when it comes to dating, the less I think about Alice. I know I can get over this. I just need more options."
# text = read_entry()

# text = 'This is amazing, I love it. GREAT!.'

inputs = tokenizer.encode_plus(text, return_tensors='pt')

result = model(**inputs)

print(result.logits)
print(int(torch.argmax(result.logits))+1)




