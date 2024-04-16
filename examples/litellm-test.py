from litellm import completion

import litellm 
litellm.set_verbose = True

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

response = completion(
            model="ollama/qwen:0.5b",
            messages = [{"content": "Hello, sup?", "role": "user"}],
            api_base="http://localhost:11434",
            tools=tools
)

print(response)

# print(f"<{response.model}> {response.content}")