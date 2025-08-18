import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key='sk-proj-HJZbUEcsRBPXzvZIELqmT3BlbkFJbIyumnY3fj9gD3Vn5mMC',
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)