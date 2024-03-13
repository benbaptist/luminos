from tools import Tools

import openai
import json

SYSTEM_PROMPT = """As an LLM operating within a Linux shell, your task is to execute a single prompt iteratively until its intended goal is achieved. With access to the file system and the ability to use shell commands, you must continue to iterate and execute the necessary actions until the specified objective is successfully completed. Your focus should be on persistent execution and refinement of the given prompt until the desired outcome is attained within the Linux shell environment. Once the task is complete, the conversation will be over. Do not ask the user if they would like more help."""

# Create an OpenAI client
client = openai.OpenAI()
tools = Tools()

# Modify the function to accept messages list as an argument and remove initial messages definition
def run_llm(txt, messages):
    if not messages:  # Initialize messages list with system and user message if it's empty
        messages.append(
            {
                "role": "system", 
                "content": SYSTEM_PROMPT
            }
        )
        messages.append(
            {
                "role": "user", 
                "content": txt
            }
        )

    while True:
        # Run the LLM
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            tools=tools.__obj__,
            tool_choice="auto",
        )

        # Extract the response message and tool calls
        choice = response.choices[0]
        
        message = choice.message.content
        finish_reason = choice.finish_reason

        messages.append(choice.message)

        if finish_reason == "tool_calls":
            tool_calls = choice.message.tool_calls

            for tool_call in tool_calls:
                call_id = tool_call.id
                tool_type = tool_call.type

                if tool_type == "function":
                    func = tool_call.function

                    func_name = func.name
                    func_kwargs = json.loads(func.arguments)

                    func_response = tools.call(func_name, func_kwargs)

                    print(f"{func_name}({func_kwargs})")
                    
                    messages.append(
                        {
                            "tool_call_id": call_id,
                            "role": "tool",
                            "name": func_name,
                            "content": json.dumps(func_response),
                        }
                    )
                else:
                    raise Exception(f"Invalid tool_type {tool_type}")
        else:
            # Messages append removed to avoid duplication

            print(f"<gpt> {message}")

        # Check if the finish code has been set
        if finish_reason == "stop":
            return