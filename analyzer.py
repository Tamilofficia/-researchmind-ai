import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# We use gemini-2.5-flash which is very fast and capable of JSON structured output
model = genai.GenerativeModel("models/gemini-2.5-flash")

def analyze_paper_metrics(text):
    """
    Performs a deep autopsy of a research paper.
    Returns a Python dictionary with:
    - summary: Short 3-sentence executive summary
    - critical_insights: 2-3 bullet points of the most important takeaways.
    - limitations: Known flaws, biases, or future work mentioned.
    - commercial_feasibility: An integer score 1-100 indicating how easy it is to monetize.
    - trl: Tech Readiness Level integer 1-9
    """
    
    prompt = f"""
    You are a world-class venture capitalist and AI researcher analyzing a new paper.
    
    Paper Text:
    {text[:5000]}  # Limiting context for speed and rate limits
    
    Please provide the following metrics:
    1. A punchy, 3-sentence executive summary highlighting the actual utility of this paper.
    2. Critical Insights: 2 or 3 bullet points outlining the core novelty.
    3. Key Limitations: What are the flaws, biases, or required future work admitted by the authors?
    4. A "Scientific Rigor" score from 1 to 100 representing the robustness of the methodology, datasets used, and reproducibility of the claims.
    5. A "Commercial Feasibility" score from 1 to 100 representing how easily this research translates into a profitable product.
    6. A "Tech Readiness Level" (TRL) score from 1 to 9 representing how mature the technology is.

    Respond STRICTLY with a valid JSON object matching this exact format:
    {{
        "summary": "Your 3 sentence summary here...",
        "critical_insights": "• Insight 1\\n• Insight 2",
        "limitations": "The authors note that...",
        "scientific_rigor": 90,
        "commercial_feasibility": 85,
        "trl": 4
    }}
    Do not include markdown formatting or backticks around the JSON.
    """

    try:
        response = model.generate_content(prompt)
        # Strip potential markdown formatting if the model disobeys instructions
        result_text = response.text.replace('```json', '').replace('```', '').strip()
        analysis = json.loads(result_text)
        return analysis
    except Exception as e:
        print(f"Error during paper analysis: {e}")
        return {
            "summary": "Analysis failed. Please try again.",
            "critical_insights": "N/A",
            "limitations": "N/A",
            "commercial_feasibility": 0,
            "trl": 1
        }
