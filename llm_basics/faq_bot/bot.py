"""
FAQ Bot - Tests 5 different system prompts

This shows how system prompts change AI behavior
"""

from dependencies.config import client


# ============================================================================
# 5 Different System Prompts
# ============================================================================
SYSTEM_PROMPTS = {
    "1_friendly": (
        "You are a friendly assistant. "
        "Be warm, use emojis, and make everything fun!"
    ),
    
    "2_technical": (
        "You are a technical expert. "
        "Use precise language, include code examples, be thorough."
    ),
    
    "3_concise": (
        "You are a concise assistant. "
        "Answer in 1-2 sentences maximum. Get straight to the point."
    ),
    
    "4_beginner": (
        "You are teaching a beginner with no programming knowledge. "
        "Explain like they're 5 years old. Use simple analogies."
    ),
    
    "5_sarcastic": (
        "You are a sarcastic developer who's tired of answering the same questions. "
        "Be witty and humorous."
    )
}


# ============================================================================
# Function to call OpenAI
# ============================================================================
def call_openai(system_prompt: str, user_message: str) -> str:
    """
    Make a single API call to OpenAI
    
    Args:
        system_prompt: The instruction for how the AI should behave
        user_message: What the user is asking
        model: Which AI model to use (gpt-4o, gpt-3.5-turbo, etc.)
    
    Returns:
        The AI's response as a string
    
    UNDER THE HOOD:
    1. We create a "messages" list with roles
    2. We send it to OpenAI servers
    3. OpenAI processes it with the neural network
    4. OpenAI returns a response object
    5. We extract the text and return it
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # Make the API call
    # This is the moment your code talks to OpenAI servers
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
        
    # Extract the response text
    # response object has structure like:
    # {
    #   "choices": [
    #     {
    #       "message": {
    #         "content": "The actual response text here",
    #         "role": "assistant"
    #       }
    #     }
    #   ]
    # }
    return response.choices[0].message.content


# ============================================================================
# FAQ Bot Class
# ============================================================================
class FAQBot:
    """
    FAQ Bot that tests different system prompts
    
    Shows how SYSTEM PROMPT changes response
    while question stays the same
    """
    
    def __init__(self):
        self.question = "What is the purpose of FastAPI?"
    
    def answer_with_prompt(self, prompt_name: str) -> str:
        """Get answer using specific system prompt"""
        
        system_prompt = SYSTEM_PROMPTS[prompt_name]
        response = call_openai(system_prompt, self.question)
        return response
    
    def test_all_prompts(self):
        """Test all 5 system prompts and show differences"""
        
        print("="*80)
        print("DAY 8: OpenAI API - Testing 5 Different System Prompts")
        print("="*80)
        print(f"\nQuestion: {self.question}\n")
        
        for prompt_name in SYSTEM_PROMPTS.keys():
            print(f"\n{'='*80}")
            print(f"System Prompt: {prompt_name}")
            print(f"{'='*80}")
            
            system_prompt = SYSTEM_PROMPTS[prompt_name]
            print(f"Instruction: {system_prompt}")
            print("-"*80)
            
            try:
                response = self.answer_with_prompt(prompt_name)
                print(f"Response:\n{response}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print()