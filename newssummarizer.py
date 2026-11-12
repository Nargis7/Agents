from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
# Search Tool
search_tool = TavilySearchResults(max_results=5)

# Ollama Model
llm = ChatOllama(
    model="llama3.2",
    temperature=0.7
)

# Prompt
prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.

Summarize the following news into clear bullet points.

{news}
"""
)

# Chain
chain = prompt | llm | StrOutputParser()

# Search
news_result = search_tool.run("Latest AI news of 2026")

# Summary
result = chain.invoke({"news": news_result})

print(result)

print("\nTool Description:")
print(search_tool.description)

print("\nTool Name:")
print(search_tool.name)

print("\nTool Args:")
print(search_tool.args)