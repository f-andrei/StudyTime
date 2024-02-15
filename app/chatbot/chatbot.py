from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

GPT_MODEL = "gpt-3.5-turbo"
MAX_HISTORY_LENGTH = 10

TOKEN = os.getenv('OPENAI_TOKEN')
client = OpenAI(api_key=f"{TOKEN}")

def save_context_to_json(context):
    context = context[-MAX_HISTORY_LENGTH:]
    with open('app\database\context.json', 'w') as file:
        json.dump(context, file, indent=2, separators=(',', ':'), ensure_ascii=True)


def load_json_context():
    try:
        with open('app\database\context.json', 'r') as file:
            content = json.load(file)
            return content
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Empty file or JSON decoding error: {e}")
        return [{"role": "system", "content": "You are an helpful assistant that will help with studies and tasks."}]


context_history = load_json_context()

def gpt_api(user_message, model=GPT_MODEL):
    context = load_json_context()
    context.append({"role": "user", "content": user_message})
    completion = client.chat.completions.create(
        model=model,
        messages=context,
        max_tokens=1000
    )
    chatbot_output = completion.choices[0].message.content
    context.append({"role": "assistant", "content": chatbot_output})
    save_context_to_json(context)
    return f'GPT: {chatbot_output}'

async def chat(message):
    response = gpt_api(message)
    return response





