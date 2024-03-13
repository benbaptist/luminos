from docstring_parser import parse
from openai import OpenAI
import json
from yfinance import Ticker

class ToolWeather(Tools):
    name = "weather"

    def get_current_weather(self, location):
        """openai.function: Get the current weather in a given location

        location
        :param str location: The city and state, e.g. San Francisco, CA
        """
        # Implement the weather retrieval logic here
        return f"The current weather in {location} is sunny."

class ToolStocks(Tools):
    name = "stocks"

    def price(self, ticker):
        """openai.function: Retrieve stock info for the specified ticker

        ticker
        :param str ticker: The ticker to check
        """
        ticker = Ticker(ticker)

        try:
            info = json.dumps(ticker.info)
        except AttributeError:
            return f"Cannot find stock info for `{ticker}`."

        return f"{ticker}'s info: {info}"
    
class Tools:
    def __init__(self):
        self.list_plugins = [ToolWeather, ToolStocks]

    @property
    def __obj__(self):
        l = []
        for Plugin in self.list_plugins:
            plugin = Plugin(self.thread)
            l += plugin.__func__
        return l


# Initialize OpenAI client
client = OpenAI()

# Main loop to interact with the LLM
finish_reason = ""
while finish_reason != "stop":
    task = input("Enter the task to be completed: ")

    # Initialize Tools class
    tools = Tools()

    # System prompt and user input
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task}
    ]

    # Call the LLM with the task and tools
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools.__obj__,  # Use the aggregated functions from plugins
        tool_choice="auto"
    )

    # Extract the response and finish reason
    response = completion.choices[0].message
    finish_reason = completion.choices[0].finish_reason

    # Append assistant response and tool response handling logic can be added here

    print(response)

print("Iteration stopped as instructed by the LLM.")
