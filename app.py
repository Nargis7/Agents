# from dotenv import load_dotenv
# import os
# import requests
# import streamlit as st

# from langchain_ollama import ChatOllama
# from langchain.tools import tool
# from tavily import TavilyClient
# from langchain.agents import create_agent

# load_dotenv()

# # -------------------------------
# # PAGE CONFIG
# # -------------------------------

# st.set_page_config(
#     page_title="City AI Assistant",
#     page_icon="🌍",
#     layout="wide"
# )

# # -------------------------------
# # CUSTOM CSS
# # -------------------------------

# st.markdown("""
# <style>

# .main {
#     background-color: #0f172a;
# }

# .stApp {
#     background: linear-gradient(
#         135deg,
#         #0f172a,
#         #1e293b
#     );
# }

# .title {
#     text-align:center;
#     font-size:48px;
#     font-weight:bold;
#     color:white;
# }

# .subtitle {
#     text-align:center;
#     color:#cbd5e1;
#     margin-bottom:30px;
# }

# .chat-card {
#     padding:15px;
#     border-radius:15px;
#     background:#1e293b;
#     color:white;
# }

# </style>
# """, unsafe_allow_html=True)

# # -------------------------------
# # HEADER
# # -------------------------------

# st.markdown(
#     "<div class='title'>🌍 City AI Assistant</div>",
#     unsafe_allow_html=True
# )

# st.markdown(
#     "<div class='subtitle'>Weather • News • Powered by Ollama</div>",
#     unsafe_allow_html=True
# )

# # -------------------------------
# # TOOLS
# # -------------------------------

# @tool
# def get_weather(city: str) -> str:
#     """Get current weather of a city"""

#     api_key = os.getenv("OPENWEATHER_API_KEY")

#     url = (
#         f"http://api.openweathermap.org/data/2.5/weather"
#         f"?q={city},IN&appid={api_key}&units=metric"
#     )

#     response = requests.get(url)
#     data = response.json()

#     if str(data.get("cod")) != "200":
#         return f"Weather API Error: {data.get('message')}"

#     temp = data["main"]["temp"]
#     desc = data["weather"][0]["description"]

#     return f"Weather in {city}: {desc}, {temp}°C"


# tavily_client = TavilyClient(
#     api_key=os.getenv("TAVILY_API_KEY")
# )


# @tool
# def get_news(city: str) -> str:
#     """Get latest news about a city"""

#     response = tavily_client.search(
#         query=f"latest news in {city}",
#         search_depth="basic",
#         max_results=3
#     )

#     results = response.get("results", [])

#     if not results:
#         return f"No news found for {city}"

#     output = []

#     for r in results:

#         output.append(
#             f"""
# 📰 {r.get('title')}

# 🔗 {r.get('url')}

# 📌 {r.get('content','')[:150]}...
#             """
#         )

#     return "\n\n".join(output)

# # -------------------------------
# # LLM
# # -------------------------------

# llm = ChatOllama(
#     model="llama3.2",
#     temperature=0
# )

# agent = create_agent(
#     model=llm,
#     tools=[get_weather, get_news],
#     system_prompt="""
# You are a helpful city assistant.
# Use tools whenever needed.
# """
# )

# # -------------------------------
# # SESSION
# # -------------------------------

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # -------------------------------
# # CHAT HISTORY
# # -------------------------------

# for msg in st.session_state.messages:

#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # -------------------------------
# # USER INPUT
# # -------------------------------

# prompt = st.chat_input(
#     "Ask about weather or city news..."
# )

# if prompt:

#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": prompt
#         }
#     )

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):

#         with st.spinner("Thinking..."):

#             result = agent.invoke(
#                 {
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": prompt
#                         }
#                     ]
#                 }
#             )

#             answer = result["messages"][-1].content

#             st.markdown(answer)

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": answer
#         }
#     )










































import os
import requests
import streamlit as st

from dotenv import load_dotenv
from tavily import TavilyClient

from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CityAI | Smart City Assistant",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: #0b1020;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #10182b;
    border-right: 1px solid #26334d;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(120deg, #182747, #17213a, #24204b);
    padding: 32px;
    border-radius: 20px;
    border: 1px solid #344568;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 34px;
    font-weight: 750;
    color: #ffffff;
    margin-bottom: 8px;
}

.hero p {
    color: #aab8d1;
    font-size: 15px;
}

.stat-card {
    background: #151f35;
    padding: 20px;
    border: 1px solid #2c3b58;
    border-radius: 16px;
    min-height: 115px;
}

.stat-card h3 {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 12px;
}

.stat-card h2 {
    color: #ffffff;
    font-size: 23px;
    margin: 0;
}

.section-title {
    font-size: 19px;
    font-weight: 650;
    color: #f1f5f9;
    margin-top: 25px;
    margin-bottom: 12px;
}

div[data-testid="stChatMessage"] {
    background: #151f35;
    border: 1px solid #283751;
    border-radius: 15px;
    padding: 14px;
    margin-bottom: 12px;
}

.stChatInputContainer {
    border-color: #334155;
}

.stChatInputContainer textarea {
    color: #ffffff;
}

.stButton button {
    border-radius: 10px;
    border: 1px solid #344568;
    background: #182747;
    color: white;
}

.stButton button:hover {
    border-color: #818cf8;
    color: #a5b4fc;
}

.small-text {
    color: #8190aa;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# WEATHER TOOL
# ==========================================

@tool
def get_weather(city: str) -> str:
    """Get current weather information for an Indian city."""

    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key is missing."

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": f"{city},IN",
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            },
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        if str(data.get("cod")) != "200":
            return f"Weather error: {data.get('message')}"

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        return (
            f"Weather in {city}:\n"
            f"Temperature: {temperature}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Conditions: {description}"
        )

    except requests.RequestException as e:
        return f"Weather request failed: {str(e)}"


# ==========================================
# NEWS TOOL
# ==========================================

@tool
def get_news(city: str) -> str:
    """Search for the latest news about an Indian city."""

    if not TAVILY_API_KEY:
        return "Tavily API key is missing."

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)

        response = client.search(
            query=f"latest news in {city} India",
            search_depth="basic",
            max_results=3
        )

        results = response.get("results", [])

        if not results:
            return f"No recent news found for {city}."

        news_list = []

        for item in results:
            news_list.append(
                f"Title: {item.get('title', 'No title')}\n"
                f"URL: {item.get('url', '')}\n"
                f"Summary: {item.get('content', '')[:300]}"
            )

        return "\n\n".join(news_list)

    except Exception as e:
        return f"News search failed: {str(e)}"


# ==========================================
# CREATE AI AGENT
# ==========================================

@st.cache_resource
def build_agent():

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    return create_agent(
        model=llm,
        tools=[get_weather, get_news],
        system_prompt="""
        You are CityAI, a helpful Indian city assistant.

        You can:
        1. Provide current weather information.
        2. Search for the latest city news.
        3. Answer general questions.

        Use the available tools whenever current weather
        or recent news is requested.

        Present answers clearly with headings and bullet points.
        Never invent live weather or news information.
        """
    )


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 🌍 CityAI")

    st.markdown(
        "<p class='small-text'>YOUR INTELLIGENT CITY COMPANION</p>",
        unsafe_allow_html=True
    )

    st.divider()

    if st.button("＋  New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent_messages = []
        st.rerun()

    st.markdown("### Capabilities")

    st.markdown("""
    🌤️ **Weather Intelligence**

    Get current weather and temperature.

    📰 **Latest City News**

    Discover recent news and updates.

    🤖 **AI Assistant**

    Ask questions in natural language.
    """)

    st.divider()

    st.markdown("### System Status")

    st.markdown(
        f"{'🟢' if OPENWEATHER_API_KEY else '🔴'} OpenWeather API"
    )

    st.markdown(
        f"{'🟢' if TAVILY_API_KEY else '🔴'} Tavily Search"
    )

    st.markdown("🟢 Ollama integration configured")

    st.divider()

    st.markdown(
        "<p class='small-text'>Powered by LangChain · Ollama · Streamlit</p>",
        unsafe_allow_html=True
    )


# ==========================================
# MAIN DASHBOARD
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🌍 Welcome to CityAI</h1>
    <p>
        Your intelligent assistant for weather, city news
        and real-time information.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# DASHBOARD CARDS
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h3>🌤️ WEATHER</h3>
        <h2>Live Updates</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h3>📰 CITY NEWS</h3>
        <h2>Latest Stories</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h3>🤖 AI ENGINE</h3>
        <h2>Llama 3.2</h2>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# CHAT SECTION
# ==========================================

st.markdown(
    "<div class='section-title'>💬 Chat with CityAI</div>",
    unsafe_allow_html=True
)

st.caption(
    "Ask about weather, news or anything related to Indian cities."
)


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# CHAT INPUT
# ==========================================

user_input = st.chat_input(
    "Ask me about weather, news or your city..."
)


if user_input:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response

    with st.chat_message("assistant"):

        with st.spinner("CityAI is thinking..."):

            try:

                agent = build_agent()

                st.session_state.agent_messages.append(
                    HumanMessage(content=user_input)
                )

                result = agent.invoke(
                    {
                        "messages": st.session_state.agent_messages
                    }
                )

                st.session_state.agent_messages = result["messages"]

                answer = result["messages"][-1].content

                if not isinstance(answer, str):
                    answer = str(answer)

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )

                st.info(
                    "Check whether Ollama is running "
                    "and llama3.2 is available."
                )
