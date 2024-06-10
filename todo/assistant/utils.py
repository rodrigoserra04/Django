import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_ai_suggestions(prompt):
    print("PROMPT:" + prompt)
    api_key = os.getenv('OPENAI_API_KEY')
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}'},
        json={
            'messages': [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Please provide only factual details without interpretation or analysis. Extract the tasks and deadlines and brief descriptions from the following task'" + prompt + "'."
                },
            ],
            'model': 'gpt-4o',
            'max_tokens': 500
        }
    )
    response_data = response.json()
    print("Response: ", response_data)
    return response_data.get('choices')[0].get('message').get('content')