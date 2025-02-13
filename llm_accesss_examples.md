### Anthropic LLMs Usage

```python
import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)
```

# Anthropic models
Model	            Anthropic API
Claude 3.5 Sonnet	claude-3-5-sonnet-20241022 (claude-3-5-sonnet-latest)
Claude 3.5 Haiku	claude-3-5-haiku-20241022 (claude-3-5-haiku-latest)	

Claude 3 Opus	    claude-3-opus-20240229 (claude-3-opus-latest)
Claude 3 Sonnet	    claude-3-sonnet-20240229
Claude 3 Haiku	    claude-3-haiku-20240307

### OpenAI LLMs Usage

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)
```

### OpenAI models
Model	Description
GPT-4o Our versatile, high-intelligence flagship model

GPT-4o-mini Our fast, affordable small model for focused tasks

o1 and o1-mini Reasoning models that excel at complex, multi-step tasks

GPT-4o models capable of audio inputs and outputs via REST API

DALL·E A model that can generate and edit images given a natural language prompt

### Deepseek LLMs Usage

```python
# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
```

### Deepseek models
deepseek-chat
deepseek-reasoner
