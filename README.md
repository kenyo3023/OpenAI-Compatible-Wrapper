# OpenAI-Compatible-Wrapper

A flexible wrapper implementation for Large Language Model APIs with configurable default parameters.

## Features
- Easy-to-use wrapper for OpenAI and other LLM APIs
- Configurable default parameters for chat completions
- Seamless parameter inheritance and override
- Support for both OpenAI and Azure OpenAI
- Modular and extensible design

## Quick Start
```python
from inference_engine.compatible import OpenAICompatibleWrapper

engine = OpenAICompatibleWrapper(base=openai.OpenAI, model='gpt-4o', max_tokens=1000)
```

Use the engine to generate completions:
```python
response = engine.chat.completions.create(
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)
```

Override default parameters:
```python
response = engine.chat.completions.create(
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ],
    temperature=0.5
)
```

## Advanced Usage

### Use with any OpenAI-compatible LLM API:
```python
from inference_engine.compatible import OpenAICompatibleWrapper

engine = OpenAICompatibleWrapper(base=openai.OpenAI, model='gpt-4o', max_tokens=1000)
```

### Use with OpenAI:
```python
from inference_engine.openai import OpenAIWrapper

engine = OpenAIWrapper(base=openai.OpenAI, model='gpt-4o', max_tokens=1000)
```

### Use with Anthropic:
```python
from inference_engine.anthropic import AnthropicWrapper

engine = AnthropicWrapper(base=anthropic.Anthropic, model='claude-3-opus-20240229', max_tokens=1000)
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License





