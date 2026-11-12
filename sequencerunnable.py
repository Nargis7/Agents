# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# # 1. Prompt Template
# prompt = ChatPromptTemplate.from_template(
#     "Explain {topic} in simple words"
# )

# # 2. Model
# model = ChatOllama(
#     model="llama3.2",
#     temperature=0.7
# )

# # 3. Output Parser
# parser = StrOutputParser()

# formatted_prompt = prompt.format_messages(topic="Machine Learning")

# response = model.invoke(formatted_prompt)


# final_output = parser.parse(response.content)

# print(final_output)











from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Prompt Template
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words"
)

# 2. Model
model = ChatOllama(
    model="llama3.2",
    temperature=0.7
)

# 3. Output Parser
parser = StrOutputParser()

# Chain
chain = prompt | model | parser

# Invoke
result = chain.invoke({"topic": "Machine Learning"})
print(result)