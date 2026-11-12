from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda

# Components
model = ChatOllama(
    model="llama3.2",
    temperature=0.7
)

parser = StrOutputParser()

# Two different prompts
short_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in 1-2 lines"
)

detailed_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in detail"
)

# Parallel Chain
chain = RunnableParallel({
    "short": RunnableLambda(lambda x: x["short"])
            | short_prompt
            | model
            | parser,

    "detailed": RunnableLambda(lambda x: x["detailed"])
               | detailed_prompt
               | model
               | parser
})

# Invoke
result = chain.invoke({
    "short": {"topic": "Machine Learning"},
    "detailed": {"topic": "Deep Learning"}
})

print("SHORT EXPLANATION:")
print(result["short"])

print("\nDETAILED EXPLANATION:")
print(result["detailed"])