
from dotenv import load_dotenv
import os
import requests
from pprint import pprint

from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from tavily import TavilyClient
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call

# =========================
# Environment Setup
# =========================

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

print("OpenWeather API Key Loaded:", bool(OPENWEATHER_API_KEY))
print("Tavily API Key Loaded:", bool(TAVILY_API_KEY))

# =========================
# Weather Tool
# =========================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""

    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key not found."

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": f"{city},IN",
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as e:
        return f"Weather API request failed: {e}"

    except ValueError:
        return "Invalid response received from Weather API."

    print("\nWeather API Response:")
    pprint(data)

    if str(data.get("cod")) != "200":
        return f"Weather API Error: {data.get('message')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# =========================
# News Tool
# =========================

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def get_news(city: str) -> str:
    """Get latest news about a city."""

    try:
        response = tavily_client.search(
            query=f"latest news in {city}",
            search_depth="basic",
            max_results=3
        )

    except Exception as e:
        return f"News search failed: {e}"

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"- {title}\n"
            f"Link: {url}\n"
            f"Summary: {snippet[:100]}..."
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# =========================
# Ollama LLM
# =========================

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# =========================
# Human Approval Middleware
# =========================

@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call."""

    tool_name = request.tool_call["name"]

    confirm = input(
        f"\nAgent wants to call '{tool_name}'. Approve? (yes/no): "
    )

    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    return handler(request)


# =========================
# Create Agent
# =========================

agent = create_agent(
    model=llm,
    tools=[get_weather, get_news],
    system_prompt="You are a helpful city assistant.",
    middleware=[human_approval]
)


# =========================
# Chat Loop
# =========================

print("\n===== City Assistant =====")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            }
        )

        print("\nBot:", result["messages"][-1].content)

    except Exception as e:
        print(f"\nAgent Error: {e}")
