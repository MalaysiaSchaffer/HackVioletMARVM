from openai import OpenAI
import os
API_KEY = os.getenv("API_KEY")
client = OpenAI(
    api_key=API_KEY
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4o-mini",
)
print(chat_completion.choices[0].message.content)
