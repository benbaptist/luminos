import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"},
        {"role": "assistant", "content": "Hey, how are you?"},
        {"role": "user", "content": "Doing great, thanks!"}
    ],
    system="You are a helpful AI named Claude."
)

print(message.content)

# here's an example of the output of this script: 

# % python3 examples/claude-test.py
# [TextBlock(text="Glad to hear you're doing well! How can I assist you today? Let me know if there are any topics you'd like to discuss or questions you have.", type='text')]


# api.md contains some additional information on the SDK. Here's the contents of api.md:
# Messages

# Types:

# ```python
# from anthropic.types import (
#     ContentBlock,
#     ContentBlockDeltaEvent,
#     ContentBlockStartEvent,
#     ContentBlockStopEvent,
#     ImageBlockParam,
#     Message,
#     MessageDeltaEvent,
#     MessageDeltaUsage,
#     MessageParam,
#     MessageStartEvent,
#     MessageStopEvent,
#     MessageStreamEvent,
#     TextBlock,
#     TextBlockParam,
#     TextDelta,
#     Usage,
# )
# ```

# Methods:

# - <code title="post /v1/messages">client.messages.<a href="./src/anthropic/resources/messages.py">create</a>(\*\*<a href="src/anthropic/types/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/message.py">Message</a></code>
# - <code>client.messages.<a href="./src/anthropic/resources/messages.py">stream</a>(\*args) -> MessageStreamManager[MessageStream] | MessageStreamManager[MessageStreamT]</code>