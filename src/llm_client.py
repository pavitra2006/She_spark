# llm_client.py
import os
import google.generativeai as genai


GEMINI_API_KEY = os.getenv("GEMINIAI_API_KEY")
if not GEMINI_API_KEY:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINIAI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def ask_llm(prompt):
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not set. Please add it to Streamlit secrets or your .env file."
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err_str = str(e)
        if "429" in err_str:
            import re
            match = re.search(r'retry_delay \{ seconds: (\d+) \}', err_str)
            if match:
                seconds = match.group(1)
                return (f"Gemini API quota exceeded. Please wait {seconds} seconds and try again, or reduce the size of your request. "
                        "See https://ai.google.dev/gemini-api/docs/rate-limits for details.")
            return ("Gemini API quota exceeded. Please wait a minute and try again, or reduce the size of your request. "
                    "See https://ai.google.dev/gemini-api/docs/rate-limits for details.")
        return f"Gemini API error: {e}"
