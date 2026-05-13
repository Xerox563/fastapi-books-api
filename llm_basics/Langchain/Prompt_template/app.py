from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful tutor who explains things simply."), # instrcution to the ai
    ("human", "Explain {concept} using an analogy. Keep it under {word_limit} words.") # users actual question
])

#  it builds the template from a list you give it
messages = prompt.format_messages(
    concept="neural networks",
    word_limit="50"
)

'''
This fills in all the {variable} placeholders
Returns a list of message objects (SystemMessage, HumanMessage)
These are not plain strings — they are special LangChain objects that LLMs understand
'''
for message in messages:
    print(type(message).__name__, ":", message.content)