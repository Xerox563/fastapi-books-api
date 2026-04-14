"""
DAY 8: OpenAI API Setup + First Call

Entry point - runs the FAQ bot demo

SETUP:
------
1. pip install -r requirements.txt
2. Add OPENAI_API_KEY to .env
3. python main.py
"""

# from faq_bot.bot import FAQBot
# from faq_bot_v2.bot import solve
from streaming.bot import solve


def main():
    """Run the FAQ bot demo"""
    # print("Starting FAQ Bot Demo...\n")
    # # Create bot
    # bot = FAQBot()
    # # Test all 5 system prompts
    # bot.test_all_prompts()
    # print("\n✅ Demo complete!")
    
    # faq_bot_v2 
    # solve()

    # streaming
    solve()



if __name__ == "__main__":
    main()