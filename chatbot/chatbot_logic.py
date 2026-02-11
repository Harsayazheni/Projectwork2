"""
Chatbot Logic - Groq API Integration for Career Guidance
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Groq model
MODEL = "llama-3.3-70b-versatile"

def get_career_guidance(user_message, context):
    """
    Get AI-powered career guidance using Groq API
    """

    # 🧠 SMART, FLEXIBLE SYSTEM PROMPT
    system_prompt = f"""
You are **OPUS Career Assistant**, a professional and friendly AI career advisor.

========================
HOW TO FORMAT RESPONSES
========================
- Match the format to the QUESTION TYPE
- Do NOT force bullet points everywhere
- Use:

• Short paragraphs for explanations  
• **Bold text** for emphasis  
• Bullet points ONLY when listing items or steps  
• Clear spacing so it reads well in a chat UI  

========================
STYLE RULES
========================
- Be concise but natural
- Avoid long essays
- Avoid robotic templates
- Do NOT repeat the same structure every time
- If explaining, talk like a human mentor
- If listing, keep bullets clean and minimal

========================
CONTENT RULES
========================
- ONLY answer career-related questions
  (skills, jobs, learning, resume, growth)
- If asked unrelated questions, reply ONLY with:
  "I'm specialized in career guidance. Please ask about careers, skills, or professional growth."
- When relevant, use the user's predicted career
- Be practical and actionable

========================
USER CONTEXT (DO NOT REPEAT VERBATIM)
========================
{context}
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model=MODEL,
            temperature=0.65,   # balanced: not robotic, not verbose
            max_tokens=600,     # allows paragraphs + bullets
            top_p=1,
            stream=False
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        error_msg = str(e)

        if "api_key" in error_msg.lower():
            return "⚠️ API key error. Please check your GROQ_API_KEY."
        elif "rate_limit" in error_msg.lower():
            return "⚠️ Rate limit exceeded. Please try again shortly."
        elif "timeout" in error_msg.lower():
            return "⏱️ Request timed out. Please try again."
        else:
            return f"❌ Error: {error_msg}"


def test_groq_connection():
    """Test if Groq API is configured correctly"""
    try:
        client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello"}],
            model=MODEL,
            max_tokens=10
        )
        return True, "Groq API connected successfully!"
    except Exception as e:
        return False, f"Groq API error: {str(e)}"
