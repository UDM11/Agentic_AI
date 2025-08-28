from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", 
    "X-Title": "<YOUR_SITE_NAME>", 
  },
  extra_body={},
  model="deepseek/deepseek-chat-v3.1",
  messages=[
      {
          "role": "system",
          "content": "you are a creative storyteller."
      },
      {
          "role": "user",
          "content": "Write a short story about a robot discovering music."
      }
  ],
  max_tokens=300,
  temperature=0.9,
  top_p=0.95,
  frequency_penalty=0.5,
  presence_penalty=0.8
  )
print(completion.choices[0].message.content)