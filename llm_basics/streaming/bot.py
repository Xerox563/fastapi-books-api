'''
WITHOUT STREAMING (What we did Days 8-9):
────────────────────────────────────────────
User: "Tell me about Python"
API: [waiting... waiting... waiting...]
API: "Here's the full response: Python is a..."
User sees: Entire answer at once

Problem: User waits 3 seconds for full response

WITH STREAMING (What we do today):
────────────────────────────────────────────
User: "Tell me about Python"
API: Sends word 1... word 2... word 3... (continuously)
User sees: "Python" → "is" → "a" → "programming" → "language..."

Benefit: User sees response START IMMEDIATELY, feels faster!

Real world: ChatGPT website uses streaming - you see words appear!
'''

from dependencies.config import client
import json
import time

def level_1_stream(user_message:str,user_token:int,user_temp:int):
    
    message =[
        {"role":"system","content":"Act as Joker"},
        {"role":"user","content":user_message}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=user_token,
            temperature=user_temp,
            messages=message,
            stream=True
        )

        # now response is a stream[instead of a single response]
        # we loop over each incoming chunks 
        # print(dir(response))  : To see all attributes of this response
        # for chunk in response:
        #   print(json.dumps(chunk.model_dump(),indent=2))
        
        full_response = ""
        for chunk in response:
            # Each chunk has this structure:
            # {
            #   "choices": [
            #     {
            #       "delta": {
            #         "content": "word"  ← The actual text piece
            #       }
            #     }
            #   ]
            # }
            try:
                # Extract the text from this chunk
                if chunk.choices[0].delta.content:
                    # Print WITHOUT newline so words appear on same line
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    full_response += chunk.choices[0].delta.content
                  time.sleep(0.05)
            except Exception as e:
                print(f"Error Processing chunk: {e}")
        return full_response        
    except Exception as e:  
      # Stream initialization error
        print(f"Error starting stream: {e}")
        return  


def solve():
    ans = level_1_stream("Joke about AI",100,1.0)
    print("Full Response: ",ans)


"""
DAY 10: STREAMING RESPONSES
===========================

Streaming = Getting response piece by piece instead of all at once

Why stream?
→ Feels faster to user (they see words appearing)
→ Better for real-time applications
→ Same cost, better experience

How it works:
→ API sends chunks of text as they're generated
→ You process each chunk immediately
→ Print them as they arrive
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import time  # For visual delay effect (optional)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================================
# APPROACH 1: BASIC STREAMING - Print as it comes
# ============================================================================
def stream_basic(user_message: str):
    """
    Most basic streaming - just print words as they arrive
    
    stream=True means: Don't wait for full response, send chunks
    """
    
    print("Streaming response:")
    print("-" * 80)
    
    # Make API call with stream=True
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500,
        stream=True  # ← THIS enables streaming!
    )
    
    # response is now a "stream" (iterator) instead of a single response
    # We loop through each chunk as it arrives
    
    for chunk in response:
        # Each chunk has this structure:
        # {
        #   "choices": [
        #     {
        #       "delta": {
        #         "content": "word"  ← The actual text piece
        #       }
        #     }
        #   ]
        # }
        
        # Extract the text from this chunk
        if chunk.choices[0].delta.content:
            # Print WITHOUT newline so words appear on same line
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    # After streaming is done, print newline
    print("\n" + "-" * 80)


# ============================================================================
# APPROACH 2: STREAMING WITH DELAY - See words appear slower
# ============================================================================
def stream_with_delay(user_message: str, delay: float = 0.05):
    """
    Streaming with delay between chunks - looks like typing animation
    
    delay=0.05 means wait 50ms between each word
    (makes it visible what's happening in real-time)
    """
    
    print("Streaming response (with visual delay):")
    print("-" * 80)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500,
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.content:
            # Print the chunk
            print(chunk.choices[0].delta.content, end="", flush=True)
            # Wait a bit before printing next chunk
            time.sleep(delay)  # ← This creates the "typing" effect
    
    print("\n" + "-" * 80)


# ============================================================================
# APPROACH 3: STREAMING WITH COLLECTION - Save full response
# ============================================================================
def stream_and_collect(user_message: str) -> str:
    """
    Stream the response AND collect all chunks into full text
    
    Use case: Want real-time display BUT also save the full response
    """
    
    print("Streaming response (collecting full text):")
    print("-" * 80)
    
    full_response = ""  # ← Collect all chunks here
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500,
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            
            # Display in real-time
            print(text, end="", flush=True)
            
            # Also collect for later use
            full_response += text
    
    print("\n" + "-" * 80)
    
    # Return the complete response
    return full_response


# ============================================================================
# APPROACH 4: PRACTICAL - FAQ Bot with Streaming
# ============================================================================
class StreamingFAQBot:
    """
    FAQ Bot that streams responses
    
    Real-world use case:
    → User asks question
    → Bot starts answering immediately (streaming)
    → User sees text appear in real-time
    → Feels faster and more interactive
    """
    
    def __init__(self):
        self.system_prompt = "You are a helpful FAQ assistant. Be concise."
    
    def answer_stream(self, question: str) -> str:
        """
        Answer a FAQ question with streaming
        
        Returns: Full collected response
        """
        
        print(f"\n📌 Question: {question}")
        print("📝 Answer: ", end="", flush=True)
        
        full_response = ""
        
        # Make streaming API call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.3,
            max_tokens=300,
            stream=True  # ← Streaming enabled
        )
        
        # Process each chunk
        for chunk in response:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                
                # Print immediately (real-time display)
                print(text, end="", flush=True)
                
                # Collect for return value
                full_response += text
        
        print()  # Newline after response
        return full_response


# ============================================================================
# APPROACH 5: ERROR HANDLING - What if stream fails?
# ============================================================================
def stream_with_error_handling(user_message: str):
    """
    Streaming with proper error handling
    
    Streaming can fail if:
    → Network drops mid-stream
    → API key expires
    → Rate limit hit
    
    This code handles it gracefully
    """
    
    print("Streaming with error handling:")
    print("-" * 80)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are helpful."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500,
            stream=True
        )
        
        # Process stream with error handling
        for chunk in response:
            try:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
            except Exception as e:
                # Chunk processing error
                print(f"\n⚠️ Error processing chunk: {e}")
                continue  # Continue with next chunk
    
    except Exception as e:
        # Stream initialization error
        print(f"❌ Error starting stream: {e}")
        return
    
    print("\n" + "-" * 80)


# ============================================================================
# APPROACH 6: STREAMING WITH CALLBACK - For web apps
# ============================================================================
def stream_with_callback(user_message: str, callback=None):
    """
    Streaming with callback function
    
    callback = function to call each time a chunk arrives
    
    Use case: Web app where you need to send chunks to frontend
    → Each chunk triggers callback
    → Callback sends to browser via WebSocket
    → Browser displays in real-time
    """
    
    if callback is None:
        # Default callback: just print
        callback = lambda text: print(text, end="", flush=True)
    
    print("Streaming with callback:")
    print("-" * 80)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500,
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.content:
            # Call the callback function with the chunk
            callback(chunk.choices[0].delta.content)
    
    print("\n" + "-" * 80)


# ============================================================================
# PART 3: COMPARISON - Streaming vs Non-Streaming
# ============================================================================
def compare_streaming_vs_non_streaming():
    """
    Show difference between streaming and non-streaming
    """
    
    question = "What is the Python language?"
    
    print("\n\n")
    print("="*80)
    print("COMPARISON: Streaming vs Non-Streaming")
    print("="*80)
    
    # Non-streaming (old way)
    print("\n1️⃣ NON-STREAMING (What we did on Days 8-9):")
    print("-"*80)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
        temperature=0.7,
        max_tokens=200,
        stream=False  # ← No streaming
    )
    
    # Entire response comes at once
    answer = response.choices[0].message.content
    print(answer)
    print("\n⏱️ User waits for entire response before seeing anything")
    
    # Streaming (new way)
    print("\n" + "="*80)
    print("2️⃣ STREAMING (Today's method):")
    print("-"*80)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
        temperature=0.7,
        max_tokens=200,
        stream=True  # ← Streaming enabled
    )
    
    # Response comes piece by piece
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print("\n⏱️ User sees words appearing immediately (better UX!)")


# ============================================================================
# MAIN: Run all examples
# ============================================================================
if __name__ == "__main__":
    
    test_question = "Explain FastAPI in 2 sentences"
    
    # Example 1: Basic streaming
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Streaming")
    print("="*80)
    stream_basic(test_question)
    
    # Example 2: Streaming with delay
    print("\n" + "="*80)
    print("EXAMPLE 2: Streaming with Typing Effect")
    print("="*80)
    stream_with_delay(test_question, delay=0.02)
    
    # Example 3: Stream and collect
    print("\n" + "="*80)
    print("EXAMPLE 3: Stream + Collect Full Response")
    print("="*80)
    full = stream_and_collect(test_question)
    print(f"\n📝 Full response collected: {len(full)} characters")
    
    # Example 4: FAQ Bot with streaming
    print("\n" + "="*80)
    print("EXAMPLE 4: Streaming FAQ Bot")
    print("="*80)
    faq = StreamingFAQBot()
    faq.answer_stream("How do I install FastAPI?")
    faq.answer_stream("What is a REST API?")
    faq.answer_stream("How do I use decorators in FastAPI?")
    
    # Example 5: Comparison
    compare_streaming_vs_non_streaming()


"""
KEY CONCEPTS:
=============

1. stream=True
   → Enables streaming in API call
   → Response becomes an iterator (loop through chunks)

2. chunk.choices[0].delta.content
   → Gets the text piece from each chunk
   → Could be None at end (check before using)

3. flush=True in print()
   → Forces print to display immediately
   → Important for real-time effect
   → Without it, text buffers and appears in chunks

4. Why stream?
   → Better UX (looks faster)
   → Real-time applications
   → Long responses feel interactive
   → Same cost as non-streaming

5. When to use streaming?
   → Web apps showing live response
   → Chatbot interfaces
   → Long responses (articles, code)
   → Anything where real-time matters

6. When NOT to use streaming?
   → You need the full response before processing
   → Background jobs (batch processing)
   → You're collecting response for analysis
   → Single-purpose tasks

COMMON ISSUES:
==============

"stream=True but response still slow"
→ API latency, not streaming issue
→ Streaming starts immediately, but generation is slow

"Can't access full response while streaming"
→ Collect chunks as shown in Approach 3
→ Add them to a string as they arrive

"Text doesn't appear in real-time"
→ Missing flush=True in print()
→ Add flush=True to make it instant

"How do I stop streaming?"
→ Break from loop: for chunk in response: break
→ Or stream might end naturally
"""
