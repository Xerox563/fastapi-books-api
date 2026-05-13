# An Output Parser is a tool that takes that raw text and converts it into a clean, structured Python object — like a list, a dictionary, an integer, or a custom data object.
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
import os
from dotenv import load_dotenv

print("API KEY:", os.getenv("OPENROUTER_API_KEY"))

# step 1 : create the parseer
parser = CommaSeparatedListOutputParser()

# step 2 : get the format onstructions from the parser
format_instrucions = parser.get_format_instructions() # Your response should be a list of comma separated values.

# step 3 : Injecting those instructions into the propmpt:
template = PromptTemplate(
    input_variables=["subject"], # this is provided by the user during invoke
    partial_variables={"format_instructions":format_instrucions},# langchain fills it automatically , we do not have to pass this during invoke
    template="List 5 topics in {subject}.\n{format_instructions}"
)

# Step 4: Configure OpenRouter Model : Connects your Python code to the AI model.
llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# step 5: chaining

chain = template | llm | parser 

result = chain.invoke({"subject": "machine learning"})

print(result)          # ['neural networks', 'decision trees', 'SVM', 'clustering', 'regression']
print(type(result))    # <class 'list'>
print(result[0])       # neural networks




'''
How it works behind the scenes
There are two parts to how an Output Parser works:

Part 1: 
  Format instructions. The parser generates a text description of what format the LLM should respond in. This description is automatically injected into your prompt. So the LLM knows exactly what format to use before it even answers.

Part 2: 
  Parsing. After the LLM responds, the parser reads the raw text and converts it into the Python structure you asked for. If the text does not match the expected format, it raises an error.
'''

'''
Parser Does two things ::
- Gives formatting instrcuions to AI
- Converts AI text into python objects
'''