from luminos.messages.assistant import Assistant

class Assistant(Assistant):
    def serialize(self) -> dict:
        print("WE USING THE ANTHROPIC VERSION!!!")
        
        content = [
            {"type": "text", "text": self.content}
        ]

        if len(self.tool_calls) > 0:
            for tool_call in self.tool_calls:
                content.append({
                    "type": "tool_use",
                    "id": tool_call.id,
                    "name": tool_call.content.name,
                    "input": {}
                })
        
        obj = {
            'role': 'assistant', 
            'content': content
        }

        return obj