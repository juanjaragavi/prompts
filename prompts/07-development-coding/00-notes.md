# **Development Notes:**

We are currently working on the `Users/MacBookPro/GitHub` directory, which contains all of our local GitHub repositories and projects. Help me create a Next.js application that generates a futuristic, minimalist, tool- and skill-rich chatbot wrapped around the code below. This code will serve as the model that powers the chatbot.

```python
import os
from openai import OpenAI

client = OpenAI(
  base_url="https://integrate.api.nvidia.com/v1",
  api_key=os.environ["NVIDIA_API_KEY"]  # never hardcode secrets; set via environment
)


completion = client.chat.completions.create(
  model="deepseek-ai/deepseek-v4-flash",
  messages=[{"role":"user","content":""}],
  temperature=1,
  top_p=0.95,
  max_tokens=16384,
  extra_body={"chat_template_kwargs":{"thinking":True,"reasoning_effort":"high"}},
  stream=False
)

reasoning = getattr(completion.choices[0].message, "reasoning", None) or getattr(completion.choices[0].message, "reasoning_content", None)
if reasoning:
  print(reasoning)
print(completion.choices[0].message.content)
```

The chatbot should be full featured and capable of understanding and responding to user queries in a futuristic and minimalist interface. It should leverage the provided code to interact with the OpenAI API, allowing users to ask questions, receive detailed explanations, and engage in meaningful conversations.
