import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback for now if the user hasn't set it yet, though keeping it empty might be better. 
    pass

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_claims(text):

    prompt = f"""
    Extract the key research claims from this research paper.

    Paper:
    {text[:3000]}
    """

    response = model.generate_content(prompt)

    return response.text