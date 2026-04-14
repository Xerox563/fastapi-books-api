"""
DAY 11: TOKEN COUNTING + COST TRACKING
=======================================

Why this matters:
→ Know cost BEFORE making API calls
→ Avoid surprise bills
→ Optimize your prompts
→ Budget your API usage

How it works:
→ Install tiktoken library (OpenAI's tokenizer)
→ Count tokens in prompt
→ Estimate tokens in response
→ Calculate cost
→ Track total spending
"""

import tiktoken
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Tuple
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================================
# STEP 1: UNDERSTAND TIKTOKEN - Token Counter
# ============================================================================
"""
tiktoken = OpenAI's official token counter library

Installation: pip install tiktoken

Why use it?
→ Same tokenizer OpenAI uses
→ Count tokens BEFORE sending (avoid surprises)
→ Optimize prompts to save money
"""


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """
    Count how many tokens a text is
    
    Args:
        text: The text to count
        model: Which model (gpt-4o, gpt-3.5-turbo, etc.)
    
    Returns:
        Number of tokens
    
    Under the hood:
    → tiktoken loads the tokenizer for that model
    → Splits text into tokens
    → Returns count
    """
    
    # Get tokenizer for the model
    # Each model has slightly different tokenizer
    encoding = tiktoken.encoding_for_model(model)
    
    # Count tokens in text
    tokens = encoding.encode(text)
    
    return len(tokens)


def demonstrate_tokenization():
    """Show how tokenization works"""
    
    print("="*80)
    print("HOW TOKENIZATION WORKS")
    print("="*80)
    
    texts = [
        "Hello",
        "Hello world",
        "What is Python?",
        "The quick brown fox jumps over the lazy dog",
        "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)"
    ]
    
    for text in texts:
        tokens = count_tokens(text)
        # Rough calculation: 1 token ≈ 4 characters
        chars = len(text)
        estimated_words = len(text.split())
        
        print(f"\nText: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"Characters: {chars}")
        print(f"Words: {estimated_words}")
        print(f"Tokens: {tokens}")
        print(f"Ratio: ~{chars/tokens:.1f} chars per token")


# ============================================================================
# STEP 2: PRICING CONSTANTS - Different models cost different amounts
# ============================================================================
"""
Pricing for different models (as of April 2024)

Note: Prices change, check OpenAI docs for latest
Input = cost per 1M input tokens
Output = cost per 1M output tokens
"""

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


# ============================================================================
# STEP 3: ESTIMATE RESPONSE TOKENS - Guess how long answer will be
# ============================================================================
def estimate_response_tokens(prompt_tokens: int, max_tokens: int) -> int:
    """
    Estimate how many tokens response will use
    
    Args:
        prompt_tokens: Tokens in your question
        max_tokens: Maximum tokens in response (what you set)
    
    Returns:
        Estimated tokens in response
    
    Formula:
    Most responses use 60-80% of max_tokens
    Average response ≈ max_tokens * 0.7
    
    Why estimate?
    → Can't know exact until response is generated
    → This gives you ballpark for cost estimation
    """
    
    # Simple formula: response usually ~70% of max
    # If max_tokens=500, response usually ~350 tokens
    estimated = int(max_tokens * 0.70)
    
    return estimated


# ============================================================================
# STEP 4: CALCULATE COST
# ============================================================================
def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "gpt-4o"
) -> float:
    """
    Calculate cost of API call
    
    Args:
        input_tokens: Tokens in your prompt
        output_tokens: Tokens in response
        model: Which model
    
    Returns:
        Cost in dollars
    
    Formula:
    cost = (input_tokens * input_price) + (output_tokens * output_price)
    
    Example:
    → 100 input tokens at $5 per 1M = $0.0005
    → 200 output tokens at $15 per 1M = $0.003
    → Total = $0.0035 (less than half a cent!)
    """
    
    # Get pricing for this model
    if model not in PRICING:
        raise ValueError(f"Model {model} not found in pricing")
    
    pricing = PRICING[model]
    
    # Calculate cost
    # Divide by 1,000,000 because pricing is per MILLION tokens
    input_cost = (input_tokens * pricing["input"]) / 1_000_000
    output_cost = (output_tokens * pricing["output"]) / 1_000_000
    
    total_cost = input_cost + output_cost
    
    return total_cost


def show_cost_breakdown(
    input_tokens: int,
    output_tokens: int,
    model: str = "gpt-4o"
) -> dict:
    """
    Show detailed cost breakdown
    
    Args:
        input_tokens: Tokens in prompt
        output_tokens: Tokens in response
        model: Which model
    
    Returns:
        Dict with costs
    """
    
    pricing = PRICING[model]
    
    input_cost = (input_tokens * pricing["input"]) / 1_000_000
    output_cost = (output_tokens * pricing["output"]) / 1_000_000
    total_cost = input_cost + output_cost
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total_cost, 6),
        "model": model
    }


# ============================================================================
# STEP 5: ESTIMATE COST BEFORE CALLING API
# ============================================================================
def estimate_api_call_cost(
    prompt: str,
    max_tokens: int = 500,
    model: str = "gpt-4o"
) -> dict:
    """
    ESTIMATE cost before making API call
    
    This is what you should do EVERY time:
    1. Count tokens in your prompt
    2. Estimate response tokens
    3. Calculate total cost
    4. Show user the cost
    5. Make API call only if they approve
    
    Args:
        prompt: Your question/prompt
        max_tokens: Max response length
        model: Which model
    
    Returns:
        Dict with estimated costs
    """
    
    # Count input tokens
    input_tokens = count_tokens(prompt, model)
    
    # Estimate output tokens
    output_tokens = estimate_response_tokens(input_tokens, max_tokens)
    
    # Calculate cost
    cost_breakdown = show_cost_breakdown(input_tokens, output_tokens, model)
    
    return cost_breakdown


# ============================================================================
# STEP 6: REAL API CALL WITH COST TRACKING
# ============================================================================
def call_with_cost_tracking(
    prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    max_tokens: int = 500,
    model: str = "gpt-4o",
    show_estimate: bool = True
) -> Tuple[str, dict]:
    """
    Make API call and track actual costs
    
    Args:
        prompt: User's question
        system_prompt: System instruction
        max_tokens: Max response length
        model: Which model
        show_estimate: Show cost before calling
    
    Returns:
        (response_text, cost_dict)
    
    Usage:
    answer, cost = call_with_cost_tracking("What is Python?")
    print(f"Answer: {answer}")
    print(f"Cost: ${cost['total_cost']}")
    """
    
    # STEP 1: Estimate cost
    if show_estimate:
        estimate = estimate_api_call_cost(prompt, max_tokens, model)
        print(f"\n💰 COST ESTIMATE:")
        print(f"   Input tokens: {estimate['input_tokens']}")
        print(f"   Est. output: {estimate['output_tokens']}")
        print(f"   Est. cost: ${estimate['total_cost']:.6f}")
    
    # STEP 2: Make API call
    print(f"\n📤 Making API call...")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )
    
    # STEP 3: Get ACTUAL token counts from response
    # OpenAI tells us how many tokens were actually used
    actual_input_tokens = response.usage.prompt_tokens
    actual_output_tokens = response.usage.completion_tokens
    
    # STEP 4: Calculate ACTUAL cost
    actual_cost = calculate_cost(actual_input_tokens, actual_output_tokens, model)
    
    # STEP 5: Show breakdown
    cost_breakdown = show_cost_breakdown(
        actual_input_tokens,
        actual_output_tokens,
        model
    )
    
    response_text = response.choices[0].message.content
    
    return response_text, cost_breakdown


# ============================================================================
# STEP 7: COST TRACKER CLASS - Track all your API calls
# ============================================================================
class CostTracker:
    """
    Track all your API calls and calculate total spending
    
    Why?
    → Know how much you've spent so far
    → Alert if spending is high
    → Budget your API usage
    → Optimize expensive calls
    """
    
    def __init__(self):
        self.calls = []  # List of all API calls
        self.total_tokens = 0
        self.total_cost = 0.0
    
    def add_call(self, cost_breakdown: dict, question: str = ""):
        """
        Add a call to the tracker
        
        Args:
            cost_breakdown: Dict from show_cost_breakdown()
            question: The question asked (for reference)
        """
        
        call_record = {
            "question": question[:50],  # First 50 chars
            "input_tokens": cost_breakdown["input_tokens"],
            "output_tokens": cost_breakdown["output_tokens"],
            "total_tokens": cost_breakdown["total_tokens"],
            "cost": cost_breakdown["total_cost"],
            "model": cost_breakdown["model"]
        }
        
        self.calls.append(call_record)
        
        # Update totals
        self.total_tokens += call_record["total_tokens"]
        self.total_cost += call_record["cost"]
    
    def get_summary(self) -> dict:
        """Get summary of all calls"""
        
        return {
            "total_calls": len(self.calls),
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 4),
            "average_cost_per_call": round(self.total_cost / len(self.calls), 6) if self.calls else 0,
            "calls": self.calls
        }
    
    def print_summary(self):
        """Print nice summary"""
        
        summary = self.get_summary()
        
        print("\n" + "="*80)
        print("📊 COST TRACKING SUMMARY")
        print("="*80)
        print(f"Total API calls: {summary['total_calls']}")
        print(f"Total tokens: {summary['total_tokens']:,}")
        print(f"Total cost: ${summary['total_cost']:.4f}")
        print(f"Average per call: ${summary['average_cost_per_call']:.6f}")
        print("-"*80)
        print("\nBreakdown:")
        
        for i, call in enumerate(summary['calls'], 1):
            print(f"{i}. {call['question']}")
            print(f"   Tokens: {call['total_tokens']} | Cost: ${call['cost']:.6f}")
    
    def export_json(self, filename: str = "cost_tracking.json"):
        """Save tracking data to JSON file"""
        
        summary = self.get_summary()
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Exported to {filename}")


# ============================================================================
# STEP 8: PRACTICAL EXAMPLE - FAQ Bot with Cost Tracking
# ============================================================================
class FAQBotWithCostTracking:
    """
    FAQ Bot that tracks costs
    
    Every question asked → cost is calculated and tracked
    """
    
    def __init__(self):
        self.tracker = CostTracker()
        self.system_prompt = "You are a helpful FAQ assistant. Be concise."
    
    def answer_question(self, question: str) -> str:
        """
        Answer a question and track cost
        
        Args:
            question: The FAQ question
        
        Returns:
            The answer
        """
        
        # Get answer with cost tracking
        answer, cost_breakdown = call_with_cost_tracking(
            prompt=question,
            system_prompt=self.system_prompt,
            max_tokens=300,
            model="gpt-4o",
            show_estimate=True
        )
        
        # Track this call
        self.tracker.add_call(cost_breakdown, question)
        
        # Show the answer
        print(f"\n📝 Answer:\n{answer}")
        
        return answer
    
    def show_spending(self):
        """Show total spending"""
        
        self.tracker.print_summary()


# ============================================================================
# MAIN: Demonstrate everything
# ============================================================================
if __name__ == "__main__":
    
    # DEMO 1: Show tokenization
    print("\n" + "="*80)
    print("DEMO 1: UNDERSTAND TOKENIZATION")
    print("="*80)
    demonstrate_tokenization()
    
    # DEMO 2: Show cost calculation
    print("\n\n" + "="*80)
    print("DEMO 2: CALCULATE COSTS")
    print("="*80)
    
    # Example 1: Small question
    print("\nExample 1: Small question")
    print("-"*80)
    cost1 = show_cost_breakdown(
        input_tokens=10,
        output_tokens=50,
        model="gpt-4o"
    )
    print(f"Input: {cost1['input_tokens']} tokens = ${cost1['input_cost']:.6f}")
    print(f"Output: {cost1['output_tokens']} tokens = ${cost1['output_cost']:.6f}")
    print(f"Total: ${cost1['total_cost']:.6f}")
    
    # Example 2: Large question
    print("\nExample 2: Large question")
    print("-"*80)
    cost2 = show_cost_breakdown(
        input_tokens=1000,
        output_tokens=5000,
        model="gpt-4o"
    )
    print(f"Input: {cost2['input_tokens']} tokens = ${cost2['input_cost']:.6f}")
    print(f"Output: {cost2['output_tokens']} tokens = ${cost2['output_cost']:.6f}")
    print(f"Total: ${cost2['total_cost']:.6f}")
    
    # DEMO 3: Estimate before calling
    print("\n\n" + "="*80)
    print("DEMO 3: ESTIMATE COST BEFORE CALLING")
    print("="*80)
    
    test_prompt = "What is FastAPI and how does it work?"
    estimate = estimate_api_call_cost(test_prompt, max_tokens=300, model="gpt-4o")
    print(f"\nQuestion: {test_prompt}")
    print(f"Estimated tokens: {estimate['total_tokens']}")
    print(f"Estimated cost: ${estimate['total_cost']:.6f}")
    
    # DEMO 4: Real API call with cost tracking
    print("\n\n" + "="*80)
    print("DEMO 4: REAL API CALL WITH COST TRACKING")
    print("="*80)
    
    answer, cost = call_with_cost_tracking(
        prompt="What is Python programming?",
        max_tokens=200,
        model="gpt-4o",
        show_estimate=True
    )
    
    print(f"\n📝 Answer: {answer}")
    print(f"\n💰 ACTUAL COST BREAKDOWN:")
    print(f"   Input tokens: {cost['input_tokens']}")
    print(f"   Output tokens: {cost['output_tokens']}")
    print(f"   Total tokens: {cost['total_tokens']}")
    print(f"   Total cost: ${cost['total_cost']:.6f}")
    
    # DEMO 5: FAQ Bot with cost tracking
    print("\n\n" + "="*80)
    print("DEMO 5: FAQ BOT WITH COST TRACKING")
    print("="*80)
    
    faq = FAQBotWithCostTracking()
    
    questions = [
        "How do I install FastAPI?",
        "What is a REST API?",
        "How do decorators work in FastAPI?"
    ]
    
    for q in questions:
        print(f"\n{'='*80}")
        faq.answer_question(q)
    
    # Show total spending
    faq.show_spending()


"""
KEY CONCEPTS:
=============

1. TOKENS
   ├─ 1 token ≈ 4 characters
   ├─ Use tiktoken to count
   ├─ Different text = different tokens
   └─ Longer text = more cost

2. PRICING
   ├─ Input cheaper than output
   ├─ Different models = different prices
   ├─ gpt-4o is 10x more expensive than 3.5
   └─ But smarter = worth it

3. ESTIMATION
   ├─ Count input tokens
   ├─ Estimate output (max_tokens * 0.7)
   ├─ Calculate cost
   └─ Know cost BEFORE calling

4. ACTUAL COST
   ├─ Use response.usage data
   ├─ This is the REAL cost
   ├─ Usually close to estimate
   └─ Track it for budgeting

5. TRACKING
   ├─ Record every call
   ├─ Sum up tokens and cost
   ├─ Know total spending
   └─ Alert on high usage

TIPS FOR SAVING MONEY:
======================

1. Use cheaper model if possible
   ├─ gpt-3.5-turbo for simple tasks
   ├─ gpt-4o for complex tasks

2. Reduce max_tokens if possible
   ├─ 200 instead of 500 = cheaper
   ├─ Only ask for what you need

3. Cache long prompts
   ├─ If asking same question multiple times
   ├─ Store response locally

4. Batch similar questions
   ├─ Process 20 at once instead of 20 API calls
   ├─ Reduces overhead

5. Monitor spending
   ├─ Track costs constantly
   ├─ Alert if unexpectedly high
   ├─ Optimize expensive prompts

COMMON MISTAKES:
================

❌ Not counting tokens before calling
→ Surprise costs, no budgeting

❌ Using gpt-4o for simple FAQ
→ Use gpt-3.5-turbo instead (10x cheaper)

❌ Setting max_tokens too high
→ 2000 tokens when 200 would work

❌ Asking the same question multiple times
→ Cache the response instead

❌ Not tracking spending
→ Can't see where money goes

❌ Estimating wrong (using gpt-3.5 pricing for gpt-4o)
→ Use correct model pricing
"""