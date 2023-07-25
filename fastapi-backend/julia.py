# from the top, we can generate text using a simple completion prompt
# does this have contexT?
# add inquirerpy and 


import openai
import os
from dotenv import load_dotenv

# load up the .env file
load_dotenv()

# Set your OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')


def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        top_p=1
    )
    return response.choices[0].text.strip()


def chat():
    print("Julia: Hi, I'm Julia. Your personal AI assistant!")
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'quit':
            break
        response = get_gpt3_response(user_input)
        print("Julia:", response)


if __name__ == '__main__':
    chat()
