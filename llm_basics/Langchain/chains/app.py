from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser # Converts AI response into plain text
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Debug check
print("API KEY:", os.getenv("OPENROUTER_API_KEY"))

# Step 1: Create Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful coding tutor."),
    ("human", "Explain {concept} with a simple example in Python.")
])
'''
This creates a chat-style prompt.
Internally, LangChain stores this as structured messages:
'''

# Step 2: Configure OpenRouter Model : Connects your Python code to the AI model.
llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Step 3: Output Parser : AI responses are sometimes complex objects. This converts the response into simple plain text.
parser = StrOutputParser()

# Step 4: Build LCEL[Langchai Expression language] Chain
chain = prompt | llm | parser

# Step 5: Invoke Chain
result = chain.invoke({
    "concept": "list comprehension"
})

print(result)