from dependencies.config import client

def test_parameter(temp:float,max_tokens:int):
      messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Generate the Tech Joke using santa banta ."}
    ]
      
      response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=messages,
            max_tokens=max_tokens,
            temperature=temp
      )

      return response.choices[0].message.content

# temps = [0.0,0.5,1.0,1.5]
# for t in temps:
#       res = test_parameter(t,300)
#       print("Temperature: ",res)    




tokens = [10,20,30]
temp = [0.1,1,1.5,2.0]
def solve():
    for tok in tokens:
      res = test_parameter(1,tok)
      print("-"*80)
      print("Token: ",res)

    for t in temp:
      res = test_parameter(t,50)
      print("-"*80)
      print("Temp: ",res)

'''
PARAMETER     | VALUE    | USE CASE              | BEHAVIOR
──────────────┼──────────┼─────────────────────┼──────────────────────
temperature   | 0.0-0.3  | FAQ, Facts, Code    | Consistent, boring
              | 0.5-0.8  | General use, Chat   | Balanced
              | 1.0-1.5  | Content, Ideas      | Creative
              | 1.5-2.0  | Experimental        | Random, weird
──────────────┼──────────┼─────────────────────┼──────────────────────
max_tokens    | 50-100   | Tweets, Quick reply | Very short
              | 200-500  | Paragraphs, FAQ     | Medium
              | 1000+    | Articles, Code      | Long
──────────────┼──────────┼─────────────────────┼──────────────────────
top_p         | 0.1-0.3  | Factual only        | Very restrictive
              | 0.5-0.8  | General             | Balanced
              | 0.9-1.0  | Creative            | Permissive
'''

'''
🎲 PART 4: TOP_P (Alternative to Temperature)
What is Top_P?
Top_P = nucleus sampling - another way to control randomness.
Instead of temperature's "heat", top_p thinks: "Use only the top X% probable words"
TOP_P SCALE:
═══════════════════════════════════════════════════════════

0.1 (VERY RESTRICTIVE)
├─ Only use top 10% most likely words
├─ Very consistent, boring
├─ Equivalent to temperature ≈ 0.0
└─ Use: Facts, math, FAQs

0.5 (MODERATE)
├─ Only use top 50% most likely words
├─ Good balance
├─ Equivalent to temperature ≈ 0.7
└─ Use: Most general purposes

0.9 (PERMISSIVE)
├─ Use top 90% of words
├─ Allows creative choices
├─ Equivalent to temperature ≈ 1.5
└─ Use: Creative writing

1.0 (NO RESTRICTION)
├─ Use all possible words
├─ Completely random
├─ Equivalent to temperature ≈ 2.0
└─ Use: Experimental only
Temperature vs Top_P (Comparison)
WORD PROBABILITIES:
─────────────────────────────────────
"Python" - 30%
"Java" - 25%
"C++" - 20%
"JavaScript" - 15%
"Rust" - 10%

With temperature=0.5:
├─ Flattens all probabilities slightly
├─ "Python" becomes ~28%
├─ Still favors Python, but increases others
└─ Result: Mostly Python, sometimes Java

With top_p=0.8:
├─ Takes only top 80% of cumulative probability
├─ Includes: Python(30%) + Java(25%) + C++(20%) + JS(5%)
├─ Excludes: Rust (would exceed 80%)
└─ Result: Only considers 4 languages, skips Rust

SIMPLIFIED:
Temperature = "How noisy is the signal?"
Top_P = "How many options are available?"
When to Use Top_P vs Temperature
USE TEMPERATURE:
├─ Simpler, more intuitive
├─ Most use cases
├─ "I want more/less randomness"
└─ Default choice

USE TOP_P:
├─ Advanced fine-tuning
├─ When you want to exclude "weird" words
├─ "I want only the sensible options"
└─ Combined with temperature for precision

BEST PRACTICE:
├─ Set temperature
├─ Leave top_p at 1.0 (default)
└─ Only change top_p if temperature isn't enough
'''

# How Temperature actually works under the hood
'''
TEMPERATURE = 0.0 (DETERMINISTIC):
─────────────────────────────────────
Words ranked by probability:
1. "Python" - 45% likely ← ALWAYS PICKS THIS
2. "Java" - 30% likely
3. "C++" - 15% likely
4. "Rust" - 10% likely

Result: Always says "Python" first

TEMPERATURE = 1.0 (BALANCED):
─────────────────────────────────────
Words ranked by probability:
1. "Python" - 40% likely ← COULD PICK ANY
2. "Java" - 35% likely
3. "C++" - 15% likely
4. "Rust" - 10% likely

Result: Usually "Python", sometimes "Java"

TEMPERATURE = 2.0 (CRAZY):
─────────────────────────────────────
Words ranked by probability:
1. "Python" - 20% likely ← ALMOST EQUAL CHANCE
2. "Java" - 20% likely
3. "C++" - 20% likely
4. "Rust" - 20% likely

Result: Random picks, sometimes gibberish
'''