import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)

message = client.beta.tools.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What's the weather in Benton Harbor?"},
    ],
    system="You are a helpful AI named Claude.",
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
                    }
                },
                "required": ["location"]
            }
        }
    ]
)

print(message.content)

# here's an example of the output of this script: 

# % python3 examples/claude-test.py
# [TextBlock(text="Okay, let's get the current weather for Benton Harbor:", type='text'), ToolUseBlock(id='toolu_013gKYSvDgDmXjDADzucTTkg', input={'location': 'Benton Harbor, MI', 'unit': 'fahrenheit'}, name='get_weather', type='tool_use')]