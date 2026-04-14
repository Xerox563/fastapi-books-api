"""
DAY 9: OpenAI Parameters Deep Dive
===================================

Three parameters you NEED to control:
1. temperature → How creative (0=boring, 1.5=wild)
2. max_tokens → How long the answer is
3. top_p → Advanced randomness control

We'll test them on the SAME question to see the difference.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================================
# TEMPERATURE EXPLANATION
# ============================================================================
"""
TEMPERATURE = How creative the AI is

Think of it like:
- 0.0 = Robot (always same answer)
- 0.7 = Normal person (slight variation)
- 1.5 = Crazy artist (wild ideas)

Under the hood: It changes probability distribution of word choices.
Lower = picks the most likely word always
Higher = picks from more options, even unlikely ones
"""


def test_temperature():
    """Test same question with different temperatures"""
    
    question = "Tell me a fun fact about programming."
    
    temperatures = [
        (0.0, "Robot - Same answer every time"),
        (0.7, "Normal - Balanced"),
        (1.5, "Creative - Wild ideas")
    ]
    
    print("="*80)
    print("TEMPERATURE TEST: Same question, different creativity levels")
    print("="*80)
    
    for temp, description in temperatures:
        print(f"\nTemperature: {temp} ({description})")
        print("-"*80)
        
        # Run 2 times with same temperature to show consistency
        for run in range(2):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": question}],
                temperature=temp,  # ← THIS controls creativity
                max_tokens=150
            )
            
            answer = response.choices[0].message.content
            print(f"Run {run+1}: {answer}\n")


# ============================================================================
# MAX_TOKENS EXPLANATION
# ============================================================================
"""
MAX_TOKENS = How long the response is

Think of it like cup sizes at coffee shop:
- 50 tokens = Espresso (tiny)
- 200 tokens = Regular coffee (normal)
- 1000 tokens = Bucket (huge)

1 token ≈ 4 characters, so:
- 50 tokens ≈ 200 characters ≈ 1-2 sentences
- 200 tokens ≈ 800 characters ≈ 3-4 sentences
- 1000 tokens ≈ 4000 characters ≈ full page
"""


def test_max_tokens():
    """Test same question with different response lengths"""
    
    question = "What is Python programming?"
    
    token_sizes = [
        (50, "Tiny - 1 sentence"),
        (200, "Medium - 1 paragraph"),
        (500, "Large - Full answer")
    ]
    
    print("\n\n")
    print("="*80)
    print("MAX_TOKENS TEST: Same question, different lengths")
    print("="*80)
    
    for tokens, description in token_sizes:
        print(f"\nMax Tokens: {tokens} ({description})")
        print("-"*80)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": question}],
            temperature=0.7,
            max_tokens=tokens  # ← THIS controls length
        )
        
        answer = response.choices[0].message.content
        print(f"Answer:\n{answer}\n")


# ============================================================================
# TOP_P EXPLANATION
# ============================================================================
"""
TOP_P = Advanced version of temperature

Instead of "how noisy", it's "which words to consider"
- 0.1 = Only consider top 10% most likely words (very safe)
- 0.9 = Consider top 90% of words (more creative)
- 1.0 = Consider all words (max crazy)

IMPORTANT: Usually leave at 1.0 unless you REALLY know what you're doing.
We'll skip this in our FAQ bot - temperature is enough for 99% of cases.
"""


# ============================================================================
# PRACTICAL: Build FAQ Bot with RIGHT Parameters
# ============================================================================
class FAQBot:
    """
    FAQ Bot that answers CONSISTENTLY using low temperature
    
    Why low temperature?
    → FAQ answers should be consistent
    → Customer asks same question twice → Should get same answer
    → Uses temperature=0.3 (very consistent)
    """
    
    def __init__(self):
        self.system_prompt = "You are a helpful FAQ assistant. Be concise and clear."
    
    def answer(self, question: str) -> str:
        """Answer a FAQ question"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.3,      # ← LOW = Consistent FAQ answers
            max_tokens=200,       # ← SHORT = FAQ style
            top_p=1.0             # ← Leave default
        )
        
        return response.choices[0].message.content


class ContentCreator:
    """
    Content Creator that generates VARIED content using higher temperature
    
    Why high temperature?
    → Content should be interesting and different
    → Each tweet/story should be unique
    → Uses temperature=1.0 (creative but coherent)
    """
    
    def __init__(self):
        self.system_prompt = "You are a creative content writer. Be engaging and fun."
    
    def generate(self, prompt: str) -> str:
        """Generate creative content"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,      # ← HIGH = Creative variation
            max_tokens=500,       # ← LONGER = More content
            top_p=1.0
        )
        
        return response.choices[0].message.content


# ============================================================================
# DEMO: Show the difference
# ============================================================================
if __name__ == "__main__":
    
    # Test FAQ Bot
    print("\n" + "="*80)
    print("DEMO 1: FAQ Bot (Low Temperature = Consistent)")
    print("="*80)
    
    faq = FAQBot()
    question = "How do I install FastAPI?"
    
    print(f"Question: {question}\n")
    
    for i in range(3):
        answer = faq.answer(question)
        print(f"Answer {i+1}:\n{answer}\n")
        print("-"*80 + "\n")
    
    print("Notice: All answers are NEARLY IDENTICAL (FAQ consistency)\n\n")
    
    # Test Content Creator
    print("="*80)
    print("DEMO 2: Content Creator (High Temperature = Varied)")
    print("="*80)
    
    creator = ContentCreator()
    prompt = "Write a funny one-liner about programming"
    
    print(f"Prompt: {prompt}\n")
    
    for i in range(3):
        content = creator.generate(prompt)
        print(f"Content {i+1}:\n{content}\n")
        print("-"*80 + "\n")
    
    print("Notice: All answers are DIFFERENT (content variety)\n")


"""
WHEN TO USE WHAT:
=================

temperature=0.0-0.3:
├─ FAQ answers
├─ Math problems
├─ Code generation
└─ Anything needing consistency

temperature=0.7-0.9:
├─ General questions
├─ Chatbot
├─ Customer service
└─ Balanced use cases

temperature=1.0-1.5:
├─ Creative writing
├─ Content generation
├─ Story generation
└─ Brainstorming

max_tokens=50-100:
├─ Tweets
├─ Quick replies
└─ Summaries

max_tokens=200-500:
├─ FAQ answers
├─ Paragraphs
└─ Chat responses

max_tokens=1000+:
├─ Full articles
├─ Code generation
└─ Long explanations
"""