from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from rich import print


# Tool
@tool
def get_text_length(text: str) -> int:
    """Returns the number of characters in a given text"""
    return len(text)


tools = {
    "get_text_length": get_text_length
}

# Model
llm = ChatOllama(
    model="llama3.2",
    temperature=0.7
)

# Bind Tool
llm_with_tool = llm.bind_tools([get_text_length])

messages = []

prompt = input("You: ")

messages.append(
    HumanMessage(content=prompt)
)

# First LLM call
result = llm_with_tool.invoke(messages)

messages.append(result)

# Execute tool if called
if result.tool_calls:

    tool_call = result.tool_calls[0]

    tool_name = tool_call["name"]

    tool_result = tools[tool_name].invoke(
        tool_call["args"]
    )

    messages.append(
        ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"]
        )
    )

    # Second LLM call
    result = llm_with_tool.invoke(messages)

print(result.content)