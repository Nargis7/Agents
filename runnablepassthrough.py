from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Model
model = ChatOllama(
    model="llama3.2",
    temperature=0.7
)

parser = StrOutputParser()

# Prompt to generate code
code_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code generator"),
    ("human", "{topic}")
])

# Prompt to explain code
explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who explains code in simple terms"),
    ("human", "Explain the following code in simple words:\n{code}")
])

# Step 1: Generate code
seq = code_prompt | model | parser

# Step 2: Return code and explanation in parallel
seq2 = RunnableParallel(
    {
        "code": RunnablePassthrough(),
        "explanation": explain_prompt | model | parser
    }
)

# Complete chain
chain = seq | seq2

# Run chain
result = chain.invoke(
    {"topic": "please write a code of palindrome in python"}
)

print("CODE:\n")
print(result["code"])

print("\nEXPLANATION:\n")
print(result["explanation"])