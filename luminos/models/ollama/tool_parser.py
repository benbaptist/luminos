import xml.etree.ElementTree as ET

from .messages.tool_call import ToolCall

class Function(object):
    name = None
    arguments = None

def tool_parser(xml_string):
    root = ET.fromstring("<root>" + xml_string + "</root>")

    tool_calls = []

    # Now you can iterate over the child elements (or attributes) of the root:
    for tool in root.iter("tool"):
        name = tool.find("name").text
        parameters = tool.find("parameters").text
        use_id = tool.find("use_id").text

        func = Function()
        func.name = name
        func.arguments = parameters

        tool_call = ToolCall(func, "function", use_id)

        tool_calls.append(tool_call)

    return tool_calls

if __name__ == "__main__":
    xml_string = """
<tool>
    <name>tool_name</name>
    <parameters>{"valid": "JSON"}</parameters>
    <use_id>random_id</use_id>
</tool>

<tool>
    <name>tool_name222</name>
    <parameters>{"valid": "JSON"}</parameters>
    <use_id>random_id</use_id>
</tool>
   
"""
    print(tool_parser(xml_string))