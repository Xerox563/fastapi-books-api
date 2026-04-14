'''
TOKENS = How OpenAI measures text length

Think of it like:
1 token ≈ 4 characters ≈ 0.75 words

Examples:
"Hello" = 1 token
"Hello world" = 2 tokens
"The quick brown fox" = 4 tokens
"Hello, how are you doing today?" = 6 tokens

Why measure in tokens?
→ OpenAI charges per token (not per message)
→ Different models have different token costs
→ You need to know cost BEFORE calling API
→ Prevents surprise bills
'''
'''
Different models, different costs:

GPT-3.5-turbo:
├─ Input: $0.50 per 1M tokens
├─ Output: $1.50 per 1M tokens
└─ Very cheap, good for FAQ bots

GPT-4o (our model):
├─ Input: $5 per 1M tokens
├─ Output: $15 per 1M tokens
└─ 10x more expensive but smarter

Example calculation:
───────────────────
Question: "What is Python?" (4 tokens input)
Answer: "Python is a programming language..." (20 tokens output)

Cost = (4 tokens * $5/1M) + (20 tokens * $15/1M)
     = $0.00002 + $0.0003
     = $0.00032 (0.3 cents!)

So basically: Dirt cheap per call, but adds up with volume!
'''

import tiktoken
from dependencies.config import client

def count_tokens(text:str,model:str="gpt-3.5-turbo") -> int:
    """
    Count how many tokens a text is, takes args and return the number of tokens
    Under the hood:
    → tiktoken loads the tokenizer for that model
    → Splits text into tokens
    → Returns count
    """

    # get tokenizer for the model
    encoding = tiktoken.encoding_for_model(model)

    # count tokens in text
    tokens = encoding.encode(text)

    return len(tokens)


def solve():
    texts = [
        "Hello",
        "Hello world",
        "What is Python?",
        "The quick brown fox jumps over the lazy dog",
        "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)"
    ]
    tokens = 0
    for text in texts:
        tokens = count_tokens(text)
    print("Total Tokens for the input Text: ",tokens)
    return tokens    

'''
Example:
    → 100 input tokens at $5 per 1M = $0.0005
    → 200 output tokens at $15 per 1M = $0.003
    """
'''
PRICING = {
    "gpt-3.5-turbo": {
        "input": 0.50,      # $0.50 per 1M input tokens
        "output": 1.50      # $1.50 per 1M output tokens
    },
    "gpt-4o": {
        "input": 5.00,      # $5.00 per 1M input tokens
        "output": 15.00     # $15.00 per 1M output tokens
    },
    "gpt-4-turbo": {
        "input": 10.00,
        "output": 30.00
    }
}

def calculate_cost(input_token:int,output_token:int,model:str="gpt-3.5-turbo"):
    if model not in PRICING:
        print(f"Model {model} not found in Pricing !!")

    pricing = PRICING[model]

    input_cost = (input_token*pricing["input"])/1_000_000   
    output_cost = (output_token*pricing["output"])/1_000_000   
        
    total_cost = input_cost + output_cost
    return total_cost  

def solve_main():
    res = calculate_cost(solve(),100)
    print("Final Cost: ",res)
 

'''
TOKEN COUNTING:
├─ 1 token ≈ 4 characters
├─ Use tiktoken.encoding_for_model()
└─ count_tokens(text, model) returns number

PRICING (gpt-4o):
├─ Input: $5 per 1M tokens
├─ Output: $15 per 1M tokens
└─ Example: 100 input + 200 output = $0.0035

ESTIMATION:
├─ Count input tokens
├─ Estimate output ≈ max_tokens × 0.7
├─ Calculate total cost
└─ Show user before calling

TRACKING:
├─ Record every call
├─ Sum up tokens and costs
├─ Export to JSON
└─ Monitor spending

MONEY SAVING:
├─ Use gpt-3.5-turbo for simple tasks
├─ Reduce max_tokens
├─ Cache repeated responses
└─ Monitor and optimize

'''

        

        