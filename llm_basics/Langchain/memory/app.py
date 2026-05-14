from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
# ChatPromptTemplate - Build structured chat prompts , while MessagesPlaceholder - Inserts the chat history dynamically[]This is the place where previous conversations messages are inserted 
from  langchain_community.memory import ConversationBufferWindowMemory # This provides memory storage : It stores the conversation history
# What does "Window" mean? Keep only LAST N conversations, instead of entire history.
from langchain_core.output_parsers import StrOutputParser # converts AI message -> plain string
from langchain_core.runnables import RunnablePassthrough
import os

from dotenv import load_dotenv
load_dotenv()

# load the llm model
llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Step[0]: create memory : llms have token limits without window memory[k], conversation becomes too large and expensive
memory = ConversationBufferWindowMemory(
    k=5, # store only the last 5 messages into the exchanges[user message + AI response]
    return_message=True # Return actual chat message objects instead of one big string
)

# create prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful coding tutor."),
    MessagesPlaceholder(variable_name="history"), # MessagesPlaceholder FILLS HISTORY
    ('human',"{input}")
])

# load memoyr function
def load_memory(input_data):
    # This function loads conversations history
    return memory.load_memory_variables({})["history"]
    '''
    returns:
    {
        "history": [
            HumanMessage(...),
            AIMessage(...)
        ]
    }
    '''

# Build chain
chain = (
      {
          "history":load_memory,
          "input":RunnablePassthrough,
           # After this LCEL combines result 
            # {
            # "history": [],
            # "input": "What is a for loop in Python?"
            # } 
            # This dictionary goes into the prompt template
      }
      | prompt
      | llm
      | StrOutputParser()
)   

# Step[1]: wrapper function to save messages after each response
def chat(user_message):
    response = chain.invoke(user_message)
    memory.save_context({"input",user_message},{"output",response})
    return response

# Run a conversation
print(chat("What is a for loop in Python?"))
print(chat("Can you show me an example?"))
print(chat("How is that different from a while loop?"))

# Final flow
'''
chat(user_message)
        ↓

chain.invoke(user_message)
        ↓

load_memory()
        ↓

RunnablePassthrough()
        ↓

Create dictionary:
{
  history,
  input
}
        ↓

PromptTemplate fills variables
        ↓

MessagesPlaceholder inserts old messages
        ↓

Final Prompt Created
        ↓

LLM generates response
        ↓

StrOutputParser extracts string
        ↓

response returned
        ↓

memory.save_context()
        ↓

Conversation stored
'''






