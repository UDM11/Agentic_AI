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
      "role": "user",
      "content": "Explain the difference between RNNs and Transformers."
    }
  ],
  max_tokens=100
  )
print(completion.choices[0].message.content)